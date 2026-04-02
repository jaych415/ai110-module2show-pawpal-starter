"""Automated tests for PawPal+ — run with: python -m pytest"""

from datetime import date, timedelta
import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def basic_owner():
    owner = Owner("Jordan")
    dog = Pet("Buddy", "dog")
    cat = Pet("Mochi", "cat")
    dog.add_task(Task("Morning walk",   time="07:30", duration_minutes=30, priority="high",   frequency="daily"))
    dog.add_task(Task("Afternoon walk", time="15:00", duration_minutes=30, priority="medium", frequency="daily"))
    cat.add_task(Task("Feeding",        time="08:00", duration_minutes=10, priority="high",   frequency="daily"))
    cat.add_task(Task("Playtime",       time="07:30", duration_minutes=20, priority="low",    frequency="once"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner


# ---------------------------------------------------------------------------
# Task tests
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = Task("Walk", time="08:00", duration_minutes=20)
    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_daily_recurrence_creates_next_task():
    task = Task("Feeding", time="08:00", duration_minutes=10, frequency="daily",
                due_date=date(2026, 4, 1))
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == date(2026, 4, 2)
    assert not next_task.completed


def test_weekly_recurrence_creates_next_task():
    task = Task("Grooming", time="10:00", duration_minutes=30, frequency="weekly",
                due_date=date(2026, 4, 1))
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == date(2026, 4, 8)


def test_once_task_returns_none_on_complete():
    task = Task("Vet visit", time="09:00", duration_minutes=60, frequency="once")
    assert task.mark_complete() is None


# ---------------------------------------------------------------------------
# Pet tests
# ---------------------------------------------------------------------------

def test_add_task_increases_count():
    pet = Pet("Rex", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", time="08:00", duration_minutes=20))
    assert len(pet.tasks) == 1


def test_remove_task():
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Walk", time="08:00", duration_minutes=20))
    removed = pet.remove_task("Walk")
    assert removed
    assert len(pet.tasks) == 0


def test_get_pending_tasks_excludes_completed():
    pet = Pet("Rex", "dog")
    t1 = Task("Walk", time="08:00", duration_minutes=20)
    t2 = Task("Feed", time="09:00", duration_minutes=5)
    t1.completed = True
    pet.add_task(t1)
    pet.add_task(t2)
    assert len(pet.get_pending_tasks()) == 1


# ---------------------------------------------------------------------------
# Scheduler tests
# ---------------------------------------------------------------------------

def test_sort_by_time_is_chronological(basic_owner):
    scheduler = Scheduler(basic_owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for _, t in sorted_tasks]
    assert times == sorted(times)


def test_filter_by_pet(basic_owner):
    scheduler = Scheduler(basic_owner)
    buddy_tasks = scheduler.filter_by_pet("Buddy")
    assert all(p.name == "Buddy" for p, _ in buddy_tasks)
    assert len(buddy_tasks) == 2


def test_filter_by_status_pending(basic_owner):
    scheduler = Scheduler(basic_owner)
    pending = scheduler.filter_by_status(completed=False)
    assert all(not t.completed for _, t in pending)


def test_conflict_detection(basic_owner):
    """Buddy's Morning walk and Mochi's Playtime are both at 07:30."""
    scheduler = Scheduler(basic_owner)
    warnings = scheduler.detect_conflicts()
    assert len(warnings) >= 1
    assert "07:30" in warnings[0]


def test_no_false_conflict_when_times_differ():
    owner = Owner("Sam")
    pet = Pet("Luna", "cat")
    pet.add_task(Task("Feed",  time="08:00", duration_minutes=10))
    pet.add_task(Task("Play",  time="09:00", duration_minutes=15))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


def test_mark_complete_adds_recurring(basic_owner):
    scheduler = Scheduler(basic_owner)
    buddy = basic_owner.find_pet("Buddy")
    original_count = len(buddy.tasks)
    scheduler.mark_task_complete("Buddy", "Morning walk")
    assert len(buddy.tasks) == original_count + 1


def test_empty_pet_schedule():
    owner = Owner("Empty")
    owner.add_pet(Pet("Ghost", "cat"))
    scheduler = Scheduler(owner)
    assert scheduler.build_daily_schedule() == []