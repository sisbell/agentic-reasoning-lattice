# Commit Lattice Changes

Commit changes to the lattice with meaningful, descriptive commit messages.

## Process

1. **Read the staged diff within scope:**
   ```bash
   git diff --cached -- {{lattice_dir}}
   ```
   The correct files are already staged. Do NOT run `git add` — staging
   is handled by the caller for concurrent safety.

   If this scoped diff is empty, stop and report that nothing in scope
   was staged. Do not commit.

2. **Understand what changed:**
   - New ASN added?
   - Existing ASN revised?
   - What was the nature of the revision? (claim fix, proof completion, edge case, etc.)
   - Was a review saved to `{{lattice_dir}}/discovery/review/`?
   - Was a verification artifact added or modified?

3. **Generate commit message:**

   Format:
   ```
   <type>(asn): <brief description>

   <what changed and why>
   ```

   Semantic types (apply across lattices):
   - `discovery` — new ASN
   - `review` — review saved to the lattice's review directory
   - `revise` — ASN revised to address review findings
   - `fix` — corrected an error (wrong claim, invalid proof)

   Tool-specific types (vary by lattice's verification stack):
   - `alloy` — Alloy model and check results
   - `dafny` — Dafny verification added or updated
   - Other verifier types as the lattice uses them

   Examples:
   - `discovery(asn): ASN-0004 Content Insertion`
   - `review(asn): ASN-0004 review 1 — 3 REVISE, 2 OUT_OF_SCOPE`
   - `revise(asn): ASN-0004 address review 1 — POST5 proof, empty doc boundary`
   - `alloy(asn): ASN-0004 — D1-D4 pass scope 5+7, F1/A0 skipped`
   - `dafny(asn): ASN-0004 — formalize POST1-POST5, F0-F3`
   - `fix(asn): ASN-0004 correct D2 proof — missing d2≠doc precondition`

4. **Commit only files within scope:**
   ```bash
   git commit -m "<message>" -- {{lattice_dir}}
   ```
   The `-- {{lattice_dir}}` path spec restricts the commit to staged
   changes within scope. Anything staged outside scope remains in the
   index and is not included.

5. **Report:** Show the commit hash and summary.

## Guidelines

- Be specific: "Fix D2 to require d2≠doc" not "Fix proof"
- Mention ASN numbers: "ASN-0004" not "the insertion ASN"
- Name the claims affected: "POST5, F0" not "some claims"
- If review-driven, note it: "Address review 1 issue 3: missing boundary case"
- Keep first line under 72 characters
- Body should describe WHAT changed and WHY in domain terms
