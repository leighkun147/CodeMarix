"""Simple Firestore client for persisting CodexMatrix sessions.

This module is intentionally minimal and expects environment-based configuration.
It is safe to import even when Firebase is not configured; callers should handle
RuntimeError and continue without persistence.
"""
from __future__ import annotations

from typing import Any, Dict, List
from datetime import datetime, timezone
import os
import re

try:
    from google.cloud import firestore  # type: ignore
except ImportError:  # pragma: no cover - handled at runtime
    firestore = None  # type: ignore

try:  # Optional import; only needed when running under Streamlit
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover - safe fallback when not in Streamlit
    st = None  # type: ignore

try:
    from google.oauth2 import service_account  # type: ignore
except ImportError:  # pragma: no cover - provided by google-cloud-firestore deps
    service_account = None  # type: ignore


def _require_firestore_client() -> "firestore.Client":  # type: ignore[name-defined]
    """Return an initialized Firestore client or raise a clear RuntimeError.

     Uses FIREBASE_PROJECT_ID from environment to select the project.

     Credential resolution order:
     1. If running under Streamlit and a ``[firebase_service_account]`` block
         exists in ``st.secrets``, use it to build explicit service account
         credentials (recommended for Streamlit Cloud).
     2. Otherwise, fall back to default Google credentials, which can be
         provided via ``GOOGLE_APPLICATION_CREDENTIALS`` or the runtime env.
    """
    if firestore is None:
        raise RuntimeError(
            "google-cloud-firestore is not installed. "
            "Add 'google-cloud-firestore' to requirements and redeploy."
        )

    project_id = os.getenv("FIREBASE_PROJECT_ID")
    if not project_id:
        raise RuntimeError(
            "FIREBASE_PROJECT_ID is not set. Configure it in your environment "
            "or Streamlit Cloud secrets to enable persistence."
        )

    # Preferred path for Streamlit Cloud: use a service account from secrets
    # so we don't rely on GOOGLE_APPLICATION_CREDENTIALS pointing to a file.
    if st is not None and service_account is not None:
        try:
            if "firebase_service_account" in st.secrets:
                sa_info = dict(st.secrets["firebase_service_account"])
                creds = service_account.Credentials.from_service_account_info(
                    sa_info
                )
                return firestore.Client(project=project_id, credentials=creds)
        except Exception:
            # Fall back to default credentials if secrets are missing/invalid
            pass

    # Fallback: rely on default Google credentials (e.g. local dev with
    # GOOGLE_APPLICATION_CREDENTIALS or gcloud auth).
    return firestore.Client(project=project_id)


def save_session_result(session_data: Dict[str, Any]) -> str:
    """Persist a single benchmark session into Firestore.

    The function adds a UTC timestamp field `created_at` if not already
    present and writes into the collection named by FIREBASE_COLLECTION
    (default: "codexmatrix_sessions").

    Returns the created document ID.
    """
    client = _require_firestore_client()

    collection_name = os.getenv("FIREBASE_COLLECTION", "codexmatrix_sessions")
    doc_ref = client.collection(collection_name).document()

    payload = dict(session_data)
    if "created_at" not in payload:
        payload["created_at"] = datetime.now(timezone.utc).isoformat()

    doc_ref.set(payload)
    return doc_ref.id


def fetch_recent_sessions(limit: int = 50) -> List[Dict[str, Any]]:
    """Fetch recent sessions ordered by created_at descending.

    Returns a list of dicts with an extra `id` field for the document ID.
    If Firebase is not configured, this will raise RuntimeError and callers
    should handle it gracefully.
    """
    client = _require_firestore_client()
    collection_name = os.getenv("FIREBASE_COLLECTION", "codexmatrix_sessions")

    query = (
        client.collection(collection_name)
        .order_by("created_at", direction=firestore.Query.DESCENDING)  # type: ignore[attr-defined]
        .limit(limit)
    )

    sessions: List[Dict[str, Any]] = []
    for doc in query.stream():
        data = doc.to_dict() or {}
        data["id"] = doc.id
        sessions.append(data)

    return sessions


