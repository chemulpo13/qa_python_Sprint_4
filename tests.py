import pytest


from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.collector = BooksCollector()

    def test_add_new_book(self):
        self.collector.add_new_book("1984")
        assert "1984" in self.collector.get_books_genre()

    def test_add_new_book_duplicate(self):
        self.collector.add_new_book("1984")
        self.collector.add_new_book("1984")
        assert list(self.collector.get_books_genre().keys()).count("1984") == 1

    def test_set_book_genre(self):
        self.collector.add_new_book("1984")
        self.collector.set_book_genre("1984", "Фантастика")
        assert self.collector.get_book_genre("1984") == "Фантастика"

    def test_get_book_genre_nonexistent(self):
        assert self.collector.get_book_genre("Неизвестная книга") is None

    def test_get_books_with_specific_genre(self):
        self.collector.add_new_book("1984")
        self.collector.set_book_genre("1984", "Фантастика")
        self.collector.add_new_book("Дракула")
        self.collector.set_book_genre("Дракула", "Ужасы")
        books = self.collector.get_books_with_specific_genre("Фантастика")
        assert "1984" in books
        assert "Дракула" not in books

    def test_get_books_for_children(self):
        self.collector.add_new_book("Маленький принц")
        self.collector.set_book_genre("Маленький принц", "Фантастика")
        self.collector.add_new_book("Сияние")
        self.collector.set_book_genre("Сияние", "Ужасы")
        children_books = self.collector.get_books_for_children()
        assert "Маленький принц" in children_books
        assert "Сияние" not in children_books

    def test_add_book_in_favorites(self):
        self.collector.add_new_book("1984")
        self.collector.set_book_genre("1984", "Фантастика")
        self.collector.add_book_in_favorites("1984")
        assert "1984" in self.collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites(self):
        self.collector.add_new_book("1984")
        self.collector.set_book_genre("1984", "Фантастика")
        self.collector.add_book_in_favorites("1984")
        self.collector.delete_book_from_favorites("1984")
        assert "1984" not in self.collector.get_list_of_favorites_books()

    @pytest.mark.parametrize("book_name,expected", [
        ("Книга1", None),
        ("Книга2", None),
        ("Книга3", None),
    ])
    def test_get_book_genre_multiple(self, book_name, expected):
        assert self.collector.get_book_genre(book_name) == expected

    @pytest.mark.parametrize("book_name,genre", [
        ("1984", "Фантастика"),
        ("Дракула", "Ужасы"),
        ("Маленький принц", "Фантастика"),
    ])
    def test_set_genre_for_multiple_books(self, book_name, genre):
        self.collector.add_new_book(book_name)
        self.collector.set_book_genre(book_name, genre)
        assert self.collector.get_book_genre(book_name) == genre