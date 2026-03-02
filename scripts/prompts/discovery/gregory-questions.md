You are generating focused questions for Roger Gregory, who built the udanax-green implementation of the Xanadu hypertext system.

Gregory knows the code, the data structures, and the edge cases. His answers are grounded in what the system actually DOES — behavioral evidence from the implementation.

## Your Task

Given the inquiry below and the knowledge base, generate exactly {num_questions} focused questions for Gregory. Each question must:

1. Target ONE specific behavior, ONE data structure interaction, or ONE edge case
2. Use technical vocabulary from the KB — I-addresses, V-space, spanfilade, subspaces, etc.
3. Cover a distinct aspect — no overlap between questions
4. Be specific enough to get a concrete, testable answer

## Knowledge Base

This KB summarizes what has been discovered about the implementation through testing and code analysis. Use its vocabulary and its knowledge of subsystems to formulate precise questions.

{kb}

## Inquiry

{inquiry}

## Output Format

Return ONLY the numbered questions, one per line. No preamble, no explanation.

Example output:
1. Does INSERT preserve all existing V-to-I address mappings for content before the insertion point?
2. Does the two-blade knife mechanism prevent V-address shifts from propagating into the link subspace (0.x/2.x)?
3. What entries does INSERT create in the spanfilade, and are existing entries preserved?
