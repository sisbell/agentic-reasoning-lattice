# Review of ASN-0042

This note is rigorous to a fault — the proofs are exhaustive, the invariants are individually discharged, and the worked example exercises every property on concrete addresses. The standard "by similarly" / checkmark hand-waves are absent. The findings below are therefore almost entirely the anti-bloat patterns the `review-mode.anti-bloat` classifier asks me to surface: meta-prose, forward-reference accretion, and self-restatement that compound across cycles.

## REVISE

### Issue 1: Forward-reference meta-prose around condition (v)
**ASN-0042, O17b**: "(That this prefix is the next-reachable `next(Σ.B, p, d)` for a B6-valid `(p, d)` is owned by condition (v) of the delegation predicate, not restated here.)"
**Problem**: This is pure division-of-responsibility prose — it advances no claim, it tells the reader which other clause "owns" a fact. It is the named "defers to the same downstream location" pattern: O17b, O18 ("condition (v) fixes `pfx(π') = next(Σ.B, p, d)`"), and Freshness-(v) ("condition (v) fixes `pfx(π') = c_{hwm+1}`") all re-narrate condition (v)'s content from different sections. The explanatory load is scattered across four sites.
**Required**: Delete the parenthetical. State condition (v)'s consequence once (Freshness-(v) is the natural home) and let O17b/O18 cite it without re-explaining.

### Issue 2: Formal-contract slot points back at the body
**ASN-0042, O3, Formal Contract / Postconditions**: "The monotonic-refinement corollary `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` (given `a ∈ Σ.B`) is stated and proved in the body above."
**Problem**: A postcondition slot is for the postcondition, not a pointer narrating where a proof lives. "stated and proved in the body above" is meta-prose in a structural slot.
**Required**: Either list the corollary as a postcondition (`#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))`) or drop the sentence. No back-pointer.

### Issue 3: O7(c) restates its own just-derived conclusion
**ASN-0042, O7, postcondition (c) proof**: "Thus at Σ' the recursive right is discharged: conditions (ii) and (iv) hold because π' is the only newcomer (`Π_{Σ'} ∖ Π_Σ = {π'}`), and (i) is fixed by the choice of `p''`, while (iii) and (v) remain genuine obligations on `p''`."
**Problem**: The two preceding paragraphs already derive (ii) from condition (iv), derive (iv) "independent of the choice of `p''`," and fix (i) "by the choice of `p''`." This summary says the same thing a second time — the "two paragraphs say the same thing in different words" pattern.
**Required**: Remove the summary sentence; the derivation already lands the conclusion.

### Issue 4: O10 construction re-derives a foundation definition
**ASN-0042, O10, Construction**: "By ASN-0040's `next` semantics, when `hwm_0 = 0` … `next` reduces to the field-opening branch `inc(pfx(π), 2) = pfx(π).0.1` …; when `hwm_0 ≥ 1`, the sibling-advance branch yields `inc(pfx(π).0.{hwm_0}, 0) = pfx(π).0.{hwm_0 + 1}` …"
**Problem**: The two-branch case split *is* `next(B, p, d)`'s definition in foundation ASN-0040 (`if children = ∅ then inc(p, d) else inc(max(children), 0)`). Foundation rule says foundation definitions may be used without restating them. Here the branch semantics are restated to re-derive `zeros(a')`.
**Required**: Invoke `next(Σ.B, pfx(π), 2)` directly; carry only the one fact O10 actually needs — `zeros(next(...)) = zeros(pfx(π)) + 1` via B5/B5a — without re-narrating both `inc` branches.

### Issue 5: Editorial essay in a structural note
**ASN-0042, Structural Provenance (closing)**: "Provenance is not a right that can be exercised or waived — it is an inalienable structural fact. The address encodes provenance; ownership encodes authority. Under the system as specified, these coincide."
**Problem**: This is essay content, not reasoning that advances a claim — the surrounding Nelson/Gregory citations already ground O6. "inalienable structural fact" editorializes; the precise reader skips it to reach the next claim.
**Required**: Cut to the load-bearing observation (O6's biconditional makes `ω` a function of `acct` alone). Keep the Nelson "you always know where you are" citation as design grounding; drop the aphorism.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer reconciling O6 and O2
The divergence between inalienable provenance (O6, address-encoded) and mutable effective ownership (O2) once transfer is permitted is genuinely new territory — and is already correctly parked in Open Questions. No action needed; flagging only to confirm the note does not silently assume non-transfer is permanent.

VERDICT: REVISE
