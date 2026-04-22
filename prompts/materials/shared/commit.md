# Commit Lattice Changes

Commit changes to the lattice with meaningful, descriptive commit messages.

## Process

1. **Read the staged diff:**
   ```bash
   git diff --cached
   ```
   The correct files are already staged. Do NOT run `git add` — staging
   is handled by the caller for concurrent safety.

2. **Understand what changed:**
   - New ASN added?
   - Existing ASN revised?
   - What was the nature of the revision? (claim fix, derivation completion, regime condition, etc.)
   - Was a review saved to `lattices/materials/discovery/review/`?

3. **Generate commit message:**

   Format:
   ```
   <type>(asn): <brief description>

   <what changed and why>
   ```

   Types:
   - `discovery` — new ASN
   - `review` — review saved to lattices/materials/discovery/review/
   - `revise` — ASN revised to address review findings
   - `fix` — corrected an error (wrong claim, invalid derivation)

   Examples:
   - `discovery(asn): ASN-0002 Constitution and the Nature of Heat`
   - `review(asn): ASN-0002 review 1 — 4 REVISE, 1 OUT_OF_SCOPE`
   - `revise(asn): ASN-0002 address review 1 — regime for atomic-heat regularity, postulate labeling`
   - `fix(asn): ASN-0002 correct P.equipartition — forbidden terminology in claim label`

4. **Commit:**
   ```bash
   git commit -m "<message>"
   ```

5. **Report:** Show the commit hash and summary.

## Guidelines

- Be specific: "Fix P.temp_functional to require equilibrium regime" not "Fix claim"
- Mention ASN numbers: "ASN-0002" not "the constitution ASN"
- Name the claims affected: "P.heat_as_motion, Σ.eint" not "some claims"
- If review-driven, note it: "Address review 1 issue 3: missing regime condition"
- Keep first line under 72 characters
- Body should describe WHAT changed and WHY in domain terms
