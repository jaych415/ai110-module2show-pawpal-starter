"""PawPal+ backend logic: Task, Pet, Owner, and Scheduler classes."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    time: str                          # "HH:MM" format
    duration_minutes: int
    priority: str = "medium"           # "low" | "medium" | "high"
    frequency: str = "once"            # "once" | "daily" | "weekly"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete. Returns a new Task if it recurs, else None."""
        self.completed = True
        if self.frequency == "daily":
            return Task(
                title=self.title,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == "weekly":
            return Task(
                title=self.title,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None

    def __str__(self) -> str:
        status = "✅" if self.completed else "⬜"
        return f"{status} [{self.time}] {self.title} ({self.duration_minutes} min, {self.priority})"


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    """Stores pet details and its list of tasks."""
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> bool:
        """Remove a task by title. Returns True if found and removed."""
        for i, t in enumerate(self.tasks):
            if t.title == title:
                self.tasks.pop(i)
                return True
        return False

    def get_pending_tasks(self) -> list[Task]:
        """Return only incomplete tasks."""
        return [t for t in self.tasks if not t.completed]

    def __str__(self) -> str:
        return f"{self.name} ({self.species})"


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

@dataclass
class Owner:
    """Manages one or more pets."""
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs across all pets."""
        pairs = []
        for pet in self.pets:
            for task in pet.tasks:
                pairs.append((pet, task))
        return pairs

    def find_pet(self, name: str) -> Optional[Pet]:
        """Return the Pet with the given name, or None."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Scheduler:
    """Retrieves, sorts, filters, and validates tasks across an Owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Initialize with an Owner instance."""
        self.owner = owner

    # --- retrieval ----------------------------------------------------------

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs."""
        return self.owner.get_all_tasks()

    # --- sorting ------------------------------------------------------------

    def sort_by_time(self, tasks: list[tuple[Pet, Task]] | None = None) -> list[tuple[Pet, Task]]:
        """Return tasks sorted by scheduled time (HH:MM), then by priority."""
        pairs = tasks if tasks is not None else self.get_all_tasks()
        return sorted(pairs, key=lambda pt: (pt[1].time, PRIORITY_ORDER.get(pt[1].priority, 1)))

    def sort_by_priority(self, tasks: list[tuple[Pet, Task]] | None = None) -> list[tuple[Pet, Task]]:
        """Return tasks sorted by priority first, then by time."""
        pairs = tasks if tasks is not None else self.get_all_tasks()
        return sorted(pairs, key=lambda pt: (PRIORITY_ORDER.get(pt[1].priority, 1), pt[1].time))

    # --- filtering ----------------------------------------------------------

    def filter_by_status(self, completed: bool) -> list[tuple[Pet, Task]]:
        """Return tasks matching the given completion status."""
        return [(pet, t) for pet, t in self.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list[tuple[Pet, Task]]:
        """Return tasks belonging to the named pet."""
        return [(pet, t) for pet, t in self.get_all_tasks()
                if pet.name.lower() == pet_name.lower()]

    # --- conflict detection -------------------------------------------------

    def detect_conflicts(self) -> list[str]:
        """
        Return a list of warning strings for any two tasks scheduled at
        the exact same time (for any pet combination).
        """
        warnings = []
        all_pairs = self.get_all_tasks()
        seen: dict[str, tuple[Pet, Task]] = {}
        for pet, task in all_pairs:
            key = task.time
            if key in seen:
                other_pet, other_task = seen[key]
                warnings.append(
                    f"⚠️ Conflict at {task.time}: "
                    f"'{task.title}' ({pet.name}) vs "
                    f"'{other_task.title}' ({other_pet.name})"
                )
            else:
                seen[key] = (pet, task)
        return warnings

    # --- task completion with recurrence ------------------------------------

    def mark_task_complete(self, pet_name: str, task_title: str) -> str:
        """
        Mark a task complete. If it recurs, adds the next occurrence to
        the pet's task list automatically.
        """
        pet = self.owner.find_pet(pet_name)
        if pet is None:
            return f"Pet '{pet_name}' not found."
        for task in pet.tasks:
            if task.title == task_title and not task.completed:
                next_task = task.mark_complete()
                if next_task:
                    pet.add_task(next_task)
                    return f"✅ '{task_title}' done. Next occurrence added for {next_task.due_date}."
                return f"✅ '{task_title}' marked complete."
        return f"Task '{task_title}' not found or already complete."

    # --- schedule generation ------------------------------------------------

    def build_daily_schedule(self) -> list[tuple[Pet, Task]]:
        """Return today's pending tasks sorted by priority then time."""
        pending = self.filter_by_status(completed=False)
        return self.sort_by_priority(pending)

    def schedule_summary(self) -> str:
        """Return a human-readable schedule string."""
        schedule = self.build_daily_schedule()
        if not schedule:
            return "No pending tasks for today! 🎉"
        lines = ["📅 Today's Schedule", "-" * 30]
        for pet, task in schedule:
            lines.append(f"  {task}  — {pet.name}")
        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append("\n⚠️  Conflicts Detected:")
            lines.extend(f"  {w}" for w in conflicts)
        return "\n".join(lines)