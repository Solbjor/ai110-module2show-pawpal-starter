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
        start_minute: int | None = None,
        recurrence: str = "none",  # "none" | "daily"
    ) -> None:
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.start_minute = start_minute
        self.recurrence = recurrence

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "category": self.category,
            "start_minute": self.start_minute,
            "recurrence": self.recurrence,
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
        self.skipped_tasks: list[str] = []

    def _expand_recurring_tasks(self, tasks: list[Task], day_index: int = 0) -> list[Task]:
        """Return tasks that apply to the target day based on simple recurrence rules."""
        expanded: list[Task] = []
        for task in tasks:
            recurrence = task.recurrence.lower()
            if recurrence == "none":
                expanded.append(task)
            elif recurrence == "daily":
                # Daily tasks are included for every day_index.
                expanded.append(task)
        return expanded

    def _filter_tasks(self, tasks: list[Task]) -> list[Task]:
        """Remove malformed or unsupported tasks before scheduling."""
        filtered: list[Task] = []
        for task in tasks:
            if task.duration_minutes <= 0:
                self.skipped_tasks.append(f"Skipped {task.title}: invalid duration")
                continue
            if task.priority.lower() not in {"high", "medium", "low"}:
                self.skipped_tasks.append(f"Skipped {task.title}: invalid priority")
                continue
            filtered.append(task)
        return filtered

    def _has_conflict(self, candidate: Task, scheduled: list[Task], sequential_cursor: int) -> bool:
        """Detect overlap with already scheduled fixed-time tasks."""
        candidate_start = candidate.start_minute
        if candidate_start is None:
            candidate_start = sequential_cursor
        candidate_end = candidate_start + candidate.duration_minutes

        for existing in scheduled:
            existing_start = existing.start_minute
            if existing_start is None:
                continue
            existing_end = existing_start + existing.duration_minutes
            # Two intervals overlap only when each starts before the other ends.
            if candidate_start < existing_end and existing_start < candidate_end:
                return True
        return False

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

        self.skipped_tasks = []
        recurring_expanded = self._expand_recurring_tasks(self.pet.tasks)
        filtered_tasks = self._filter_tasks(recurring_expanded)

        ordered_tasks = sorted(
            filtered_tasks,
            key=lambda task: (
                priority_rank.get(task.priority, 99),
                preference_score(task),
                task.start_minute if task.start_minute is not None else 10**9,
                task.duration_minutes,
            ),
        )

        remaining_minutes = self.owner.available_minutes
        self.plan = []
        sequential_cursor = 0
        for task in ordered_tasks:
            if self._has_conflict(task, self.plan, sequential_cursor):
                self.skipped_tasks.append(f"Skipped {task.title}: time conflict")
                continue
            if task.duration_minutes > remaining_minutes:
                self.skipped_tasks.append(f"Skipped {task.title}: not enough time")
                continue

            self.plan.append(task)
            remaining_minutes -= task.duration_minutes
            if task.start_minute is None:
                sequential_cursor += task.duration_minutes
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
        if self.skipped_tasks:
            explanation.append("Skipped tasks:")
            explanation.extend(self.skipped_tasks)
        return "\n".join(explanation)


# Backward-compatible aliases from earlier UML naming.
PetTask = Task
Schedule = Scheduler
