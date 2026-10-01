# Testing Bug Fix and Retest Process

## 1 Obtain and identify the application

1. Record the assigned repository URL and assignment identifier.
2. Clone the repository without modifying the original default branch.
3. Read its README and identify the language, runtime, dependency manager, test command, and expected game behavior.
4. Record the starting commit so the initial behavior can be reproduced.

## 2 Establish the baseline

1. Install only the dependencies declared by the project.
2. Run all four supplied test cases before changing code.
3. Save the unedited command and complete result.
4. Record which tests pass or fail and whether the game behavior matches the README.

## 3 Reproduce and diagnose the defect

1. Reproduce the failing behavior using the smallest reliable sequence of actions.
2. Trace the failing test from its assertion to the relevant game function or state transition.
3. Identify the root cause rather than changing the expected result to hide the failure.
4. Add or refine a regression test only when it represents the specified behavior.

## 4 Apply the patch

1. Make the smallest code change that corrects the root cause.
2. Preserve public interfaces unless the specification requires a change.
3. Avoid unrelated formatting or feature additions.
4. Record changed files and explain how the patch addresses the failure.

## 5 Retest

1. Run the originally failing test and confirm that it now passes.
2. Run all four supplied tests to detect regressions.
3. Start the game and manually verify the affected user path when practical.
4. Save the test command, timestamp, summary, and evidence location.

## 6 Publish evidence

1. Commit the patch and test evidence with a descriptive message.
2. Push the corrected code to the student's authorized repository.
3. Add the corrected repository and commit links to the test record.
4. Do not mark the exercise complete unless the initial failure, patch, and successful retest are all documented.

## Evidence quality checklist

- [ ] Starting repository and commit are recorded.
- [ ] Game purpose and expected behavior are explained.
- [ ] Four initial test results are present.
- [ ] The defect is reproducible.
- [ ] Root cause is described in plain language.
- [ ] Patch files or commit are linked.
- [ ] The affected test passes after the fix.
- [ ] All four tests pass or any remaining failure is explained.
- [ ] Corrected repository link is accessible to the evaluator.

