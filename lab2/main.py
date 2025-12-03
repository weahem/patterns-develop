from __future__ import annotations  # Позволяет использовать отложенные аннотации

from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# === Абстрактный класс книги ===
class Book(ABC):
    def __init__(self, title: str, author: str, copies: int, location: str):
        self.title = title
        self.author = author
        self.copies = copies
        self.location = location

    @property
    @abstractmethod
    def genre(self) -> str:
        pass

    @abstractmethod
    def get_extra_fields(self) -> Dict[str, str]:
        """Возвращает словарь дополнительных атрибутов для отображения."""
        pass

    def display_info(self) -> str:
        extra = ", ".join(f"{k}: {v}" for k, v in self.get_extra_fields().items())
        return (
            f"[{self.genre}] «{self.title}» — {self.author} | "
            f"Экземпляров: {self.copies}, Местоположение: {self.location} | {extra}"
        )

# === Конкретные типы книг ===
class FictionBook(Book):
    def __init__(self, title: str, author: str, copies: int, location: str, age_rating: str):
        super().__init__(title, author, copies, location)
        self.age_rating = age_rating

    @property
    def genre(self) -> str:
        return "художественная"

    def get_extra_fields(self) -> Dict[str, str]:
        return {"Возрастной рейтинг": self.age_rating}

class ScienceBook(Book):
    def __init__(self, title: str, author: str, copies: int, location: str, field: str):
        super().__init__(title, author, copies, location)
        self.field = field

    @property
    def genre(self) -> str:
        return "научная"

    def get_extra_fields(self) -> Dict[str, str]:
        return {"Область науки": self.field}

class ReferenceBook(Book):
    def __init__(self, title: str, author: str, copies: int, location: str, edition: str):
        super().__init__(title, author, copies, location)
        self.edition = edition

    @property
    def genre(self) -> str:
        return "справочная"

    def get_extra_fields(self) -> Dict[str, str]:
        return {"Издание": self.edition}

# === Абстрактная фабрика ===
class BookCreator(ABC):
    @abstractmethod
    def get_extra_prompts(self) -> Dict[str, str]:
        """Возвращает подсказки для дополнительных полей: {'ключ': 'подсказка'}"""
        pass

    @abstractmethod
    def create_book(self, title: str, author: str, copies: int, location: str, extra: Dict[str, str]) -> Book:
        pass

# === Конкретные фабрики ===
class FictionBookCreator(BookCreator):
    def get_extra_prompts(self) -> Dict[str, str]:
        return {"age_rating": "Введите возрастной рейтинг (например, 12+, 16+, 18+): "}

    def create_book(self, title: str, author: str, copies: int, location: str, extra: Dict[str, str]) -> Book:
        return FictionBook(title, author, copies, location, extra["age_rating"])

class ScienceBookCreator(BookCreator):
    def get_extra_prompts(self) -> Dict[str, str]:
        return {"field": "Введите научную область (например, Физика, Биология): "}

    def create_book(self, title: str, author: str, copies: int, location: str, extra: Dict[str, str]) -> Book:
        return ScienceBook(title, author, copies, location, extra["field"])

class ReferenceBookCreator(BookCreator):
    def get_extra_prompts(self) -> Dict[str, str]:
        return {"edition": "Введите издание (например, 2-е, Исправленное): "}

    def create_book(self, title: str, author: str, copies: int, location: str, extra: Dict[str, str]) -> Book:
        return ReferenceBook(title, author, copies, location, extra["edition"])

# === Менеджер библиотеки (синглтон) ===
class LibraryManager:
    _instance: Optional[LibraryManager] = None
    _books: List[Book]
    _creators: Dict[str, BookCreator]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Присваиваем значения БЕЗ аннотаций типов
            cls._instance._books = []
            cls._instance._creators = {
                "художественная": FictionBookCreator(),
                "научная": ScienceBookCreator(),
                "справочная": ReferenceBookCreator(),
            }
        return cls._instance

    def register_creator(self, genre: str, creator: BookCreator):
        """Позволяет расширять систему новыми жанрами."""
        self._creators[genre.lower()] = creator

    def get_supported_genres(self) -> List[str]:
        return list(self._creators.keys())

    def add_book_interactive(self):
        print("\n➕ Добавление новой книги...")
        title = input("Введите название книги: ").strip()
        author = input("Введите имя автора: ").strip()

        print("Доступные жанры:", ", ".join(self.get_supported_genres()))
        while True:
            genre = input("Введите жанр: ").strip().lower()
            if genre in self._creators:
                break
            print("⚠️ Некорректный жанр. Выберите из:", ", ".join(self.get_supported_genres()))

        while True:
            try:
                copies = int(input("Введите количество экземпляров: "))
                if copies > 0:
                    break
                else:
                    print("⚠️ Количество должно быть больше 0.")
            except ValueError:
                print("⚠️ Введите целое число.")

        location = input("Введите местоположение (например, Полка A3): ").strip()

        # Запрос дополнительных полей через фабрику
        creator = self._creators[genre]
        extra = {}
        for key, prompt in creator.get_extra_prompts().items():
            value = input(prompt).strip()
            extra[key] = value

        book = creator.create_book(title, author, copies, location, extra)
        self._books.append(book)
        print("✅ Книга успешно добавлена!")

    def filter_by_genre(self, genre: str) -> List[Book]:
        genre = genre.lower()
        return [book for book in self._books if book.genre == genre]

    def list_all_books(self):
        if not self._books:
            print("📭 Библиотека пуста.")
            return
        print("\n📚 Все книги в библиотеке:")
        for i, book in enumerate(self._books, 1):
            print(f"{i}. {book.display_info()}")

    def list_books_by_genre(self):
        print("\n🔍 Фильтрация книг по жанру")
        print("Доступные жанры:", ", ".join(self.get_supported_genres()))
        genre = input("Введите жанр для фильтрации: ").strip().lower()
        books = self.filter_by_genre(genre)
        if books:
            print(f"\n📖 Книги в жанре «{genre}»:")
            for book in books:
                print(f" • {book.display_info()}")
        else:
            print(f"📭 Книг в жанре «{genre}» не найдено.")

# === Главное меню ===
def main():
    lib = LibraryManager()
    print("📚 Добро пожаловать в систему управления библиотекой!")
    while True:
        print("\n" + "="*50)
        print("1. Добавить новую книгу")
        print("2. Показать все книги")
        print("3. Фильтровать книги по жанру")
        print("4. Выйти")
        choice = input("Выберите действие (1–4): ").strip()

        if choice == "1":
            lib.add_book_interactive()
        elif choice == "2":
            lib.list_all_books()
        elif choice == "3":
            lib.list_books_by_genre()
        elif choice == "4":
            print("👋 До свидания!")
            break
        else:
            print("⚠️ Некорректный выбор. Пожалуйста, введите число от 1 до 4.")

if __name__ == "__main__":
    main()