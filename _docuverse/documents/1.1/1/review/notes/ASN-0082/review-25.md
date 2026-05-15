# Review of ASN-0082

## REVISE

### Issue 1: Foundation invariants D-CTG, D-MIN, D-SEQ restated in generalized form inconsistent with foundation

**ASN-0082, Foundation Invariants section**: "**D-CTG** (VContiguity): within subspace S, V_S(d) is order-contiguous — `(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`."

**Problem**: The foundation ASN-0036 explicitly restricts D-CTG to the text subspace V_1(d) and includes a Frame note: "The link subspace `V_2(d)` is exempt — sparse with tombstones is permitted." D-MIN and D-SEQ in the foundation are likewise text-only. ASN-0082's recap silently generalizes all three to "within subspace S," contradicting the foundation's explicit text-only restriction and exemption of the link subspace. The foundation is supposed to be cited unchanged, not silently extended.

**Required**: Either restate D-CTG, D-MIN, D-SEQ exactly as the foundation has them (text-only), or explicitly justify the generalization with a derivation showing why link subspaces also satisfy these invariants — recognizing this would contradict the foundation's "sparse with tombstones" frame note. Whichever path is taken, the recap must match what the foundation actually says.

### Issue 2: Contraction operation depends on the generalized invariants without justification

**ASN-0082, Contraction formal contract**: "Containment: with D-SEQ giving `V_S(d) = {[S, k] : 1 ≤ k ≤ N}`, the condition `p₂ + w₂ − 1 ≤ N`..."

**Problem**: The containment precondition assumes D-SEQ holds for V_S(d) at arbitrary S. The D-SEP(b) proof uses D-CTG to derive `r ∈ V_S(d)` for general S. The D-CTG-post derivation assumes pre-state V_S(d) is contiguous regardless of S. None of these hold for non-text subspaces under the foundation. The operation is implicitly text-subspace-only but isn't stated as such.

**Required**: Restrict the contraction operation's preconditions to S = 1 (text subspace), or explicitly add D-CTG / D-MIN / D-SEQ on V_S(d) as preconditions and acknowledge that the operation is only well-defined where these hold. The current implicit assumption is the kind of hand-wave the review rubric forbids.

### Issue 3: D-MIN-post over-asserts for subspaces where D-MIN doesn't apply

**ASN-0082, D-MIN-post**: "When the post-state subspace S is non-empty, the minimum V-position is `[S, 1, ..., 1]`."

**Problem**: D-MIN per the foundation applies only to V_1(d) (text subspace). For non-text subspaces, the foundation doesn't require any minimum-position invariant — link subspaces may have arbitrary gaps. D-MIN-post claims preservation of a property not required pre-state for non-text subspaces, and the proof's first case ("L ≠ ∅: the pre-state minimum is min(V_S(d)) = [S, 1] (D-MIN)") simply invokes D-MIN for general S, which the foundation does not supply.

**Required**: Restrict D-MIN-post to S = 1 (consistent with the foundation), or derive D-MIN for non-text subspaces. Currently the lemma claims more than the foundation supports.

### Issue 4: D-BJ proof references "established above" without explicit derivation in proof

**ASN-0082, D-BJ proof of (a)**: "Both ordinals satisfy ord(v) ≥ w_ord (established above)."

**Problem**: The "establishment above" is in the D-SHIFT definition paragraph at depth #p = 2, but the chain is informal: "vₘ ≥ ord(r)₁ = pₘ + c" where the inference vₘ ≥ pₘ + c ≥ c isn't spelled out as `vₘ ≥ c` (the precondition TA3-strict actually needs). The reader has to assemble it. For a load-bearing precondition feeding TA3-strict in the bijection proof, the derivation should be explicit in the proof itself: from `ord(v) ≥ ord(r) = ord(p) ⊕ w_ord` and `ord(p) ≥ 1` (S8a componentwise positivity), conclude `ord(v) ≥ w_ord` step by step.

**Required**: Inline the derivation `ord(v) ≥ w_ord` in the D-BJ proof (and the D-SHIFT well-definedness paragraph) with explicit citation of TA-dom or NAT-addbound to make the inequality propagation visible.

### Issue 5: I3-C frame is incompatible with any operation that actually adds content

**ASN-0082, I3-C**: "I3-C (content store): `dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a))` — S9 (TwoStreamSeparation, ASN-0036) guarantees existing content is preserved; the shift stores no new content, so dom(C') = dom(C)"

