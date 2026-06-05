# Review of ASN-0115

## REVISE

### Issue 1: R9 origin-traceability cites S7 for positions S7 does not cover

**ASN-0115, R9 (CoherentMultiOriginAssembly)**: "The resolution is origin-traceable: each active position `v` resolves to `a = Σ.M(d)(v)`, and that address determines `origin(a)`, the home document of the content (S7)…"

**Problem**: The quantifier ranges over *each active position*, but S7 (StructuralAttribution, ASN-0036) attributes only content addresses — its precondition is `a ∈ dom(Σ.C)`. A link-subspace active position (`subspace(v) = s_L`) resolves by S3★ to `a ∈ dom(Σ.L)`, where S7's `origin` is not defined. The provenance of link addresses is supplied instead by `home` (ASN-0043, L1a) / the HomeOriginCoincidence fact (ASN-0086), neither of which is invoked. As written, the universal origin-traceability claim is discharged only for the content sub-case.

**Required**: Either restrict the quantifier to content positions (`subspace(v) = s_C`), or separately discharge link-subspace provenance by citing the link-address `home`/origin machinery (ASN-0043 L1a, ASN-0086 HomeOriginCoincidence). R10 already establishes link positions deliver references; R9's traceability claim must align its scope with that split.

### Issue 2: R8 omits the content-position hypothesis its proof depends on

**ASN-0115, R8 (TransclusionRevelation)**: "If two active positions `v, v'` … satisfy `Σ.M(d)(v) = Σ.M(d')(v') = a`, then (i) the two delivered items carry the identical value `Σ.C(a)`, by R2; (ii) … so `origin` of both is one and the same (S4, S7)…"

**Problem**: The hypothesis constrains only that both positions resolve to the same address `a`; it does not state `subspace(v) = subspace(v') = s_C`. But conclusion (i) asserts the items carry `Σ.C(a)` (a content value), and (ii) invokes S4/S7 (content-address attribution). These hold only when `a ∈ dom(Σ.C)`. Two positions could equally share a *link* address (both `s_L`), in which case the shared content is a link, the items are `⟨ref, a⟩` (R10), and `Σ.C(a)` is undefined. The claim's stated conclusions are established only for the content sub-case, yet the hypothesis admits the link sub-case.

**Required**: State `subspace(v) = s_C` (equivalently `a ∈ dom(Σ.C)`) as a hypothesis of R8, or add the link-share sub-case (two positions referencing one link address deliver identical `⟨ref, a⟩` items, with provenance via `home`). Note that SD (store disjointness) already forces `v, v'` into one subspace once they share `a`, so the restriction is clean.

## OUT_OF_SCOPE

### Topic 1: Single boundary-crossing span (one span yielding both content and link items)

**Why out of scope**: The V-spec definition deliberately restricts `σ` to ordinal-level spans, for which the ContiguousSubtrees argument confines `⟦σ⟧` to one subspace; the straddling case is correctly deferred to an Open Question. This is new territory, not an error.

### Topic 2: Inline provenance, channel faithfulness, unbound-reference targets

**Why out of scope**: R2's frame limit (channel) and R9's traceability-vs-inline distinction are explicitly bounded, with the residual questions parked in Open Questions. These belong to future ASNs.

VERDICT: REVISE
