# Review of ASN-0091

## REVISE

### Issue 1: Realization headline overstates uniformity of the K.μ~ mechanism

**ASN-0091, "REARRANGE_K Realises the Abstract Class" (opening sentence)**: "REARRANGE_K (the cut-sequence operation of ASN-0084) is one concrete realisation of the abstract Vstream-only class via ASN-0047's K.μ~ operation."

**Problem**: The collapse case (developed in the preceding section) establishes that when the affected-range value sequence is fixed by the cut-induced rotation/swap, K.μ~ is *not* the realiser — its admissibility clause (ii) `M'(d) ≠ M(d)` fails, and the transition is the identity (empty composite), realised by SequentialTransitionAxiom's reflexive closure rather than by K.μ~. REARRANGE_K is defined wherever R-PRE holds (it is not given a non-triviality precondition), so the collapse case is a genuine, reachable input. The realisation of REARRANGE_K therefore splits across two distinct mechanisms — K.μ~ in the non-trivial case, the identity composite in the collapse case — yet the section's framing names a single mechanism "via K.μ~." The body resolves this, but the headline claim is literally not uniform over REARRANGE_K's domain.

**Required**: Qualify the opening claim to scope "via K.μ~" to the non-trivial case, and name the identity/empty composite as the realiser for the rotation/swap-invariant (collapse) case, so the realisation statement is uniform over R-PRE-admissible inputs.

### Issue 2: K.μ~ admissibility clause (iii) not explicitly discharged for REARRANGE_K's π

**ASN-0091, "K.μ~ Admissibility Clauses"**: the subsection discharges the abstract RA-* clauses *from* K.μ~'s definitional clauses, but to use K.μ~ as the realiser one must also verify REARRANGE_K's cut-induced π *satisfies* K.μ~'s admissibility clauses (i)–(v) (ASN-0047).

**Problem**: Clause (iv) subspace-preservation is covered (fact (b)/RE-subpres), clause (v) link-subspace-fixing is covered (RE-sub/non-S branch), clauses (i)/(ii) are covered (RA-adm per-invariant; collapse/non-trivial split). But clause (iii) — π *length-preserving*, `#π(v) = #v` — is never explicitly verified as an obligation on REARRANGE_K's π. It is derivable (cuts are depth-2 by CS4, π maps within a fixed subspace whose common depth m_S is preserved because RA-dom fixes V_S(d) and hence m_S), but the realisation argument leaves this step implicit. A realisation claim that a transition *is* a valid K.μ~ transition must close every admissibility clause.

**Required**: Add the explicit discharge of K.μ~ clause (iii) for REARRANGE_K's π (e.g., from CS4 plus S8-depth invariance of m_S across the transition), completing the forward direction of the realisation argument.

## OUT_OF_SCOPE

### Topic 1: Rearrangement semantics on the link subspace
**Why out of scope**: CS3 fixes the cut subspace at s_C, so REARRANGE_K touches only content; link-subspace reordering is a distinct operation with its own invariants, correctly deferred (Open Question 2).

### Topic 2: Realisation of arbitrary well-formedness-preserving bijections
**Why out of scope**: Whether every admissible π is a finite composition of cut-sequence rearrangements (Open Question 5) is a completeness result for a future ASN, not a defect in this one's abstract-class-plus-one-realiser structure.

VERDICT: REVISE
