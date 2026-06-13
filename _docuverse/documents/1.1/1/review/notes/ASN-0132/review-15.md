# Review of ASN-0132

The operation is a thin, correct layer over ASN-0121: `countlinks_FTT` is the cardinality of the satisfying-addressable set already carved out by `sat`/`addressable`. I checked the logic and found no correctness defects. Well-definedness (finite subset of `dom(Σ.L)`), CN-LOC (locality from FL-LOC), CN-UNIT's four collapses (including the version-refraction reduction via J4's content-only frame), the CN-MONO wp derivation (the `¬(E (b,F',G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` conjunct matching FL-WP(a), collapsing under R0a's discipline), and the worked example all hold — I re-checked the example's arithmetic (`s ⊕ δ(8,8) = 1.0.1.0.1.0.1.13`; `nullified(Σ)={a₂}`; count `=2`; `|addressable|=4`; the `H₂` zero from `d₂ ⋠ d₁`) and it is sound. All cross-references are to foundation ASNs.

The ASN carries the anti-bloat classifier and has already had one trim cycle (CN-LOC/CN-ENUM/CN-SNAP). The remaining findings are residual meta-prose around forward references and a scope-decision restated three times.

## REVISE

### Issue 1: The cost scope-decision is stated three times, and the body answers its own open question
**ASN-0132, "Cost, and the meaning of asking for a number" + final implementation note + Open Question 5**:
- Essay: "But it is *not* a correctness obligation, and we decline to elevate it to a claim, because an alternative implementation that computes the cardinality by materialising the satisfying set and taking its length is *correct as to value*..."
- Implementation note: "It confirms the position taken here: the number is determined by the specification, the price is left to the implementation, and a back end is free to pay full enumeration cost for a cardinality without being wrong."
- Open Question 5: "...and is any such relationship a correctness obligation or only a quality of service?"

**Problem**: "Cost-asymmetry is quality-of-service, not a correctness obligation" is asserted in the essay, restated in the implementation note's closing sentence, and then re-posed as the second half of Q5 — which the body has already settled. This is the defensive-justification + same-thing-twice pattern, compounded by an open question that re-asks a resolved point.
**Required**: State the scope decision once (cost is QoS, not a correctness obligation). Trim the "we decline to elevate it... because..." defense. Hold the implementation note to *what the back end does* (it pays full enumeration cost) without re-arguing the position. Reframe Q5 to ask only the genuinely open part (what cost relationship would let a count serve as a planning primitive), dropping the already-answered "is it an obligation" clause.

### Issue 2: Within-document deferrals accrete, and one is a dangling backward reference
**ASN-0132, CN-DEF / CN-ZERO / CN-ORPHAN**:
- CN-DEF: "(...a matter of cost, taken up in the final section...)"
- CN-ZERO: "A link satisfying `q` but displayed nowhere is still counted (we return to this under CN-ORPHAN)."
- CN-ORPHAN: "This explains, finally, the asymmetry we deferred."

**Problem**: These are navigational pointers, not reasoning. The CN-ORPHAN opener is the worst case: it refers back to "the asymmetry we deferred," but no earlier passage explicitly sets aside an "asymmetry" under that name — the reader cannot locate what was deferred, and the sentence adds nothing the next sentence ("A link can be counted yet not discoverable; the counted *set* is a superset of what any document surfaces...") does not already state directly.
**Required**: Remove the three navigational pointers. Make each point where it lands. In CN-ORPHAN, open directly with the count⊇discovery statement, dropping "This explains, finally, the asymmetry we deferred."

### Issue 3: CN-UNIT's closing synthesis ends on a circular recap
**ASN-0132, "The unit is identity," paragraph after the four cases**: "The four cases share a shape: each rejected unit is an `Σ.M`-quantity or an inside-`touch` quantity, and CN-LOC excludes the former while the existential structure of `touch` absorbs the latter. The count is keyed to identity because the satisfying *set* is keyed to identity."

**Problem**: The first sentence does useful unifying work (naming the two mechanisms). The second restates the section heading ("The unit is identity") as a self-referential conclusion — recap, not advance.
**Required**: Cut the final sentence; the two-mechanism observation in the preceding clause already closes the section.

## OUT_OF_SCOPE

No overreach to report. The ASN correctly confines itself to the count operation: CN-OBT explicitly disclaims delivery ("a separate concern across a separate boundary, out of scope here"), and the cross-regime V-spec/I-address invariant, single-server concurrency, caching, fragmented-identity counting, and federated counts are all left to Open Questions rather than asserted as claims. The boundary is drawn correctly.

META: (none — the ASN specifies an operation and its state-guarantees abstractly; the implementation notes are demarcated and do not constitute the specification.)

VERDICT: REVISE
