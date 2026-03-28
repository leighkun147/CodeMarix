# 🎯 MILITARY COMMAND CENTER - VISUAL REFERENCE GUIDE

## UI Component Showcase

### 1. Page Layout Overview
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚔️ CODEXMATRIX: MILITARY AI COMMAND CENTER            ┃ ← Military Header
┣━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃             ┃                                         ┃
┃  SIDEBAR    ┃       MAIN CONTENT AREA                ┃
┃             ┃                                         ┃
┃  • Input    ┃  Results Display                        ┃
┃    Form     ┃  ├─ Winner Announcement               ┃
┃  • Status   ┃  ├─ Metrics                           ┃
┃  • Control  ┃  ├─ Leaderboard                       ┃
┃             ┃  └─ 5 Analysis Tabs                   ┃
┃             ┃     ├─ 📊 Heatmap                     ┃
┃             ┃     ├─ 📈 Rankings                    ┃
┃             ┃     ├─ 🎯 Comparison                  ┃
┃             ┃     ├─ 🎯 TACTICAL RADAR ⭐          ┃
┃             ┃     └─ 💾 Raw Data                    ┃
┣━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 🔐 Privacy Notice & Footer                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

### 2. Military Header Component
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   █ ⚔️ CODEXMATRIX: MILITARY AI COMMAND CENTER        │
│                                                         │
│   • Background: Linear gradient (#00ff41 → #00d9ff)   │
│   • Border: 3px solid #00ff41 (neon green)           │
│   • Glow: 0 0 30px rgba(0, 255, 65, 0.3)             │
│   • Typography: JetBrains Mono, Bold, Uppercase      │
│   • Animation: Blinking cursor, sweep effect          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 3. Winner Announcement Banner
```
╔═════════════════════════════════════════════════════════╗
║                                                         ║
║           🏆 SESSION WINNER: CLAUDE-3-OPUS 🏆         ║
║                          4.82/5.0                      ║
║                                                         ║
║  • Background: Gradient green → cyan                   ║
║  • Border: 3px solid #00ff41                          ║
║  • Glow: Double box-shadow effect                      ║
║  • Animation: Sweep highlight across text             ║
║  • Text: White, uppercase, 28px bold                  ║
║                                                         ║
╚═════════════════════════════════════════════════════════╝
```

---

### 4. Metric Cards (Session Statistics)
```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ 📊 Problems      │  │ 🤖 Models        │  │ 💻 Languages     │
│ Tested           │  │ Evaluated        │  │ Used             │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│                  │  │                  │  │                  │
│        5         │  │        3         │  │        2         │
│                  │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
  ▲ Green left         ▲ Green left         ▲ Green left
  │ border (4px)       │ border (4px)       │ border (4px)
  Cyan top border      Cyan top border      Cyan top border
  (2px)               (2px)                (2px)
```

---

### 5. Tab Navigation
```
  [HEATMAP] [RANKINGS] [COMPARISON] [🎯 RADAR] [RAW DATA]
   ────────  ─────────  ───────────  ─────────  ─────────
   
UNSELECTED TAB:
├─ Background: #0f1419 (dark navy)
├─ Text: #a0a0a0 (gray)
├─ Border: 1px #1a2332
└─ Hover: Green glow effect

SELECTED TAB (🎯 RADAR):
├─ Background: #00ff41 (neon green)
├─ Text: #0a0e1a (dark)
├─ Border: 2px #00ff41
└─ Glow: 0 0 20px rgba(0, 255, 65, 0.5)
└─ Animation: Instant color transition
```

---

### 6. Tactical Radar Tab - UI Layout
```
┌─────────────────────────────────────────────────────────┐
│ 🎯 TACTICAL RADAR ANALYSIS SYSTEM                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 📡 Enhanced multi-dimensional performance              │
│ visualization                                          │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🎮 ANALYSIS MODE ───────────┐                         │
│ ┌──────────────────────────┐│  [Model Selector]       │
│ │ ○ 📊 Single Model        ││  ┌─────────────────┐    │
│ │ ○ ⚔️ Model Overlay       ││  │ Select model... │    │
│ └──────────────────────────┘│  └─────────────────┘    │
│                             │                         │
├─────────────────────────────┼─────────────────────────┤
│                                                         │
│ ┌──────────────────────────────────────────────────┐  │
│ │      [RADAR CHART VISUALIZATION]                 │  │
│ │                                                  │  │
│ │            TACTICAL ANALYSIS:                   │  │
│ │         GREEN PENTAGON SHAPE                    │  │
│ │                                                  │  │
│ │    (5 dimensions, 1-5 scale, neon glow)        │  │
│ │                                                  │  │
│ └──────────────────────────────────────────────────┘  │
│                                                         │
│ [📋 DETAILED METRICS BREAKDOWN] (expandable)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 7. Single Model Radar Visualization
```
                    Documentation
                        /\
                       /  \
                      /    \
                     /      \
                Security    Correctness
                   /            \
                  /              \
              5.0 ──────2.5────── 5.0
               /                    \
              /                      \
         4.5 ────────────────────── 4.2
            /                        \
    Efficiency ─────── 3.8 ───── Readability

    • Pentagon shape = balanced performance
    • Neon green color (#00ff41)
    • Hovertext shows exact scores
    • Interactive markers at each dimension
    • Scale: 1-5 (outer edge = 5.0)
```

---

### 8. Model Overlay Comparison (⚔️ Mode)
```
                    Documentation
                        /\
                   ___/  \___
              ___/          \___
             /  🟢 Model 1    \
            /  🔵 Model 2      \
      Security          Correctness
           /  \/  \        /  \  \  \
          /  Model 1 overlaid  2  \
      3.8 ──────2.5────────── 5.0  4.2
       /                              \
      /                                \
Efficiency ─── 3.8 ─ (gap 1.2) ─ 5.0 ─ Readability

Legend:
─ 🟢 Green (solid line)  = Model 1 (primary)
─ 🔵 Cyan (dashed)      = Model 2 (comparison)
└─ Distance = score value on 1-5 scale
└─ Overlap area = competitive similarity
```

---

### 9. Color Palette Visual Reference
```
PRIMARY COLORS
┌────────────────────────────────────────────────┐
│ ACCENT PRIMARY (Neon Green)                    │
│ #00ff41 | RGB(0, 255, 65)                     │
│ ▓███████████████████████████████████████       │
│ Usage: Main UI, glow effects, borders         │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ ACCENT SECONDARY (Cyan)                        │
│ #00d9ff | RGB(0, 217, 255)                    │
│ ░███████████████████████████████████████       │
│ Usage: Overlays, secondary focus              │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ WARNING (Alert Orange)                         │
│ #ff6b35 | RGB(255, 107, 53)                   │
│ ▒███████████████████████████████████████       │
│ Usage: Alerts, critical info                  │
└────────────────────────────────────────────────┘

BACKGROUND COLORS
┌────────────────────────────────────────────────┐
│ MAIN (#0a0e1a)      │ SECONDARY (#0f1419)     │
│ ▓▓▓▓▓▓▓▓░░░░░░░░░░░ │ ▓▓▓▓▓▓▓░░░░░░░░░░░░░│
│ Dark Navy           │ Slightly Lighter       │
└────────────────────────────────────────────────┘

TEXT COLORS
┌────────────────────────────────────────────────┐
│ PRIMARY (#f0f0f0)   │ SECONDARY (#a0a0a0)    │
│ ░░░░░░░░░░░░░░░░░░ │ ▒░░░░░░░░░░░░░░░░░░░ │
│ Bright White        │ Medium Gray            │
└────────────────────────────────────────────────┘
```

---

### 10. Animated Elements

#### Blinking Status Indicator
```
Frame 1:  █ SYSTEM ONLINE     (opacity: 1.0)
Frame 2:  █ SYSTEM ONLINE     (opacity: 1.0)
Frame 3:  ░ SYSTEM ONLINE     (opacity: 0.0)  ← Blink
Frame 4:  ░ SYSTEM ONLINE     (opacity: 0.0)  ← Blink
F then repeat...

Animation: @keyframes blink
├─ 0%, 49%:   opacity: 1
└─ 50%, 100%: opacity: 0
Duration: 1000ms (repeating)
```

#### Sweep Highlight Effect
```
Frame 1:  [════════════════════]  gradient at left
Frame 2:  ███[════════════════]   gradient moving right
Frame 3:  ██████[════════════]    gradient middle
Frame 4:  ████████[════════]      gradient near right
Frame 5:  ██████████[════]        gradient exit right

Animation: @keyframes sweep
├─ 0%:   left: -100%
└─ 100%: left: 100%
Duration: 2000ms (repeating)
Effect: Highlight sweep across button/banner
```

---

### 11. Button Styling States

#### DEFAULT STATE
```
┌─────────────────────────────────┐
│   🚀 START BENCHMARK            │
└─────────────────────────────────┘
• Gradient: #00ff41 (left) → #00d9ff (right)
• Border: 2px solid #00ff41
• Text: White, uppercase, bold
• Padding: 12px 24px
• Box-shadow: 0 0 15px rgba(0, 255, 65, 0.3)
```

#### HOVER STATE
```
┌─────────────────────────────────┐
│   🚀 START BENCHMARK            │ ✨
└─────────────────────────────────┘
  (Elevated, glowing effect)

Changes:
• Box-shadow: 0 0 30px rgba(0, 255, 65, 0.6),
              0 0 50px rgba(0, 217, 255, 0.3)
• Transform: translateY(-2px) [lifted]
• Duration: 0.3s
```

#### ACTIVE/CLICKED STATE
```
┌─────────────────────────────────┐
│   🚀 START BENCHMARK            │ ⚡
└─────────────────────────────────┘
  (Pressed, intense glow)

Changes:
• Transform: translateY(0px) [returned]
• Box-shadow: Inset glow + outer glow
• Effect: Immediate feedback
```

---

### 12. Data Visualization in Tabs

#### Tab 1: Heatmap
```
         Model1  Model2  Model3
Model1    ███     ███     ██
Model2    ███     ███     ███
Model3    ██      ███     ███

Legend: Dark=Low, Bright=High (Viridis scale)
Title: "How did each model score others?"
```

#### Tab 2: Rankings by Criteria
```
Scores per Criterion (Bar Charts)

Correctness
████████████ Model1 (4.5)
██████████ Model2 (4.0)
███████ Model3 (3.5)

Efficiency
██████████ Model1 (4.0)
██████████████ Model2 (4.5)
██████ Model3 (3.0)
...
```

#### Tab 3: Comparison
```
Top 3 Models Grouped Bar Chart

         ▓ Model1  ░ Model2  ▒ Model3
Correct  ████     ████     ███
Efficien ███      ████     ██
Readable ████     ███      ████
Docs     ███      ██       ███
Securit  █████    ████     ████
```

#### Tab 4: 🎯 TACTICAL RADAR (NEW)
```
[🎮 ANALYSIS MODE selector]

Single Model:
Point to pentagon → See exact score
Hover anywhere → Tooltip appears

Model Overlay:
🟢 Green + 🔵 Cyan overlaid
Visual gap = performance difference
Larger envelope = better performer
```

#### Tab 5: Raw Data
```
{
  "session_info": {
    "start_time": "2026-03-21T14:32:00",
    "models": ["Model1", "Model2"],
    "winner": "Model1",
    "winner_score": 4.82
  },
  "leaderboard": {...},
  ...
}

[📥 DOWNLOAD BUTTON]
```

---

### 13. User Interaction Flow

#### Entry Point
```
1. Launch: streamlit run app.py
   ↓
2. See: Military-themed header "CODEXMATRIX: MILITARY AI COMMAND CENTER"
   ↓
3. Sidebar: Input form (problems, models, languages, API keys)
   ↓
4. Click: "🚀 START BENCHMARK"
```

#### Benchmark Execution
```
Phase 1: Code Generation
├─ Progress bar (0 → 100%)
├─ Status: "🔄 Generating code..."
└─ Complete: "✅ Code generation complete!"

Phase 2: Peer Review
├─ Progress bar (0 → 100%)
├─ Status: "🔄 Performing peer reviews..."
└─ Complete: "✅ Peer review complete!"

Phase 3: Real-time Analysis
└─ Status: "📊 Analyzing results..."
```

#### Results Display
```
1. Winner Announcement (glowing banner)
   ↓
2. Session Statistics (4 metric cards)
   ↓
3. Leaderboard (data table)
   ↓
4. 5 Analysis Tabs
   ├─ TAB 1: Heatmap
   ├─ TAB 2: Rankings
   ├─ TAB 3: Comparison
   ├─ TAB 4: 🎯 TACTICAL RADAR ← START HERE
   └─ TAB 5: Raw Data
   ↓
5. In RADAR Tab:
   ├─ Select: Single Model OR Model Overlay
   ├─ Choose: Model(s) from dropdown
   ├─ View: Radar pentagon visualization
   └─ Expand: Detailed metrics breakdown
```

---

## 🎯 Key Design Principles

1. **Neon Military Aesthetic**: Green + Cyan on dark navy
2. **Terminal Coding Feel**: Monospace font, sharp borders
3. **Command Center Authority**: Grid, scan lines, status indicators
4. **Interactive Feedback**: Hover glows, smooth transitions
5. **Tactical Focus**: Clear winner determination, dimension analysis
6. **Professional Polish**: Consistent spacing, typography, color usage

---

## 📱 Responsive Behavior

```
Mobile (< 640px):
├─ Single column layout
├─ Stacked radar chart
├─ Full-width buttons
└─ Vertical tab navigation

Tablet (640-1024px):
├─ Two-column layout
├─ Medium-sized charts
├─ Split button layout
└─ Horizontal tabs with icons

Desktop (1024px+):
├─ Multi-column layout
├─ Large radar charts
├─ Full-featured UI
└─ All visual effects enabled
```

---

**Design System v1.0 | Military Command Center**  
**Tactical Radar Analysis Visualization**  
**Production Ready | March 21, 2026**
