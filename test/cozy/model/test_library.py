import pytest
from peewee import SqliteDatabase

from cozy.ext import inject
from cozy.extensions.set import split_strings_to_set


@pytest.fixture(autouse=True)
def setup_inject(peewee_database):
    inject.clear_and_configure(lambda binder: binder.bind(SqliteDatabase, peewee_database))
    yield
    inject.clear()


def test_library_contains_books():
    from cozy.model.library import Library

    library = Library()

    assert len(library.books) > 0


def test_authors_contains_every_author_from_db():
    from cozy.model.library import Library
    from cozy.db.book import Book

    library = Library()
    books = Book.select(Book.author).distinct().order_by(Book.author)
    authors_from_db = [book.author for book in books]
    authors_from_db = list(split_strings_to_set(set(authors_from_db)))

    # we cannot assert the same content as the library filters books without chapters
    assert len(library.authors) > 0
    assert library.authors.issubset(authors_from_db)


def test_readers_contains_every_reader_from_db():
    from cozy.model.library import Library
    from cozy.db.book import Book

    library = Library()
    books = Book.select(Book.reader).distinct().order_by(Book.reader)
    readers_from_db = [book.reader for book in books]
    readers_from_db = list(split_strings_to_set(set(readers_from_db)))

    # we cannot assert the same content as the library filters books without chapters
    assert len(library.readers) > 0
    assert library.readers.issubset(readers_from_db)
