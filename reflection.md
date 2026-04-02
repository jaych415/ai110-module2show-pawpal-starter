# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included a few main classes. I had a Pet class to store information about each pet, such as name and needs. I also had a Task class to represent things like feeding or walking. Then I had a Scheduler class that was responsible for organizing and assigning tasks. Each class had a clear role, with the Scheduler doing most of the decision making.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed during implementation. At first, I tried to keep all scheduling logic inside one class, but it became too messy. I later separated some logic into helper methods to make the code easier to read and manage. This made debugging and updating the system much simpler.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers time, task priority, and basic preferences such as when a task should be done. I decided these were the most important because tasks need to be completed on time, and some tasks matter more than others, like feeding over playing.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is that it may not always give the most optimal schedule for every preference. Instead, it focuses on making sure high priority tasks are completed first. This is reasonable because it is more important that critical tasks are done than having a perfectly balanced schedule.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools to help with brainstorming ideas, debugging code, and improving structure. Asking specific questions about errors or how to organize classes was especially helpful. It also helped explain concepts when I was unsure.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

There was a moment where the AI suggested a solution that did not fully match my design. Instead of using it directly, I reviewed the logic and tested it with my own examples. This helped me confirm what worked and what needed to be changed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested basic behaviors such as whether tasks were scheduled at the correct time and if higher priority tasks were handled first. These tests were important to make sure the system worked as expected.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that my scheduler works correctly for normal cases. If I had more time, I would test edge cases like overlapping tasks, empty schedules, or tasks with the same priority.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with how the scheduler logic turned out. It is simple but effective and handles the main requirements.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve how preferences are handled and make the scheduling more flexible. I would also clean up parts of the code to make it more efficient.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned is that designing systems takes multiple revisions. I also learned that AI is useful, but it is important to check and understand its suggestions before using them.
