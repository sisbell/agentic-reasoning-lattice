# Review of ASN-0068

This is a rigorous note. The CV-MAX existence/uniqueness proof is sound (the right/left-walk construction, the lockstep-offset δ argument, and the offset-uniqueness via T3 all check out), the worked examples compute correctly (verified Examples 1, 4, 5 against the arrangements), and CV-FIN's injective-map bound is valid. No mathematical errors found. Foundation citations (ASN-0034/0036/0047/0053/0058) are used correctly; no non-foundation cross-references. The findings below are confined to the anti-bloat patterns the classifier asks for.

## REVISE

### Issue 1: Rationale-around-precondition in CV-IN
**ASN-0068, CV-IN**: "A common subspace identifier `S ∈ {s_C, s_L}` governs both restrictions — common because cross-subspace I-addresses are disjoint (`dom(C)` vs. `dom(L)`, L14, ASN-0047), so a mixed input could never yield a coincident I-address."
**Problem**: The precondition need only *state* that a single common `S` governs both restrictions. The "common because … so a mixed input could never yield a coincident I-address" clause is rationale for why the constraint is needed — the exact "new prose around a precondition explains why it is needed rather than what it says" pattern the anti-bloat lens targets.
**Required**: State the requirement (common `S`) without the embedded justification; the disjointness argument, if wanted at all, is already carried structurally by the `s_L` claims (CV-LINK-DEGEN).

### Issue 2: Misattributed consequence grouping for CV-IDENT
**ASN-0068, "The Correspondence Relation"**: "*The relation is determined entirely by current state*. The expression depends only on `M(d_a)`, `M(d_b)`, and the restrictions; no history is consulted… We name two consequences." — followed by CV-IDENT and CV-PROV-FORGOTTEN.
**Problem**: CV-PROV-FORGOTTEN genuinely follows from "no history consulted." CV-IDENT (correspondence is I-address equality, not value equality) does **not** follow from state-determination — it follows from the defining equation ranging over I-addresses. The scaffolding presents two claims as consequences of a premise that supports only one of them.
**Required**: Re-attribute CV-IDENT (it is a consequence of the defining equation `M(d_a)(v_a)=M(d_b)(v_b)`, established earlier in the same section), or drop the "two consequences of state-determination" framing.

### Issue 3: Undeveloped application flourish in the opening
**ASN-0068, opening (third paragraph)**: "it inherits from the addressing scheme the same atomic, identity-grounded discipline that underwrites attribution, royalty flow, and link survival."
**Problem**: "royalty flow" and "link survival" are downstream applications named but not developed or used anywhere in this note. This is essay flourish in a motivational slot — the kind of prose a precise reader skips past.
**Required**: Trim to the load-bearing claim (correspondence is exact and structural, grounded in I-address identity); drop the application name-drops.

## OUT_OF_SCOPE

### Topic 1: Replication open question
**ASN-0068, Open Questions**: "Under what conditions must `compareversions` return identical results across replicated copies of the docuverse…"
**Why out of scope**: Replication / inter-server (BEBE) is declared out of scope for this ASN. As a forward-looking open question this is acceptable (it does not claim coverage), but it should not be developed into a claim here; flagging so the boundary stays explicit.

VERDICT: REVISE