**Problem**: An INSERT that "places n ≥ 1 new content elements" (per the ASN's own setup paragraph) must extend dom(C). I3-C says dom(C') equals dom(C) — strictly forbidding content addition. The ASN later says "the content-placement postcondition is an operation-level concern deferred to a future INSERT ASN," but the future ASN's content placement would directly violate I3-C as currently stated. The frame as written is internally inconsistent with the operation it claims to characterize.

**Required**: Either weaken I3-C to S0's form (`dom(C) ⊆ dom(C') ∧ (A a ∈ dom(C) : C'(a) = C(a))`) — making it specifically about existing content preservation, not store-equality — or clearly scope I3 as the "shift sub-operation of INSERT" rather than "INSERT modifies M(d) to produce M'(d)" as the prose currently frames it.

### Issue 6: Worked example doesn't include a non-text subspace case

**ASN-0082, Worked Examples**: All insertion and contraction worked examples use S = 1 (text subspace).

**Problem**: I3 is stated for general S ≥ 1 and the I3-X frame explicitly references cross-subspace preservation, but no worked example exercises an insertion into S = 2 (link subspace) or verifies that a text-subspace insertion leaves a sparse link subspace unchanged. Without an example, the cross-subspace claims can't be verified against a concrete scenario.

**Required**: Add a worked example with a non-trivial pre-state containing both text and link subspaces, showing how I3-X preserves the link subspace under text insertion (or vice versa).

### Issue 7: No weakest-precondition analysis for any of the introduced lemmas

**ASN-0082, throughout**: The ASN derives consequences of I3 / D-* postconditions but never computes weakest preconditions backwards from desired properties.

**Problem**: For an ASN whose stated purpose is to extend ASN-0053 with operation postconditions that future operation ASNs will compose with, wp analysis is the natural way to expose what each lemma actually requires. The depth-compatibility precondition on I3, the containment precondition on contraction, and the `#p = 2` scoping axiom are all best understood as wp-derived constraints, but the ASN states them without showing the wp calculation.

**Required**: Add a wp section for at least one non-trivial postcondition — e.g., wp for I3-VP (S8a preservation) backwards through the shift, showing exactly why componentwise positivity of v is needed on positions 1..m−1. The review rubric explicitly calls out missing wp as a depth issue.

### Issue 8: D-SEQ-post relies on the D-SEQ derivation in ASN-0036 without confirming preconditions in the post-state

**ASN-0082, D-SEQ-post proof**: "These three conditions — contiguity, minimum at [S, 1], and uniform depth 2 — are exactly the preconditions of the D-SEQ derivation (ASN-0036)."

**Problem**: The D-SEQ derivation in ASN-0036 (per the foundation extract) actually requires four conditions: contiguity (D-CTG), minimum (D-MIN), common depth (S8-depth), and S8a. The proof asserts three and elides S8a — even though S8a-post is established as a separate lemma. More importantly, the foundation's D-SEQ is text-only, so invoking "the D-SEQ derivation" for general S inherits Issue 1's foundation mismatch.

**Required**: Cite S8a-post alongside the other three preconditions, and either restrict D-SEQ-post to S = 1 or reproduce the derivation locally for general S rather than citing the foundation's text-only version.

## OUT_OF_SCOPE

### Topic 1: Generalization of contraction to depth #p > 2
**Why out of scope**: The ASN explicitly flags this as an open question and provides a detailed three-part justification (TA4 zero-prefix structural constraint, Literary Machines design intent, udanax-green implementation reality) for the depth-2 restriction. The deeper-depth generalization belongs in a future ASN.

### Topic 2: Full INSERT operation including content placement at gap positions
**Why out of scope**: The ASN scopes itself to the shift sub-operation. The content-placement postconditions, re-establishment of D-CTG/D-MIN/D-SEQ via gap filling, and S7-style new-content allocation belong in a future INSERT ASN. (Note: Issue 5 above is about internal inconsistency of the current scope, not about deferring content placement.)

### Topic 3: Link-subspace contraction semantics
**Why out of scope**: If link subspaces use tombstoning rather than shift-on-delete (per the foundation's D-CTG frame note), then contraction in the shift sense doesn't apply to link subspaces at all — there's a different operation (tombstone) to specify. This belongs in a separate ASN about link-subspace mutation.

VERDICT: REVISE
