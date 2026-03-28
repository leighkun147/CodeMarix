# 🎯 Military Command Center - Design System Document

## 1. COLOR PALETTE

### Primary Colors
```
┌─────────────────────────────────────────────────────────┐
│ ACCENT PRIMARY (Neon Green)                             │
│ HEX: #00ff41  |  RGB: 0, 255, 65                        │
│ Usage: Main emphasis, glow effects, status indicators  │
│ ▓████████████████████████████████████████████████████████│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ACCENT SECONDARY (Cyan Targeting)                       │
│ HEX: #00d9ff  |  RGB: 0, 217, 255                       │
│ Usage: Secondary focus, overlays, borders               │
│ ░████████████████████████████████████████████████████████│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ WARNING (Alert Orange)                                  │
│ HEX: #ff6b35  |  RGB: 255, 107, 53                      │
│ Usage: Alerts, errors, critical information            │
│ ▒████████████████████████████████████████████████████████│
└─────────────────────────────────────────────────────────┘
```

### Background Colors
```
┌─────────────────────────────────────────────────────────┐
│ BACKGROUND MAIN (Deep Navy)                             │
│ HEX: #0a0e1a  |  RGB: 10, 14, 26                        │
│ Usage: Page background, primary container              │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ BACKGROUND SECONDARY (Navy)                             │
│ HEX: #0f1419  |  RGB: 15, 20, 25                        │
│ Usage: Secondary containers, panels, cards             │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ BACKGROUND TERTIARY (Grid Navy)                         │
│ HEX: #141820  |  RGB: 20, 24, 32                        │
│ Usage: Grid overlays, tertiary backgrounds             │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└─────────────────────────────────────────────────────────┘
```

### Text Colors
```
┌─────────────────────────────────────────────────────────┐
│ TEXT PRIMARY (Bright White)                             │
│ HEX: #f0f0f0  |  RGB: 240, 240, 240                     │
│ Usage: Main text, headings, primary CTA                │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ TEXT SECONDARY (Gray)                                   │
│ HEX: #a0a0a0  |  RGB: 160, 160, 160                     │
│ Usage: Secondary text, disabled states, labels         │
│ ▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└─────────────────────────────────────────────────────────┘
```

### Support Colors
```
┌─────────────────────────────────────────────────────────┐
│ BORDER                                                  │
│ HEX: #1a2332  |  RGB: 26, 35, 50                        │
│ Usage: Component borders, dividers                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ GRID OVERLAY                                            │
│ RGBA: (0, 255, 65, 0.05)                               │
│ Usage: Subtle background grid pattern                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ SCAN LINE EFFECT                                        │
│ RGBA: (0, 255, 65, 0.1)                                │
│ Usage: CRT-style horizontal lines background           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ GLOW EFFECT                                             │
│ Shadow: 0 0 20px rgba(0, 255, 65, 0.5)                 │
│ Usage: Button hover, active elements                   │
└─────────────────────────────────────────────────────────┘
```

---

## 2. TYPOGRAPHY

### Font Stack
```
Primary Font: JetBrains Mono
Fallback 1:   Roboto Mono
Fallback 2:   Courier New
Type:         Monospace (Code-centric aesthetic)

Import:
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');
```

### Font Weights & Usage
```
┌──────────┬──────────────┬───────────────────────────────┐
│ Weight   │ Style        │ Usage                         │
├──────────┼──────────────┼───────────────────────────────┤
│ 400      │ Regular      │ Body text, descriptions       │
│ 600      │ SemiBold     │ Secondary headings, emphasis  │
│ 700      │ Bold         │ Main headings, buttons        │
└──────────┴──────────────┴───────────────────────────────┘
```

### Typography Scale
```
H1 (Title):           24px | Bold (700) | Uppercase | 2px letter-spacing
H2 (Subheader):       20px | Bold (700) | Uppercase | 1px letter-spacing
H3 (Section):         18px | SemiBold (600) | Mixed case
Body Text:            14px | Regular (400) | Mixed case
Small Text:           12px | Regular (400) | Mixed case
Button Text:          14px | Bold (700) | UPPERCASE | 1px letter-spacing
Label Text:           12px | SemiBold (600) | Mixed case
```

---

## 3. COMPONENT LIBRARY

### 3.1 Military Header
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ █ CODEXMATRIX: MILITARY AI COMMAND CENTER           ┃
┃ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┃
┃ ┃ (Blinking cursor indicator)                    ┃ ┃
┃ ┃ (Green to Cyan gradient)                       ┃ ┃
┃ ┃ (Sweep animation effect)                       ┃ ┃
┃ ┃ (Neon glow: 0 0 30px rgba(0,255,65,0.3))      ┃ ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

