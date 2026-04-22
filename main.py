import sys
from PyQt6.QtWidgets import QApplication
from editor.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Pine Script Editor")
    app.setOrganizationName("PineScriptEditor")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
