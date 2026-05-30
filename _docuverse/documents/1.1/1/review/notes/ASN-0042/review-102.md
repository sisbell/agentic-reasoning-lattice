# Review of ASN-0042

## REVISE

### Issue 1: Condition (iv) given two contradictory characterizations in O7(c)
**ASN-0042, Delegation / O7 postcondition (c) proof**: "Conditions (iii) and (iv) constrain the target prefix p'', not the delegator, and are obligations on the choice of delegate prefix. Thus at Σ' conditions (i), (ii), and (iv) are discharged for π' as delegator..."
**Problem**: Within two consecutive sentences condition (iv) is placed in two incompatible buckets — first as "an obligation on the choice of delegate prefix" (grouped with (iii)), then as "discharged for π' as delegator." It cannot be both. In fact (iv) — `¬(E π'' ∈ Π_{Σ'} : p'' ≺ pfx(π''))` — is *automatically* satisfied at Σ' for **any** p'' ≻ pfx(π'): any π'' ∈ Π_Σ extending p'' would extend pfx(π'), contradicting the original delegation's (iv), and π' itself does not extend p''. So only (iii) (`zeros(p'') ≤ 1`) genuinely constrains the target; (iv) is discharged at Σ' regardless of p''.
**Required**: State that (i), (ii), (iv) are discharged at Σ' independent of the choice of p''; that (iii) constrains the target prefix; and that only (v) is a genuine per-state obligation. Remove (iv) from the "obligations on the choice of delegate prefix" grouping.

### Issue 2: Per-state (v) caveat restated redundantly in O7(c)
**ASN-0042, O7 postcondition (c) body and Formal Contract**: the body says condition (v) "is left as a per-state obligation on p''," then immediately "Postcondition (c) thus asserts the *right*... conditional on... p'' being both fresh and next-reachable," and the Formal Contract postcondition (c) repeats "condition (v) is *not* asserted at Σ' for arbitrary p'' but remains a per-state obligation on p''."
**Problem**: The same caveat is made three times in different words — the "two paragraphs say the same thing" accretion pattern the anti-bloat classifier targets.
**Required**: State the (v) per-state obligation once (in the body), and let the Formal Contract reference it rather than re-prove it.

### Issue 3: Decorative cross-references to O17b's "single allocation point"
**ASN-0042, O10 body, O10 unilateral discussion, and DelegatorAllocatesPrefix closing**: "This is exactly the abstract image of the single allocation point corroborated at O17b, which advances unilaterally past delegated slots"; "The single allocation point corroborated at O17b runs under the session's own account-tumbler authority..."
**Problem**: The O17b implementation motif ("single allocation point") is re-invoked approvingly in at least three downstream slots where it advances no claim — these are decorative back-links, not steps in any derivation. This is the "multiple paragraphs defer to the same location" accretion pattern; a reader must skip past them to follow the proofs.
**Required**: Keep the implementation corroboration at O17b; drop the repeat invocations in O10 and DelegatorAllocatesPrefix, or fold each into a single trailing sentence if the link is load-bearing.

### Issue 4: Notation well-definedness paragraph is defensive meta-prose
**ASN-0042, Definition (delegated)**: "This reading is well-defined: O15's membership clause places π' ∈ Π_{Σ'}, so pfx_{Σ'}(π') exists; and O13 (PrefixImmutability) fixes it for all subsequent states, so the choice of Σ' as the evaluation state is immaterial to the value."
**Problem**: This justifies *why* the two-state reading of `pfx(π')` is well-formed rather than stating the reading itself. The load-bearing content — "delegator prefix read at Σ, delegate prefix at Σ'" — is already stated in the next sentence; the well-definedness gloss is the "why the notation is needed" accretion pattern.
**Required**: Reduce to the operative convention (delegator prefix at Σ, delegate prefix at Σ'); the immutability justification can be a parenthetical citation to O13 rather than a standalone defense.

## OUT_OF_SCOPE

### Topic 1: ASN-0040 registry well-formedness in the worked example
**Why out of scope**: The worked example deliberately defers B1-contiguity/B6-depth of the seeded registry to ASN-0040 ("well-formedness... is ASN-0040's responsibility"). The seed ordering (e.g., children of `[1,0,2]` baptized while `[1,0,2]` is unbaptized) is admissible under ASN-0040's stream semantics and is not an ownership-model obligation. No revision needed in this ASN.

META: (none — the ASN stays squarely in ownership-of-addresses territory; the findings are local imprecision and prose accretion, not drift.)

VERDICT: REVISE
