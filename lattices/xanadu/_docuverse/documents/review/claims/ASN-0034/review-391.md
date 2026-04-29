# Regional Review — ASN-0034/T4 (cycle 1)

*2026-04-22 23:33*

### T4a/T4b/T4c lack formal contracts
**Class**: REVISE
**Foundation**: (internal)
**ASN**: T4 body paragraph: "Three first-class numbered theorems, each a downstream combination of T4 with additional foundations rather than a consequence of T4 alone, round out the parsing picture. **T4a (SyntacticEquivalence)** ... **T4b (UniqueParse)** ... **T4c (LevelDetermination)** ..."
**Issue**: T4a, T4b, T4c are designated "first-class numbered theorems" and named as if co-equal with T4, but no Formal Contract blocks are provided for them — no Axiom/Consequence/Depends enumeration. Every other named item in the ASN (T0, NAT-zero, NAT-discrete, NAT-order, NAT-closure, NAT-card, T4) carries a Formal Contract. The content of T4a–c lives only in narrative prose embedded inside T4's body paragraph, so the theorem statements (e.g. the iff of T4c's level-determination, T4a's equivalence direction, T4b's four partial projections) cannot be cited downstream in the contract format the ASN otherwise uses.
**What needs resolving**: Either give T4a, T4b, T4c their own Formal Contract blocks (with Preconditions, Axiom/Consequence, Depends), or demote them from "first-class numbered theorems" to explicit forward references to a section/ASN where they are formalized.

### Ungrounded dependencies NAT-sub and NAT-addcompat
**Class**: REVISE
**Foundation**: (internal)
**ASN**: T4 body: "**T4a (SyntacticEquivalence)** adds NAT-sub — whose conditional-closure clause gives `#t − 1 ∈ ℕ` under the locally unpacked `#t ≥ 1` from T0 ..." and "**T4c (LevelDetermination)** combines T4 with NAT-addcompat's strict successor inequality `n < n + 1` ..."
**Issue**: NAT-sub and NAT-addcompat are invoked by name, with specific clauses cited (conditional-closure of subtraction, strict successor inequality), but neither appears as a top-level item in this ASN and neither is declared in any Depends slot. They are also not foundation statements imported for this ASN (no Foundation Statements section). The prose references therefore float: a downstream reader cannot locate the cited axioms.
**What needs resolving**: Either add NAT-sub and NAT-addcompat as formal items in this ASN with their own Axiom/Depends, or mark them as imports from an external ASN and list them in the appropriate Depends slot of whichever theorem invokes them.

### Forward reference to nonexistent "T4c Exhaustion paragraph"
**Class**: REVISE
**Foundation**: (internal)
**ASN**: T4 Formal Contract Axiom: "Exhaustion of `zeros(t) ∈ {0, 1, 2, 3}` is not asserted here; T4c's Exhaustion paragraph derives it from the bound `zeros(t) ≤ 3` using iterated NAT-order trichotomy and NAT-discrete."
**Issue**: T4's Axiom defers exhaustion to "T4c's Exhaustion paragraph," but T4c has no formal statement in this ASN, let alone a subdivision called "Exhaustion." The deferral is therefore a pointer into empty space. Separately, the Axiom declines to commit to `zeros(t) ∈ {0,1,2,3}` while the per-`k` schema is quantified only "at which `zeros(t) = k`," so the schema collectively leaves open whether any T4-valid tumbler need land in {0,1,2,3} at all — that work is pushed to the nonexistent T4c paragraph.
**What needs resolving**: Either prove exhaustion inside T4's own body (from `zeros(t) ≤ 3`, NAT-order trichotomy, NAT-discrete, and NAT-zero) and state it as a Consequence, or, if T4c is given a Formal Contract per the first finding, ensure that contract contains the Exhaustion claim T4 defers to.

### Use-site inventory and register meta-prose in foundation bodies
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: NAT-closure body: "The axiom slot introduces `+` before constraining it: its first clause `+ : ℕ × ℕ → ℕ` posits the signature — fixing arity (binary) and codomain (ℕ). The operation is posited directly on ℕ rather than derived from an earlier axiom — the same register NAT-order uses to posit `<` (with its axiom opening `< ⊆ ℕ × ℕ` before the strict-total-order clauses)." Similar register-matching prose appears in NAT-order ("NAT-closure follows the same register for the arithmetic primitive…").
**Issue**: Paragraphs that explain why each axiom is written the way it is (matching a "register," paralleling another foundation's opening move) are meta-commentary on the document, not statements about ℕ or `+` or `<`. They do not advance any reasoning that later claims depend on. The precise reader must skip past them to read the axiom itself.

### Derivation essay inside NAT-zero body
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: NAT-zero body: "Suppose some `n ∈ ℕ` did satisfy `n < 0`; the second clause forces `0 < n ∨ 0 = n`. In the first case, `0 < n` and `n < 0` together yield `0 < 0` by transitivity, contradicting irreflexivity. In the second case, `0 = n` rewrites `n < 0` to `0 < 0`, again contradicting irreflexivity."
**Issue**: A complete proof-by-cases lives inline in the body prose of a foundation axiom item. The Consequence `¬(n < 0)` is correct and the derivation is valid, but two-case prose expanding the lift from the disjunction is the kind of content the formalization layer, not the axiom statement, should carry. The axiom's body ends up as essay rather than as a terse claim.

### T4 body paragraph recounts each dependency's use-site
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: T4 body: "T0 fixes the carrier as ℕ; NAT-order supplies the strict total order `<` … NAT-closure supplies `1 ∈ ℕ` together with closure … NAT-zero together with NAT-discrete (at `m = 0`) force every non-zero component to be strictly positive …"
**Issue**: The body enumerates, per dependency, what that dependency contributes to T4's axiom clauses. The same information is then repeated in the Depends slot, which is the canonical location for use-site justification. The body-level inventory is redundant with the Depends block and dilutes the actual mathematical content of T4 (definition of `zeros(t)`, the field-segment constraint, field segments).

VERDICT: REVISE
