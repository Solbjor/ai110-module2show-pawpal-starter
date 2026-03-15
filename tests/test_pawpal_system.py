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
