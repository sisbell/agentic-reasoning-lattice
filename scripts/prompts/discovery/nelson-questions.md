You are generating focused questions for Ted Nelson, the designer of the Xanadu hypertext system.

Nelson thinks about content, identity, permanence, links, documents, users, sharing, and versions. He designed the system's guarantees — what it MUST do, independent of any implementation.

## Your Task

Given the inquiry below, generate exactly {num_questions} focused questions for Nelson. Each question must:

1. Target ONE guarantee or ONE design property
2. Use design vocabulary — content, identity, permanence, links, documents, sharing, versions
3. Cover a distinct aspect — no overlap between questions
4. NOT use implementation terms (I-addresses, V-space, spanfilade, subspace, enfilade, tumbler, POOM)

## Inquiry

{inquiry}

## Output Format

Return ONLY the numbered questions, one per line. No preamble, no explanation.

Example output:
1. What must the system guarantee about the permanence of content once it enters the storage layer?
2. How does the design ensure that links survive editing operations on linked content?
3. Must insertion into one document leave all other documents completely unaffected?
