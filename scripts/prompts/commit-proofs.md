# Commit Proof Changes

Commit changes to `vault/proofs/` — the curated, human-reviewed proof library.

These changes are deliberate promotions or updates. They should never come from
automated pipelines.

## Process

1. **Check for changes:**
   ```bash
   git status vault/proofs/
   ```

2. **If changes exist, read the diffs:**
   ```bash
   git diff vault/proofs/
   git diff --cached vault/proofs/
   ```

3. **Understand what changed:**
   - New proof module promoted from modeling?
   - Existing foundation updated (new lemma, refactored helper)?
   - Bridge lemma added for downstream use?

4. **Stage only vault/proofs/:**
   ```bash
   git add vault/proofs/
   ```

5. **Generate commit message:**

   Format:
   ```
   promote(<module>): <brief description>
   ```

   Examples:
   - `promote(TumblerAlgebra): add LessThanIntro bridge lemma`
   - `promote(TumblerAlgebra): LexicographicOrder, MutualInverse from modeling-1`
   - `promote(Foundation): refactor Pad helpers for clarity`

6. **Commit:**
   ```bash
   git commit -m "<message>"
   ```

7. **Report:** Show the commit hash and summary.

## Guidelines

- Name the module: `TumblerAlgebra` not `proofs`
- Name the specific additions: `LessThanIntro` not `a lemma`
- Note the source if from modeling: `from modeling-1`
- Keep first line under 72 characters
