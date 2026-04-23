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

## Coupling

Prose and formal content are authored as a pair. A revision that grows
one without the other introduces Sprawl. But do not remove prose that a
reader encountering the claim for the first time would need to
understand what it means.

## Discipline — Resolution ranking

When a review finding admits multiple resolutions that would close it
equally well, follow this ranking:

    delete > restructure > add

This is a tiebreaker for close calls, not a mandate. Findings that
require adding (a missing axiom, a missing precondition, a needed
clarification deletion wouldn't preserve) produce additions regardless.
The ranking applies only when the choice between valid resolutions is
genuinely judgment.

Within that scope, five directives:

1. **Prefer deletion over addition.** If a finding can be resolved by
   deleting the flagged construction or its surrounding justification,
   delete. Only add when no deletion resolves the finding.

2. **When a finding says drop X, drop X — do not relocate.** Moving X
   to a different paragraph, rephrasing X in a new place, or folding X
   into an adjacent clause all leave the drift in the file. Relocation
   is not deletion.

3. **Do not justify excluded cases.** If a claim's carrier or precondition
   excludes a case, do not write prose about what would happen in that
   case. Defensive prose for cases that cannot arise is dead weight.

4. **No meta-commentary.** No "this structure is exhaustive," no
   "matches the convention in sibling claims," no inline citation-site
   enumeration, no defensive justification of past findings.

5. **When adding is required, add the minimum.** A missing axiom is an
   axiom statement — not an axiom plus a paragraph explaining why it is
   needed plus a defense of its bundling.

## Rules

1. Apply exactly the fix described in the finding's **What needs resolving**
   section. Follow it precisely. If the finding admits a structural fix
   (rephrase, move, or remove) that resolves the underlying issue, prefer
   it over extending.

2. The fix may require changes in multiple claim sections. Make all
   necessary changes — do not leave half the fix done.

3. If the fix requires changing a definition's usage throughout the ASN
   (e.g., replacing "T" with "the set of T4-valid addresses"), apply the
   change consistently everywhere the term appears in the affected context.

4. If the fix affects formal contracts, update them to match.

5. If the fix adds new dependencies, add them to the `depends` list in
   the affected claim's `.yaml` file AND update the prose to justify why
   the dependency is used. Do not add to YAML without updating prose.
   Do not write use-site inventories in prose ("invoked at X, Y, Z…") —
   that tracking belongs in metadata, not narrative.

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

7. Do not change anything beyond what the finding requires. Exception:
   meta-prose in the finding's area (defenses of past findings, naming
   rationales, citation-site tracking) may be removed. Prose that states
   what the claim means — semantic properties, contrasts, worked examples
   — may not.

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
