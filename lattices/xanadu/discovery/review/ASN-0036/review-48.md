# Proof Verification: S3

RESULT: FOUND

**Problem**: S3 has no proof and no formal contract. The property section contains only a weakest-precondition *analysis* — it describes what operations *would need to satisfy* to preserve S3, but never formally establishes that S3 holds as an invariant. The only `*Proof.*` block and `*Formal Contract:*` block present belong to the S1 dependency, not to S3 itself.

Specifically, proving S3 as an invariant requires two obligations:

1. **Base case**: S3 holds in the initial state (trivially, if `M(d)` is empty for all `d`, or by construction).
2. **Inductive step**: Every state transition `Σ → Σ'` preserves S3. This has two sub-cases:
   - *New mappings*: Any operation adding `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)`. The wp discussion sketches this but doesn't prove it — it states the requirement without showing all operations satisfy it.
   - *Existing mappings*: References valid in `Σ` remain valid in `Σ'`. This follows from S1 (`dom(Σ.C) ⊆ dom(Σ'.C)`), but the derivation is never written out.

The narrative at "a valid reference cannot become dangling through any subsequent state transition" is the right argument for the second sub-case, but it appears as prose commentary, not as a proof step.

**Required**: 
1. Add a `*Proof.*` block for S3 that establishes both the base case and the inductive step (citing S1 for preservation of existing references, and either enumerating operations or declaring the wp constraint as an axiom for new references).
2. Add a `*Formal Contract:*` for S3. Based on the property's nature as a state invariant, it should be:
   ```
   *Formal Contract:*
   - *Invariant:* (A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))
   ```
