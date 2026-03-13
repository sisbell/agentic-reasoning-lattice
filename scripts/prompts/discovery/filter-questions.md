You are filtering generated questions for scope. Given an inquiry and a list of excluded topics, decide which questions are in scope and which are out of scope.

## Inquiry

{inquiry}

## Excluded Topics

{out_of_scope}

## Questions

{questions}

## Task

For each question, output KEEP or DROP followed by the question number. A question is DROP if it is primarily about any of the excluded topics. If a question touches an excluded topic only incidentally while primarily addressing an in-scope concern, KEEP it.

Output ONLY lines in this format, one per question:
KEEP 1
DROP 2
KEEP 3
...
