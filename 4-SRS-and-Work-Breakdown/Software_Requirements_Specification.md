# Software Requirements Specification

## Book Club Reading Challenge and Discussion Portal

**Problem statement:** 55  
**Document version:** 1.0  
**Status:** Baseline for design, implementation, and testing

## 1 Introduction

### 1.1 Purpose

This Software Requirements Specification defines the expected behavior and quality of a web portal for a community book club. The portal centralizes personal reading goals, progress tracking, spoiler-aware discussions, monthly book-selection polls, and club membership administration.

### 1.2 Scope

The first release will allow club members to set a goal for the current book, log pages or chapters read, see percentage progress, participate in discussion threads, reveal spoiler-tagged content intentionally, vote once in an active monthly poll, and view poll results. Discussion leads will create polls, and system administrators will manage memberships.

The first release does not include electronic-book hosting, book purchases, public social networking, real-time video meetings, or automated book recommendations.

### 1.3 Definitions

| Term | Meaning |
|---|---|
| Club Member | An authenticated participant in the book club. |
| Discussion Lead | A member authorized to create and manage monthly polls. |
| System Administrator | A user authorized to manage memberships and system operation. |
| Reading goal | A personal target measured in pages or chapters for the current book. |
| Spoiler tag | Metadata that causes discussion content to be hidden until explicitly revealed. |
| Monthly poll | A time-bounded vote with at least two candidate books. |
| RTM | Requirements Traceability Matrix. |

### 1.4 References

- Problem Statement 55, Book Club Reading Challenge and Discussion Portal.
- Requirements table and UML use-case diagram in `1-Requirements-Engineering`.
- Architecture overview in `2-Architectural-Diagram`.

## 2 Overall description

### 2.1 Product perspective

The product is a browser-based information system. Users access a responsive web interface backed by an application API and relational database. It may be deployed as a single modular application for the initial release.

### 2.2 User classes

| User class | Primary capabilities |
|---|---|
| Club Member | Manage personal goal and progress, post or view discussions, reveal spoilers, vote, and view results. |
| Discussion Lead | All member capabilities plus create and manage the monthly poll. |
| System Administrator | Manage club membership, roles, account status, and operational settings. |

### 2.3 Operating environment

- Current desktop and mobile browsers with JavaScript enabled.
- HTTPS network connection.
- Server runtime capable of hosting the application API.
- Relational database with transactional and unique-constraint support.

### 2.4 Assumptions and dependencies

- A user must have one stable account identity before voting.
- The club has one current book and at most one active selection poll for a given voting period.
- Discussion leads provide valid candidate books and a deadline.
- Availability depends on hosting, monitoring, and backup services selected during deployment.

### 2.5 Constraints

- A member must not cast more than one vote in the same poll.
- Spoiler content must not appear unmasked in previews or search results.
- Persistent user content must survive an ordinary application restart.
- Authorization decisions must be enforced on the server.

## 3 Functional requirements

### FR-001 Spoiler protection

The system shall hide content in spoiler-tagged discussion comments until the club member explicitly reveals it or the application confirms that the relevant chapter has been read.

**Acceptance criteria:** Spoiler content remains masked in thread previews and search output. An explicit reveal displays it for the requesting user. Unauthorized previews never contain the raw spoiler text.

### FR-002 Personal reading goal

The system shall allow a club member to create and edit a personal reading goal, measured in pages or chapters, for the current club book.

**Acceptance criteria:** The saved goal persists across sessions, is visible to its owner, accepts only positive values within configured limits, and can be edited without deleting prior progress entries.

### FR-003 Reading progress

The system shall allow a club member to record pages or chapters read and display progress as a percentage of the current goal.

**Acceptance criteria:** For a 300-page goal and 90 pages recorded, the displayed progress is 30%. Progress persists after signing out and never displays a negative percentage.

### FR-004 Monthly poll creation

The system shall allow a discussion lead to create a monthly book-selection poll with at least two candidate books and a closing deadline and shall make the active poll visible to club members.

