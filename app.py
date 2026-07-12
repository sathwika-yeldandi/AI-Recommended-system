import csv
import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Dict, List

MOVIES: List[Dict[str, str]] = [
    {"title": "Avengers", "genre": "Action"},
    {"title": "Batman Begins", "genre": "Action"},
    {"title": "Titanic", "genre": "Romance"},
    {"title": "La La Land", "genre": "Romance"},
    {"title": "Interstellar", "genre": "Sci-Fi"},
    {"title": "The Conjuring", "genre": "Horror"},
    {"title": "The Shining", "genre": "Horror"},
]


def load_movies_from_csv(file_path: str) -> List[Dict[str, str]]:
    movies: List[Dict[str, str]] = []
    with open(file_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            movies.append({"title": row["title"], "genre": row["genre"]})
    return movies


def recommend_items(items: List[Dict[str, str]], preferred_genres: List[str]) -> List[str]:
    normalized_genres = {genre.strip().lower() for genre in preferred_genres if genre and genre.strip()}
    return [
        item["title"]
        for item in items
        if item["genre"].strip().lower() in normalized_genres
    ]


class RecommendationApp:
    def __init__(self, root: tk.Tk, items: List[Dict[str, str]]) -> None:
        self.root = root
        self.items = items
        self.root.title("AI Recommendation System")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        self.root.configure(bg="#f4f7fb")
        self.favorites_file = Path(__file__).with_name("favorites.json")
        self.favorites: List[Dict[str, str]] = self.load_favorites()

        header_frame = tk.Frame(root, bg="#ffffff", bd=1, relief=tk.RIDGE)
        header_frame.pack(fill=tk.X, padx=12, pady=(12, 10))
        tk.Label(header_frame, text="AI Recommendation System", font=("Segoe UI", 18, "bold"), fg="#1f3c88", bg="#ffffff").pack(pady=(10, 4))
        tk.Label(header_frame, text="Discover movies by genre, title, or a random pick", font=("Segoe UI", 10), fg="#5a6c85", bg="#ffffff").pack(pady=(0, 10))

        genres = sorted({item["genre"] for item in items})
        self.genre_var = tk.StringVar(value=genres[0] if genres else "")
        self.genre_dropdown = tk.OptionMenu(root, self.genre_var, *genres)
        self.genre_dropdown.config(width=28, bg="#ffffff", fg="#234", highlightbackground="#dfe7f5", bd=1, font=("Segoe UI", 10))
        self.genre_dropdown.pack(pady=(4, 6))

        tk.Label(root, text="Search by title", font=("Segoe UI", 10), fg="#4b5b6e", bg="#f4f7fb").pack(pady=(2, 2))
        self.title_entry = tk.Entry(root, width=36, bg="#ffffff", fg="#233", insertbackground="#233", bd=1, relief=tk.SOLID)
        self.title_entry.pack(pady=(0, 6))

        search_action_frame = tk.Frame(root, bg="#f4f7fb")
        search_action_frame.pack(pady=(0, 8))
        tk.Button(search_action_frame, text="OK", width=10, command=self.show_title_search, bg="#8e44ad", fg="white", relief=tk.RAISED, bd=1).pack(side=tk.LEFT, padx=6)

        button_frame = tk.Frame(root, bg="#f4f7fb")
        button_frame.pack(pady=8)
        tk.Button(button_frame, text="Get Recommendations", width=18, command=self.show_recommendations, bg="#3f7cff", fg="white", relief=tk.RAISED, bd=1).pack(side=tk.LEFT, padx=4, pady=2)
        tk.Button(button_frame, text="Show All Movies", width=18, command=self.show_all_movies, bg="#ff8a00", fg="white", relief=tk.RAISED, bd=1).pack(side=tk.LEFT, padx=4, pady=2)
        tk.Button(button_frame, text="Random Movie", width=14, command=self.show_random_movie, bg="#00b894", fg="white", relief=tk.RAISED, bd=1).pack(side=tk.LEFT, padx=4, pady=2)
        tk.Button(button_frame, text="Clear", width=10, command=self.clear_results, bg="#7f8c8d", fg="white", relief=tk.RAISED, bd=1).pack(side=tk.LEFT, padx=4, pady=2)
        tk.Button(button_frame, text="Search Title", width=14, command=self.show_title_search, bg="#8e44ad", fg="white", relief=tk.RAISED, bd=1).pack(side=tk.LEFT, padx=4, pady=2)
        tk.Button(button_frame, text="Add Favorite", width=14, command=self.add_favorite, bg="#e17055", fg="white", relief=tk.RAISED, bd=1).pack(side=tk.LEFT, padx=4, pady=2)
        tk.Button(button_frame, text="Favorites", width=12, command=self.show_favorites, bg="#0984e3", fg="white", relief=tk.RAISED, bd=1).pack(side=tk.LEFT, padx=4, pady=2)

        tk.Label(root, text="Results", font=("Segoe UI", 11, "bold"), fg="#233", bg="#f4f7fb").pack(pady=(8, 4))
        self.result_text = tk.Text(root, height=12, width=52, wrap=tk.WORD, bg="#ffffff", fg="#233", insertbackground="#233", bd=1, relief=tk.SOLID)
        self.result_text.pack(padx=10, pady=(2, 10))
        self.result_text.configure(state="disabled")

    def show_recommendations(self) -> None:
        selected_genre = self.genre_var.get().strip()
        matches = recommend_items(self.items, [selected_genre])

        if matches:
            self._set_result("Recommended Movies:\n" + "\n".join(f"- {title}" for title in matches))
        else:
            self._set_result("No movies found for those genres.")

    def show_all_movies(self) -> None:
        movie_list = "All Movies:\n" + "\n".join(f"- {item['title']} ({item['genre']})" for item in self.items)
        self._set_result(movie_list)

    def show_random_movie(self) -> None:
        import random

        movie = random.choice(self.items)
        self._set_result(f"Random Pick:\n- {movie['title']} ({movie['genre']})")

    def show_title_search(self) -> None:
        query = self.title_entry.get().strip().lower()
        matches = [item for item in self.items if query in item["title"].lower()]

        if matches:
            self._set_result("Search Results:\n" + "\n".join(f"- {item['title']} ({item['genre']})" for item in matches))
        else:
            self._set_result("No movie found with that title.")

    def add_favorite(self) -> None:
        title = self.title_entry.get().strip()
        if not title:
            self._set_result("Enter a title before adding a favorite.")
            return

        for item in self.items:
            if item["title"].lower() == title.lower():
                if item not in self.favorites:
                    self.favorites.append(item)
                    self.save_favorites()
                self._set_result("Favorite added:\n" + "\n".join(f"- {favorite['title']} ({favorite['genre']})" for favorite in self.favorites))
                return

        self._set_result("No movie found with that title.")

    def load_favorites(self) -> List[Dict[str, str]]:
        if self.favorites_file.exists():
            with open(self.favorites_file, encoding="utf-8") as handle:
                return json.load(handle)
        return []

    def save_favorites(self) -> None:
        with open(self.favorites_file, "w", encoding="utf-8") as handle:
            json.dump(self.favorites, handle, indent=2)

    def show_favorites(self) -> None:
        if self.favorites:
            content = "Favorites:\n" + "\n".join(f"- {favorite['title']} ({favorite['genre']})" for favorite in self.favorites)
        else:
            content = "No favorites saved yet."
        self._set_result(content)

    def remove_favorite(self, title: str) -> None:
        self.favorites = [favorite for favorite in self.favorites if favorite["title"].lower() != title.lower()]
        self.save_favorites()
        self.show_favorites()

    def clear_results(self) -> None:
        self._set_result("")

    def _set_result(self, content: str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, content)
        self.result_text.configure(state="disabled")


def main() -> None:
    data_file = Path(__file__).with_name("movies.csv")
    if data_file.exists():
        items = load_movies_from_csv(str(data_file))
    else:
        items = MOVIES

    root = tk.Tk()
    RecommendationApp(root, items)
    root.mainloop()


if __name__ == "__main__":
    main()
