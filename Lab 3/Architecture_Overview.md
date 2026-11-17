# Book Club Architecture Analysis

## Scenario and requirements

Problem Statement 55 is the Book Club Reading Challenge and Discussion Portal. Its actors are Club Member, Discussion Lead, and System Administrator. The architecture is a proposed design, not evidence of an implemented or benchmarked system.

| Requirement | Design responsibility |
|---|---|
| FR-001 | Discussion Service hides spoiler-tagged text in threads, previews, and search until an explicit reveal or the relevant chapter is marked as read. Web UI presents the reveal control. |
| FR-002 | Reading Challenge Service creates and edits a member's page-based goal for the current club book. Repository Gateway persists the goal. |
| FR-003 | Reading Challenge Service records pages or chapters read and calculates progress against the goal. Chapter entries require book-specific page mapping before comparison with a page-based goal. |
| FR-004 | Poll Service restricts poll creation to Discussion Leads, validates at least two candidate books and a deadline, and makes published polls visible to members. |
| FR-005 | Poll Service permits one vote per member per poll. Database uniqueness protects the rule under concurrent requests. |
| NFR-001 | Application API verifies active sessions. Atomic vote transactions prevent duplicate votes. Committed tally events reach connected clients through Server-Sent Events (SSE). |
| NFR-002 | Durable database commits preserve logs and comments across application restarts. Health checks, automatic restart, backups, and restoration tests support the 99% monthly availability target. |

The main challenges are protecting spoilers across every display path, maintaining vote correctness during simultaneous submissions, and preserving saved records after a restart. Progress entry and poll feedback must remain understandable, including validation errors and expired deadlines.

## Architectural style comparison

| Style | Benefits for this project | Limitations for this project | Decision |
|---|---|---|---|
| Layered | Separates display logic, club rules, and persistence. One server application can coordinate voting and shared club data without remote calls between business modules. | Changes can affect neighbouring layers. Individual modules cannot be deployed or scaled independently. | Selected as a layered modular monolith. |
| Microservices | Polls and discussions could scale independently. Separate deployments isolate service changes. | Network failures, deployment overhead, and distributed consistency complicate membership checks and vote results. | Not selected for the current project scope. |
| Client-server | A browser client and central server simplify access control and keep club records in one place. | This deployment style alone does not separate business responsibilities. A central server remains a bottleneck and failure point. | Used for deployment, with layered structure inside the server. |

Layered architecture is selected because goals, discussions, and polls need distinct rules but share club identity and persistent records. Keeping the business modules in one application also avoids inter-service network calls during voting. The browser and server still form a client-server deployment; the two descriptions address different concerns.

## Components

| Component | Layer | Responsibility |
|---|---|---|
| Web UI | Presentation | Displays goals, progress, protected discussions, polls, and live tally updates. |
| Application API | Business | Validates requests, verifies active sessions and roles, handles membership administration, dispatches operations, and streams committed poll results through SSE. |
| Reading Challenge Service | Business | Validates personal goals and progress entries and calculates progress percentages. |
| Discussion Service | Business | Manages threads and comments and applies spoiler visibility rules before returning content. |
| Poll Service | Business | Validates poll creation, candidate selection, deadlines, duplicate votes, and tally changes. |
| Repository Gateway | Data | Implements identity and domain repositories, parameterized queries, and atomic vote transactions. |
| Relational Database | Data | Stores accounts, memberships, books, goals, progress, threads, comments, polls, candidates, and votes durably. |

The four Business components belong to one server application. Component separation describes replaceable modules with interface contracts, not independently deployed microservices. The diagram shows logical dependencies, not physical machines.

## Interface contracts

Every solid connection is an assembly between a required socket on the consumer and a provided ball on the provider. Small boundary squares represent ports. Requests run from consumer to provider; responses return on the same connection. The assemblies express component dependencies without redundant usage arrows.

