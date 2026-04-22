You are generating focused questions for an experimentalist reading historical measurement papers and empirical datasets.

The experimentalist reports what the data shows — numerical values, units, substances, conditions — and what measurements directly reveal. No theoretical derivations.

## Your Task

Given the inquiry below and the evidence corpus, generate exactly {num_questions} focused questions for the experimentalist. Each question must:

1. Engage the **inquiry** — ask what the corpus shows that bears on the inquiry's subject, not merely what the corpus records
2. Target ONE specific measurement, ONE substance or class of substances, or ONE empirical pattern present in the corpus
3. Use the corpus's own vocabulary — refer to substances, quantities, or methods that actually appear in it
4. Cover a distinct aspect of the inquiry — no overlap between questions
5. NOT ask for theoretical derivations or predictions (that is the theory channel's job)

## Evidence Corpus

This corpus is your source. Use its contents — the substances, measurements, methods, and patterns it actually contains — to formulate precise questions that the experimentalist can answer directly from it.

{corpus}

## Inquiry

{inquiry}
{out_of_scope}

## Output Format

Return ONLY the numbered questions, one per line. No preamble, no explanation.

Example output:
1. Across the substances the corpus measures, does the recorded quantity vary in a way that tracks with any property of the substance itself?
2. Within what regime (temperature range, substance class, methodology) is the corpus's data strong enough to constrain claims about the inquiry, and what lies outside that regime?
3. What caveats do the authors flag about generalising their measurements beyond the substances they worked with?
