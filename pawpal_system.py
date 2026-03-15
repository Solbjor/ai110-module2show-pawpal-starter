"""
PawPal+ backend — class stubs (no logic yet).

Relationships
-------------
Owner  1 ──< * Pet
Pet    1 ──< * PetTask
Schedule aggregates one Owner + one Pet and works over its PetTask list.
"""

from __future__ import annotations


class PetTask:
    """A single care task for a pet."""

    def __init__(
        self,
        title: str,
        duration_minutes: int,
        priority: str,   # "low" | "medium" | "high"
        category: str,   # "walk" | "feeding" | "meds" | "grooming" | "enrichment" | "appointment"
    ) -> None:
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "category": self.category,
        }


class Pet:
    """A pet owned by an Owner; holds a list of care tasks."""

    def __init__(self, name: str, species: str, age: int) -> None:
        self.name = name
        self.species = species
        self.age = age
        self.tasks: list[PetTask] = []

    def add_task(self, task: PetTask) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass


class Owner:
    """A pet owner who has one or more pets and a daily time budget."""

    def __init__(
        self,
        name: str,
        available_minutes: int,
        preferences: list[str] | None = None,
    ) -> None:
        self.name = name
        self.available_minutes = available_minutes
        self.preferences: list[str] = preferences or []
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, name: str) -> None:
        pass


class Schedule:
    """Builds and explains a daily care plan for one pet."""

    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner = owner
        self.pet = pet
        self.plan: list[PetTask] = []

    def generate(self) -> list[PetTask]:
        """Select and order tasks within the owner's time budget."""
        pass

    def explain(self) -> str:
        """Return a human-readable explanation of why each task was chosen."""
        pass
