# Review of ASN-0091

## REVISE

### Issue 1: Meta-prose framing in "State-Component-Only Invariants"

**ASN-0091, State-Component-Only Invariants**: "The binary transition invariants — those of the form `(A Σ → Σ' :: …)`, relations on the *pair* of states rather than per-state predicates, and so outside the per-state foundation list RA-adm discharges above — are discharged by a single **transition-satisfaction** principle: every such invariant constrains one or more state components … and RA-frame fixes each of those components *with equality* … The class — ASN-0036's S0, S1; ASN-0047's P0, P1, P2, L12, P3; ASN-0093's M1, C0 — is therefore discharged uniformly by RA-frame, with no per-invariant argument required."

**Problem**: This note carries `review-mode.anti-bloat`. The load-bearing content here is small: "RA-frame fixes C, L, E, R, dom(M) with equality, so every monotonicity/value-preservation invariant over those components holds trivially; this discharges S0, S1, P0, P1, P2, L12, P3, M1, C0." Everything else — the "transition-satisfaction principle" naming, the meta-classification of invariant shape ("relations on the *pair* of states rather than per-state predicates, and so outside the per-state foundation list…"), and the defensive "with no per-invariant argument required" — is framing the reader must read past to reach the actual discharge. The principle is asserted to cover "the binary transition invariants" *as a class*, but completeness of the enumerated members is never argued — so the meta-framing buys generality it doesn't establish, while the enumeration does the real work.

**Required**: Collapse to the substantive sentence: RA-frame fixes the named components with equality, discharging the listed invariants. Drop the "transition-satisfaction principle" coinage, the pair-vs-per-state meta-classification, and "with no per-invariant argument required." If the list is meant to be exhaustive over binary transition invariants of the foundation, say so as a checked enumeration rather than as a general principle.

---

Everything else I checked holds up. Spot-verified: the L-chain successor identification (`shift(x,1) = inc(x,0)` via TA5-SigValid on T4-valid chain elements) and its use in the coalescence/equality witnesses; the RE-trans (iii) routing through CL-OWN + S3★ to land `a ∈ dom(Σ.C)` before invoking C2; the collapse-case realiser (`Σ' = Σ` via the empty sequence when K.μ~ clause (ii) fails); the RE-proj uniformity across the two witnesses in the non-uniqueness example; and the boundary handling (empty/identity/collapse, start/end cuts, strict-ordering forcing `w_α, w_β, w_μ ≥ 1`). The five worked examples each exercise a distinct mechanism (3-cut, 4-cut μ-displacement, in-S exterior fixity, within-block bijection freedom, net-effect collapse) and are not redundant.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics

**Why out of scope**: Posed correctly as an Open Question. REARRANGE_K fixes the cut subspace at `s_C` (CS3), so RE-sub leaves `s_L` verbatim; defining a reordering operation *on* the link subspace is new territory, not a gap in this ASN.

### Topic 2: Reconstitution of a same-source span split across a cut

**Why out of scope**: RE-trans establishes per-fragment origin preservation but explicitly declines to assert joint reconstitution; this is flagged as an Open Question and belongs to a future ASN.

VERDICT: REVISE
