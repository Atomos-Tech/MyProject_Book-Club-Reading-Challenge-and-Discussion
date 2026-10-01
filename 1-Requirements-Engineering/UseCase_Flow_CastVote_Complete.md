# Use Case Flow Cast Vote in Monthly Poll

## Identification

| Field | Value |
|---|---|
| Use case | Cast Vote in Monthly Poll |
| ID | UC-08 |
| Implements | FR-005 |
| Includes | UC-09 Verify Duplicate Vote |
| Supports | NFR-001 |
| Primary actor | Club Member |
| Supporting actor | System identity and vote-log verification |

## Preconditions

1. The club member has an authenticated, active session.
2. A monthly poll is open and the current time is before its deadline.
3. The poll contains at least two candidate books.

## Trigger

The club member selects a candidate book and confirms the vote.

## Main success scenario

1. The club member opens the current monthly poll.
2. The system displays the candidate books and voting deadline.
3. The member selects one candidate.
4. The member confirms the submission.
5. The system verifies that the member has not already voted in this poll.
6. The system records the member-and-poll vote atomically.
7. The system increments the selected candidate's tally.
8. The system displays the updated result and confirms that the vote was recorded.
9. The use case ends successfully.

## Alternate flow A1 Duplicate vote

This flow begins at main step 5.

1. The system finds an existing vote for the same member and poll.
2. The system rejects the new submission.
3. The existing vote and every candidate tally remain unchanged.
4. The system displays: **You have already voted in this poll.**
5. The use case ends without recording another vote.

## Alternate flow A2 Poll closes before confirmation

This flow begins at main step 4.

1. The system rechecks the voting deadline.
2. If the deadline has passed, the system does not record the vote.
3. The system displays that the poll is closed and shows final results if permitted.

## Exception flow E1 Recording failure

This flow begins at main step 6.

1. The data store fails to complete the vote transaction.
2. The system rolls back the transaction so that neither the vote record nor tally is partially updated.
3. The system logs the failure without exposing sensitive account information.
4. The system asks the member to retry later.

## Postconditions

### Success

- Exactly one vote is associated with the member and poll.
- The selected candidate's tally includes the vote.
- The result displayed to authorized users reflects the committed record.

### Failure

- No additional vote is recorded.
- Existing votes and tallies remain unchanged.

