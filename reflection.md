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

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
