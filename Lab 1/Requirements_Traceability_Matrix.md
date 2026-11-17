# Requirements Traceability Matrix

The matrix connects every approved requirement to the related use case, architecture component, acceptance method, and planned verification. This ensures that each requirement is designed and testable.

| Requirement | Requirement summary | Source | Use case | Architecture component | Acceptance or verification | Test ID |
|---|---|---|---|---|---|---|
| FR-001 | Hide spoiler-tagged discussion content until the member explicitly reveals it or marks the chapter as read. | Problem Statement 55 | View Discussion Thread; Reveal Spoiler Content | Discussion Service and Web UI | Confirm spoiler text remains obscured in the thread preview and search results until an authorized reveal action. | TC-RE-01 |
| FR-002 | Let a club member create and edit a personal reading goal for the current book. | Project scope | Set Reading Goal | Reading Challenge Service | Save a goal, sign out and sign in again, then confirm the same value is displayed and can be edited. | TC-RE-02 |
| FR-003 | Let a club member record pages or chapters read and show progress as a percentage of the goal. | Project scope | Log Reading Progress | Reading Challenge Service | Record progress against a known goal and verify the percentage calculation and persistence. | TC-RE-03 |
| FR-004 | Let a discussion lead create a monthly poll with at least two candidate books and a deadline, visible to members. | Problem Statement 55 | Create Monthly Poll | Poll Service | Create a valid poll and verify member visibility; reject a poll with fewer than two candidates or no deadline. | TC-RE-04 |
| FR-005 | Allow each member to vote only once in a monthly poll. | Problem Statement 55 | Cast Vote; Verify Duplicate Vote | Poll Service and Data Store | Submit a first vote successfully, submit a second vote for the same member and poll, and verify rejection with no tally change. | TC-RE-05 |
| NFR-001 | Prevent duplicate votes using verified user identity and update the tally promptly under normal and peak load. | Problem Statement 55 | Verify Duplicate Vote; View Poll Results | Authentication, Poll Service, Data Store | Enforce a unique member-and-poll constraint and verify atomic vote recording; measure result-update latency against the agreed target. | TC-NFR-01 |
| NFR-002 | Target 99% monthly availability and preserve reading logs and discussion comments across service restarts. | Project scope | All persistent workflows | Application Services, Data Store, Backup and Monitoring | Perform restart and recovery testing, verify persisted records, and review monthly uptime monitoring. | TC-NFR-02 |

## Traceability notes

- `FR-005` and `NFR-001` deliberately share the duplicate-vote verification path: the functional rule defines the behavior, while the non-functional requirement strengthens its reliability and performance.
- Test identifiers provide a stable handoff to implementation and testing. Detailed application tests should use the same IDs when execution begins.
- If a requirement changes, update the corresponding use case, SRS section, architecture mapping, and test before approval.

