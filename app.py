import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=60, preferences=[])

if "selected_pet_name" not in st.session_state:
    st.session_state.selected_pet_name = ""

if "schedule_output" not in st.session_state:
    st.session_state.schedule_output = []

owner = st.session_state.owner

owner_name = st.text_input("Owner name", value=owner.name)
available_minutes = st.number_input(
    "Available minutes today",
    min_value=0,
    max_value=24 * 60,
    value=int(owner.available_minutes),
    step=5,
)
preferences_text = st.text_input("Preferences (comma-separated)", value=", ".join(owner.preferences))

# Keep owner object in sync with UI inputs on each rerun.
owner.name = owner_name
owner.available_minutes = int(available_minutes)
owner.preferences = [pref.strip() for pref in preferences_text.split(",") if pref.strip()]

st.markdown("### Pets")
pet_col1, pet_col2, pet_col3, pet_col4 = st.columns(4)
with pet_col1:
    new_pet_name = st.text_input("New pet name", value="Mochi")
with pet_col2:
    new_pet_species = st.selectbox("Pet species", ["dog", "cat", "other"])
with pet_col3:
    new_pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=2)
with pet_col4:
    add_pet_clicked = st.button("Add pet")

if add_pet_clicked:
    if not new_pet_name.strip():
        st.warning("Please enter a pet name before adding a pet.")
    elif any(existing_pet.name == new_pet_name.strip() for existing_pet in owner.pets):
        st.warning("A pet with this name already exists.")
    else:
        owner.add_pet(Pet(name=new_pet_name.strip(), species=new_pet_species, age=int(new_pet_age)))
        st.session_state.selected_pet_name = new_pet_name.strip()
        st.success(f"Added pet: {new_pet_name.strip()}")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    if st.session_state.selected_pet_name not in pet_names:
        st.session_state.selected_pet_name = pet_names[0]

    selected_pet_name = st.selectbox(
        "Select pet",
        pet_names,
        index=pet_names.index(st.session_state.selected_pet_name),
    )
    st.session_state.selected_pet_name = selected_pet_name
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
else:
    st.info("No pets yet. Add a pet to start creating tasks.")
    selected_pet = None

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

category = st.selectbox(
    "Category",
    ["walk", "feeding", "meds", "enrichment", "grooming", "appointment"],
    index=0,
)

if st.button("Add task"):
    if selected_pet is None:
        st.warning("Add and select a pet before adding tasks.")
    elif not task_title.strip():
        st.warning("Please enter a task title.")
    else:
        selected_pet.add_task(
            Task(
                title=task_title.strip(),
                duration_minutes=int(duration),
                priority=priority,
                category=category,
            )
        )
        st.success(f"Added task for {selected_pet.name}: {task_title.strip()}")

if selected_pet is not None and selected_pet.tasks:
    st.write(f"Current tasks for {selected_pet.name}:")
    st.table([task.to_dict() for task in selected_pet.tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if selected_pet is None:
        st.warning("Add and select a pet before generating a schedule.")
    else:
        scheduler = Scheduler(owner, selected_pet)
        plan = scheduler.generate()
        st.session_state.schedule_output = [task.to_dict() for task in plan]
        st.session_state.schedule_explanation = scheduler.explain()

if st.session_state.schedule_output:
    st.write("Generated schedule:")
    st.table(st.session_state.schedule_output)
    st.markdown("### Why this plan?")
    st.write(st.session_state.get("schedule_explanation", ""))
