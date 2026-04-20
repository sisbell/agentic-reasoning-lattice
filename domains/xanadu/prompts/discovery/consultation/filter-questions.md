You are filtering generated questions for scope. Given an inquiry and exclusion criteria, decide which questions are in scope and which should be dropped.

## Inquiry

{inquiry}

## Excluded Topics

{out_of_scope}

{foundation_block}

## Questions

{questions}

## Task

For each question, output KEEP or DROP followed by the question number.

A question is DROP if:
- It is primarily about any of the excluded topics, OR
- Its answer is already established by the foundation topics listed above

If a question touches an excluded or established topic only incidentally while primarily addressing an in-scope concern, KEEP it.

Output ONLY lines in this format, one per question:
KEEP 1
DROP 2
KEEP 3
...
