# Review of ASN-0075

I checked the four core lemmas (D-WIT, D-EXH, D-DISCR, D-NEED), the operation definition and its disjointness, the wp analysis, the worked example, and the subspace/identity/origin claims. The mathematics is sound: D-WIT correctly routes through S3★/L14/P4★, D-EXH's "impossible row" is properly excluded, the two D-DISCR histories genuinely agree on `(C, L, E, M)` while diverging on `R`, and the worked example computes to `({b}, {c})` as claimed. I found no correctness gap. The issues below are the forward-reference/meta-prose accretion the note's classifier flags.

## REVISE

### Issue 1: Observationality used before it is stated (defer-to-downstream)
**ASN-0075, "The SHOWDELETIONS Operation" (wp paragraph) and "Vacuity of both report halves"**: "SHOWDELETIONS reads state and returns a result without modifying any component (its observational frame is formalised as D-OBS)" and later "Since SHOWDELETIONS only reads state (D-OBS) ...".
**Problem**: The wp derivations depend on the operation being observational, but the formal claim D-OBS appears several sections later. Two separate sections forward-defer to the same downstream location to license a fact they consume — exactly the accretion pattern named for this note.
**Required**: State the observational fact (D-OBS) before the wp analysis that relies on it, or carry the wp analysis after D-OBS, so no section consumes observationality on a forward promise.

### Issue 2: Defensive "not an additional postcondition" meta-prose
**ASN-0075, "Non-emptiness of one report half"**: "The last conjunct (presence in `d_B`) is what makes the report *recoverable* in the sense of D-IDENT — every reported deletion has a concrete witness in the partner document. This is not an additional postcondition; it is implicit in the definition of `DeletedFromAWithB`."
**Problem**: The closing sentence does not advance the wp computation; it defends the prose against a misreading ("don't take this as a new postcondition") and forward-references D-IDENT for interpretive color. This is meta-prose the reader must step past to follow the derivation.
**Required**: Delete the defensive sentence. The wp formula already shows the third conjunct `a ∈ ran(M(d_B))` is part of the unpacked definition; no disclaimer is needed.

### Issue 3: Independence-from-hypothesis aside in the disjointness argument
**ASN-0075, "Definition (SHOWDELETIONS)"**: "The two halves are necessarily disjoint, and the disjointness is unconditional — it needs neither D-EXH nor any composite-boundary hypothesis."
**Problem**: The clause after the dash justifies what the argument does *not* require rather than carrying the argument. The actual proof (contradictory range-membership on `M(d_B)`) stands on its own; the "needs neither X nor Y" framing is defensive scaffolding.
**Required**: Drop the "it needs neither D-EXH nor any composite-boundary hypothesis" clause and state the disjointness directly from the contradictory `M(d_B)`-membership conditions.

## OUT_OF_SCOPE

### Topic 1: Invocation at non-composite-boundary (mid-composite) states
**Why out of scope**: D-BOUND axiomatizes that SHOWDELETIONS is invoked only at composite boundaries, which is what D-WIT/D-EXH need (P4★ holds there). The behavior of a hypothetical mid-composite invocation belongs to a consistency/concurrency ASN (already raised in the Open Questions), not a revision here.

### Topic 2: Link-subspace deletion reporting
**Why out of scope**: D-SUBSP correctly shows cross-document deletion comparison is structurally meaningful only in `s_C`; a per-document link-deletion analysis is genuinely new territory, not a defect in this note.

VERDICT: REVISE
