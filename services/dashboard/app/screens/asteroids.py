from textual.screen import Screen
from textual.widgets import DataTable, Static
from textual import work

from app.client.api_client import get_analyzed_asteroids

class AsteroidsScreen(Screen):

    def compose(self):
        yield Static("ANALYZED ASTEROIDS", id="title")

        self.table = DataTable(id="asteroids_table")

        self.table.add_columns(
            "ID",
            "Name",
            "Risk",
            "Score",
            "Energy (MT)",
            "Distance (km)",
            "Diameter (km)",
            "Velocity (km/s)",
        )

        yield self.table

    def on_mount(self):
        self.load_asteroids()

    @work
    async def load_asteroids(self):
        self.table.clear()

        asteroids = await self.run_in_thread(get_analyzed_asteroids)

        for a in asteroids:
            self.table.add_row(
                a.get("id", "?"),
                a.get("name", "?"),
                a.get("risk_level", "?"),
                f"{a.get('risk_score', 0):.1f}",
                f"{a.get('energy_mt', 0):.2f}",
                f"{a.get('distance_km', 0):.0f}",
                f"{a.get('diameter_km', 0):.3f}",
                f"{a.get('velocity_kps', 0):.2f}",
            )
