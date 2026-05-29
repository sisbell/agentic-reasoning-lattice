# Review of ASN-0036

## REVISE

### Issue 1: S8a restates the domain-restriction axiom and carries defensive meta-prose
**ASN-0036, S8a (V-position componentwise positivity and depth)**: "A one-line reformulation of the domain-restriction axiom, not an independent claim: since `zeros(v) = 0` iff every component is positive (T0, T4), the axiom's `zeros(v) = 0 ∧ #v ≥ 2` is equivalently ..."
**Problem**: The `Σ.M(d)` domain-restriction axiom already states `zeros(t) = 0 ∧ #t ≥ 2`. S8a re-states the same content in per-component form and then adds the disclaimer "not an independent claim." That disclaimer is exactly the kind of defensive meta-prose the `review-mode.anti-bloat` classifier targets — it explains the claim's relationship to another claim rather than advancing the claim itself, and it sits in a structural (named-claim) slot. Two paragraphs in the document now assert the same fact in different words.
**Required**: Either fold the per-component form directly into the domain-restriction axiom (and delete S8a), or keep S8a as a bare restatement used for citation and drop the "not an independent claim" / "is equivalently" framing.

### Issue 2: S2 duplicates the `Σ.M(d)` partial-function axiom
**ASN-0036, S2 (Arrangement functionality)**: "*Axiom (definitional):* `Σ.M(d) : T ⇀ T` is a (partial) function — `(A d, v, a₁, a₂ : ...: a₁ = a₂)`."
**Problem**: The `Σ.M(d)` block already declares `Σ.M(d) : T ⇀ T` as a partial function; single-valuedness is the definitional content of a (partial) function. S2 re-declares the same property. Under the anti-bloat classifier this is a same-thing-twice pattern. The accompanying prose ("This is inherent in the concept of a 'virtual byte stream'") is justification, not new content.
**Required**: Keep a single statement of single-valuedness. If S2 must exist as a citable name for the S8 proof, reduce it to the named restatement and drop the duplicated declaration and the inherent-in-the-concept essay.

### Issue 3: Under-cited promotion step in the S8 within-subspace lemma
**ASN-0036, S8 proof, within-subspace lemma, Case j = m**: "NAT-discrete (ASN-0034) at `(m, n) := (v_m, t_m)` promotes the strict inequality `v_m < t_m` to `v_m + 1 ≤ t_m`."
**Problem**: The note follows a scrupulous per-step citation discipline elsewhere, but this promotion is not discharged by NAT-discrete alone. From `v_m < t_m`, ruling out `t_m < v_m + 1` requires NAT-discrete (`v_m ≤ t_m < v_m + 1 ⟹ t_m = v_m`) **plus** NAT-order (irreflexivity to contradict `t_m = v_m`, and trichotomy to conclude `v_m + 1 ≤ t_m`). NAT-order is cited only later, for the final incompatibility, not for the promotion itself.
**Required**: Cite NAT-order alongside NAT-discrete at the promotion step, matching the convention applied to the structurally identical step in ASN-0034's own dependency notes.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG, D-MIN, S2, S3
The ASN correctly defers (in Open Questions) what INSERT/DELETE/COPY/REARRANGE and the insertion-displacement mechanism must guarantee to preserve the contiguity invariants. This is operation-specific effect, explicitly out of scope; the deferral is appropriate and is not an error in this ASN.

### Topic 2: Subspace-alignment as an arrangement invariant
Whether `subspace(v)` must match the first element-field component of `M(d)(v)` is raised as an operations-layer obligation rather than a strand-level invariant. This belongs to a future operations ASN, not here.

VERDICT: REVISE
