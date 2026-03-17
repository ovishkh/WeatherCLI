from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input, Button, DataTable, Label, Tree
from textual.widgets.tree import TreeNode
from textual.binding import Binding
from textual.screen import Screen
from textual import on

import requests
import pandas as pd
from datetime import datetime

from api.weather_api import API_KEY, WEATHER_URL, fetch_weather_for_country
from models.weather_model import Weather
from services.history_service import HistoryService
from favorites.favorites_service import FavoritesService
from resources.goods import PREDEFINED_CITIES, WEATHER_TIPS, WEATHER_QUOTES

class WeatherDashboard(Static):
    """Main dashboard view."""
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Weather Dashboard", id="view-title"),
            Container(id="dashboard-content"),
            id="main-view"
        )

class WeatherSearch(Static):
    """Search view."""
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Search City", id="view-title"),
            Input(placeholder="Enter city name...", id="search-input"),
            Container(id="search-results"),
            id="main-view"
        )

class FavoritesView(Static):
    """Favorites view."""
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Favorite Cities", id="view-title"),
            Container(id="favorites-content"),
            id="main-view"
        )

class HistoryView(Static):
    """History view."""
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Search History", id="view-title"),
            DataTable(id="history-table"),
            id="main-view"
        )

class AboutView(Static):
    """About view."""
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("About WeatherCLI", id="view-title"),
            Static(
                "WeatherCLI v3.0\n\n"
                "A modern Terminal User Interface for real-time weather updates.\n"
                "Developed by Team Tengen.\n\n"
                "Features:\n"
                "- Real-time weather data\n"
                "- Favorite cities management\n"
                "- Search history\n"
                "- Weather-based tips and quotes",
                id="about-text"
            ),
            id="main-view"
        )

class CountriesView(Static):
    """Countries view for predefined cities."""
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Countries & Regions", id="view-title"),
            Container(id="countries-content"),
            id="main-view"
        )

class Sidebar(Static):
    """Sidebar navigation."""
    def compose(self) -> ComposeResult:
        tree = Tree("Menu", id="nav-tree")
        tree.root.expand()
        tree.root.add_leaf("Dashboard", data="home")
        tree.root.add_leaf("Search", data="search")
        tree.root.add_leaf("Countries", data="countries")
        tree.root.add_leaf("Favorites", data="favorites")
        tree.root.add_leaf("History", data="history")
        tree.root.add_leaf("About", data="about")
        yield tree

