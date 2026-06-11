# Review of ASN-0120

## REVISE

### Issue 1: The ρ-to-resolve correspondence is overstated — it omits the depth-mismatch extension the ASN itself just admitted

**ASN-0120, "What the endset arguments name, and what resolution recovers"**: "This is ASN-0058's `resolve` lifted to a spec-set: writing `resolve(d_j, σ_j)` for that ASN's recovery of the I-address runs under `σ_j`, `ρ(R, Σ)` is the union over `j` of the I-addresses those runs name. The one divergence: `resolve` is defined only for a *well-formed content reference* — one in which every depth-`m` position of `⟦σ_j⟧` is active in `d_j`'s arrangement — whereas `ρ` filters to the currently-active positions … and so resolves *partial* spans as well"

**Problem**: The correspondence claim and its qualification are both imprecise. ASN-0058's `resolve` is defined only on a ContentReference, whose conditions include (iii) `#ℓ = #u = m` with `m` the common arrangement depth (S8-depth) — a condition this ASN explicitly drops two sentences earlier ("Note what `wf` does *not* require: that `#u_j` equal the common depth S8-depth fixes…"). For a depth-mismatched spec — exactly the input `wf` admits and the preceding prose works through with the `[1,1]`-bounds-depth-3 example — `resolve(d_j, σ_j)` is undefined (the spec is not a ContentReference at all), so "ρ is the union of the I-addresses those runs name" has no referent there, and the divergence is not "one": ρ extends `resolve` along two independent axes (partiality of the span's active positions, and depth mismatch between spec and arrangement; condition (i) `V_{u₁}(d_s) ≠ ∅` is dropped as well). The gloss of "well-formed content reference" as just the activity condition mischaracterizes the foundation's definedness domain. In a spec headed for formalization, a foundation-correspondence statement with the wrong scope is the kind of sentence that gets transcribed into a false lemma.

**Required**: Scope the correspondence correctly — e.g., "where `resolve` is defined (the spec is an ASN-0058 ContentReference and every position in range is active), ρ's per-spec contribution coincides with the I-addresses `resolve` names; ρ extends it to partial and depth-mismatched specs via the active-position filter" — and drop or correct "the one divergence." One- or two-clause fix; no claim content changes.

## OUT_OF_SCOPE

### Topic 1: Link retirement / un-making
**Why out of scope**: ML7 correctly notes the transition vocabulary contains no link-removing operation and that a retirement facility would be a model extension. That is a future-ASN decision, not a gap here.

### Topic 2: Direct I-address endset arguments (ghost/foreign endsets)
**Why out of scope**: The ASN explicitly restricts MAKELINK-via-V-specs to content-backed endsets and defers the I-address argument shape; reaching L4/L9's full generality is new territory, consistent with the ghost-restriction paragraph.

### Topic 3: Semantics of the empty one-sided link and link-subspace endset arguments
**Why out of scope**: Both are correctly carried as Open Questions; the ASN settles everything operationally needed (definedness, L3-legality, inertness in ML9) without prejudging the deferred semantics.

The rest of the ASN holds up under detailed checking: the recovery equation's F-trace motivation (frontier leak) is sound and the interior-overreach case is correctly disposed of; the extensional coverage form follows from LP-Fin Corollary in both directions; the empty-resolution boundary is settled once with acceptable cross-references from ML5/ML6 (the prior consolidation did its job); ML6's necessity-and-sufficiency for L3 is a genuine two-direction discharge; ML9's wp handles the home-document boundary case and the partial-operation definedness conjunct properly; and the worked example exercises ML0, ML1, ML2's merge legality (including the failure case when only `a₁` is resolved), and all four discoverability outcomes including non-discoverability from the home. No anti-bloat findings rise to flag level — the design-derivation passages (why not store V-positions, why F rather than the store) are generative reasoning, not meta-prose.

VERDICT: REVISE
