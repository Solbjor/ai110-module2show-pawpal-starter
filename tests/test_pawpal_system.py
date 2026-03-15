from pawpal_system import Owner, Pet, Scheduler, Task


def test_scheduler_respects_time_and_priority() -> None:
    owner = Owner("Jordan", available_minutes=30)
    pet = Pet("Mochi", "dog", 4)
    pet.add_task(Task("Long walk", 25, "medium", "walk"))
    pet.add_task(Task("Medication", 10, "high", "meds"))
    pet.add_task(Task("Quick feed", 10, "high", "feeding"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner, pet)
    plan = scheduler.generate()

    assert [task.title for task in plan] == ["Medication", "Quick feed"]
    assert sum(task.duration_minutes for task in plan) <= owner.available_minutes


def test_tasks_are_stored_per_pet() -> None:
    owner = Owner("Jordan", available_minutes=90)
    dog = Pet("Mochi", "dog", 4)
    cat = Pet("Luna", "cat", 2)

    dog.add_task(Task("Walk", 20, "high", "walk"))
    cat.add_task(Task("Litter", 15, "medium", "grooming"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    assert [task.title for task in dog.tasks] == ["Walk"]
    assert [task.title for task in cat.tasks] == ["Litter"]
    assert len(owner.pets) == 2


def test_preferences_influence_order_for_equal_priority() -> None:
    owner = Owner("Jordan", available_minutes=60, preferences=["meds", "walk"])
    pet = Pet("Mochi", "dog", 4)

    pet.add_task(Task("Walk outside", 20, "high", "walk"))
    pet.add_task(Task("Give meds", 20, "high", "meds"))

    scheduler = Scheduler(owner, pet)
    plan = scheduler.generate()

    assert [task.title for task in plan] == ["Give meds", "Walk outside"]


def test_filtering_skips_invalid_tasks() -> None:
    owner = Owner("Jordan", available_minutes=60)
    pet = Pet("Mochi", "dog", 4)

    pet.add_task(Task("Bad duration", 0, "high", "meds"))
    pet.add_task(Task("Bad priority", 10, "urgent", "walk"))
    pet.add_task(Task("Valid task", 10, "medium", "feeding"))

    scheduler = Scheduler(owner, pet)
    plan = scheduler.generate()

    assert [task.title for task in plan] == ["Valid task"]
    assert any("Bad duration" in msg for msg in scheduler.skipped_tasks)
    assert any("Bad priority" in msg for msg in scheduler.skipped_tasks)


def test_conflict_detection_skips_overlapping_fixed_time_task() -> None:
    owner = Owner("Jordan", available_minutes=90)
    pet = Pet("Mochi", "dog", 4)

    pet.add_task(Task("Morning meds", 20, "high", "meds", start_minute=540))
    pet.add_task(Task("Vet call", 15, "high", "appointment", start_minute=550))

    scheduler = Scheduler(owner, pet)
    plan = scheduler.generate()

    assert [task.title for task in plan] == ["Morning meds"]
    assert any("Vet call" in msg and "time conflict" in msg for msg in scheduler.skipped_tasks)


def test_daily_recurring_task_is_included() -> None:
    owner = Owner("Jordan", available_minutes=60)
    pet = Pet("Mochi", "dog", 4)

    pet.add_task(Task("Daily meds", 10, "high", "meds", recurrence="daily"))
    pet.add_task(Task("One-off walk", 20, "medium", "walk", recurrence="none"))

    scheduler = Scheduler(owner, pet)
    plan = scheduler.generate()

    assert [task.title for task in plan] == ["Daily meds", "One-off walk"]


def test_back_to_back_fixed_time_tasks_do_not_conflict() -> None:
    owner = Owner("Jordan", available_minutes=60)
    pet = Pet("Mochi", "dog", 4)

    # Edge case: second task starts exactly when first ends.
    pet.add_task(Task("Task A", 20, "high", "meds", start_minute=540))
    pet.add_task(Task("Task B", 15, "high", "feeding", start_minute=560))

    scheduler = Scheduler(owner, pet)
    plan = scheduler.generate()

    assert [task.title for task in plan] == ["Task A", "Task B"]
