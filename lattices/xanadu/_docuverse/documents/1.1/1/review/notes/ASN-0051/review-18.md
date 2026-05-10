# Review of ASN-0051

## REVISE

### Issue 1: SV7 scope is misleadingly narrow
**ASN-0051, TransclusionCouplingAbsence**: "This architectural property — that transclusion inherits link discoverability without coupling — is *stronger* than SV8 for K.μ⁺/K.μ⁺_L transitions: SV8 gives ⊆ (monotonicity) for arbitrary transitions; SV7 gives = (invariance) for arrangement extensions specifically."
**Problem**: The equality `discover_s(A) in Σ' = discover_s(A) in Σ` holds for *every* elementary transition that holds L in frame — which is all of K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, and K.ρ. The only transition where SV8's ⊆ can be strict is K.λ (which adds a new link). The proof uses nothing specific to K.μ⁺/K.μ⁺_L — it depends solely on L being in frame. Stating the result only for K.μ⁺/K.μ⁺_L and calling it "stronger than SV8 for K.μ⁺/K.μ⁺_L transitions" implies that the equality is specific to these transitions, when in fact K.λ is the sole exception.
**Required**: Either generalize SV7 to all L-preserving transitions (equivalently, all elementary transitions except K.λ), or add a sentence noting the broader scope: "The same equality holds for all elementary transitions except K.λ; we highlight K.μ⁺/K.μ⁺_L because the transclusion application is the architecturally significant case."

### Issue 2: SV13(g) and properties table inconsistent with SV11's cover qualification
**ASN-0051, SurvivabilityTheorem (g)**: "the surviving text-subspace projection in any document decomposes into finitely many ordinal-contiguous fragments within mapping blocks"
**Problem**: SV11's body explicitly establishes that fragments form a *cover*, not a partition, of π_text(e, d) — due to non-injective arrangements (S5) where distinct blocks share I-addresses. The sentence "The fragment collection is therefore a *cover* of π_text(e, d), not necessarily a partition; summing fragment widths may overcount distinct I-addresses" appears in SV11. Yet SV13(g) and the SV11 row in the properties table both say "decomposes" without this qualification. In mathematical usage "decomposes" often implies partition, and a reader relying on SV13 alone could incorrectly assume disjointness.
**Required**: Qualify SV13(g) and the SV11 properties-table entry to say "covers" or "decomposes (as a cover, not necessarily a partition)," consistent with SV11's explicit discussion.

### Issue 3: SV6 parenthetical about T5 is confusing
**ASN-0051, CrossOriginExclusion proof**: "(T5 provides supporting context: since origin(s) is a prefix of both s and s ⊕ ℓ, every t in the interval satisfies origin(s) ≼ t — but the prefix property alone does not force the separator positions to align, which is what the sandwich argument above establishes.)"
**Problem**: This parenthetical introduces T5 and immediately says it is insufficient. A reader may wonder whether T5 plays any role in the proof (it does not — the sandwich argument is self-contained). The effect is to distract from the actual proof mechanism.
**Required**: Either remove the parenthetical entirely (the proof stands without it) or rephrase to clearly separate it from the proof chain, e.g., as a post-proof remark: "Note: T5 gives the weaker result origin(s) ≼ t for every t in the interval, but this prefix containment does not force separator positions to align — the sandwich argument above establishes the stronger claim."

## OUT_OF_SCOPE

### Topic 1: Same-origin coverage growth formalization
**Why out of scope**: The ASN correctly identifies that byte-level span closure depends on allocation discipline (sequential sibling increment), which is an architectural property not formalized in any current foundation ASN. Formalizing this requires an allocation-discipline ASN that constrains how allocators produce addresses within a document, and would give a same-origin analogue of SV6. The ASN's informal analysis (referencing Gregory's green allocator and Nelson's append-only Istream) is honest about the gap.

### Topic 2: Link-subspace contribution to projection
**Why out of scope**: SV11 restricts to π_text(e, d) and explicitly defers the link-subspace contribution. L13 (ReflexiveAddressing) and L4(c) (cross-subspace endsets) mean endsets can reference link addresses, which would enter π(e, d) through link-subspace V-positions (K.μ⁺_L). This is a natural extension requiring the Link Subspace ASN.

META: The ASN is squarely on-track — it defines survivability in terms of abstract state transitions and proves each claim from the foundation. No drift.

VERDICT: REVISE
