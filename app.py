"""PawPal+ Streamlit UI — run with: streamlit run app.py"""

import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Your smart pet care scheduler")

# ---------------------------------------------------------------------------
# Session state — persist Owner across reruns
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None

# ---------------------------------------------------------------------------
# Step 1: Owner setup
# ---------------------------------------------------------------------------
with st.expander("👤 Owner Setup", expanded=st.session_state.owner is None):
    owner_name = st.text_input("Owner name", value="Jordan")
    if st.button("Save owner"):
        st.session_state.owner = Owner(name=owner_name)
        st.success(f"Welcome, {owner_name}!")

if st.session_state.owner is None:
    st.info("Enter your name above to get started.")
    st.stop()

owner: Owner = st.session_state.owner

# ---------------------------------------------------------------------------
# Step 2: Add a pet
# ---------------------------------------------------------------------------
with st.expander("🐶 Add a Pet"):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", key="new_pet_name")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])
    if st.button("Add pet"):
        if pet_name.strip():
            if owner.find_pet(pet_name):
                st.warning(f"'{pet_name}' already exists.")
            else:
                owner.add_pet(Pet(name=pet_name.strip(), species=species))
                st.success(f"Added {pet_name} the {species}!")
        else:
            st.error("Pet name cannot be blank.")

if not owner.pets:
    st.info("Add at least one pet to continue.")
    st.stop()

pet_names = [p.name for p in owner.pets]

# ---------------------------------------------------------------------------
# Step 3: Add a task
# ---------------------------------------------------------------------------
with st.expander("📋 Add a Task"):
    t_pet  = st.selectbox("Assign to pet", pet_names, key="task_pet")
    t_title = st.text_input("Task title", value="Morning walk", key="task_title")
    c1, c2, c3 = st.columns(3)
    with c1:
        t_time = st.text_input("Time (HH:MM)", value="08:00", key="task_time")
    with c2:
        t_dur = st.number_input("Duration (min)", 1, 240, 20, key="task_dur")
    with c3:
        t_pri = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_pri")
    t_freq = st.selectbox("Frequency", ["once", "daily", "weekly"], key="task_freq")
    if st.button("Add task"):
        if t_title.strip():
            pet = owner.find_pet(t_pet)
            pet.add_task(Task(
                title=t_title.strip(),
                time=t_time,
                duration_minutes=int(t_dur),
                priority=t_pri,
                frequency=t_freq,
            ))
            st.success(f"Task '{t_title}' added to {t_pet}.")
        else:
            st.error("Task title cannot be blank.")

# ---------------------------------------------------------------------------
# Step 4: Generate schedule
# ---------------------------------------------------------------------------
st.divider()
st.subheader("📅 Daily Schedule")

scheduler = Scheduler(owner)

# Conflict warnings
conflicts = scheduler.detect_conflicts()
if conflicts:
    for w in conflicts:
        st.warning(w)

schedule = scheduler.build_daily_schedule()

if not schedule:
    st.success("No pending tasks — all done! 🎉")
else:
    PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    rows = []
    for pet, task in schedule:
        rows.append({
            "Priority": PRIORITY_EMOJI.get(task.priority, "") + " " + task.priority,
            "Time": task.time,
            "Pet": pet.name,
            "Task": task.title,
            "Duration": f"{task.duration_minutes} min",
            "Frequency": task.frequency,
        })
    st.table(rows)

# ---------------------------------------------------------------------------
# Step 5: Mark a task complete
# ---------------------------------------------------------------------------
st.divider()
st.subheader("✅ Mark Task Complete")

pending_options = [
    f"{pet.name} — {task.title}"
    for pet, task in schedule
]

if pending_options:
    selected = st.selectbox("Select a task to mark complete", pending_options)
    if st.button("Mark complete"):
        pet_n, task_n = selected.split(" — ", 1)
        msg = scheduler.mark_task_complete(pet_n, task_n)
        st.success(msg)
        st.rerun()
else:
    st.info("No pending tasks to complete.")