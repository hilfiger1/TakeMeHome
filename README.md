## TakeMeHome – How to run `testing.py` (step‑by‑step)

Important notice

- This program is for personal learning/experimentation only. Do NOT use it to actually book SRT tickets. That would violate SRT’s booking policies and terms of service. You are solely responsible for how you use this code.

What this script does (high level)

- Opens the SRT website in Google Chrome.
- You manually log in and navigate to the regular ticket search page when prompted.
- You enter your search criteria in the terminal (departure, arrival, date, time, number of adults).
- The script repeatedly searches and checks results. If it finds a “예약하기” button at your requested time, it clicks it and then stops so you can continue manually.

Prerequisites

- A Mac with macOS (instructions use Terminal). Windows/Linux users can adapt the same commands in PowerShell/Bash.
- Python 3.9 or newer. Check with:
  - `python3 --version`
- Google Chrome installed and up to date. Check by opening Chrome and going to `chrome://settings/help`.
- Internet connection.

Install Python once (if needed)

- macOS often includes Python 3, but if you need it, install via Homebrew:
  - Install Homebrew (if not installed):
    - `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  - Then install Python:
    - `brew install python`

Get the code (if you haven’t already)

- If you already have this folder locally, skip this section. Otherwise:
  - `git clone git@github.com:hilfiger1/TakeMeHome.git`
  - `cd TakeMeHome`

Open the project folder in Terminal

- If you use Finder: right‑click the folder and choose “New Terminal at Folder” (or open Terminal and `cd` into the folder). For example:
  - `cd /Users/jinwoopark/auto_srt_ticketing`

Create and activate a virtual environment (recommended)

- Create a venv (one time):
  - `python3 -m venv .venv`
- Activate it (every new terminal session before running the script):
  - `source .venv/bin/activate`

Install required Python packages

- Install Selenium (and any future packages listed in requirements):
  - `python3 -m pip install --upgrade pip`
  - `pip install selenium`

Why no separate ChromeDriver setup?

- `testing.py` uses Selenium Manager which automatically locates/downloads a compatible ChromeDriver. You normally do NOT need to download or point to a driver manually.

Run the script

1) Make sure Chrome is closed or you don’t mind a new window opening.
2) In Terminal, from the project folder (and with the virtual environment active):
   - `python3 testing.py`
3) The script will open Chrome and load the SRT login page.
4) Follow on‑screen instructions in Terminal:
   - Choose a login method when prompted (회원번호 / 이메일 / 휴대전화번호).
   - Enter the requested login credentials in the Terminal prompt fields.
   - Then, as prompted by the script, manually click the appropriate buttons in the browser to complete login and navigate to the 일반승차권 조회 page.
5) Once the script detects the correct page, it will ask you for search inputs in the Terminal:
   - Departure station (e.g., 동대구)
   - Arrival station (e.g., 수서)
   - Date in YYYYMMDD (e.g., 20240917)
   - Time in HHMMSS (e.g., 160000 for 16:00)
   - Number of adult passengers (e.g., 1)
6) The script will now loop:
   - It clicks “조회하기”, waits briefly, scans the results, and looks for a row at your requested time with a visible “예약하기” button.
   - If found, it clicks that button and stops, keeping the browser open so you can continue manually. It won’t proceed with any booking actions for you.
   - If not found, it waits a short random delay and tries again.

Safety and policy reminder

- Do NOT use this program to actually book SRT tickets. It is against SRT’s booking policies. This is only a side project for learning and personal experimentation.
- You must follow all relevant terms of service and applicable laws.

Understanding inputs and behavior

- Date: must be exactly 8 digits (YYYYMMDD). Example: 20240917.
- Time: must be exactly 6 digits (HHMMSS). Example: 160000 means 16:00.
- Stations: must match what the SRT site expects (Korean station names, e.g., 동대구, 수서).
- The script relies on specific element IDs/CSS on the SRT site. If SRT changes their pages, the script may need updates.

Common issues and fixes

- Chrome/Driver mismatch:
  - If Chrome opens then fails immediately, update Chrome to the latest version and rerun. Selenium Manager should fetch a matching driver.
- Elements not found / timeouts:
  - The site may have changed or be slow. Try again later. If errors persist, the element IDs/CSS in `testing.py` may need adjustments.
- Korean page layout differences:
  - Ensure you are on the correct page: 일반승차권 조회. Follow the Terminal prompts closely.
- Permissions / Gatekeeper on macOS:
  - If macOS blocks Python or ChromeDriver, open System Settings → Privacy & Security and allow the blocked item, then rerun.
- Virtual environment not active:
  - If `selenium` is “not found”, make sure you activated the venv: `source .venv/bin/activate` and then reinstall: `pip install selenium`.

How to stop the script

- Press `Ctrl + C` in Terminal to stop it at any time.
- When the script reports it found and clicked “예약하기”, it will keep the browser open and wait until you press Enter in Terminal.

Notes about `main.py`

- `main.py` is a separate experimental script that uses a hardcoded ChromeDriver path via Selenium’s `Service`. For beginners, prefer `testing.py` because it auto‑manages the driver. If you use `main.py`, ensure the `chrome_driver_path` matches your system.

Project link

- Repository: https://github.com/hilfiger1/TakeMeHome.git

License and responsibility

- No warranty. Use at your own risk. You are responsible for complying with SRT’s policies and all laws. This code is provided for educational purposes only.


