
# Class Workout 105 — 1RM Helper

Two interfaces that share one math module:

- **Web app (Streamlit):** runs locally or deploys free to Streamlit Community Cloud.
- **Desktop app (Tkinter):** runs as a simple macOS window; can be bundled with PyInstaller.

## Files

- `one_rm_core.py` — pure math functions
- `app_streamlit.py` — Streamlit web UI
- `desktop_tk.py` — Tkinter desktop UI
- `requirements.txt` — only needs Streamlit

## Run locally (web)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app_streamlit.py
```

## Run locally (desktop)

```bash
python3 desktop_tk.py
```

## Build a macOS app (optional)

```bash
pip install pyinstaller
pyinstaller --windowed --onefile desktop_tk.py
```

The resulting app bundle will be in `dist/`.

## Deploy free (phone-friendly)

1. Push this folder to a GitHub repo.
2. Go to Streamlit Community Cloud → **Deploy app**.
3. Point to `app_streamlit.py`, and it will read `requirements.txt` automatically.

## Notes

- Class 1RM rule = measured working weight **+ add-on** (default +10 lb). It **ignores reps**.
- Epley/Brzycki use reps and are shown side-by-side for context.
- All outputs are **rounded to the nearest 5 lb** and plate math is shown for **Bench Press** and **Incline Bench**.
- Plate inventory assumed: 45, 25, 10, 5; bar = 45 lb.
