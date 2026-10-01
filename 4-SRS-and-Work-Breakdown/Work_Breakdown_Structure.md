# Work Breakdown Structure

## 1 Project management

| WBS | Work package | Output | Completion condition |
|---|---|---|---|
| 1.1 | Confirm scope and stakeholders | Approved scope statement | Actors, included features, and exclusions are documented. |
| 1.2 | Maintain delivery plan | Prioritized task list | Every work package has an owner and status. |
| 1.3 | Manage risks and changes | Risk and change log | Material changes are traced to requirements and tests. |

## 2 Requirements engineering

| WBS | Work package | Output | Completion condition |
|---|---|---|---|
| 2.1 | Analyze Problem Statement 55 | Actor and feature summary | Club Member, Discussion Lead, and Administrator responsibilities are clear. |
| 2.2 | Define functional requirements | FR-001 to FR-005 | Each requirement has acceptance criteria. |
| 2.3 | Define non-functional requirements | NFR baseline | Integrity, availability, security, accessibility, and maintainability are measurable. |
| 2.4 | Model use cases | UML diagram and detailed vote flow | Main, alternate, and exception paths are present. |
| 2.5 | Establish traceability | RTM | Every requirement maps to design and verification evidence. |

## 3 Architecture and design

| WBS | Work package | Output | Completion condition |
|---|---|---|---|
| 3.1 | Select architecture | Layered modular architecture decision | Style and rationale are documented. |
| 3.2 | Design components | Component diagram and responsibilities | UI, API, services, data, and operations are represented. |
| 3.3 | Design data model | Entity relationships and constraints | All persistent entities and the unique vote rule are defined. |
| 3.4 | Design interfaces | Screen and API contracts | Inputs, outputs, validation, and permissions are specified. |

## 4 Implementation

| WBS | Work package | Output | Completion condition |
|---|---|---|---|
| 4.1 | Set up project | Repository, environments, and quality checks | The project builds and checks run consistently. |
| 4.2 | Implement identity and roles | Authentication and authorization module | Protected actions reject unauthorized users. |
| 4.3 | Implement goals and progress | Reading challenge module | Goal persistence and progress calculation pass tests. |
| 4.4 | Implement discussion and spoilers | Discussion module | Spoilers stay masked until an authorized reveal. |
| 4.5 | Implement monthly polls | Poll creation and result views | Candidate and deadline validation pass tests. |
| 4.6 | Implement vote integrity | Transactional vote operation | Duplicate and partial votes are impossible. |
| 4.7 | Implement administration | Membership controls and audit events | Role and status changes are protected and recorded. |

## 5 Verification and validation

| WBS | Work package | Output | Completion condition |
|---|---|---|---|
| 5.1 | Prepare unit tests | Automated module tests | Core business rules have positive and negative coverage. |
| 5.2 | Prepare integration tests | API and database tests | Persistence, permissions, and transaction behavior are verified. |
| 5.3 | Execute system tests | Test report | End-to-end workflows meet acceptance criteria. |
| 5.4 | Test quality attributes | Performance, restart, recovery, and accessibility evidence | Baseline quality targets are evaluated and exceptions recorded. |
| 5.5 | Resolve defects and retest | Defect and retest log | Critical defects are closed and affected tests pass. |

## 6 Delivery

| WBS | Work package | Output | Completion condition |
|---|---|---|---|
| 6.1 | Assemble documentation | README, RE, architecture, SRS, WBS, and testing folders | Repository structure matches the submission instructions. |
| 6.2 | Add project-tool evidence | GitHub and Jira screenshots | Evidence files are readable and linked from the README. |
| 6.3 | Add AI-assisted development evidence | Copilot screenshot or repository link | Evidence identifies the code or repository. |
| 6.4 | Final review | Submission checklist | Links work, documents render, and no required item is missing. |

## Suggested execution order

1. Baseline requirements and RTM.
2. Approve architecture and data constraints.
3. Implement authentication, reading, discussion, and polling modules.
4. Add unit and integration tests during implementation.
5. Execute system, recovery, performance, and accessibility checks.
6. Fix defects, retest, and package all evidence in the repository.

