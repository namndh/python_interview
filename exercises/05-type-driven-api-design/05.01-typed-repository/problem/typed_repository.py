"""Day 5: implement generic protocols and a typed service boundary."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, TypeVar


class EntityNotFound(LookupError):
    pass


class DuplicateEntity(ValueError):
    pass


class Entity(Protocol):
    @property
    def id(self) -> str: ...


T = TypeVar("T", bound=Entity)


class Repository(Protocol[T]):
    def get(self, entity_id: str) -> T: ...
    def add(self, entity: T) -> None: ...
    def remove(self, entity_id: str) -> T: ...
    def list(self) -> tuple[T, ...]: ...


@dataclass(frozen=True)
class User:
    id: str
    email: str
    display_name: str


class InMemoryRepository(Repository[T]):
    def __init__(self) -> None:
        raise NotImplementedError

    def get(self, entity_id: str) -> T:
        raise NotImplementedError

    def add(self, entity: T) -> None:
        raise NotImplementedError

    def remove(self, entity_id: str) -> T:
        raise NotImplementedError

    def list(self) -> tuple[T, ...]:
        raise NotImplementedError


class UserService:
    def __init__(self, repository: Repository[User], make_id: Callable[[], str]) -> None:
        raise NotImplementedError

    def register(self, email: str, display_name: str) -> User:
        raise NotImplementedError

    def rename(self, user_id: str, display_name: str) -> User:
        raise NotImplementedError
