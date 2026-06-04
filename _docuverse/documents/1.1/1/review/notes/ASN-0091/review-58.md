# Review of ASN-0091

## REVISE

### Issue 1: The RA-adm "three-layer" discharge routes through an RA-adm-dependent lemma (circular), and is partly redundant

**ASN-0091, "REARRANGE_K Realises the Abstract Class" (RA-adm row of the abstract-clause table and the three discharge paragraphs)**: "discharged in three layers: shape package (from RA-dom), subspace preservation (RE-subpres), and the remaining per-state invariants (via ExtendedReachableStateInvariants)." Yet RE-subpres is "derived earlier from RA-π, RA-frame's Σ'.C = Σ.C and Σ'.L = Σ.L, pre-state S3★, **RA-adm** (for both post-state S3★ and post-state S3★-aux), and foundation L14."

**Problem**: Layer 2 of the discharge of RA-adm cites RA-adm (post-state S3★, S3★-aux) in its own derivation — circular when the goal is to *establish* RA-adm for REARRANGE_K. Separately, layer 3 (ExtendedReachableStateInvariants) is stated to discharge "the full per-state invariant package," which already includes S3★ and S3★-aux; that makes layer 2 redundant, and subspace preservation is in any case discharged constructively by admissibility clause (iv) ("Discharged from the cut-sequence construction alone"). The layering thus contains both a circular citation and a redundant layer.

**Required**: Discharge RA-adm for REARRANGE_K solely via the constructive routes (clause (iv) branch structure of R-PPERM/R-SPERM, plus ExtendedReachableStateInvariants), and present RE-subpres as a *downstream consequence* of RA-adm rather than as a layer that establishes it. Remove the redundant layer or state precisely what layers 1–2 add beyond layer 3.

### Issue 2: Ordering/routing-justification meta-prose around RA-dom's source

**ASN-0091, "Shape package (constructive, from RA-dom)"**: "RA-dom is supplied *directly* as the domain clause of ASN-0084's PivotPostcondition/SwapPostcondition — not via ASN-0047's K.μ~-FIX — so these discharges consult neither pre-state S3 nor pre-state S8, and remain derivable at any unified-state pre-state, including those populating the link subspace where the ASN-0036 forms of S3 and S8 fail."

**Problem**: This justifies *which source* is used and argues non-circularity of the routing rather than advancing the claim — the anti-bloat forward-reference/ordering-justification pattern. The clause being established (dom(Σ'.M(d)) = dom(Σ.M(d))) needs only its source cited, not a comparative argument about an alternative source and the pre-state conditions it would have required.

**Required**: State RA-dom's source in one clause and delete the comparative "not via … so these discharges consult neither …" justification.

### Issue 3: Net-effect distinction restated in two places

**ASN-0091, "REARRANGE as Vstream-Only Operation"** (the "That the two come apart is witnessed concretely…" paragraph and the surrounding "The realisation therefore splits on net effect…") versus the **clause (ii) discharge** row: "(ii) non-trivial net effect M'(d) ≠ M(d) | holds directly: M'(d) ≠ M(d) is the net-effect hypothesis under which K.μ~ is the realiser."

**Problem**: The collapse/non-trivial split (π ≠ id as permutation vs. M'(d) ≠ M(d) as net effect, with the S5 witness and the SequentialTransitionAxiom reflexive fallback) is developed at length in the abstract section and then re-asserted in the table. The two passages carry the same load-bearing point in different words.

**Required**: Keep the substantive distinction in one location (the abstract section's witness is the stronger one) and have the table cite it rather than re-deriving the hypothesis.

## OUT_OF_SCOPE

### Topic 1: Reconstitution of a same-source span split across two non-contiguous pieces
**Why out of scope**: This is correctly deferred to the first Open Question; RE-trans establishes per-piece origin (RE-origin) but not joint reconstitution, which is new territory for a future ASN, not a defect here.

### Topic 2: Link-subspace REARRANGE semantics and its invariants
**Why out of scope**: The ASN scopes REARRANGE_K's cut subspace to content (CS3, S = s_C) and lists link-subspace rearrangement as an Open Question; a distinct operation belongs in a future ASN.

### Topic 3: Upper bound on run-cardinality increase per invocation
**Why out of scope**: RE-frag establishes the *possibility* of increase; a quantitative bound is a separate result flagged as an Open Question.

VERDICT: REVISE
