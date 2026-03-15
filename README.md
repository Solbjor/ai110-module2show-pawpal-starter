# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.



# PawPal+ Project Reflection

## 1. System Design

- A user should be able to add a pet to their pet list
- A user should be able to create a task for a pet.
- A user user should be able to visualize all current tasks. 

**a. Initial design**

- Briefly describe your initial UML design.
The initial UML consists of 4 main candid classes: Owner which can have many Pets, who can have many Tasks associated with them. Schedule aggregates Owner + Pet to produce a task plan. 
- What classes did you include, and what responsibilities did you assign to each?
Owner, holds information about the pet owner such as name and availability, as well as pets. Pets has information about the pet such as species, name, and tasks associated. Task has title, priority, and description of what the task should do.

**b. Design changes**

- Did your design change during implementation?
No, it has not changed since creating the UML.
- If yes, describe at least one change and why you made it.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers preferences and time available to the Owner when it comes to creating its plans. 
- How did you decide which constraints mattered most?
I decided based on what the user would place the most value on in terms of constraining. Time is a key factor compared to preferences, as the
time they have available is influenced by many outside factors that at times can't be altered. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler prioritizes high value tasks first before preferred tasks, and only adds tasks if they fit the time.
- Why is that tradeoff reasonable for this scenario?
The trade off is reasonable since we are trying to set the schedule based on what tasks should be completed first since 
care planning needs to be quick.
---
