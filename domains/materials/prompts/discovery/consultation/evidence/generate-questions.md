You are generating focused questions for an experimentalist reading measured heat-capacity and materials data.

The experimentalist reports what the data shows — numerical values, units, substances, conditions — and what measurements directly reveal. No theoretical derivations.

## Your Task

Given the inquiry below, generate exactly {num_questions} focused questions for the experimentalist. Each question must:

1. Target ONE specific measurement, ONE substance or class of substances, or ONE empirical pattern
2. Use measurement vocabulary — temperature, specific heat, molar heat capacity, element, substance, mass, measurement method
3. Cover a distinct aspect — no overlap between questions
4. NOT ask for theoretical derivations or predictions (that is the theory channel's job)

## Inquiry

{inquiry}
{out_of_scope}

## Output Format

Return ONLY the numbered questions, one per line. No preamble, no explanation.

Example output:
1. What values of specific heat are reported for solid elements in the corpus, and across what temperature range?
2. Which substances show the largest and smallest molar heat capacities in the data?
3. Does the data suggest any pattern relating heat capacity to atomic mass or to the kind of substance?
