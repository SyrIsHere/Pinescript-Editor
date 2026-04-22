import json
from pathlib import Path
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import QApplication

class ThemeManager:
    def __init__(self):
        self.themes_dir = Path(__file__).parent.parent / "themes"
        self.current_theme = None
        
    def load_theme(self, theme_name):
        theme_path = self.themes_dir / f"{theme_name}.json"
        if not theme_path.exists():
            theme_path = self.themes_dir / "dark.json"
        
        with open(theme_path, 'r') as f:
            self.current_theme = json.load(f)
        return self.current_theme
    
    def apply_theme(self, widget):
        if not self.current_theme:
            return
        
        colors = self.current_theme['colors']
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(colors['background']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors['foreground']))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors['editor_background']))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors['editor_foreground']))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors['selection']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors['foreground']))
        
        widget.setPalette(palette)
        
    def get_syntax_colors(self):
        if not self.current_theme:
            return {}
        return self.current_theme.get('syntax', {})
