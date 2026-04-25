# Regional Review — ASN-0034/Divergence (cycle 5)

*2026-04-24 05:59*

### NAT-wellorder still carries the symbol-provenance paragraph that was systematically removed from sibling axioms
**Class**: REVISE
**Foundation**: (internal)
**ASN**: NAT-wellorder, paragraph between the formal statement and the Formal Contract: "The axiom body invokes the non-strict companion `≤`, which is not a primitive of ℕ — it is *defined* in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`."
**Issue**: This is the same "axiom body invokes symbol X, defined in dependency Y" pattern flagged in the prior cycle for NAT-addcompat, NAT-cancel, and NAT-discrete and removed from each. NAT-wellorder was not named in that finding and the paragraph survived. The Depends citation already states the same content with use-site detail ("supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`), used in the inner quantifier `(A n ∈ S :: m ≤ n)` that characterizes `m` as a least element of `S`"). With the parallel paragraphs gone from the three other NAT-* axioms, this one stands alone as residual reviser-drift defense of the Depends list.
**What needs resolving**: Remove the symbol-provenance sentence. The Depends citation already names the supplied symbol and its use site; the axiom body and least-element prose can sit directly against the Formal Contract.

### Divergence Postconditions slot carries "tight bounds" meta-commentary
**Class**: REVISE
**Foundation**: (internal)
**ASN**: Divergence, *Formal Contract → Postconditions*: "in case (ii), `divergence(a, b) = #a + 1` in sub-case (ii-a) (where `#a < #b`) and `divergence(a, b) = #b + 1` in sub-case (ii-b) (where `#b < #a`) — **the exact per-case values serve as tight bounds**; `divergence(a, b) = divergence(b, a)` for all `a ≠ b`."
**Issue**: The trailing clause "the exact per-case values serve as tight bounds" is annotation about the strength of the postcondition rather than a postcondition itself. The two equalities `= #a + 1` and `= #b + 1` already are the postconditions; calling them "tight bounds" inside the Postconditions slot is meta-commentary on what the slot contains. The same paragraph also dual-purposes the case (i) line ("the designating description bounds the returned index by `1 ≤ divergence(a, b) ≤ #a` and `divergence(a, b) ≤ #b`") — bounds derived from the Definition's conjuncts, repeated here as if they were independent postconditions. The slot should state what callers can rely on, not editorialize about how tight those guarantees are.
**What needs resolving**: Drop the "tight bounds" gloss. State the postconditions in case (ii) as the equalities `divergence(a, b) = #a + 1` (sub-case ii-a) and `divergence(a, b) = #b + 1` (sub-case ii-b) without the framing clause. Decide whether the case (i) bounds line is a postcondition (state it as one, without the "designating description bounds" framing) or a derived consequence already implicit in the Definition (drop it).

VERDICT: REVISE
