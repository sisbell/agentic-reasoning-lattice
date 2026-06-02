# Review of ASN-0086

## REVISE

### Issue 1: Unit-depth-discipline induction skips the off-`A_rel` Nullify target case, breaking wp Case 2 and R-Scope

**ASN-0086, "Definition — layer-reachable" discharge paragraph**: "By the commitment, every transition that grows `L_R` is a `Nullify`, which adds the single tuple `(b, ∅, {(a, δ(1, #a))})`; its to-span is unit-depth with target `a ∈ A_rel^{Σ'}` (the retractor is deposited at `a` in the self-emit case, or `a` pre-exists in `A_rel^Σ ⊆ A_rel^{Σ'}` in the P1 case…)."

**Problem**: The induction enumerates exactly two cases for the Nullify target — *self-emit* (`a = a_emit(Σ, d_retr)`) and *P1* (`a ∈ A_rel^Σ`) — and asserts `a ∈ A_rel^{Σ'}`. It never shows these are exhaustive. They are not. `Nullify(Σ, d_retr, a)` is gated only by **P0** (`d_retr ∈ dom(Σ.M)`); P1 is explicitly demoted to a "scope condition," not a precondition (and Step 4 of the Worked Sketch exercises a call with P1 false). So a layer caller may invoke `Nullify(Σ, d_retr, a)` with `a ∉ A_rel^Σ` **and** `a ≠ a_emit(Σ, d_retr)` — e.g. a ghost address. The emitted retraction tuple then carries a to-span target `a ∉ A_rel^{Σ'}` (the only new key is the emitter `e ≠ a`), directly violating the unit-depth discipline's `t ∈ A_rel^Σ` clause. The induction silently presumes the third case cannot occur.

This is not cosmetic. The `t ∈ A_rel^Σ` clause is load-bearing in **wp Case 2**: "every pre-existing `L_R^Σ` tuple has a unit-depth to-span `{(b, δ(1, #b))}` … the fresh `a` is prefix-incomparable with every such `b` by … R0a." The R0a antichain argument needs `b ∈ dom(Σ.L)`. A concrete counterexample: take `b = b_L(d) = [d.0.s_L]`, the link sub-allocator *anchor*, which is a `zeros = 3` ghost link address never emitted into `dom(Σ.L)`. `Nullify(Σ, d_retr, b_L(d))` is a legal layer call. Its to-coverage is `{t : b_L(d) ≼ t} ⊇ A_L(d)` — the entire link sibling stream, including every *future* emission at `d`. Any subsequent `Emit_K(Σ', d, F, G)` is then born nullified, falsifying wp Case 2's "no pre-existing retraction covers the fresh `a`." The same ghost-target call also falsifies R-Scope's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`, since the intersection becomes the whole on-chain subtree.

**Required**: Make the case split exhaustive by constraining the operation, not the proof. Add a Nullify precondition `P1 ∨ (a = a_emit(Σ, d_retr))` (the target must be an existing link address or the call's own self-emit address), or otherwise forbid retraction targets outside `A_rel`. Then re-derive the discipline induction, wp Case 2, and R-Scope under the strengthened precondition. If unrestricted (ghost-prefix) retraction targets are intended to be permitted, the unit-depth discipline must drop `t ∈ A_rel^Σ` and wp Case 2 must be re-proved without it (and will not hold as stated).

### Issue 2: R-Scope is asserted of the Nullify *operation* but proved only on the `a ∈ A_rel^Σ` sub-domain

**ASN-0086, R-Scope**: "for any `a ∈ A_rel^Σ` … the `→`-step taken by `Nullify(Σ, d_retr, a)` … gives `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`."

**Problem**: R-Scope is the named "single-tuple scope" guarantee, but its domain is `a ∈ A_rel^Σ`, whereas `Nullify` accepts targets outside that set. The self-emit case (`a = a_emit`, `a ∉ A_rel^Σ`) is patched only later, inline in wp Case 1 ("R-Scope's domain `a ∈ A_rel^Σ` does not cover this `a`, but the conclusion does, via R0a directly"). A reader reaching for "Nullify has single-tuple scope" gets a lemma that does not cover all invocations of the operation it names, and (per Issue 1) the uncovered ghost-target case makes the conclusion *false*, not merely unproved.

**Required**: After fixing the Nullify precondition (Issue 1), restate R-Scope over the full admissible target domain (`P1 ∨ self-emit`) and fold the self-emit branch into the lemma rather than into the wp narrative, so the scope guarantee is co-extensive with the operation.

### Issue 3: Properties table over-narrates; "= X + Y + Z" dependency inventories accrete in structural slots

**ASN-0086, "Properties Introduced" table** (anti-bloat classifier): rows restate full lemma bodies — e.g. R0: "over →*-reachable Σ, for every caller-supplied home `d ∈ dom(Σ.M)`, emission allocates an address with two explicit postconditions — *fresh* against `dom(Σ.L)` and *on-chain* in `A_L(d)`, homed at `d` — in both the first- and subsequent-emission branches, yielding a →*-reachable post-state Σ'" — and several rows append upstream-dependency inventories (R5: "(= L1 + L1b + OrdinalDisplacement + T12 + PrefixSpanCoverage + L4(c) + L13)"; R-Scope: "(= R0a antichain + K.λ freshness + P1 + L12a)").

**Problem**: A summary table's slot is a one-line pointer; here it carries re-narrated statements and ingredient lists that duplicate the proof bodies. This is exactly the use-site/derivation-inventory accretion the `review-mode.anti-bloat` classifier warns compounds across cycles.

**Required**: Reduce each row to a one-line statement pointer. Drop the `= A + B + C` ingredient lists (the proof bodies already carry the derivations) or keep at most the single defining reduction where a property is a genuine alias (e.g. R2 = L12).

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity model for `Emit` vs `Observe`
The Open Questions raise whether `Emit` must be atomic w.r.t. concurrent `Observe` and the consistency model for observing `A_K` transitions. This note correctly works in ASN-0093's sequential-atomic transition model; a concurrency semantics is a future ASN, not a defect here.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
Multi-arity links (`|Σ.L(a)| > 3`) inhabit `A_rel` but index no `L_K`. Whether they define binary projections or higher-arity relations is genuinely new territory, appropriately deferred.

VERDICT: REVISE
