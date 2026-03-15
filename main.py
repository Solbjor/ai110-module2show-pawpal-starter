from __future__ import annotations

import inspect

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_data() -> tuple[Owner, Pet, Pet]:
    owner = Owner(
        name="Jordan",
        available_minutes=75,
        preferences=["morning_walk", "meds_first"],
    )

    dog = Pet(name="Mochi", species="dog", age=4)
    cat = Pet(name="Luna", species="cat", age=2)

    dog.add_task(Task("Morning walk", 25, "high", "walk"))
    dog.add_task(Task("Breakfast feeding", 10, "high", "feeding"))
    cat.add_task(Task("Litter cleaning", 15, "medium", "grooming"))
    cat.add_task(Task("Play session", 20, "low", "enrichment"))

    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat


def run_demo() -> None:
    owner, dog, cat = build_demo_data()

    print("=== PawPal+ Phase 2 Demo ===")
    print(f"Owner: {owner.name} | Available minutes: {owner.available_minutes}")
    print(f"Pets: {[pet.name for pet in owner.pets]}")

    print("\nData trace:")
    print("1) Owner stores pets in owner.pets")
    print(f"   owner.pets -> {[pet.name for pet in owner.pets]}")
    print("2) Each Pet stores tasks in pet.tasks")
    print(f"   {dog.name}.tasks -> {[task.to_dict() for task in dog.tasks]}")
    print(f"   {cat.name}.tasks -> {[task.to_dict() for task in cat.tasks]}")

    dog_scheduler = Scheduler(owner, dog)
    dog_plan = dog_scheduler.generate()

    print("3) Scheduler reads owner + pet and generates plan")
    print(f"   generated plan -> {[task.to_dict() for task in dog_plan]}")
    print("\nPlan explanation:")
    print(dog_scheduler.explain())

    print("\nMethod inspection: Scheduler.generate")
    print(inspect.getsource(Scheduler.generate))


if __name__ == "__main__":
    run_demo()
