import os
import unittest
from tempfile import NamedTemporaryFile

from main import load_movies_from_csv, parse_genres, recommend_items


class RecommendationSystemTests(unittest.TestCase):
    def test_recommends_matching_genre_case_insensitively(self) -> None:
        items = [{"title": "Avengers", "genre": "Action"}, {"title": "Titanic", "genre": "Romance"}]
        self.assertEqual(recommend_items(items, "action"), ["Avengers"])

    def test_returns_empty_list_for_unknown_genre(self) -> None:
        items = [{"title": "Avengers", "genre": "Action"}]
        self.assertEqual(recommend_items(items, "Comedy"), [])

    def test_loads_movies_from_csv(self) -> None:
        with NamedTemporaryFile("w", newline="", encoding="utf-8", delete=False) as handle:
            handle.write("title,genre\nAvengers,Action\nTitanic,Romance\n")
            temp_path = handle.name

        try:
            loaded_items = load_movies_from_csv(temp_path)
        finally:
            os.remove(temp_path)

        self.assertEqual(loaded_items, [{"title": "Avengers", "genre": "Action"}, {"title": "Titanic", "genre": "Romance"}])

    def test_parses_multiple_genres_from_comma_separated_input(self) -> None:
        self.assertEqual(parse_genres("Action, Romance , Horror"), ["Action", "Romance", "Horror"])


if __name__ == "__main__":
    unittest.main()
