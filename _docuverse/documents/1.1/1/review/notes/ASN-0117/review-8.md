# Review of ASN-0117

## REVISE

### Issue 1: DELETE is identified with K.μ⁻, but K.μ⁻ cannot left-shift survivors

**ASN-0117, "DELETE(d, p, w)" Effect**: "Concretely it *is* the foundation transition **K.μ⁻ (ArrangementContraction)** of the extended-state model … specialised to the text subspace and realised through ASN-0082's left-shift displacement."

**Problem**: K.μ⁻ as axiomatized in ASN-0047 is a *prefix-retention truncation*. Its postcondition is `dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`, and its per-subspace scope fixes the retained domain as `R := ∪_S {[S,1,…,1,k] : 1 ≤ k ≤ n'_S}` — a contiguous prefix of each subspace run, with surviving mappings **unchanged at their original V-positions**. DELETE removes a span from the *middle* and shifts the suffix left. This directly violates K.μ⁻'s value-preservation clause. In the ASN's own worked example (N=5, delete q₃, c=2), `q₃ ∈ dom(M'(d))` with `M'(d)(q₃) = a₅`, whereas `M(d)(q₃) = a₃`; so `M'(d)(q₃) ≠ M(d)(q₃)`. K.μ⁻ can express only a *suffix* deletion (the boundary case J+c=N+1, R=∅); for any mid-document span it is not K.μ⁻ — nor any other single ASN-0047 atomic transition (K.μ~ preserves domain cardinality; K.μ⁺ adds content). The ASN even contradicts itself on this point: the wp section declines LP10 precisely "because LP10's premise is a K.μ⁻ prefix-retention truncation, in which survivors keep their V-positions unshifted, whereas DELETE left-shifts the suffix." DELETE cannot both *be* K.μ⁻ and behave unlike K.μ⁻.

**Required**: Either (a) define DELETE as a valid ASN-0047 *composite* (e.g., K.μ⁻ retaining the prefix q₁…q_{J−1}, then K.μ⁺ re-placing the survivors at q_J…q_{N−c}) and discharge the resulting coupling obligations (J0/J1★/J1'★ — note re-added survivors are not range-new content, which must be argued), or (b) drop the "is K.μ⁻" identification, treat DELETE as a contraction not in the ASN-0047 atomic vocabulary, and justify the extended-state appeals (S3★, entity/provenance frames) independently. The LP10 paragraph and the Effect paragraph must be reconciled.

### Issue 2: DEL-FENT, DEL-FPROV, and hence P4★/P7a/P1/P8 rest solely on the invalid citation

**ASN-0117, Frame (DEL-FENT, DEL-FPROV)**: "`Σ'.E = Σ.E` … This is K.μ⁻'s entity frame (ASN-0047)"; "`Σ'.R = Σ.R` … This is K.μ⁻'s provenance frame (ASN-0047)."

**Problem**: These frames are justified *only* by the K.μ⁻ identification refuted in Issue 1. Unlike S3★ — which the well-formedness section re-derives directly from DEL-CIMM/DEL-FSUB/DEL-LIMM and so survives — the entity and provenance frames have no independent derivation in the ASN. With the K.μ⁻ citation removed, P4★ (Contains_C(Σ') ⊆ R') and P7a both lose their stated grounds, since both invoke `R' = R` via DEL-FPROV, and P1/P8 invoke DEL-FENT.

**Required**: Supply a direct argument that DELETE leaves E and R fixed (e.g., DELETE neither baptizes nor removes any entity, and records/retracts no provenance; P2 forbids retraction regardless), independent of the K.μ⁻ name — or fold it into whatever composite/transition reframing resolves Issue 1.

## OUT_OF_SCOPE

### Topic 1: Deletion of V-positions of depth m > 2
DELETE inherits the depth-2 restriction (`m = #p = 2`) from ASN-0082's contraction, which is proven only at depth 2. Generalizing to deeper text subspaces requires extending the foundation displacement work first; it is not an error in this ASN.

### Topic 2: Reconstructibility / backtrack state beyond the content store
The Open Questions correctly defer what additional state (version graph, prior arrangements) backtrack requires for exact reconstruction. This is future territory, not a gap in DELETE's arrangement semantics.

VERDICT: REVISE
