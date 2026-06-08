# Review of ASN-0100

## REVISE

### Issue 1: Prepend boundary (j=0, full-clearance) lacks a concrete worked example

**ASN-0100, A Worked Example / §The Operation**: The note works the interior case (j=2), the append boundary (j=N), the empty-document case, and a deep-subspace m_C=3 case — but never the **j=0 prepend on a non-empty document**.

**Problem**: j=0 is the uniquely stressful K.μ⁻ scenario. There `Left = ∅`, so `n'_{s_C} = p_m − 1 = 0` is *forced* — the canonical decomposition performs full content-subspace clearance (`V_{s_C}(d_intermediate) = ∅`, D-CTG★/D-MIN★/D-SEQ★ holding vacuously) followed by a single K.μ⁺ that re-adds the entire run `{[s_C,1,…,1,k] : 1 ≤ k ≤ N+n}` from the minimum, with *every* pre-state position shifted. This combination (forced full shrinkage + total shift + re-pin of min) appears nowhere as a concrete scenario; it is only described abstractly in the Σ'-uniqueness section (where `n'_{s_C}=0` is presented as an *optional* alternative decomposition, not as the *forced* j=0 case). The append example covers insert-after-all; the symmetric and harder insert-before-all is not exhibited. The rubric makes boundary cases and a concrete check of key postconditions mandatory.

**Required**: Add a worked j=0 example on a non-empty document (e.g. `INSERT(d, [1,1], ⟨v₀⟩)` with `V_{s_C}(d) = {[1,1],…,[1,5]}`), showing the forced K.μ⁻ with `n'_{s_C}=0`, the vacuous post-K.μ⁻ intermediate, the full-run K.μ⁺, and verification of INS.inv.seq / D-MIN★ on the post-state.

### Issue 2: Reviser-drift paragraph inside a worked example that stipulated the contrary case

**ASN-0100, Empty-document first insertion, "Cleared-but-residual subtlety"**: The example explicitly stipulates "no content has ever been allocated under `d` — `{a' ∈ dom(Σ.C) : origin(a') = d} = ∅`" so that K.α's first-emission branch fires. A trailing paragraph then imagines the *excluded* residual-content case ("When such residual content exists … K.α … fires the *subsequent*-emission branch").

**Problem**: This matches the anti-bloat pattern "a paragraph imagines a case the claim's carrier or precondition already excludes." The content itself (empty arrangement ≠ empty content store, which selects the K.α branch) is genuine and worth stating once — but its home is not inside an example that has just stipulated the opposite. As placed, the reader must read past a counterfactual to follow the example.

**Required**: Relocate the empty-arrangement/non-empty-store distinction to INS.alloc (or a single precondition-state note), and let the worked example carry only its stipulated first-emission case.

## OUT_OF_SCOPE

### Topic 1: Re-pinning m_C after content-subspace clearance
**Why out of scope**: The interaction between K.μ⁻ full clearance (which permits a later insert to re-pin `m_C` at any value ≥ 2) and prior cleared content's old V-depth touches DELETE/clearance mechanics (K.μ⁻ as an operation), not INSERT's per-state effect. INSERT correctly treats the cleared state as a precondition state; the clearance operation belongs elsewhere.

### Topic 2: Link-subspace insertion, COPY, concurrent INSERT serialisation
**Why out of scope**: Correctly deferred by the note's own Bounding-the-Scope section and Open Questions; these are distinct operations/protocols.

VERDICT: REVISE
