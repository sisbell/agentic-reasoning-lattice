# Commit Proof Changes

Commit changes to `{{proofs_dir}}` — the curated, human-reviewed proof library.

These changes are deliberate promotions or updates. They should never come from
automated pipelines.

## Process

1. **Check for changes:**
   ```bash
   git status {{proofs_dir}}
   ```

2. **If changes exist, read the diffs:**
   ```bash
   git diff {{proofs_dir}}
   git diff --cached {{proofs_dir}}
   ```

3. **Understand what changed:**
   - New proof module promoted from verification?
   - Existing foundation updated (new lemma, refactored helper)?
   - Bridge lemma added for downstream use?

4. **Stage only `{{proofs_dir}}`:**
   ```bash
   git add {{proofs_dir}}
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

6. **Commit only files within scope:**
   ```bash
   git commit -m "<message>" -- {{proofs_dir}}
   ```
   The `-- {{proofs_dir}}` path spec restricts the commit to staged
   changes within scope. Anything staged outside scope remains in the
   index and is not included.

7. **Report:** Show the commit hash and summary.

## Guidelines

- Name the module: `TumblerAlgebra` not `proofs`
- Name the specific additions: `LessThanIntro` not `a lemma`
- Note the source if from modeling: `from modeling-1`
- Keep first line under 72 characters
