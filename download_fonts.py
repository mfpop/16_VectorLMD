"""
Script to download the Righteous and Lora fonts and save them to the static/css directory
"""

import os
import requests
import shutil
from pathlib import Path

# Define font URLs
FONTS = {
    "Righteous.woff": "https://fonts.gstatic.com/s/righteous/v14/1cXxaUPXBpj2rGoU7C9WiHGF.woff",
    "Lora-Regular.woff2": "https://fonts.gstatic.com/s/lora/v32/0QI6MX1D_JOuGQbT0gvTJPa787weuxJBkqt8ndeY9Z6JTg.woff2",
    "Lora-Regular.woff": "https://fonts.gstatic.com/s/lora/v32/0QI6MX1D_JOuGQbT0gvTJPa787weuxJBkq58ndeY9Z4.woff",
    "Lora-Bold.woff2": "https://fonts.gstatic.com/s/lora/v32/0QI6MX1D_JOuGQbT0gvTJPa787z5vBJBkqt8ndeY9Z6JTg.woff2",
    "Lora-Bold.woff": "https://fonts.gstatic.com/s/lora/v32/0QI6MX1D_JOuGQbT0gvTJPa787z5vBJBkq58ndeY9Z4.woff",
    "Lora-Italic.woff2": "https://fonts.gstatic.com/s/lora/v32/0QI8MX1D_JOuMw_hLdO6T2wV9KnW-MoFoqF2mvWc3ZyhTjcV.woff2",
    "Lora-Italic.woff": "https://fonts.gstatic.com/s/lora/v32/0QI8MX1D_JOuMw_hLdO6T2wV9KnW-MoFoqF2mvWc3ZyHTjc.woff",
}

# Path to save the fonts
BASE_DIR = Path(__file__).resolve().parent
SAVE_DIR = BASE_DIR / "static" / "css"


def download_fonts():
    # Ensure directory exists
    os.makedirs(SAVE_DIR, exist_ok=True)

    for font_name, font_url in FONTS.items():
        save_path = SAVE_DIR / font_name
        print(f"Downloading {font_name} to {save_path}")

        try:
            # Make request to download the font
            response = requests.get(font_url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Save the font file
            with open(save_path, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)

            print(f"{font_name} downloaded successfully!")
        except Exception as e:
            print(f"Error downloading {font_name}: {e}")


if __name__ == "__main__":
    download_fonts()
