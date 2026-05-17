# Review of ASN-0086

## REVISE

### Issue 1: Nullify's single-tuple-scope is discipline-conditional but the proof header and Remark misrepresent the role of P3.

**ASN-0086, Definition — Nullify, "Single-tuple scope, from P3 directly" paragraph and "Remark on discharging P3" paragraph**: The paragraph claims single-tuple-scope follows "from P3 directly" while the argument body invokes three sources: P3 (for the prior-state part `{a' ∈ dom(Σ.L) : a ≼ a'} = {a}`), R0 Step 2's specific construction (for `b ≠ a`), and "R0a's reachable-state antichain property at Σ' giving `a ⊀ b`" (for the post-state part). The Remark goes further: "P3's separate listing makes Nullify's single-tuple-scope claim well-defined for any system in which P3 holds at a — including ones for which the sibling-frontier discipline of R0a is asserted only as an interface contract on Emit_K".

**Problem**: P3 alone is insufficient. P3 constrains `dom(Σ.L)` at the prior state Σ; the conclusion `{a' ∈ dom(Σ'.L) : a ≼ a'} = {a}` is over `dom(Σ'.L) = dom(Σ.L) ∪ {b}` and depends on whether the new emitter address `b` is a prefix-extension of `a`. As the ASN itself acknowledges in the substrate-primitive discussion ("a hypothetical alternative emission policy that deposited at `a' = a₁.1` would satisfy the primitive's conditions"), the substrate emission primitive admits emissions at strict prefix-extensions of existing link addresses. Under such an emission, `b` could be `a.1`, `a` ≼ `b`, and `nullified(Σ')` would gain both `a` and `b` — breaking single-tuple-scope. The conclusion is therefore discipline-conditional in exactly the way R0a is, and R0a is explicitly tagged as such while single-tuple-scope is not.

**Required**: Either (i) revise the header to acknowledge the multiple dependencies (e.g., "Single-tuple scope, from P3 plus the emission discipline"), tag the conclusion `[discipline-conditional]` parallel to R0a, and rewrite the Remark to distinguish "P3 makes the substrate-level precondition well-defined" from "the conclusion is discharged" (the latter still requires R0a or an equivalent discipline); or (ii) constrain the Emit_R composed by Nullify to use R0 Step 2's construction directly (not the broader substrate emission primitive), so single-tuple-scope follows from P3 and the construction without invoking R0a's reachable-state antichain.

### Issue 2: R0 Step 4's invariant verification chain omits L12b.

**ASN-0086, R0 Step 4 ("Each invariant is verified directly:")**: The bullet list verifies L-fin, L0, L1, L1a, L1b, L1c, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11a, L11b, L12, L12a, L13, L14, L14a (and partial-function-ness, and ASN-0036 S-invariants as a group) — but does not include L12b (HomeDocumentPersistence).

**Problem**: L12b is a named L-lemma from ASN-0043 ("The home documents of all existing links remain allocated across every state transition"). The verification chain claims to verify every L-invariant — and explicitly includes other lemmas (L2, L11a, L11b, L13, L14, L14a) — but skips L12b. The omission is a completeness gap. L12b's verification is trivial under R0's Frame (`Σ'.M = Σ.M`, so prior homes stay in `dom(Σ'.M)`; new home `d ∈ dom(Σ.M)` by Step 1), but the exhaustive form of the verification chain requires it to be stated.

**Required**: Add a bullet verifying L12b's preservation: by Frame `Σ'.M = Σ.M`, `dom(Σ.M) ⊆ dom(Σ'.M)`, so prior homes `{home(a') : a' ∈ dom(Σ.L)}` ⊆ `dom(Σ'.M)`; the new home `d = home(a) ∈ dom(Σ.M) = dom(Σ'.M)` by Step 1.

## OUT_OF_SCOPE

(none — the ASN's Open Questions section already covers genuine future-ASN items: arrangement-relation invariants, higher-arity active subsets, second-order retraction semantics, Observe ordering, atomicity/concurrency, retraction cardinality bounds, substrate-level adoption of the sibling-frontier discipline, and dynamic type-catalog extension.)

VERDICT: REVISE