class WeatherApp(App):
    """WeatherCLI TUI Application."""
    
    CSS = """
    Screen {
        background: #1e1e2e;
        color: #cdd6f4;
    }
    Header {
        background: #11111b;
        color: #89b4fa;
        height: 3;
        border-bottom: solid #313244;
    }
    Footer {
        background: #11111b;
        color: #a6adc8;
    }
    Sidebar {
        width: 25;
        background: #181825;
        border-right: solid #313244;
        dock: left;
    }
    #nav-tree {
        background: transparent;
        border: none;
        padding: 1 2;
    }
    #main-view {
        padding: 2;
    }
    #view-title {
        color: #89b4fa;
        text-style: bold;
        margin-bottom: 2;
        font-size: 150%;
    }
    Input {
        background: #313244;
        border: solid #45475a;
        color: #cdd6f4;
        margin-bottom: 2;
    }
    DataTable {
        height: 100%;
        background: #181825;
        border: solid #313244;
    }
    .weather-card {
        background: #313244;
        padding: 1 2;
        border: solid #45475a;
        margin-bottom: 1;
        height: auto;
    }
    .city-name {
        color: #f9e2af;
        text-style: bold;
    }
    .temp {
        color: #fab387;
    }
    .condition {
        color: #a6e3a1;
    }
    .hidden {
        display: none;
    }
    #card-actions {
        margin-top: 1;
        height: 3;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "switch_view('home')", "Dashboard"),
        Binding("s", "switch_view('search')", "Search"),
        Binding("f", "switch_view('favorites')", "Favorites"),
        Binding("h", "switch_view('history')", "History"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Sidebar()
        with Container(id="content-area"):
            yield WeatherDashboard(id="home-view")
            yield WeatherSearch(id="search-view")
            yield CountriesView(id="countries-view")
            yield FavoritesView(id="favorites-view")
            yield HistoryView(id="history-view")
            yield AboutView(id="about-view")
        yield Footer()

    def on_mount(self) -> None:
        # Initial view setup
        for view_id in ["search", "countries", "favorites", "history", "about"]:
            self.query_one(f"#{view_id}-view").add_class("hidden")
        
        self.update_history_table()
        self.load_default_dashboard()

    def load_default_dashboard(self) -> None:
        container = self.query_one("#dashboard-content")
        container.mount(Label("Fetching world weather..."))
        
        # Fetch weather for a few popular cities for the dashboard
        default_cities = ["London", "Tokyo", "New York"]
        container.query("*").remove()
        
        for city in default_cities:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            try:
                response = requests.get(WEATHER_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    weather = Weather(data)
                    container.mount(
                        Vertical(
                            Label(f"[b]{weather.city}[/b]", classes="city-name"),
                            Label(f"{weather.temp_c}°C - {weather.weather.capitalize()}", classes="condition"),
                            classes="weather-card"
                        )
                    )
            except:
                pass

    @on(Tree.NodeSelected)
    def handle_nav(self, event: Tree.NodeSelected) -> None:
        view_id = event.node.data
        if view_id:
            self.action_switch_view(view_id)

    def action_switch_view(self, view_id: str) -> None:
        # Hide all views
        for view in self.query("#content-area > Static"):
            view.add_class("hidden")
        
        # Show selected view
        target_view = self.query_one(f"#{view_id}-view")
        target_view.remove_class("hidden")

        if view_id == "history":
            self.update_history_table()
        elif view_id == "favorites":
            self.update_favorites_view()
        elif view_id == "countries":
            self.update_countries_view()

    def update_countries_view(self) -> None:
        container = self.query_one("#countries-content")
        container.query("*").remove()
        for country in PREDEFINED_CITIES.keys():
            container.mount(Button(country.capitalize(), id=f"country-{country}", variant="success"))

    def update_history_table(self) -> None:
        table = self.query_one("#history-table", DataTable)
        table.clear(columns=True)
        if HistoryService.history:
            headers = list(HistoryService.history[0].keys())
            table.add_columns(*headers)
            for entry in HistoryService.history:
                table.add_row(*[str(v) for v in entry.values()])

    def update_favorites_view(self) -> None:
        container = self.query_one("#favorites-content")
        container.query("*").remove()
        if FavoritesService.favorites:
            for city in FavoritesService.favorites:
                container.mount(Button(city, id=f"fav-{city}", variant="primary"))
        else:
            container.mount(Label("No Favorites yet! Add some from Search."))

    @on(Input.Submitted, "#search-input")
    def handle_search(self, event: Input.Submitted) -> None:
        query = event.value.strip().lower()
        if not query:
            return

        results_container = self.query_one("#search-results")
        results_container.query("*").remove()
        results_container.mount(Label("Searching..."))

        weather_list = []
        if query in PREDEFINED_CITIES:
            # Handle country search
            weather_data = fetch_weather_for_country(query)
            # Find the actual city objects
            # For simplicity, we'll just use the dictionaries returned by fetch_weather_for_country
            # But the card expects a Weather object. Let's adjust.
            for data_dict in weather_data:
                # We can't easily turn dict back to object without another API call or modifying fetch_weather_for_country
                # Let's just create a helper to mount the card from dict
                self.mount_weather_card(data_dict, results_container)
                HistoryService.add_to_history(data_dict)
            results_container.query("Label").remove() # remove "Searching..."
        else:
            # Treat input as a city name
            params = {"q": query, "appid": API_KEY, "units": "metric"}
            try:
                response = requests.get(WEATHER_URL, params=params)
                results_container.query("*").remove()
                if response.status_code == 200:
                    data = response.json()
                    weather = Weather(data)
                    self.mount_weather_card(weather.to_dict(), results_container, weather.tip, weather.quote)
                    HistoryService.add_to_history(weather.to_dict())
                else:
                    results_container.mount(Label(f"Error: {response.status_code} - City not found."))
            except Exception as e:
                results_container.mount(Label(f"Error: {str(e)}"))

    def mount_weather_card(self, data: dict, container, tip=None, quote=None) -> None:
        city = data["City"]
        temp = data["Temperature (°C)"]
        cond = data["Condition"]
        
        card = Vertical(
            Label(f"[b]{city}[/b]", classes="city-name"),
            Label(f"Temp: {temp}°C", classes="temp"),
            Label(f"Condition: {cond}", classes="condition"),
            classes="weather-card"
        )
        if tip:
            card.mount(Label(f"\n[i]{quote}[/i]", id="weather-quote"))
            card.mount(Label(f"[b]Tip:[/b] {tip}", id="weather-tip"))
        
        actions = Horizontal(
            Button("Add to Favorites", id=f"add-fav-{city}"),
            id="card-actions"
        )
        card.mount(actions)
        container.mount(card)

    @on(Button.Pressed)
    def handle_button(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if not btn_id:
            return

        if btn_id.startswith("add-fav-"):
            city = btn_id.replace("add-fav-", "")
            FavoritesService.add_to_favorites(city)
            self.notify(f"Added {city} to Favorites!")
            self.update_favorites_view()
        elif btn_id.startswith("country-"):
            country = btn_id.replace("country-", "")
            self.action_switch_view("search")
            self.query_one("#search-input").value = country
            self.query_one("#search-input").action_submit()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()
