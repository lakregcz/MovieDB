import flet as ft
import requests
from io import BytesIO
import base64
import webbrowser
import asyncio

API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_READ_ACCESS_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/w1280"


class TMDBApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_content_type = "movie"
        self.current_selection = None
        self.search_results = []

        self.page.title = "MovieDB - Movie & TV Discovery"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0a0a0a"
        self.page.padding = 0
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.window_resizable = True
        self.page.window_maximizable = True
        self.page.fonts = {
            "Netflix": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
        }

        self.colors = {
            "primary": "#e50914",
            "secondary": "#221f1f",
            "background": "#141414",
            "surface": "#1f1f1f",
            "text_primary": "#ffffff",
            "text_secondary": "#b3b3b3",
            "accent": "#46d369"
        }

        self.setup_ui()

    def setup_ui(self):
        self.movie_button = ft.ElevatedButton(
            "Movies",
            bgcolor=self.colors["primary"] if self.current_content_type == "movie" else self.colors["surface"],
            color=self.colors["text_primary"],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            on_click=lambda _: self.change_content_type("movie")
        )

        self.tv_button = ft.ElevatedButton(
            "TV Shows",
            bgcolor=self.colors["primary"] if self.current_content_type == "tv" else self.colors["surface"],
            color=self.colors["text_primary"],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            on_click=lambda _: self.change_content_type("tv")
        )

        header = ft.Container(
            content=ft.Row([
                ft.Text(
                    "FlixSearch",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=self.colors["primary"],
                    font_family="Inter"
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row([
                        self.movie_button,
                        self.tv_button
                    ], spacing=10)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
            bgcolor=self.colors["background"],
            border=ft.border.only(bottom=ft.BorderSide(1, "#333"))
        
        self.search_field = ft.TextField(
            hint_text=f"Search for {self.current_content_type}s...",
            border_radius=25,
            filled=True,
            bgcolor=self.colors["surface"],
            border_color="transparent",
            focused_border_color=self.colors["primary"],
            hint_style=ft.TextStyle(color=self.colors["text_secondary"]),
            text_style=ft.TextStyle(color=self.colors["text_primary"], size=16),
            content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self.search_content,
            width=600,
            height=50
        )

        search_section = ft.Container(
            content=ft.Column([
                ft.Container(height=40),
                ft.Row([
                    self.search_field,
                    ft.ElevatedButton(
                        "Search",
                        bgcolor=self.colors["primary"],
                        color=self.colors["text_primary"],
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=25),
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        ),
                        on_click=self.search_content,
                        height=50
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                ft.Container(height=40)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=self.colors["background"],
            padding=ft.padding.all(20)
        )

        self.results_grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=220,
            child_aspect_ratio=0.65,
            spacing=20,
            run_spacing=25,
            padding=ft.padding.all(20)
        
        self.details_modal = self.create_details_modal()

        main_content = ft.Column([
            search_section,
            ft.Container(
                content=self.results_grid,
                expand=True,
                bgcolor=self.colors["background"]
            )
        ], spacing=0)

        content_stack = ft.Stack([
            main_content,
            self.details_modal
        ])

        self.page.add(
            ft.Column([
                header,
                ft.Container(
                    content=content_stack,
                    expand=True
                )
            ], spacing=0, expand=True)
        )

    def create_details_modal(self):
        self.modal_backdrop = ft.Container(
            width=400,
            height=600,
            border_radius=15,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS
        )

        self.modal_title = ft.Text(
            "",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=self.colors["text_primary"]
        )

        self.modal_meta = ft.Text(
            "",
            size=14,
            color=self.colors["text_secondary"]
        )

        self.modal_overview = ft.Text(
            "",
            size=14,
            color=self.colors["text_primary"],
            max_lines=8
        )

        self.modal_rating = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.STAR, color="#ffd700", size=20),
                ft.Text("", size=16, color=self.colors["text_primary"], weight=ft.FontWeight.BOLD)
            ], spacing=5),
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            bgcolor=self.colors["surface"],
            border_radius=20
        )

        modal_content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=self.colors["text_primary"],
                        bgcolor=self.colors["surface"],
                        on_click=self.close_modal
                    )
                ]),
                ft.Row([
                    self.modal_backdrop,
                    ft.Container(
                        content=ft.Column([
                            self.modal_title,
                            ft.Container(height=10),
                            self.modal_meta,
                            ft.Container(height=15),
                            self.modal_rating,
                            ft.Container(height=20),
                            ft.Text("Overview", size=18, weight=ft.FontWeight.BOLD, color=self.colors["text_primary"]),
                            ft.Container(height=10),
                            self.modal_overview,
                            ft.Container(height=30),
                            ft.ElevatedButton(
                                "View on TMDB",
                                bgcolor=self.colors["primary"],
                                color=self.colors["text_primary"],
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=25),
                                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                                ),
                                on_click=self.open_tmdb_page,
                                width=200
                            )
                        ], spacing=0),
                        padding=ft.padding.all(30),
                        width=400
                    )
                ], spacing=30, alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=0),
            bgcolor=self.colors["secondary"],
            border_radius=20,
            padding=ft.padding.all(20),
            width=900,
            height=700,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLACK38,
                offset=ft.Offset(0, 10)
            )
        )

        return ft.Container(
            content=ft.Stack([
                ft.Container(
                    bgcolor="#000000aa",
                    on_click=self.close_modal
                ),
                ft.Container(
                    content=modal_content,
                    alignment=ft.alignment.center
                )
            ]),
            visible=False,
            expand=True
        )

    def change_content_type(self, content_type):
        self.current_content_type = content_type
        self.search_field.hint_text = f"Search for {content_type}s..."
        self.movie_button.bgcolor = self.colors["primary"] if content_type == "movie" else self.colors["surface"]
        self.tv_button.bgcolor = self.colors["primary"] if content_type == "tv" else self.colors["surface"]
        self.results_grid.controls.clear()
        self.page.update()

    async def search_content(self, e=None):
        query = self.search_field.value.strip()
        if not query:
            return

        self.results_grid.controls.clear()

        loading_card = ft.Container(
            content=ft.Column([
                ft.ProgressRing(color=self.colors["primary"]),
                ft.Text("Searching...", color=self.colors["text_primary"])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=200,
            height=300,
            bgcolor=self.colors["surface"],
            border_radius=10,
            padding=ft.padding.all(20),
            alignment=ft.alignment.center
        )
        self.results_grid.controls.append(loading_card)
        self.page.update()

        headers = {
            "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}",
            "accept": "application/json"
        }

        params = {
            "api_key": API_KEY,
            "query": query,
            "include_adult": "false",
            "language": "en-US",
            "page": 1
        }

        try:
            response = requests.get(
                f"{BASE_URL}/search/{self.current_content_type}",
                headers=headers,
                params=params
            )
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])
            self.search_results = results

            self.results_grid.controls.clear()

            if not results:
                no_results = ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=60, color=self.colors["text_secondary"]),
                        ft.Text("No results found", color=self.colors["text_secondary"], size=16)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=200,
                    height=300,
                    alignment=ft.alignment.center
                )
                self.results_grid.controls.append(no_results)
                self.page.update()
                return

            for item in results:
                card = self.create_result_card(item)
                self.results_grid.controls.append(card)

            self.page.update()

        except Exception as e:
            self.results_grid.controls.clear()
            error_card = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, size=60, color=self.colors["primary"]),
                    ft.Text(f"Error: {str(e)}", color=self.colors["text_primary"], text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=200,
                height=300,
                alignment=ft.alignment.center
            )
            self.results_grid.controls.append(error_card)
            self.page.update()

    def create_result_card(self, item):
        title = item.get("title" if self.current_content_type == "movie" else "name", "Unknown")
        poster_path = item.get("poster_path")
        rating = item.get("vote_average", 0)

        if poster_path:
            image_url = f"{IMAGE_BASE_URL}{poster_path}"
            poster = ft.Image(
                src=image_url,
                width=200,
                height=300,
                fit=ft.ImageFit.COVER,
                border_radius=10
            )
        else:
            poster = ft.Container(
                content=ft.Icon(ft.Icons.MOVIE, size=60, color=self.colors["text_secondary"]),
                width=200,
                height=300,
                bgcolor=self.colors["surface"],
                border_radius=10,
                alignment=ft.alignment.center
            )

        rating_badge = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.STAR, color="#ffd700", size=12),
                ft.Text(f"{rating:.1f}", size=12, color=self.colors["text_primary"], weight=ft.FontWeight.BOLD)
            ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            bgcolor="#00000088",
            border_radius=10,
            top=10,
            right=10
        )

        card_content = ft.Stack([
            poster,
            rating_badge
        ])

        title_text = ft.Text(
            title,
            size=13,
            color=self.colors["text_primary"],
            weight=ft.FontWeight.W_500,
            max_lines=3,
            text_align=ft.TextAlign.CENTER,
            overflow=ft.TextOverflow.ELLIPSIS,
            width=200
        )

        card = ft.Container(
            content=ft.Column([
                card_content,
                ft.Container(height=15),
                ft.Container(
                    content=title_text,
                    width=200,
                    height=60,
                    alignment=ft.alignment.center
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(8),
            border_radius=15,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=lambda e, item=item: self.show_details(item),
            on_hover=self.card_hover_effect
        )

        return card

    def card_hover_effect(self, e):
        e.control.scale = 1.05 if e.data == "true" else 1.0
        e.control.update()

    def show_details(self, item):
        self.current_selection = item
        title = item.get("title" if self.current_content_type == "movie" else "name", "Unknown")
        self.modal_title.value = title

        date = item.get("release_date" if self.current_content_type == "movie" else "first_air_date", "")
        year = date[:4] if date else "Unknown"

        if self.current_content_type == "movie":
            meta_text = f"Movie • {year}"
        else:
            meta_text = f"TV Show • {year}"

        self.modal_meta.value = meta_text

        rating = item.get("vote_average", 0)
        self.modal_rating.content.controls[1].value = f"{rating:.1f}"

        overview = item.get("overview", "No overview available.")
        self.modal_overview.value = overview

        backdrop_path = item.get("backdrop_path") or item.get("poster_path")
        if backdrop_path:
            image_url = f"{BACKDROP_BASE_URL}{backdrop_path}"
            self.modal_backdrop.content = ft.Image(
                src=image_url,
                width=400,
                height=600,
                fit=ft.ImageFit.COVER
            )
        else:
            self.modal_backdrop.content = ft.Container(
                content=ft.Icon(ft.Icons.MOVIE, size=100, color=self.colors["text_secondary"]),
                alignment=ft.alignment.center,
                bgcolor=self.colors["surface"]
            )

        self.details_modal.visible = True
        self.page.update()

    def close_modal(self, e):
        self.details_modal.visible = False
        self.page.update()

    def open_tmdb_page(self, e):
        if self.current_selection:
            item_id = self.current_selection.get("id")
            if item_id:
                url = f"https://www.themoviedb.org/{self.current_content_type}/{item_id}"
                webbrowser.open(url)


def main(page: ft.Page):
    app = TMDBApp(page)


if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP
    )