def fetch_model_stats() -> List[Dict[str, Any]]:
    """Fetch aggregated model+language statistics from Firestore.

    Returns a list of dicts with an extra ``id`` field for the document ID.
    Documents live under the collection configured by ``MODEL_STATS_COLLECTION``
    (default: ``model_stats``).
    """
    client = _require_firestore_client()
    collection_name = os.getenv("MODEL_STATS_COLLECTION", "model_stats")

    results: List[Dict[str, Any]] = []
    for doc in client.collection(collection_name).stream():
        data = doc.to_dict() or {}
        data["id"] = doc.id
        results.append(data)

    return results


def _slugify(value: str) -> str:
    """Convert arbitrary text into a safe Firestore key fragment.

    Lowercases and replaces non-alphanumeric characters with underscores.
    Ensures a stable mapping suitable for field paths.
    """
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = value.strip("_")
    return value or "unknown"


def _model_lang_doc_id(model: str, language: str) -> str:
    """Build a stable document id for a model+language pair."""
    return f"{_slugify(model)}_{_slugify(language)}"


def update_model_aggregates(
    model_scores: Dict[str, Dict[str, float]],
    languages: List[str],
    rubric_keys: List[str],
    session_start_iso: str | None = None,
) -> None:
    """Update global and daily aggregates for each model/language pair.

    This implements the "Aggregator-First" pattern:

    - Global stats live in collection ``model_stats`` (configurable via
      ``MODEL_STATS_COLLECTION``).
    - Each document represents a single ``model + language`` pair, with
      running totals for each rubric dimension and ``total_tests_conducted``.
    - Daily trend data is stored in a ``history`` sub-collection (configurable
      via ``MODEL_STATS_HISTORY_SUBCOLLECTION``) with one document per
      ``YYYY-MM-DD`` containing daily running sums.

    Args:
        model_scores: {model_name: {rubric_label: average_score, ...}}
        languages: List of languages used in the session.
        rubric_keys: Ordered list of rubric labels to enforce a stable map.
        session_start_iso: Optional ISO8601 timestamp string for the session
            start time. If omitted or invalid, the current UTC time is used.
    """
    if not model_scores or not languages or not rubric_keys:
        return

    client = _require_firestore_client()

    root_collection_name = os.getenv("MODEL_STATS_COLLECTION", "model_stats")
    history_subcollection = os.getenv(
        "MODEL_STATS_HISTORY_SUBCOLLECTION", "history"
    )

    # Determine canonical UTC timestamp for this session
    dt: datetime
    if session_start_iso:
        try:
            dt = datetime.fromisoformat(session_start_iso)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
        except Exception:
            dt = datetime.now(timezone.utc)
    else:
        dt = datetime.now(timezone.utc)

    today_str = dt.date().isoformat()  # YYYY-MM-DD

    for model_name, scores in model_scores.items():
        if not scores:
            continue

        for language in languages:
            doc_id = _model_lang_doc_id(model_name, language)
            doc_ref = client.collection(root_collection_name).document(doc_id)

            # Global aggregates for this model+language
            update_data: Dict[str, Any] = {
                "model": model_name,
                "language": language,
                "rubric_keys": rubric_keys,
                "last_updated": dt.isoformat(),
                "total_tests_conducted": firestore.Increment(1),  # type: ignore[arg-type]
            }

            # Increment running sums for each rubric dimension
            for rubric in rubric_keys:
                raw_score = scores.get(rubric)
                try:
                    score_val = float(raw_score) if raw_score is not None else 0.0
                except (TypeError, ValueError):
                    score_val = 0.0

                field_key = _slugify(rubric)
                update_data[f"running_sum.{field_key}"] = firestore.Increment(  # type: ignore[arg-type]
                    score_val
                )

            # Merge into the aggregate document
            doc_ref.set(update_data, merge=True)

            # Daily time-series shard under history/{YYYY-MM-DD}
            history_ref = doc_ref.collection(history_subcollection).document(
                today_str
            )

            daily_update: Dict[str, Any] = {
                "model": model_name,
                "language": language,
                "date": today_str,
                "daily_tests_conducted": firestore.Increment(1),  # type: ignore[arg-type]
            }

            for rubric in rubric_keys:
                raw_score = scores.get(rubric)
                try:
                    score_val = float(raw_score) if raw_score is not None else 0.0
                except (TypeError, ValueError):
                    score_val = 0.0

                field_key = _slugify(rubric)
                daily_update[
                    f"daily_sum.{field_key}"
                ] = firestore.Increment(  # type: ignore[arg-type]
                    score_val
                )

            history_ref.set(daily_update, merge=True)
