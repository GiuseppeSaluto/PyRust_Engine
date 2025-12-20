from textual.app import App, ComposeResult
from textual.binding import Binding

from app.screens.home import HomeScreen

class AstroForgeDashboard(App):
    """AstroForge Dashboard - Terminal UI"""

    CSS_PATH = None
    TITLE = "AstroForge"
    SUB_TITLE = "Asteroid Risk Analysis Dashboard"  
    
    BINDINGS = [
        Binding("q", "quit", "Quit the application", show=True),
        Binding("h", "go_home", "Go to Home Screen", show=True),
    ]

    def on_mount(self) -> None:
        """Called when the app starts."""
        self.push_screen(HomeScreen())
        
if __name__ == "__main__":
    AstroForgeDashboard().run()