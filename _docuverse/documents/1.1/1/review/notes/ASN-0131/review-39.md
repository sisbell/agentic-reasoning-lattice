# Review of ASN-0131

This is a strong, rigorous note. The definition is clean, the proofs that carry weight (union-distributivity, the contraction weakest-precondition RE-CWP, the retraction analysis, the worked instance) are correct and shown in full, boundary cases are explicitly enumerated (empty image, no addressable links, empty endset slot), and the wp analysis is non-trivial. Soundness/completeness are correctly characterised as immediate reads of the comprehension rather than hand-waved theorems. I verified the worked example's `coverage(e₃) ∩ dom(Σ.C) = ∅` field-agreement argument, the RE-CWP derivation against D-CWP, the RE-SEL = `findlinks_V ∩ addressable` factoring, and the retraction forward/backward halves (R6a + R-Scope) — all hold. I checked the prose for the accretion patterns the anti-bloat classifier targets; the dense passages (the ASN-0086 bridge, the per-transition stability walkthrough) are load-bearing rather than meta-prose, and I did not have to skip past justification to follow a claim. The standing-assumption bridge in particular — including its "populated-arrangement states the empty-arrangement layer never reaches" clause — is the *crux* of why ASN-0086's `Σ.L`-only lemmas transfer to ASN-0047, not over-elaboration.

One substantive defect remains.

## REVISE

### Issue 1: The insert/delete stability rests on an asserted cross-model lift and a depth-restricted delete citation, presented generally

**ASN-0131, "Stability: the answer as the document is edited," under "Under editing of the queried document"**: "ASN-0082 models these primitives over a `(C, M)` state with no link store, framing only the content store (I3-C, D-I); but each is an arrangement edit touching `Σ.M(d)` alone, so lifted to the full `(C, L, E, M, R)` state it frames `Σ.L`, `Σ.E`, and `Σ.R` as well — the link store, in particular, is left fixed (`L' = L`)... an insertion at `p` of width `n` carries the content at every position `v ≥ p` up to `shift(v, n)` (I3), and a deletion carries the content lying above the removed span back down (D-SHIFT)."

**Problem**: Two gaps, both in this subsection's invocation of ASN-0082.

(a) *The lift is asserted, not derived.* ASN-0082's I3/D-SHIFT are defined over a `(C, M)`-only state and prove frame conditions only for `C` (I3-C: `dom(C') = dom(C)`; D-I: `Σ'.C = Σ.C`). The note extends them to the full `(C, L, E, M, R)` state and asserts the new frame clauses `Σ.L`, `Σ.E`, `Σ.R` are framed. This is plausible — an M-only edit ought to frame everything else — but it is an extension of a foundation operation beyond its defined model, stated without derivation. The retraction- and emission-stability arguments depend on `addressable`/`Avail` being fixed across these edits, so the `L' = L` clause of the lift is load-bearing.

(b) *The delete citation is depth-restricted but presented generally.* ASN-0082's D-SHIFT (and the underlying Contraction) carries the precondition `#p = 2` — it is established only for depth-2 text positions. ASN-0082's insert (I3) is general (`#p ≥ 2`). The note presents insert and delete symmetrically and reasons about "a delete reaching *into* `W`" and the "pure loss" gap case for a general content region `W ⊆ s_C`, whose common depth `m_{s_C}` may exceed 2 (S8-depth, S8a give only `m_{s_C} ≥ 2`). At depth `m > 2` the cited D-SHIFT does not apply, so the delete half of the shift analysis is foundation-validated only at depth 2 — an asymmetry with the insert half that the note does not flag. (The worked instance is depth-2, which masks the gap.)

**Required**: Either restrict the shift-based *delete* discussion to depth 2 (matching D-SHIFT's `#p = 2` precondition), or — cleaner — note that D-SHIFT is the depth-2 realization and that the stability conclusion RE-EDIT actually needs (`addressable`/`Avail` fixed, only the image moves) follows from the shared M-only frame of *any* arrangement edit on `Σ.M(d)`, the same frame the K.μ movers carry, rather than from D-SHIFT's specifics. State the cross-model lift explicitly as that extension (M-only ⟹ frames `L`, `E`, `R`), or ground it.

## OUT_OF_SCOPE

The seven Open Questions appropriately defer the genuinely new territory (whole-endset vs touching-spans surfacing, multiplicity preservation, V-rendered answers, intersection-distributivity given non-injective arrangements, non-co-resident link stores, type-slot-against-content, link-subspace regions). The note also keeps clean of the listed out-of-scope operations: it explicitly distinguishes RE's identity-withholding answer from FINDLINKSFROMTOTHREE ("there is no four-set request here differentiating slot from slot") and from link counting/enumeration, and cites rather than rebuilds ASN-0127's image machinery and existence/discovery taxonomy. No scope trespass to flag.

VERDICT: REVISE
