# Review of ASN-0051

## REVISE

### Issue 1: SV11 block decomposition scope in the two-subspace model
**ASN-0051, Partial Survival**: "Since B covers only text-subspace V-positions (ASN-0058's block decomposition is defined for the text-subspace arrangement), define the *text-subspace projection* π_text(e, d) = coverage(e) ∩ ran_text(M(d)), where ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ subspace(v) = s_C} = ⋃_k I(β_k)."

**Problem**: The equality `ran_text(M(d)) = ⋃_k I(β_k)` requires the block decomposition to cover exactly content-subspace V-positions. But ASN-0058's B1 condition is `v₁ ≥ 1`, which in the extended model (ASN-0047) includes both content-subspace (`v₁ = s_C`) and link-subspace (`v₁ = s_L`) V-positions, since SC-NEQ gives `s_C ≥ 1` and `s_L ≥ 1`. ASN-0058's informal description says "text-subspace," which in ASN-0036 means `v₁ = 1`, but B1's formal condition `v₁ ≥ 1` is strictly broader. If the decomposition includes link-subspace blocks, `⋃_k I(β_k)` contains link I-addresses and the equality with `ran_text(M(d))` fails.

**Required**: Either (a) explicitly restrict the block decomposition to content-subspace by defining B as the maximally merged decomposition of the restriction `M(d)|_{V_{s_C}(d)}` — which satisfies C1a's conditions (functionality from S2, finiteness from S8-fin, fixed depth from S8-depth within subspace s_C) — or (b) add a one-sentence justification for why ASN-0058's v₁ ≥ 1 is read as v₁ = s_C in the extended model.

### Issue 2: SV7 conflates discovery mechanism with valid composite construction
**ASN-0051, Link Discovery**: "What SV7 captures is the *absence of coupling constraints*: no K.ρ (provenance recording), no link-store operation, and no additional elementary transition is required for d₂ to inherit all of a's link associations. K.μ⁺ alone suffices..."

**Problem**: "K.μ⁺ alone suffices" and "no K.ρ... is required" are true for the discovery mechanism (discover_s operates on coverage and dom(L), both independent of R), but a valid composite transition that includes K.μ⁺ placing a new I-address into d₂'s content-subspace arrangement *does* require K.ρ, via J1★ (ExtensionRecordsProvenanceContent, ASN-0047). The ASN later says SV7 is "not formally stronger than SV8," which clarifies intent, but the initial statement could lead a reader to conclude the composite transition needs no K.ρ step.

**Required**: Add a sentence noting that J1★ may require K.ρ as part of a valid composite, but K.ρ does not affect the discovery result (it modifies R, not L or M), so the discovery mechanism is coupling-free even when the composite is not.

### Issue 3: SV11 fragment overlap under within-document sharing
**ASN-0051, Partial Survival**: "Therefore π_text(e, d) decomposes into finitely many *fragments*, each a contiguous ordinal subsequence within some mapping block's I-extent"

**Problem**: When M(d) is non-injective (within-document sharing, S5), two blocks can have overlapping I-extents — e.g., β₁ = (v₁, a, 3) and β₂ = (v₄, a, 2) give I(β₁) ∩ I(β₂) = {a, a+1} ≠ ∅. If these shared I-addresses lie in coverage(e), they appear in fragments from both blocks. The set-union formula `π_text(e, d) = ⋃_{j,k} (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))` is correct (set union is idempotent), but "decomposes into fragments" suggests a partition. The m · p bound counts fragment *objects* (per-block), not distinct I-addresses — summing fragment widths would overcount.

**Required**: Add a note that fragments from distinct blocks may share I-addresses when M(d) is non-injective, so the fragment collection is a cover of π_text(e, d), not necessarily a partition. Alternatively, restrict the fragment definition to the maximally merged decomposition (unique by M12), which doesn't prevent I-extent overlap but at least pins the block set.

## OUT_OF_SCOPE

### Topic 1: Fork vitality preservation
**Why out of scope**: The ASN correctly lists this in open questions. J4 (ForkComposite) gives `ran(M'(d_new)) ⊆ ran(M(d_src))`, so projection can only shrink — bilateral vitality in d_src does not guarantee bilateral vitality in d_new. Characterising when forks preserve vitality requires constraints on which arrangement entries the fork copies, which is a versioning question beyond this ASN.

### Topic 2: Formal byte-level allocation closure
**Why out of scope**: The ASN's remark on same-origin coverage growth honestly identifies that byte-level closure "follows from allocation discipline assumptions not formalised in this ASN." Formalising sequential allocation discipline (sibling-only increment within the element ordinal, no child-spawning within content allocation) belongs in an allocation discipline ASN, not here. The architectural analysis (Nelson citations, Gregory's implementation) is appropriate evidence at this stage.

### Topic 3: Link-subspace contribution to projection
**Why out of scope**: The ASN explicitly defers link-subspace fragment structure to the Link Subspace ASN. The definitions (π, locate, vitality) are intentionally general — they include link-subspace I-addresses — which is correct. The detailed analysis of how L13 (ReflexiveAddressing) and CL-OWN (LinkSubspaceOwnership) interact with projection is new territory.

VERDICT: REVISE
