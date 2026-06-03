# Review of ASN-0091

## REVISE

### Issue 1: S5 is discharged with a justification that does not justify it

**ASN-0091, "Per-Invariant Discharges (ASN-0036 Foundation Invariants)", S5 bullet**: "S5 (UnrestrictedSharing). Existential about states trivially preserved across a transition that admits arrangements with shared I-addresses (RA-π's bijectivity allows distinct V-positions to map to the same I-address)."

**Problem**: S5 (ASN-0036) is `(A N ∈ ℕ :: (E Σ :: Σ is the initial state of a model of S0–S3 ∧ ...))` — an existential over the *existence of some model's initial state*. It is a fixed theorem of the model class, not a per-state predicate that could be gained or lost across a transition. Whether the current REARRANGE step's π admits shared I-addresses is irrelevant to S5's truth: even a transition producing no sharing whatsoever would leave S5 intact, because S5 never speaks about the current state Σ. The parenthetical reasoning therefore ties preservation to a fact (RA-π allows sharing) that has no bearing on the claim — a non-sequitur of exactly the "justification that doesn't justify" kind. The conclusion (S5 holds at Σ') is correct, but for the wrong reason.

**Required**: Discharge S5 as a state-independent theorem — analogous to the RE-origin treatment ("origin is a function on tumblers, not state, so it has no temporal dimension at all") — rather than as a transition-relative preservation. Remove the appeal to RA-π's bijectivity.

### Issue 2: RA-adm's quantifier is ill-typed for non-per-state foundation results

**ASN-0091, abstract class definition (RA-adm)**: "every foundation invariant satisfied by Σ is satisfied by Σ' (RA-adm)"

**Problem**: The phrase "satisfied by Σ" presupposes that every foundation invariant is a state predicate. Several are not: S5 (existential over models), T0(a)/T0(b) (unboundedness of the address space), and the composite-boundary properties P4★/P4a/P7a (which the ASN itself must handle outside the per-state frame — witness the dedicated "P4a Handling" subsection acknowledging "RA-frame does not discharge it directly"). For these, "satisfied by Σ" has no state-relative content, so RA-adm as written is either vacuous or ill-typed on those conjuncts. This is the same root cause as Issue 1: the discharge machinery treats the foundation-invariant set as uniformly per-state.

**Required**: Restate RA-adm to range over *per-state* foundation invariants, with composite-boundary properties (P4★, P4a, P7a) and state-independent theorems (S5, T0(a/b)) called out and discharged by their own arguments (as is already done, partially, for P4a and S5). This makes explicit that RA-adm is a per-state-invariant-preservation clause, not a blanket "all foundation results" clause.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN fixes the cut subspace at S = s_C (CS3) and correctly relegates link-subspace reordering to an open question. A rearrangement operation on the link subspace, and the invariants it must preserve, is new territory for a future ASN, not an error here.

### Topic 2: Upper bound on run-decomposition cardinality growth
**Why out of scope**: RE-frag establishes that fragmentation occurs; quantifying the maximum cardinality increase per invocation is a distinct analytical question, correctly listed under Open Questions.

VERDICT: REVISE
