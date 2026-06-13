# Review of ASN-0130

I worked through every claim against its preconditions and boundary cases. This is an exceptionally rigorous note, and the proofs hold up under scrutiny. I verified in particular:

- **The stratification (PR2 → PR-SIG → PR0(iii))** is non-circular: PR2's acyclicity proof uses only conditions (i)/(ii)/(iv) and the sequential-transition total order (ASN-0093), never `sig`, so PR-SIG's induction on first-registration order is well-founded before the type layer is built, and PR0(iii)'s typing then rests on grounded signatures.
- **PR0's weakest precondition** is genuinely weakest: I checked sufficiency and necessity across all four cases (active incumbent → hit/reject both preserve; no incumbent + VALID + d∈dom(M) + C3 → fresh active deposit; born-nullified ¬C3 → POST-ref false). The hit-shaping argument (slot-1 coverage forces `a'=a`, PR-ENC-uniq forces slot-2 equality) correctly establishes that a VALID-passing call with an active incumbent must hit.
- **PR3a's substitution induction** is complete: WT-α and WT-W are correctly conditioned on exactly the freshness PR3's renaming arranges (expansion names disjoint from author names, fresh against `expand(r)`/the `Eⱼ`); the k-fold PC2 discharge with the `Γⱼ` indexing checks out, and capture-freedom holds because each `yⱼ` sits only under `u`'s own (fresh) binders.
- **PR2's self-reference exclusion** is airtight: a deposit is a miss, all validated tuples at one start are I0-equal, so no active witness for a self-reference exists at the pre-state; the hit case is excluded by the same induction.
- **PR5's ST⁺ soundness**, including the aggregate-threshold extension: PD0's aggregate stability consumes only threshold *fixity*, and an environment-bound parameter is as fixed across a step as a literal (same `args` both sides), so the `count(D) ≥ x` / `count(D) ≤ x` extension is sound. The per-instantiation reading degrades to PD0's literal rules at every instantiation. I stress-tested the negation/implication compounds.
- **Boundary cases**: empty `A_def` (rejected at (0)), single-address run (n=1, trivial contiguity), closed term (k=0, ST⁺ ≡ ST), born-nullified registration, de-register/re-register (multiple deposit events, handled by PR2's event-wise argument), certify on non-Boolean (rejected at (0)) and de-registered (rejected at (i)) targets — all covered.
- The `is_pd_stable(t)` exact-coverage argument (distinct content-run starts are prefix-incomparable, so `t ∈ subtree(t')` between starts forces `t' = t`) is correct, and the note is honest about the universal-lint domain limitation (non-predicate definitions can't be excluded in PL).
- View-independence (PR-VIEW) correctly separates fixed-view-but-non-grow-only reads (e.g. `A_W`) — the worked example's `quiescent_v1` passes (ii) and fails (iii), exactly as it should.

The anti-bloat classifier: prior accumulation appears to have been pruned (consistent with the recent "tighten proofs" revisions). Remaining editorial framing ("load-bearing," "central scoping hypothesis," "what certification buys") is light and does not impede the argument; the parentheticals (registration-vs-allocation order, ghost-reference clarification) and the worked composition's capture contrast are substantive, not meta-prose. The parallel restatements in PR5a explicitly defer to PR0/PR1 ("PR1's analogue, same proof shape"; "the wp mirrors PR0's") rather than re-deriving. No forward-reference accretion rises to a finding.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Obtaining contiguous runs under concurrent same-document allocation
PR0(i) requires `A_def` to be one uninterrupted K.α chain segment, and the worked composition's step 1 correctly flags that this holds only "with no other K.α scoped to `d_b` interleaved." `register_pred` *validates* contiguity (rejecting a split run), so safety is unaffected; what is unaddressed is the *liveness* guarantee that a builder can reliably reserve a contiguous multi-address segment when allocation to its home document is contended.

**Why out of scope**: The substrate's per-document chains plus sequential atomicity (ASN-0093) make this achievable for a document's sole allocator, and the worked example assumes that posture. A formal "an owner can always allocate a contiguous run of length n" liveness/protocol guarantee is new territory (and arguably an ASN-0093-level concern), not an error in this note's safety claims. It is not among the note's own scoped-out items (concrete encoding, activation, certifier internals, naming, portability, dangling references, certificate classes).

VERDICT: CONVERGED
