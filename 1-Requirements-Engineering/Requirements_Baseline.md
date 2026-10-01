# Requirements Baseline

## Book Club Reading Challenge and Discussion Portal

### Actors

- Club Member
- Discussion Lead
- System Administrator

## Functional requirements

| ID | Description | Priority | Acceptance criteria |
|---|---|---|---|
| FR-001 | The system shall hide spoiler-tagged discussion content until a club member explicitly reveals it or marks the relevant chapter as read. | High | Spoiler content remains masked in discussion previews and search results until an authorized reveal action occurs. |
| FR-002 | The system shall allow a club member to create and edit a personal reading goal, measured in pages or chapters, for the current club book. | High | A valid goal persists across sessions and remains editable without removing recorded progress. |
| FR-003 | The system shall allow a club member to record pages or chapters read and display progress as a percentage of the active goal. | Medium | A goal of 300 pages with 90 pages recorded displays 30 percent progress and persists after a new session begins. |
| FR-004 | The system shall allow a discussion lead to create a monthly poll with at least two candidate books and a future deadline. | High | A valid poll becomes visible to members; missing deadlines and fewer than two candidates are rejected. |
| FR-005 | The system shall allow each club member to cast no more than one vote in the same monthly poll. | High | A first valid vote is recorded. A later vote from the same account is rejected without changing any tally. |

## Non-functional requirements

| ID | Category | Description | Priority | Acceptance criteria |
|---|---|---|---|---|
| NFR-001 | Integrity and performance | Vote recording shall verify the authenticated member, enforce a unique member-and-poll record, and update the tally atomically. | High | Concurrent duplicate submissions produce one committed vote, and the result update meets the benchmark target defined for the test environment. |
| NFR-002 | Availability and durability | The portal shall target 99 percent monthly availability and preserve confirmed reading logs and discussion comments across ordinary service restarts. | Medium | Monitoring demonstrates the availability target, and restart testing confirms that committed records remain intact. |

## Requirement relationships

- FR-001 maps to View Discussion Thread and Reveal Spoiler Content.
- FR-002 maps to Set Reading Goal.
- FR-003 maps to Log Reading Progress.
- FR-004 maps to Create Monthly Poll.
- FR-005 and NFR-001 map to Cast Vote and Verify Duplicate Vote.
- NFR-002 applies to every workflow that stores persistent information.

The detailed traceability matrix is maintained in `Requirements_Traceability_Matrix.md`.
