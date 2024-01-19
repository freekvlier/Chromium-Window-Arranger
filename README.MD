# Chromium Window Arranger
## Overview
This Python script is designed to automate the launching and arrangement of multiple Chromium browser instances, each configured with a different proxy. The goal is to open specified URLs simultaneously in these instances and arrange the windows in a grid on the user's screen.

## Features
- Fetches a list of proxy addresses from a specified website.
- Launches Chromium browser instances with separate proxies.
- Opens a target URL in each browser window.
- Arranges the browser windows in a customizable grid layout.

## Prerequisites
- Python 3.x
- Chrome WebDriver: Download the appropriate version matching your Chrome browser from here and ensure it's in your system's PATH.

## Usage
#### 1. Clone this repository to your local machine:
```bash
git clone https://github.com/freekvlier/chromium-window-arranger.git
```
#### 2. Navigate to the project directory:
```bash
cd chromium-window-arranger
```

#### 3. Create a Virtual Environment (Optional but recommended):
```bash
python -m venv env
```
#### 4. Activate the Virtual Environment

Activate the virtual environment to isolate your package dependencies.

- Windows:
```bash
.\env\Scripts\activate
```

- Mac/Linux:
```bash
source env/bin/activate
```

#### 5. Install Required Python Packages:
```bash
pip install -r requirements.txt
```
This installs the necessary Python packages (requests, beautifulsoup4, selenium, pygetwindow, pyautogui) for the scrip

#### 6. Run the script:
```bash
python main.py
```
Press 'Q' in terminal to exit the program.

## Configuration
- Adjust the NUM_PROXIES_TO_FETCH variable to specify the number of proxy addresses to fetch.
- Modify the TARGET_URL variable to set the URL to be opened in all browser windows.