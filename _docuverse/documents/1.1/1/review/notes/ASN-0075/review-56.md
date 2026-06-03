# Review of ASN-0075

I checked the lemma chain (D-WIT → D-EXH → D-DISCR → D-NEED), the two-history non-discrimination construction, the wp derivations, the worked example, and the auxiliary claims. The mathematics is sound: D-WIT's use of S3★/L14/P4★ is careful, the impossible-row exclusion in D-EXH is correct, the two histories in D-DISCR genuinely agree on (C,L,E,M) while differing on R, and the worked example checks out (SHOWDELETIONS(d_A,d_B) = ({b},{c}), with D-SYM verified). The note is in good shape on correctness. The issues below are the meta-prose accretion the `review-mode.anti-bloat` classifier flags — and the recent "expand D-BOUND/D-SUBSP justifications" revision appears to have introduced exactly this.

## REVISE

### Issue 1: D-BOUND introduction enumerates its downstream consumers
**ASN-0075, "Boundary precondition (D-BOUND)"**: "D-WIT and D-EXH carry this composite-boundary condition as an explicit hypothesis; D-BOUND is the operation precondition that supplies it."
**Problem**: This sentence is plumbing meta-prose — it explains which lemmas consume the precondition rather than advancing what the precondition *is*. It matches the named anti-pattern (a definition's introduction enumerating downstream consumers). The following sentence then restates the precondition again ("the last conjunct being D-BOUND"), so the section states the same fact in three forms (the prose, the consumer inventory, the formula).
**Required**: State the precondition once — `Σ` is reachable from `Σ_0` by valid composite transitions, so SHOWDELETIONS is invoked at a composite boundary — and drop the consumer inventory. D-WIT/D-EXH already name the composite-boundary hypothesis at their own sites; they do not need to be re-announced here.

### Issue 2: Q0 wp re-derives the D-OBS pass-through already stated generally
**ASN-0075, wp section under "The SHOWDELETIONS Operation"**: The general rule is given — "By D-OBS the operation modifies no state component, so wp computations for state-level predicates pass through unchanged from the pre-state: `wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)` whenever `P` depends only on `Σ`." Then for Q0: "Since SHOWDELETIONS modifies no state component (D-OBS) and `Q0` depends only on `Σ`'s components `M`, `R`, `dom(C)` … the wp formula is the precondition conjoined with `Q0` unpacked at the pre-state."
**Problem**: The Q0 paragraph re-derives the pass-through that the general rule already establishes for every state-level `P`. The Q1 derivation, by contrast, does not restate it — so the treatment is both redundant and inconsistent.
**Required**: Cite the general rule for Q0 (as Q1 does) instead of re-deriving D-OBS pass-through a second time.

### Issue 3: "Restriction to the Content Subspace" states "not incidental" twice
**ASN-0075, "Restriction to the Content Subspace"**: opens with "Confining the operation to the content subspace … is essential rather than incidental," and after the justification repeats "This restriction is not incidental: …".
**Problem**: The framing claim ("essential rather than incidental" / "not incidental") is asserted before and after the proof. The second occurrence does carry new content (the CL-OWN witness-asymmetry argument), but the repeated framing phrase is filler.
**Required**: Drop the opening "essential rather than incidental" framing; let the justification (`output ⊆ dom(C)`) and the CL-OWN asymmetry argument carry the point. The reader does not need to be told twice that the restriction matters.

## OUT_OF_SCOPE

### Topic 1: Restoration / recovery operation that consumes SHOWDELETIONS output
**Why out of scope**: The final open question and D-ACT gesture at an operation that reintroduces deleted content into a target arrangement. Defining that operation and its origin/link-resolvability guarantees is new territory for a future ASN, not a gap in this observational specification.

### Topic 2: Multi-document (n > 2) generalization and witness structure
**Why out of scope**: The binary asymmetric pair is what this ASN specifies; the n-document witness structure raised in the open questions is genuinely new work.

VERDICT: REVISE