CSS Properties:
- Border: 2px solid #00ff41
- Background: linear-gradient(135deg, #00ff41, #00d9ff)
- Padding: 20px 25px
- Border-radius: 0px (sharp military style)
- Box-shadow: 0 0 30px rgba(0, 255, 65, 0.3),
              inset 0 0 30px rgba(0, 255, 65, 0.1)
```

### 3.2 Radar Container
```
┌──────────────────────────────────────────────────┐
│ ▲ TACTICAL ANALYSIS: MODEL_NAME                  │
│ ┌──────────────────────────────────────────────┐ │
│ │                                              │ │
│ │         [RADAR PENTAGON CHART]               │ │
│ │                                              │ │
│ │  (Green neon glow around pentagon)           │ │
│ │  (Grid scanlines visible)                    │ │
│ │  (Interactive hover tooltips)                │ │
│ │                                              │ │
│ └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘

CSS Properties:
- Border: 3px solid #00ff41
- Background-color: #0f1419
- Padding: 20px
- Box-shadow: 0 0 20px #00ff41,
              inset 0 0 20px rgba(0, 255, 65, 0.05),
              0 0 40px rgba(0, 255, 65, 0.2)
- Position: relative
```

### 3.3 Button Styles
```
DEFAULT STATE:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓    HOVER STATE:
┃  🚀 START BENCHMARK        ┃    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛    ┃  🚀 START BENCHMARK        ┃  ✨
                                  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
Background Gradient: 135deg (#00ff41 0%, #00d9ff 100%)
Border: 2px solid #00ff41
Color: #0a0e1a
Font-weight: 700
Letter-spacing: 1px
Padding: 12px 24px
Border-radius: 0px

Hover Effects:
- Box-shadow: 0 0 30px rgba(0, 255, 65, 0.6),
              0 0 50px rgba(0, 217, 255, 0.3)
- Transform: translateY(-2px)
```

### 3.4 Metric Card
```
╔════════════════════════════════════════════════╗
║ 📊 Problems Tested                             ║
║                                                ║
║ 5                                              ║
║                                                ║
╚════════════════════════════════════════════════╝
│ ╔─ Green left border (4px)
│ ╠─ Cyan top border (2px)
│ ╚─ Green top glow animation

CSS Properties:
- Background-color: #0f1419
- Border-left: 4px solid #00ff41
- Border-top: 2px solid #00d9ff
- Padding: 20px
- Box-shadow: 0 0 20px rgba(0, 255, 65, 0.15),
              inset 0 0 20px rgba(0, 255, 65, 0.05)
```

### 3.5 Tab Navigation
```
    [HEATMAP]  [RANKINGS]  [COMPARISON]  [🎯 RADAR]  [RAW DATA]
     ──────      ────────    ───────────  ───────────  ────────
     
Selected Tab: Green background, white text, glowing border
Unselected: Dark gray background, bordercolor

CSS Properties:
- Border-bottom: 2px solid #00ff41
- Tab hover: Background #141820, box-shadow glow
- Tab active: Background #00ff41, color #0a0e1a
```

### 3.6 Text Input & Selectors
```
┌──────────────────────────────────────────────────────┐
│ Select a model for analysis                          │▼│
├──────────────────────────────────────────────────────┤
│ ○ Model 1                                            │
│ ○ Model 2                                            │
│ ● Model 3 (selected)                                │
│ ○ Model 4                                            │
└──────────────────────────────────────────────────────┘

Border-color: #00d9ff
Background: #0f1419
Focus shadow: 0 0 15px rgba(0, 217, 255, 0.3)
```

---

## 4. LAYOUT SYSTEM

### Page Layout
```
┌────────────────────────────────────────────────────────┐
│ HEADER (Military Theme Applied Globally)               │
├────────────────┬────────────────────────────────────────┤
│                │                                        │
│ SIDEBAR        │ MAIN CONTENT AREA                     │
│                │                                        │
│ (220px)        │ (Responsive, fluid)                   │
│                │                                        │
│ • Input Form   │ • Results Display                     │
│ • Settings     │ • Visualizations                      │
│ • Status       │ • Tabs & Panels                       │
│                │                                        │
├────────────────┴────────────────────────────────────────┤
│ FOOTER (Privacy Notice)                                │
└────────────────────────────────────────────────────────┘
```

### Grid System
```
12-Column Grid (Streamlit default)

Full Width:
├─ 1:1 Split ─┤
├── 1:2 Split ────┤
├─── 1:3:1 Split ──────┤
└─────────────────────┘
```

### Spacing Scale
```
xs:  4px    (Component padding)
sm:  8px    (Component margin)
md:  16px   (Section margin)
lg:  24px   (Major section margin)
xl:  32px   (Layout spacing)
```

---

## 5. ANIMATION & EFFECTS

### Keyframe Animations
```css
@keyframes blink {
    0%, 49%   { opacity: 1; }
    50%, 100% { opacity: 0; }
}
Duration: 1s | Infinite | Timing: linear

@keyframes sweep {
    0%   { left: -100%; }
    100% { left: 100%; }
}
Duration: 2s | Infinite | Timing: ease-in-out
```

### Transition Effects
```css
Button hover:       all 0.3s ease
Color fade:         color 0.2s ease
Box-shadow glow:    box-shadow 0.3s ease
Transform move:     transform 0.2s ease
Slide in:           0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)
```

### Visual Effects
```
Glow Effect:
  box-shadow: 0 0 20px rgba(0, 255, 65, 0.5)
  
Scan Lines Animation:
  repeating-linear-gradient(0deg, rgba(0,255,65,0.1) 0px, 
                                  rgba(0,255,65,0.1) 1px,
                                  transparent 1px,
                                  transparent 2px)

Grid Overlay:
  repeating-linear-gradient(90deg, rgba(0,255,65,0.05) 0px,
                                   rgba(0,255,65,0.05) 1px,
                                   transparent 1px,
                                   transparent 40px)
```

---

## 6. RESPONSIVE DESIGN

### Breakpoints
```
Mobile:    < 640px
Tablet:    640px - 1024px
Desktop:   1024px - 1920px
Ultra-HD:  > 1920px
```

### Adaptive Layouts
- Full width on mobile (single column)
- 2-column layout on tablet
- 3+ columns on desktop
- Radar charts scale with viewport
- Navigation adjusts for screen size

---

## 7. ACCESSIBILITY

### Color Contrast
```
Primary Text on Background:  #f0f0f0 on #0a0e1a = 15:1 ✅
Accent on Background:        #00ff41 on #0a0e1a = 13:1 ✅
Secondary Text:              #a0a0a0 on #0f1419 = 4.5:1 ✅
```

### Interactive Elements
- All buttons have clear hover states
- Focus indicators visible (2px border)
- Tab navigation supported
- Semantic HTML used throughout
- ARIA labels where applicable

---

## 8. BRAND VOICE

### Messaging Tone
- **Technical**: Use of military terminology
- **Precise**: Clear, actionable language
- **Professional**: Executive-level communication
- **Actionable**: "Deploy", "Analyze", "Tactical", "Command"

### Language Patterns
```
INSTEAD OF:          USE:
"Run the app"        "Deploy the system"
"Upload results"     "Transmit data"
"Dashboard"          "Command Center"
"Compare"            "Tactical Overlay"
"Analysis"           "Tactical Analysis"
"Model"              "Unit" / "Asset"
"Performance"        "Tactical Performance"
```

---

## 9. IMPLEMENTATION CHECKLIST

- [x] Color palette defined and applied
- [x] Typography system established
- [x] Component library created
- [x] Layout grid implemented
- [x] Animation keyframes defined
- [x] Responsive breakpoints set
- [x] Accessibility standards met
- [x] Brand voice documented
- [x] Military aesthetic applied globally
- [x] Radar chart visualization built
- [x] Overlay comparison mode implemented
- [x] Tab system integrated

---

## 10. FILES & REFERENCES

### Main Files
```
src/ui_components.py          - UI component library
app.py                        - Main application
MILITARY_THEME_GUIDE.md       - Detailed theme guide
TACTICAL_RADAR_QUICKSTART.md  - Quick start guide
```

### Key Variables
```
MILITARY_THEME dict:
  - bg_main, bg_secondary, bg_tertiary
  - accent_primary, accent_secondary
  - text_primary, text_secondary
  - border, grid, glow, scan_color

RUBRIC_GROUPED dict:
  - 5 tactical dimensions
  - Aggregation mapping
```

---

**Design System Version**: 1.0  
**Last Updated**: March 21, 2026  
**Status**: 🟢 Production Ready  
**Theme**: Military Command Center
