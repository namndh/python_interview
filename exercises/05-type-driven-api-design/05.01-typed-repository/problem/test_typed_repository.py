import pytest

from typed_repository import (
    DuplicateEntity,
    EntityNotFound,
    InMemoryRepository,
    User,
    UserService,
)


def test_generic_repository_crud_and_snapshot() -> None:
    repository = InMemoryRepository[User]()
    user = User("1", "one@example.com", "One")
    repository.add(user)
    assert repository.get("1") == user
    assert repository.list() == (user,)
    with pytest.raises(DuplicateEntity):
        repository.add(user)
    assert repository.remove("1") == user
    with pytest.raises(EntityNotFound):
        repository.get("1")


def test_service_normalizes_and_enforces_email_uniqueness() -> None:
    repository = InMemoryRepository[User]()
    ids = iter(["u1", "u2"])
    service = UserService(repository, lambda: next(ids))
    user = service.register("  Ada@Example.COM ", "  Ada Lovelace  ")
    assert user == User("u1", "ada@example.com", "Ada Lovelace")
    with pytest.raises(DuplicateEntity):
        service.register("ADA@example.com", "Another Ada")


@pytest.mark.parametrize("email", ["", "no-at-sign", "@example.com", "a@"])
def test_service_rejects_invalid_email(email: str) -> None:
    service = UserService(InMemoryRepository(), lambda: "id")
    with pytest.raises(ValueError):
        service.register(email, "Name")


def test_rename_replaces_immutable_user() -> None:
    repository = InMemoryRepository[User]()
    service = UserService(repository, lambda: "u1")
    original = service.register("a@example.com", "Before")
    renamed = service.rename(original.id, " After ")
    assert renamed == User("u1", "a@example.com", "After")
    assert repository.get("u1") == renamed
