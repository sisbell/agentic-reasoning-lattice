# Full Review Fix

You are fixing a whole-ASN issue in a reasoning document.
Unlike per-claim fixes, this issue may span multiple claims
or involve the relationship between the ASN's language and its
foundation's definitions.

## ASN File

The ASN is at `{{asn_path}}`. Read it, apply the fix, write it back.

## Finding

{{finding}}

## Style

Write in Dijkstra's style: prose with embedded formalism. Each formal
statement must be justified in the sentence that introduces it. Each case
must be explicit — no "by similar reasoning." End proofs with ∎.

## Rules

1. Apply exactly the fix described in the finding's **What needs resolving**
   section. Follow it precisely.

2. The fix may require changes in multiple claim sections. Make all
   necessary changes — do not leave half the fix done.

3. If the fix requires changing a definition's usage throughout the ASN
   (e.g., replacing "T" with "the set of T4-valid addresses"), apply the
   change consistently everywhere the term appears in the affected context.

4. If the fix affects formal contracts, update them to match.

5. If the fix adds new dependencies, add them to the `depends` list in
   the affected claim's `.yaml` file. Do not remove existing dependencies.
   If a finding identifies an undeclared dependency (a claim used in a
   proof but not in the `.yaml` depends list), always add it to the `.yaml`
   — do not just mention it in the prose or formal contract.

6. If the fix requires a new claim that doesn't exist, create both files
   in `{{asn_path}}/`. Use the label as the filename.

   `{Label}.yaml`:
   ```yaml
   label: AX-1
   name: InitialEmpty
   type: axiom
   depends:
     - D2
   ```

   `{Label}.md`:
   ```markdown
   **AX-1 (InitialEmpty).** [definition or statement]

   *Formal Contract:*
   - *Axiom:* [formal assertion]
   ```

7. Do not change anything beyond what the finding requires.

8. **YAML formatting.** When writing any `.yaml` file, ensure the YAML is
   valid. If a value contains colons, quotes, or spans multiple lines
   (common in `summary` fields with math notation), use a literal block
   scalar (`|`) or a quoted string. For example:

   ```yaml
   summary: |
     Defines dom(A) = ⋃{domₛ(A) : s reachable} — the colon in the set
     comprehension requires a block scalar or quoting.
   ```

   Do not write a plain scalar summary that contains an unescaped colon
   followed by a space — YAML will parse it as a key-value separator and
   break the file.
