You are generating focused questions for a theorist working from Maxwell's *Theory of Heat* (1871) and classical kinetic-theory / statistical-mechanics writings.

The theorist reasons about energy, motion, temperature, pressure, and how physical systems behave under general principles — independent of specific measurements.

## Your Task

Given the inquiry below, generate exactly {num_questions} focused questions for the theorist. Each question must:

1. Target ONE theoretical concept or ONE claim the theory would make
2. Use theoretical vocabulary — energy, equipartition, degrees of freedom, collision, pressure, temperature, molecular motion
3. Cover a distinct aspect — no overlap between questions
4. NOT ask for specific numeric values from measurements (that is the evidence channel's job)

## Inquiry

{inquiry}
{out_of_scope}

## Output Format

Return ONLY the numbered questions, one per line. No preamble, no explanation.

Example output:
1. What does equipartition predict for the average kinetic energy of a molecule at temperature T?
2. How does the theory relate the total energy of a system to its microscopic motion?
3. What constraints does the theory place on heat exchanges between bodies at different temperatures?
