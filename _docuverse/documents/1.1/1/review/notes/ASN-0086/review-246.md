# Review of ASN-0086

## REVISE

### Issue 1: Worked sketch re-proves L-invariants that R0 already discharges generically, plus an "identical in form" deferral
**ASN-0086, Worked Sketch, Step 1**: "*L-invariant verification at b₁.* R0 verifies each L-invariant against an arbitrary K.λ-emitted address; the concrete b₁ ... admits the same checks by direct inspection: L0 ... L1 ... L1a ... L1b ... L1c ... The remaining state-local L-invariants (L3, L4(c), L12, L12a, L-fin) discharge by R0's generic argument ... The later fresh emissions in this sketch (a₂, b₂, a₃) are all siblings of b₁ ... ; their L-invariant discharge is identical in form to this one."

**Problem**: The sketch's purpose is to demonstrate R0–R6 on concrete tumblers. The L-invariants are not properties introduced by this ASN — R0's own proof already establishes that *every* K.λ emission preserves the full L-invariant catalog (the sketch even says so: "R0 verifies each L-invariant against an arbitrary K.λ-emitted address"). Re-verifying L0/L1/L1a/L1b/L1c at the concrete `b₁`, then deferring the rest with "discharge by R0's generic argument," then noting future emissions are "identical in form to this one," is exactly the forward-reference accretion the classifier targets: verification prose that restates a guarantee already in hand. The reader must skip past it to follow the R0–R6 demonstration the sketch exists to give.

**Required**: Drop the per-emission L-invariant re-verification and the "identical in form" sentence. Cite R0 once ("each emission's L-invariants hold by R0") and keep the sketch focused on the relational properties (R0a freshness/antichain, R3 monotonicity, R6a/R6b/R6c) that are this ASN's actual content.

### Issue 2: Redundant defensive exhaustiveness clause in the transition-relation definition
**ASN-0086, "State transition relation"**: "...and the substrate exposes no removal, replacement, or in-place mutation transition that touches `(dom(Σ.C), dom(Σ.M), dom(Σ.L))`."

**Problem**: The relation is defined as `→ ≡ K.σ ∪ K.α ∪ K.λ`, and each K-operation's contract (with ASN-0093's C0/M1/L12 foundation invariants) already fixes append-only-at-fresh-key semantics. The "no removal/replacement/mutation" clause adds no content beyond the `≡` definition plus the cited frame conditions; it is a defensive exhaustiveness restatement.

**Required**: Delete the clause. The `≡` definition and the per-K-op frame citations already carry it.

### Issue 3: Conceptual contrast essay misplaced in the TupleAddress definition
**ASN-0086, "Definition — TupleAddress"**: "The address component `a` is what distinguishes this structure from the set-theoretic typed relation (a subset of `℘(A) × ℘(A)`, distinguished only by content): each tuple carries an address that participates in the relation's identity, which the content-only projection `(a, F, G) ↦ (coverage(F), coverage(G))` discards."

**Problem**: This is motivational/analogical essay content about *why* addressed tuples differ from set-theoretic relations. It does not advance the definition (`addr` is already fully specified by the preceding sentence). Per the classifier, the issue is placement: conceptual framing belongs in the note's opening ("We are looking for what a relation algebra ... affords"), not inside a structural Definition slot a precise reader is scanning for the map's signature.

**Required**: Move the contrast to the introduction, or cut it. The definition needs only `addr(a, F, G) = a` and the injection/onto characterization.

## OUT_OF_SCOPE

The genuine future-territory questions (cross-`Σ.M`/`L_K` visibility invariants, higher-arity projections, concurrency/atomicity of Observe vs. Emit, elevating the unit-depth discipline to a substrate guarantee) are already correctly parked in the Open Questions section rather than smuggled into proofs. No additional out-of-scope items.

VERDICT: REVISE
