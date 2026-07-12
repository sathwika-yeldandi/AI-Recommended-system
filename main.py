import csv
from pathlib import Path
from typing import Dict, List, Sequence, Union

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


def parse_genres(input_text: str) -> List[str]:
    return [genre.strip() for genre in input_text.split(",") if genre.strip()]


def recommend_items(items: List[Dict[str, str]], preferred_genre: Union[str, Sequence[str]]) -> List[str]:
    if isinstance(preferred_genre, str):
        preferred_genres = parse_genres(preferred_genre)
    else:
        preferred_genres = [genre.strip() for genre in preferred_genre if genre and genre.strip()]

    normalized_genres = {genre.lower() for genre in preferred_genres}
    return [
        item["title"]
        for item in items
        if item["genre"].strip().lower() in normalized_genres
    ]


def show_available_movies(items: List[Dict[str, str]]) -> None:
    print("\nAvailable Movies:")
    for item in items:
        print(f"- {item['title']} ({item['genre']})")


def run_menu(items: List[Dict[str, str]]) -> None:
    while True:
        print("\nMenu")
        print("1. View all movies")
        print("2. Get recommendations")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_available_movies(items)
        elif choice == "2":
            print("Enter one or more genres separated by commas (for example: Action, Romance)")
            genres = input("Genre(s): ")
            matches = recommend_items(items, genres)

            if matches:
                print("\nRecommended Movies:")
                for title in matches:
                    print(f"- {title}")
            else:
                print("No movies found for those genres.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def main() -> None:
    data_file = Path(__file__).with_name("movies.csv")

    if data_file.exists():
        movies = load_movies_from_csv(str(data_file))
    else:
        movies = MOVIES

    print("AI Recommendation System")
    print("Available genres: Action, Romance, Sci-Fi, Horror")
    run_menu(movies)


if __name__ == "__main__":
    main()
