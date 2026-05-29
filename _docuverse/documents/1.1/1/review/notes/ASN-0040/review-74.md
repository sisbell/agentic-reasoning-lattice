# Review of ASN-0040

## REVISE

### Issue 1: B6 necessity for condition (i) rests on an unstated "injectivity" property
**ASN-0040, B6 necessity, sub-case (b):** "Condition (i) excludes such parents here not to avoid a T4 violation but to keep the namespace map injective: were ([1, 0], 1) admitted, two distinct namespaces would share their entire stream."
**Problem**: The necessity direction concedes that at the d = 1 trailing-zero case condition (i) is *not* necessary for T4 of the stream (S2 shows the stream is fully valid), and props up the conclusion on "the namespace map injective." But injectivity of the map (p, d) ↦ S(p, d) is never stated as a property of this ASN. B7 establishes only *disjointness over B6-valid pairs* — and trailing-zero parents are excluded from B6 by (i) — so B7 cannot speak to the relaxed setting where ([1, 0], 1) would be admitted. The justification therefore appeals to a desideratum the specification does not define. A precise reader cannot check "(i) is necessary" against any stated obligation.
**Required**: Either (a) state namespace-map injectivity as an explicit property of the ASN (S2 is the witness for its failure under relaxation) and cite it at this step, or (b) drop the children-T4 necessity argument for the d = 1 case and exclude trailing-zero parents directly: a trailing-zero tumbler fails T4 (`t_{#t} ≠ 0`), so it is not a valid address and (i) excludes it at the parent level without any injectivity detour.

### Issue 2: Atomicity (B4) is asserted and re-glossed redundantly
**ASN-0040, B4 / Bop:** "This indivisibility is a primitive structural assumption on Σ ... not a property we derive. The read of `s.B ∩ S(p, d)` is exact because it consults the precondition state s by definition of the operation."
**Problem**: B4 atomicity now appears in the B4 property body, the Bop `STRUCTURAL` line, the Bop contract's "Structural assumptions on Σ," and B8's preconditions. The B4 prose adds a "why we do not derive it" gloss and restates the read-against-precondition semantics already fixed by the Bop postcondition. This is meta-prose the reader must skip to reach the claim — exactly the accretion the anti-bloat classifier targets.
**Required**: State B4 once as the structural assumption; remove the "not a property we derive" commentary and the duplicated read-semantics sentence (already implied by `POST: s'.B = s.B ∪ {next(s.B, p, d)}`).

### Issue 3: B6 necessity is over-exampled
**ASN-0040, B6 necessity, sub-case (a):** three worked micro-examples (`[0,1,2]`, `[0]`, `[1,0,1,0,1,0,1,0,1]`) are threaded through one sub-case alongside the d = 1 tangent.
**Problem**: Concrete examples are welcome, but stacking three inside a single necessity sub-case forces the reader to re-derive the same propagation mechanism (TA5(b) preserves the defect; B5/B5a fix the zero count) three times. The argument is the same in each; only the defect class differs.
**Required**: Keep one representative example for the positional-defect class and one for the count-violation class; the singleton `p = [0]` and the leading-zero `[0,1,2]` collapse to a single positional witness.

## OUT_OF_SCOPE

### Topic 1: B3 ghost-validity forward requirement
**Why out of scope**: B3 imposes a constraint on a future `Occupied` predicate rather than defining content storage here. Content storage is explicitly deferred, and B3 is correctly framed as a forward requirement, so it is not a defect — noted only to confirm it was read and is not flagged as drift.

VERDICT: REVISE