| Interface | Consumer | Provider | Technology and exchanged data |
|---|---|---|---|
| IPortalAPI | Web UI | Application API | HTTPS JSON requests/responses; SSE sends committed tallies over an HTTPS stream. |
| IReading | Application API | Reading Challenge Service | In-process calls for verified member identity, goals, progress entries, and calculated progress. |
| IDiscussion | Application API | Discussion Service | In-process calls for threads, comments, reveal state, chapter-read state, and permitted content. |
| IPoll | Application API | Poll Service | In-process calls for verified identity and role, polls, candidate choice, and committed tallies. |
| IIdentityStore | Application API | Repository Gateway | In-process calls for accounts, active sessions, memberships, roles, and authorized membership updates. |
| IReadingStore | Reading Challenge Service | Repository Gateway | In-process calls for goals, progress records, and chapter-to-page metadata. |
| IDiscussionStore | Discussion Service | Repository Gateway | In-process calls for threads, comments, spoiler tags, and chapter-read/reveal records. |
| IPollStore | Poll Service | Repository Gateway | In-process calls for polls, candidates, and transactional vote insertion with authoritative tallies. |
| ISQL | Repository Gateway | Relational Database | Parameterized SQL over a TLS-protected database connection; rows and commit/rollback outcomes. |

## Interaction flows

### Reading progress

1. Web UI submits the goal or progress entry through IPortalAPI.
2. Application API verifies an active session and record ownership before calling IReading.
3. Reading Challenge Service validates the entry. For a positive page-based goal, progress equals pages read divided by goal pages, multiplied by 100. Chapter entries use the current book's page mapping; entries without a valid mapping are rejected.
4. IReadingStore persists the data through Repository Gateway and ISQL. Confirmation and updated progress return only after a successful commit.

### Discussion and spoiler visibility

1. Application API validates the session and club access before calling IDiscussion.
2. Discussion Service loads content and visibility records through IDiscussionStore.
3. Spoiler text remains hidden unless an explicit reveal is recorded or the associated chapter is marked as read. Hidden text is omitted from preview and search responses rather than protected by visual blur alone.
4. Web UI displays permitted content and a reveal control. A reveal request follows the same authenticated path and updates visibility state.

### Monthly poll voting

1. Web UI sends the selected poll and candidate through IPortalAPI.
2. Application API verifies an active session and club membership through IIdentityStore, then calls IPoll with a trusted member identity.
3. Poll Service validates that the poll is open and the candidate belongs to it. Poll creation separately requires the Discussion Lead role, at least two candidates, and a deadline.
4. IPollStore starts a transaction. A lock on the poll row keeps deadline checks and vote changes consistent; the database clock checks the deadline within the transaction.
5. A unique constraint on `(member_id, poll_id)` rejects duplicate votes, including simultaneous requests. A valid insertion increments the candidate tally within the same transaction. Invalid, closed, or duplicate submissions roll back without changing the original vote or tally.
6. After commit, the updated tally returns through IPoll and IPortalAPI. Application API sends the committed result through SSE. Reconnecting clients fetch the authoritative tally before resuming the stream, so missed notifications do not corrupt results.

## Security and performance decisions

The browser never accesses the database directly. Application API checks authentication, club membership, record ownership, and role permissions on the server. Business modules validate domain rules. Repository Gateway uses parameterized queries; the database enforces referential integrity and unique votes. Passwords and session tokens are excluded from logs. Spoiler filtering occurs before content reaches the browser.

In-process business calls avoid the extra network round trips of separate microservices. Indexes on member goals, thread identifiers, and poll identifiers reduce common lookup work. SSE delivers committed tally changes without repeated full-page polling. These are expected benefits, not measured latency claims. Poll-row locking simplifies correctness but serializes voting within a poll; concurrent-load tests must assess this tradeoff.

The 99% monthly availability target requires operational verification. Durable storage, monitoring, automatic restart, scheduled backups, and tested restoration are deployment provisions rather than additional business components. Restart tests must confirm that committed logs and comments remain intact. Backups mitigate storage loss; database durability protects records during application restarts. Neither alone guarantees uptime.

## Submission coverage

| Lab requirement | Location |
|---|---|
| Scenario review and functional/non-functional requirements | Scenario and requirements above |
| Analysis of all three architectural styles | Architectural style comparison above |
| Selected architecture and component identification | Components above and component diagram |
| At least five UML components | Seven stereotyped component rectangles |
| At least four provided/required interfaces | Nine named ball-and-socket assemblies with ports |
| Dependencies, interactions, and technology labels | Diagram assemblies, interface contracts, and interaction flows |
| Word justification of at most one page | Architectural_Justification.docx |
| Two scenario reasons, security advantage, performance benefit | Architectural_Justification.docx and its PDF export |
| Diagram and justification PDF exports | Book_Club_Component_Diagram.pdf and Architectural_Justification.pdf |

## References

- Lab 3 Component Modelling and Architectural Pattern Selection, supplied seven-page handout.
- Problem Statement 55 requirements table, UML use-case diagram, and Cast Vote flow in Folder 1. These source documents remain unchanged.
