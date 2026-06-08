# Review of ASN-0107

## REVISE

### Issue 1: D2 reordering states an incorrect necessity ("only when π fixes Wᵢ setwise")

**ASN-0107, §"Two Anchorings", D2 reordering clause**: "the forward image of a *fixed sub-region* `Wᵢ` is preserved only when `π` fixes `Wᵢ` setwise — `π⁻¹(Wᵢ) ∩ dom = Wᵢ ∩ dom`" — and again in the worked instance: "K.μ~ preserves `num_disc` only when `π` fixes each query region setwise".

**Problem**: This is asserted as a *necessary* condition (image preserved ⟹ π fixes Wᵢ), but it is only *sufficient*. Because arrangements may map distinct V-positions to the same I-address (content sharing, M13/S5), the forward image of a sub-region can be preserved by a non-trivial reorder that does not fix the region setwise. Concrete counterexample, all within K.μ~ admissibility and D-SEQ★:

- Content subspace of `d_q` with positions `p₁=[1,1], p₂=[1,2], p₃=[1,3], p₄=[1,4]`, and `M: p₁↦a, p₂↦a, p₃↦b, p₄↦c` (sharing of `a` permitted).
- `π = (p₁ p₂)(p₃ p₄)`. Then `M' : p₁↦a, p₂↦a, p₃↦c, p₄↦b`, so `M'≠M` (non-trivial, clause (ii)); π is length-, subspace-, link-subspace-preserving.
- `W₁ = {p₁}`: `Q₁(Σ) = {M(p₁)} = {a}`, `Q₁(Σ') = {M(π⁻¹(p₁))} = {M(p₂)} = {a}` — **image preserved** — yet `π⁻¹(W₁) = {p₂} ≠ {p₁} = W₁`, so π does **not** fix `W₁` setwise.

So "image preserved ⟹ π fixes Wᵢ" is false. The worked-instance *example* (count moves 3→0) is correct, but it does not establish the general necessity the surrounding sentence claims.

**Required**: Restate as sufficiency ("if π fixes `Wᵢ` setwise then `Qᵢ` is preserved; this holds e.g. when `Wᵢ` is an entire subspace"), or give the exact characterization (`Qᵢ` preserved iff `{M(d_q)(u) : u ∈ π⁻¹(Wᵢ)∩dom} = {M(d_q)(u) : u ∈ Wᵢ∩dom}`, which sharing can satisfy without setwise fixity). Adjust the worked-instance sentence accordingly.

### Issue 2: A2's `Q₂ = Q₃ = T` special case is incompatible with the discovery anchoring it is stated under

**ASN-0107, §"How the Count Changes: Content Added", A2**: "In the special case where the query leaves the to- and type-parts unconstrained (`Q₂ = Q₃ = T` ...), every shared link discoverable through the from-slot is also counted, and the count rises by exactly the links thus shared."

**Problem**: A2 is framed about the *discovery count* of "a query against `d_new`". But the discovery anchoring definition resolves *all three* parts through the arrangement, `Qᵢ(Σ) = {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ dom(Σ.M(d_q))}` — a finite image set, never `T`. A request with `Q₂ = Q₃ = T` is only meaningful under existence anchoring (directly-given parts), which A2 itself says leaves the count unchanged. The special case therefore mixes a per-slot anchoring (from resolved through `d_new`, to/type given as `T`) that no definition in the ASN supports. `num_disc(d_q, W, Σ)` has no provision for unconstrained parts.

**Required**: Either define a mixed/per-slot anchoring (some slots resolved through an arrangement, others given directly) and state A2 against it, or correct A2 to use a discovery-resolvable form for all three parts (e.g. `W₂, W₃` ranging over the whole respective subspaces of `d_new`) and show those resolve to the relevant address sets rather than `T`.

## OUT_OF_SCOPE

### Topic 1: Partiality of `num_disc` when `d_q ∉ dom(Σ.M)`
The discovery definition restricts `d_q ∈ dom(Σ.M)` but does not state the operation's behavior (undefined vs. zero) for an unregistered querying document. This is a small definitional completeness matter that could be addressed in a future refinement of the discovery-anchoring contract rather than a defect in the present claims.

VERDICT: REVISE
