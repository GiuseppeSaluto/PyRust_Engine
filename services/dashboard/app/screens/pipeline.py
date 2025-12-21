from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Horizontal
from textual import work

from app.client.api_client import run_pipeline, get_system_status

class PipelineScreen(Screen):

    def compose(self):
        yield Static("PIPELINE CONTROL", id="title")

        with Vertical(id="stats"):
            yield Static("Unprocessed: --", id="unprocessed")
            yield Static("Analyzed today: --", id="analyzed_today")
            yield Static("High / Critical risks: --", id="high_risks")
            yield Static("Last run: --", id="last_run")

        with Horizontal(id="actions"):
            yield Button("Run Pipeline", id="run_pipeline")
            yield Button("Back", id="back")

    def on_mount(self):
        self.refresh_stats()
        self.set_interval(20, self.refresh_stats)

    @work
    async def refresh_stats(self):
        status = get_system_status()
        backend = status.get("backend", {})

        if backend.get("status") != "ok":
            self.query_one("#unprocessed").update("Backend unreachable")
            return

        stats = backend

        self.query_one("#unprocessed").update(
            f"Unprocessed: {stats.get('unprocessed', '--')}"
        )
        self.query_one("#analyzed_today").update(
            f"Analyzed today: {stats.get('analyzed_today', '--')}"
        )
        self.query_one("#high_risks").update(
            f"High / Critical risks: {stats.get('high_risks', '--')}"
        )
        self.query_one("#last_run").update(
            f"Last run: {stats.get('last_pipeline_run', '--')}"
        )

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "run_pipeline":
            self.run_pipeline()

        elif event.button.id == "back":
            self.app.pop_screen()

    @work
    async def run_pipeline(self):
        self.query_one("#last_run").update("Running pipeline...")
        result = run_pipeline(limit=100)

        if "error" in result:
            self.query_one("#last_run").update("Pipeline failed")
        else:
            self.query_one("#last_run").update("Pipeline completed")
            self.refresh_stats()
