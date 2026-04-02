# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan and track care tasks for their pets, with smart scheduling logic built in Python.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

## Features

- **Add owners, pets, and tasks** — enter pet info and care tasks with time, duration, priority, and frequency
- **Priority-based scheduling** — tasks are sorted by priority (high → medium → low), then by time
- **Sorting by time** — view all tasks in strict chronological order across all pets
- **Filtering** — filter tasks by pet name or completion status
- **Conflict detection** — automatically warns when two tasks are scheduled at the exact same time
- **Recurring tasks** — daily and weekly tasks auto-generate their next occurrence when marked complete
- **Mark tasks complete** — one-click completion from the UI, with recurrence handled automatically
- **Color-coded display** — 🔴 High / 🟡 Medium / 🟢 Low priority indicators in the schedule table

## Smarter Scheduling

PawPal+ goes beyond a simple task list with three algorithmic capabilities:

**1. Priority + Time Sorting** — The daily schedule sorts tasks by priority level first (so high-priority tasks always appear at the top), then by scheduled time within each priority tier. This ensures critical care like medication is never buried under low-priority items.

**2. Conflict Detection** — The `Scheduler.detect_conflicts()` method scans all tasks across all pets and flags any two tasks sharing the exact same start time. Warnings are displayed prominently in the UI using `st.warning()` so the owner can reschedule before their day begins.

**3. Recurring Task Automation** — Tasks with `frequency="daily"` or `frequency="weekly"` automatically schedule their next occurrence using Python's `timedelta` when marked complete. The owner never has to manually re-enter a routine task.

## System Architecture

The backend is organized into four classes in `pawpal_system.py`:

| Class | Responsibility |
|-------|---------------|
| `Task` | Stores a single care activity and handles recurrence logic |
| `Pet` | Holds pet info and owns a list of tasks |
| `Owner` | Manages multiple pets and aggregates task access |
| `Scheduler` | Sorts, filters, detects conflicts, and builds the daily schedule |

See `uml_final.png` for the full class diagram.

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the CLI demo

```bash
python main.py
```

## Testing PawPal+

### Run tests

```bash
python -m pytest
```

### What the tests cover

- **Task completion** — verifies `mark_complete()` flips the completed flag
- **Daily recurrence** — confirms a daily task generates a next-day occurrence
- **Weekly recurrence** — confirms a weekly task generates a next-week occurrence
- **One-time tasks** — verifies `once` tasks return `None` on completion (no recurrence)
- **Task addition** — verifies adding a task increases a pet's task count
- **Task removal** — verifies `remove_task()` correctly removes by title
- **Pending task filter** — verifies completed tasks are excluded from pending list
- **Sorting correctness** — verifies tasks are returned in strict chronological order
- **Pet filtering** — verifies `filter_by_pet()` returns only that pet's tasks
- **Conflict detection** — verifies two tasks at the same time trigger a warning
- **No false conflicts** — verifies tasks at different times produce no warnings
- **Recurrence on complete** — verifies marking a recurring task complete adds the next instance

### Confidence Level

⭐⭐⭐⭐ (4/5) — Core scheduling behaviors are well covered. Edge cases not yet tested include tasks spanning midnight, invalid time formats, and owners with 10+ pets.

## 📸 Demo

<a href="/course_images/ai110/pawpalss.png" target="_blank">
  <img src="/course_images/ai110/pawpalss.png" title="PawPal App" width="" alt="PawPal App" class="center-block" />
</a>