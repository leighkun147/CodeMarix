FROM python:3.12-slim

WORKDIR /app

# Copy backend files
COPY backend/requirements.txt .
COPY src /app/src
COPY backend/main.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run app
CMD ["python", "main.py"]
