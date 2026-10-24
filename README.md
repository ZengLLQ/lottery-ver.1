# Doorprize Lottery App (v1)

> Clean, rapid-built fullscreen doorprize lottery draw application built in **Python Tkinter** featuring duplicate prevention, draw history tracking, and big-screen display.

---

## ✦ Background

Created as a rapid coding challenge ("Debora x Ling-Ling's Workspace") to build a reliable, production-ready doorprize drawing application in **under 17 minutes** without any AI assistance.

## 🎯 Features

- **Fullscreen Stage Presentation:** Designed specifically for auditoriums, banquets, and stage projectors with high-contrast `#0a0a0a` dark theme.
- **Duplicate Prevention:** Drawn numbers are automatically stored in `lottery_used_numbers.json` so no participant wins twice.
- **Batch Draws:** Draw single or multiple winner numbers simultaneously (e.g., 5, 10, or custom batches).
- **History & Persistence:** Full draw log with timestamps stored in `lottery_history.json`.
- **Keyboard Shortcuts:**
  - `F11` or `Escape` to toggle fullscreen mode.
  - Spacebar or Enter to trigger the draw.

## 📁 Repository Structure

```
├── lottery_app.py               # Main application entry point & Tkinter UI
├── lottery_history.json         # Persisted winning draw history log
├── lottery_used_numbers.json    # Registered pool of drawn numbers
├── pyproject.toml               # Project metadata
└── uv.lock                      # uv package lockfile
```

## 🛠️ Getting Started

### Prerequisites

- Python 3.10+ with Tkinter

### Running the App

```bash
# Clone the repository
git clone https://github.com/ZengLLQ/lottery-ver.1.git
cd lottery-ver.1

# Run the app
python lottery_app.py
```

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
