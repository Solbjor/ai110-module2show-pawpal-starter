"""
PawPal+ backend — class stubs (no logic yet).

Relationships
-------------
Owner  1 ──< * Pet
Pet    1 ──< * Task
Scheduler aggregates one Owner + one Pet and works over its Task list.
"""

from __future__ import annotations


class Task:
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
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        self.tasks = [task for task in self.tasks if task.title != title]


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
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        self.pets = [pet for pet in self.pets if pet.name != name]


class Scheduler:
    """Builds and explains a daily care plan for one pet."""

    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner = owner
        self.pet = pet
        self.plan: list[Task] = []

    def generate(self) -> list[Task]:
        """Select and order tasks within the owner's time budget."""
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        preference_rank = {pref.lower(): index for index, pref in enumerate(self.owner.preferences)}

        def preference_score(task: Task) -> int:
            # Match preference hints against task category/title (e.g., "meds_first", "morning_walk").
            title = task.title.lower()
            category = task.category.lower()
            best_score = len(preference_rank)
            for pref, pref_index in preference_rank.items():
                if pref in category or pref in title or category in pref or title in pref:
                    best_score = min(best_score, pref_index)
            return best_score

        ordered_tasks = sorted(
            self.pet.tasks,
            key=lambda task: (
                priority_rank.get(task.priority, 99),
                preference_score(task),
                task.duration_minutes,
            ),
        )

        remaining_minutes = self.owner.available_minutes
        self.plan = []
        for task in ordered_tasks:
            if task.duration_minutes <= remaining_minutes:
                self.plan.append(task)
                remaining_minutes -= task.duration_minutes
        return self.plan

    def explain(self) -> str:
        """Return a human-readable explanation of why each task was chosen."""
        if not self.plan:
            return "No tasks selected for the current schedule."

        explanation = [
            f"Schedule for {self.pet.name}: selected {len(self.plan)} task(s) "
            f"within {self.owner.available_minutes} available minutes."
        ]
        for index, task in enumerate(self.plan, start=1):
            explanation.append(
                f"{index}. {task.title} ({task.duration_minutes} min, priority: {task.priority})"
            )
        return "\n".join(explanation)


# Backward-compatible aliases from earlier UML naming.
PetTask = Task
Schedule = Scheduler
