# Review of ASN-0098

## REVISE

### Issue 1: Overstated "cannot extend the link's reach" claim, contradicted in its own paragraph

**ASN-0098, "Frame Conditions: When Projection Does Not Move"** (paragraph following the LP6/LP7/LP14 template): "This is the precise sense in which 'insertion at the boundary of a linked passage' cannot extend the link's reach: insertion as a composite (allocate + arrange) splits into a K.α step (no projection effect) and a K.μ⁺ step. The K.μ⁺ step might add a V-position to the projection, but only if the new V-position's I-address is in coverage(e)."

**Problem**: The sentence asserts insertion "cannot extend the link's reach," then immediately concedes "The K.μ⁺ step might add a V-position to the projection." As stated this is self-contradictory. The claim that boundary insertion *cannot* extend reach is true only for *tight* endsets and is established later as LP19; here it is asserted unconditionally for an arbitrary endset `e`, where it is in fact false (LP9 growth applies when the fresh I-address lands in `coverage(e)`). This is LP19's conclusion smuggled in as already-true at the LP6/LP7/LP14 site — forward-reference accretion.

**Required**: Restrict the claim to the allocation half only (K.α alone displaces nothing — which is all LP6 establishes), and drop the "cannot extend the link's reach" framing here. Defer the boundary-exclusion claim to LP19 where tightness is in force, or state it explicitly as conditional on tightness.

### Issue 2: Orphan decorative reference

**ASN-0098, "Frame Conditions"** (same paragraph, final sentence): "By T10a (AllocatorDiscipline, ASN-0034), each new K.α-allocated I-address is structurally distinct from all prior allocations."

**Problem**: This sentence is dropped at the end of the paragraph and is not used by any local argument — projection invisibility of fresh addresses follows from the arrangement not yet referencing them, not from structural distinctness. A foundation citation appended without a consuming step.

**Required**: Remove, or attach it to a claim that actually uses distinctness (it belongs to the LP19a freshness argument, where it is already covered by the freshness precondition).

### Issue 3: Essay framing around a forward reference in the projection definition

**ASN-0098, "The Projection Operation"**: "Every guarantee in this ASN follows from one observation: of the two inputs, only the arrangement varies. The endset stands still ... we therefore characterise projection displacement by examining what each editing operation does to Σ.M(d); LP4 below carries the formal claim that this is the only source of displacement."

**Problem**: "Every guarantee in this ASN follows from one observation" is essayistic scene-setting, and "LP4 below carries the formal claim" is a forward pointer to a claim not yet stated. This is meta-prose around a forward reference — the reader must defer to LP4 to learn what is actually asserted.

**Required**: State the operative fact at LP4 only; trim the anticipatory framing here to the mechanical content (projection reads `coverage(e)` and `Σ.M(d)`; the former is endset-fixed).

### Issue 4: Methodological forward-pointer preceding the definitions it describes

**ASN-0098, "Boundary and Width Behaviour"**: "The achievability arguments below proceed under the canonical assumption — every span exhibited has `ℓ = δ(n, #s)` — and exhaust `F ∩ [s, s ⊕ ℓ)` by structural partition. The count within each structural case is finite by LP-Fin ..."

**Problem**: This paragraph describes the method of "the achievability arguments below" before the `tight` definition and the achievability paragraph it refers to. It is scaffolding prose deferring to a downstream location; its substantive content (finiteness, decidability) is already carried by LP-Fin and the `tight` definition.

**Required**: Fold the substantive decidability remark into the `tight` definition (which already invokes LP-Fin) and delete the anticipatory description.

### Issue 5: Redundant restatement in Discovery Independence

**ASN-0098, "Discovery Independence of Origin"**: the four consecutive sentences ("depends on none of them," "visible by inspection of LP12," "The home document is a metadata property ... not a constraint," "Similarly, origin is a metadata property ... so discovery is indifferent to provenance").

**Problem**: These circle a single point — discovery is I-address-based and provenance-indifferent — restated in four forms. One derivation from LP12 suffices.

**Required**: Collapse to a single sentence: by inspection LP12's RHS references only `coverage` and `ran(Σ.M(d))`, so discoverability is independent of `home(a)` and of coverage origins.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive, V-order reflection, cross-document operation comparison
**Why out of scope**: These are correctly deferred to the Open Questions and name future ASNs (reverse lookup, V-order vs I-order preservation under K.μ~). Not errors here.

### Topic 2: Non-canonical span finitude
**Why out of scope**: LP-Fin and tightness are scoped to canonical spans by design; the link-canonical contraction case is explicitly listed as open. New territory, not a defect.

VERDICT: REVISE
