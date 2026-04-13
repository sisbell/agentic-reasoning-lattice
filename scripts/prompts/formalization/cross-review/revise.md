# Cross-cutting Fix

You are fixing a cross-cutting issue in an ASN reasoning document.
Unlike per-property fixes, this issue may span multiple properties
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

2. The fix may require changes in multiple property sections. Make all
   necessary changes — do not leave half the fix done.

3. If the fix requires changing a definition's usage throughout the ASN
   (e.g., replacing "T" with "the set of T4-valid addresses"), apply the
   change consistently everywhere the term appears in the affected context.

4. If the fix affects formal contracts, update them to match.

5. If the fix adds new dependencies, add them to the `depends` list in
   the affected property's `.yaml` file. Do not remove existing dependencies.

6. If the fix requires a new property that doesn't exist, create both files:
   - `{Label}.yaml` with fields: label, name, type, depends
   - `{Label}.md` with bold header, definition/statement, and formal contract
   Filenames are derived from labels: strip parentheses, replace spaces/commas
   with hyphens (e.g., `V_S(d)` → `V_Sd`, `subspace(v)` → `subspace`).

7. Do not change anything beyond what the finding requires.
