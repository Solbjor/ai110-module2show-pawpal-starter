## PawPal+ UML

+------------------+          +------------------+
|      Owner       |          |       Pet        |
+------------------+  1    *  +------------------+
| - name: str      |--------->| - name: str      |
| - available_min  |          | - species: str   |
|   utes: int      |          | - age: int       |
| - preferences:   |          | - tasks: list    |
|   list[str]      |          +------------------+
| - pets: list     |          | + add_task()     |
+------------------+          | + remove_task()  |
| + add_pet()      |          +--------+---------+
| + remove_pet()   |                   |
+------------------+                   | 1
                                        |
                                        | *
                             +----------v---------+
                             |      PetTask       |
                             +--------------------+
                             | - title: str       |
                             | - duration_min     |
                             |   utes: int        |
                             | - priority: str    |
                             | - category: str    |
                             +--------------------+

+---------------------------+
|         Schedule          |
+---------------------------+
| - owner: Owner            |-----> Owner
| - pet: Pet                |-----> Pet
| - plan: list[PetTask]     |
+---------------------------+
| + generate() -> list      |
| + explain() -> str        |
+---------------------------+

Relationships:
  Owner  1 ──< * Pet        (Owner has many Pets)
  Pet    1 ──< * PetTask    (Pet has many Tasks)
  Schedule aggregates Owner + Pet, produces an ordered plan from PetTask list



@startuml PawPal+

class Owner {
  + name: str
  + available_minutes: int
  + preferences: list[str]
  + pets: list[Pet]
  + add_pet(pet: Pet): None
  + remove_pet(name: str): None
}

class Pet {
  + name: str
  + species: str
  + age: int
  + tasks: list[PetTask]
  + add_task(task: PetTask): None
  + remove_task(title: str): None
}

class PetTask {
  + title: str
  + duration_minutes: int
  + priority: str
  + category: str
  + to_dict(): dict
}

class Schedule {
  + owner: Owner
  + pet: Pet
  + plan: list[PetTask]
  + generate(): list[PetTask]
  + explain(): str
}

Owner "1" --> "*" Pet : owns
Pet "1" --> "*" PetTask : has
Schedule --> Owner : references
Schedule --> Pet : references
Schedule ..> PetTask : produces plan

@enduml