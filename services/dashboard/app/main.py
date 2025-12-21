from textual.app import App
from textual.binding import Binding
from app.scheduler import PipelineScheduler

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
        
        scheduler =  PipelineScheduler(interval_seconds=600)
        scheduler.run_background()
        
        self.push_screen(HomeScreen())
        
if __name__ == "__main__":
    AstroForgeDashboard().run()