"""
Script to download the Righteous font and save it to the static/css directory
"""

import os
import requests
import shutil
from pathlib import Path

# URL for Righteous font from Google Fonts
FONT_URL = "https://fonts.gstatic.com/s/righteous/v14/1cXxaUPXBpj2rGoU7C9WiHGF.woff"

# Path to save the font
BASE_DIR = Path(__file__).resolve().parent
SAVE_PATH = BASE_DIR / "static" / "css" / "Righteous.woff"


def download_font():
    print(f"Downloading Righteous font to {SAVE_PATH}")
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

        # Make request to download the font
        response = requests.get(FONT_URL, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the font file
        with open(SAVE_PATH, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        print("Font downloaded successfully!")
        return True
    except Exception as e:
        print(f"Error downloading font: {e}")
        return False


if __name__ == "__main__":
    download_font()
