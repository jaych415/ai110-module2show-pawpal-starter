"""CLI demo script for PawPal+ — run with: python main.py"""

from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ------------------------------------------------------------------
owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="cat")
buddy = Pet(name="Buddy", species="dog")

owner.add_pet(mochi)
owner.add_pet(buddy)

# --- Add tasks (intentionally out of order to test sorting) -----------------
mochi.add_task(Task("Evening feeding",  time="18:00", duration_minutes=10, priority="high",   frequency="daily"))
mochi.add_task(Task("Playtime",         time="10:00", duration_minutes=20, priority="medium", frequency="daily"))
mochi.add_task(Task("Vet checkup",      time="09:00", duration_minutes=60, priority="high",   frequency="once"))

buddy.add_task(Task("Morning walk",     time="07:30", duration_minutes=30, priority="high",   frequency="daily"))
buddy.add_task(Task("Afternoon walk",   time="15:00", duration_minutes=30, priority="medium", frequency="daily"))
# Intentional conflict with Mochi's vet checkup — same time
buddy.add_task(Task("Grooming",         time="09:00", duration_minutes=45, priority="low",    frequency="weekly"))

# --- Run scheduler ----------------------------------------------------------
scheduler = Scheduler(owner)

print(scheduler.schedule_summary())

print("\n--- Sorted by time only ---")
for pet, task in scheduler.sort_by_time():
    print(f"  {task.time}  {pet.name:8}  {task.title}")

print("\n--- Pending tasks for Mochi ---")
for _, task in scheduler.filter_by_pet("Mochi"):
    if not task.completed:
        print(f"  {task}")

print("\n--- Mark 'Morning walk' complete ---")
print(scheduler.mark_task_complete("Buddy", "Morning walk"))

print("\n--- Schedule after completion ---")
print(scheduler.schedule_summary())