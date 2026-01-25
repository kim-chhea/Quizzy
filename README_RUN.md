# Run the app locally

## Quick steps (Windows)
1. Open PowerShell and cd to the project folder (where `app.py` lives).
2. Recommended: run `run.bat` (the batch file will create a local `.venv`, install deps and start Streamlit):
   ```
   run.bat
   ```

## Using PowerShell script (preferred for PowerShell users)
1. If you have script execution restrictions, run PowerShell as Administrator and execute:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
2. Run the included helper script:
   ```powershell
   .\setup.ps1 -InstallOnly   # create .venv and install requirements
   .\setup.ps1 -Run           # install (if needed) and launch Streamlit
   ```

## Manual setup (cross-platform)
1. Create & activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows (PowerShell): . .venv\Scripts\Activate.ps1
   # Windows (cmd): .venv\Scripts\activate.bat
   # macOS / Linux: source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```

---

If you'd like, you can also use the included VS Code Task: **Terminal > Run Task > Run Quizzy (Streamlit)** to install and start the app automatically.

```

</file>

Done — after adding these files, run run.bat in the project folder to start the app. If you want, I can produce a git patch or a single zipped payload next.
```
