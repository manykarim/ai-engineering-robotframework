## ADDED Requirements

### Requirement: A guide to building libraries and tools
`docs/building-with-agents.md` SHALL describe, for participants, how to prepare an agent before it builds a Robot Framework library or tool:
- the five kinds of context, as headings in a project's `AGENTS.md`: toolstack, references, concepts, examples and the specification;
- why the project starts outside any other project's folder;
- which User Guide chapters and Robot API pages to point the agent to, for the pinned Robot Framework version;
- how to save a reference the agent cannot fetch.

It SHALL be linked from both bonus labs and listed on the site. The curriculum's Module 10 and the run sheet SHALL name the bonus chapters in the Monday plan.

#### Scenario: Preparing an agent for a listener
- **WHEN** a participant reads the guide before writing a listener
- **THEN** it names the User Guide's *Listener interface* chapter and the `robot.api.interfaces.ListenerV3` entry on the Robot API's `robot.api` page, both for Robot Framework 7.5

#### Scenario: A reference behind a bot wall
- **WHEN** the agent cannot fetch a service's API manual, as with TestRail's
- **THEN** the guide says how to save the reference into the project and point the agent to the saved file
