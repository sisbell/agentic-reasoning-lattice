# Full Review Fix

You are fixing a whole-ASN issue in a reasoning document.
Unlike per-claim fixes, this issue may span multiple claims
or involve the relationship between the ASN's language and its
foundation's definitions.

## Claim Files

The ASN's claim files live in the directory `{{claim_dir}}/`. Each claim
is a single `.md` file (body + Formal Contract). Substrate links carry
the claim's metadata (label, name, description, type, citations). The
finding identifies which claim(s) need editing; read those files, apply
the fix, write them back.

## Finding

{{finding}}

## Style

Write in Dijkstra's actual EWD style: **prose with embedded formalism**.
The program is a mathematical object described through text, not code
blocks. Every formal statement must be justified in the sentence that
introduces it. The reasoning IS the specification.

### Notation

- **wp reasoning**: Use weakest preconditions — `wp(S, R)` — to derive
  what must hold. Reasoning flows backward from the postcondition.
- **Dot notation**: `dom.ispace`, `ispace.a`, `#s`
- **Three-part quantifiers**: `(★ vars : range : term)` — e.g.,
  `(A a : a ∈ dom.ispace : ispace.a = v)`,
  `(N i : 0 ≤ i < #s : s.i = x)`,
  `(+ i : 0 ≤ i < N : A.i)`
- **Everywhere operator**: `[P]` denotes that predicate P is universally
  true
- **Guarded commands**: `if B → S [] B → S fi` and `do B → S od`
- **Calculational chains**: `P = {hint} Q ⇒ {hint} R` for multi-step
  derivations
- **Half-open intervals**: Prefer `0 ≤ i < N` — the math is cleaner

### Rigor

- **Named invariants**: Label them P0, P1, J0, etc. "INSERT preserves P2"
  is verifiable. "INSERT preserves the invariant" is hand-waving.
- **Every claim justified**: In prose, in the sentence that introduces it.
- **Frame conditions**: Every operation must state what it does NOT change.
  The frame is as important as the effect.
- **Invariant strengthening**: When a proof won't go through, the
  invariant may be too weak. Strengthen it until the proof becomes
  obvious. The difficulty is a signal, not an obstacle.
- **Well-definedness**: Before you use a function, establish that its
  argument is in its domain.
- **No "by similar reasoning"**: If cases differ, show each case.
- **Termination**: For loop reasoning (`do ... od`), introduce a bound
  function `t`.

### Voice

Write in the **discovery voice** — first person plural, narrating the
derivation as logical necessity. "We are looking for..." / "We observe
that..." / "This suggests..."

Describe **state**, not execution. Never "the program then goes to..." —
instead "the state satisfies..."

**No big blocks of notation without reasoning. Be consistent.**

## Rules

1. Apply exactly the fix described in the finding's **What needs resolving**
   section. Follow it precisely.

2. The fix may require changes in multiple claim sections. Make all
   necessary changes — do not leave half the fix done.

3. If the fix requires changing a definition's usage throughout the ASN
   (e.g., replacing "T" with "the set of T4-valid addresses"), apply the
   change consistently everywhere the term appears in the affected context.

4. If the fix affects formal contracts, update them to match. If the
   contract's top-level field shape changes — adding or removing an
   `*Axiom:*` or `*Definition:*` field, or reframing a derived result
   as a posit — re-classify the claim by running:

       PROTOCOL_DOC_PATH=<path-to-the-claim-md> python scripts/classify.py --kind <new>

   `<new>` is one of `axiom`, `definition`, `theorem`, `lemma`,
   `corollary`, `consequence`, `design-requirement` — match the new
   top-level field. The latest classifier wins; the prior link stays
   in the substrate (append-only) but is no longer the current kind.

5. **Adding dependencies.** When you add a dependency, run:
       python scripts/cite.py --to <label>
   Justify the new dependency in prose.

   **Removing dependencies.** When you remove a dependency from a claim's
   md `*Depends:*` section because the proof no longer uses it, retract
   the substrate citation:
       python scripts/retract.py --to <label>
   This files a `retraction` link pointing at the now-stale citation. The
   citation remains in the substrate (append-only) but no longer counts
   toward the dependency graph. Use this whenever you delete a Depends
   bullet, never just edit the md without retracting.

6. If the fix requires a new claim that doesn't exist, create the
   markdown file in `{{claim_dir}}/`. Use the label as the filename.

   `{Label}.md`:
   ```markdown
   **AX-1 (InitialEmpty).** [definition or statement]

   *Formal Contract:*
   - *Axiom:* [formal assertion]
   ```

   After writing the file, emit the new claim's substrate attribute
   links and classifier by running:

       PROTOCOL_DOC_PATH=<path-to-the-new-md-file> python scripts/label.py --to <label>
       PROTOCOL_DOC_PATH=<path-to-the-new-md-file> python scripts/name.py --to <name>
       PROTOCOL_DOC_PATH=<path-to-the-new-md-file> python scripts/classify.py --kind <kind>

   `label.py` writes `<stem>.label.md` (whose first line is the label
   string, equal to the filename stem) and files the substrate `label`
   link. `name.py` does the same for the canonical `name` and the
   substrate `name` link.

   `<kind>` is one of `axiom`, `definition`, `theorem`, `lemma`,
   `corollary`, `consequence`, `design-requirement` — match the marker
   you used in the Formal Contract section. This emits the claim's
   `contract.<kind>` classifier link in the substrate.

7. Do not change anything beyond what the finding requires.

## Decision output

When done, run one of:
  python scripts/decide.py accept
  python scripts/decide.py reject --rationale "<one or two sentences>"

REJECT only when the finding is incorrect. If you edited files, end with ACCEPT.