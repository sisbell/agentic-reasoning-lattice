# Commit Vault Changes

Commit changes to the vault with meaningful, descriptive commit messages.

## Process

1. **Check for changes:**
   ```bash
   git status vault/
   ```

2. **If changes exist, read the diffs:**
   ```bash
   git diff vault/
   git diff --cached vault/
   ```

3. **Understand what changed:**
   - New ASN added?
   - Existing ASN revised?
   - What was the nature of the revision? (property fix, proof completion, edge case, etc.)
   - Was a review saved to `vault/2-review/`?
   - Was a Dafny file added or modified?

4. **Stage the changes:**
   ```bash
   git add vault/asns/ vault/requirements/ vault/1-promote/ vault/2-review/ vault/3-modeling/ vault/experts/ 2>/dev/null; true
   ```

   **Important:** Never stage `vault/proofs/`. That directory contains curated,
   human-reviewed proof files. Changes there are committed manually by the
   operator using a separate, deliberate process.

5. **Generate commit message:**

   Format:
   ```
   <type>(asn): <brief description>

   <what changed and why>
   ```

   Types:
   - `discovery` — new ASN
   - `review` — review saved to vault/2-review/
   - `revise` — ASN revised to address review findings
   - `alloy` — Alloy model and check results
   - `dafny` — Dafny formalization added or updated
   - `fix` — corrected an error (wrong property, invalid proof)

   Examples:
   - `discovery(asn): ASN-0004 Content Insertion`
   - `review(asn): ASN-0004 review 1 — 3 REVISE, 2 OUT_OF_SCOPE`
   - `revise(asn): ASN-0004 address review 1 — POST5 proof, empty doc boundary`
   - `alloy(asn): ASN-0004 — D1-D4 pass scope 5+7, F1/A0 skipped`
   - `dafny(asn): ASN-0004 — formalize POST1-POST5, F0-F3`
   - `fix(asn): ASN-0004 correct D2 proof — missing d2≠doc precondition`

6. **Commit:**
   ```bash
   git commit -m "<message>"
   ```

7. **Report:** Show the commit hash and summary.

## Guidelines

- Be specific: "Fix D2 to require d2≠doc" not "Fix proof"
- Mention ASN numbers: "ASN-0004" not "the insertion ASN"
- Name the properties affected: "POST5, F0" not "some properties"
- If review-driven, note it: "Address review 1 issue 3: missing boundary case"
- Keep first line under 72 characters
- Body should describe WHAT changed and WHY in domain terms
