import sys
import os
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply modern stylesheet
    # Path when running from source
    style_sheet_path = os.path.join(os.path.dirname(__file__), "src", "ui", "resources", "modern_style.qss")

    # Path when running from a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        style_sheet_path = os.path.join(sys._MEIPASS, "src", "ui", "resources", "modern_style.qss")
    
    try:
        with open(style_sheet_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Warning: Stylesheet not found at {style_sheet_path}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())