**Acceptance criteria:** Valid polls appear to members immediately. The system rejects a poll with fewer than two candidates, a missing deadline, or a deadline that is not in the future.

### FR-005 One vote per member

The system shall allow a club member to cast at most one vote in a monthly poll.

**Acceptance criteria:** The first valid vote is recorded. Any later vote by the same member in the same poll is rejected, the original record remains unchanged, and no tally is incremented.

### Supporting administrative requirement

The system shall allow an administrator to activate, suspend, and assign permitted roles to club memberships. Administrative actions shall be recorded with actor, time, and action type.

## 4 Non-functional requirements

### NFR-001 Vote integrity and responsiveness

The system shall verify the authenticated member identity and enforce a unique vote for each member-and-poll pair. Vote recording and tally update shall occur in one atomic transaction. Under the agreed benchmark load, the updated result should be returned within the performance target established by the test environment.

### NFR-002 Availability and durability

The deployed service shall target at least 99% monthly availability. Confirmed goals, progress records, comments, polls, and votes shall survive ordinary service restarts. Backups and a documented recovery procedure shall protect against data loss.

### NFR-003 Security

- All authenticated traffic shall use HTTPS.
- Passwords, if stored by this system, shall use an approved adaptive password hash.
- Sessions shall expire and be invalidated on sign-out.
- Server-side authorization shall protect lead and administrator operations.
- Logs shall not contain passwords, session tokens, or unmasked private discussion content.

### NFR-004 Usability and accessibility

- Primary workflows shall work with keyboard navigation.
- Form fields shall have visible labels and validation messages.
- Color shall not be the only indicator of state.
- The interface shall adapt to common mobile and desktop viewport sizes.

### NFR-005 Maintainability

Business logic shall be separated by reading, discussion, polling, and membership capabilities. Automated tests shall cover the critical spoiler, progress, poll-validation, and duplicate-vote rules.

## 5 External interface requirements

### 5.1 User interface

The web interface shall provide a dashboard, goal and progress forms, a discussion-thread view with spoiler controls, an active-poll view, a poll-creation form for discussion leads, and membership controls for administrators.

### 5.2 Application interfaces

The application API shall expose authenticated operations for goals, progress, discussions, polls, votes, and memberships. Request validation errors shall use consistent status codes and user-safe messages.

### 5.3 Data interface

The relational database shall support transactions, foreign keys, and a unique constraint for one vote per member per poll. Timestamps shall be stored consistently and poll-deadline comparisons shall use a single server-side time standard.

## 6 Data requirements

| Entity | Essential data |
|---|---|
| User | Identifier, display name, authentication reference, status |
| Membership | User, club, role, activation state |
| Book | Identifier, title, author, page or chapter metadata |
| ReadingGoal | User, book, unit, target, created and updated times |
| ReadingProgress | Goal, amount, recorded time |
| DiscussionThread | Club, book or chapter context, title |
| Comment | Thread, author, body, spoiler flag, chapter context, time |
| Poll | Club, title, opening time, deadline, status |
| PollCandidate | Poll, book |
| Vote | Poll, candidate, member, recorded time |

## 7 Business rules

1. A poll must contain at least two distinct candidates.
2. A poll deadline must be in the future when published.
3. A closed poll does not accept votes.
4. A member may have only one vote per poll.
5. Vote rejection must not change any tally.
6. Reading progress belongs to the authenticated member's goal.
7. Only a discussion lead may publish or modify a poll.
8. Only an administrator may change membership roles or activation state.

## 8 Verification and acceptance

The RTM in `1-Requirements-Engineering` defines verification for every baseline requirement. Acceptance requires:

- successful execution of functional and authorization tests;
- explicit duplicate-vote and transaction-failure tests;
- restart and recovery verification for persistent records;
- responsive and keyboard-accessible inspection of primary workflows; and
- review of logs to confirm that protected values are not exposed.

## 9 Future enhancements

Potential later releases may add notifications, book metadata integration, multiple clubs per account, recommendations, richer moderation, and analytics. These features are outside the baseline and require separate approval.

