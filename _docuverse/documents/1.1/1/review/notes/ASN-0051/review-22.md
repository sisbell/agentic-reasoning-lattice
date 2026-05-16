# Review of ASN-0051

## REVISE

### Issue 1: SV0 is a definitional unfolding presented as a theorem

**ASN-0051, "Endset Projection" section, SV0 (ResolutionCurrentness)**: "locate(e, d) is determined entirely by coverage(e) and the current M(d)"

**Problem**: The definition of locate(e, d) is `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`. The claim SV0 makes is essentially restating this definition — locate explicitly takes only coverage(e) and M(d) as inputs. The "proof" argues that the link doesn't store V-addresses, but this is a consequence of the definition, not a substantive theorem.

**Required**: Either (a) reframe as a clarifying observation following from the definition, (b) strengthen to a substantive system-architectural claim (e.g., "no conforming implementation can produce different locate values for the same coverage and M(d)"), or (c) drop SV0 as it adds no new content beyond the definition.

### Issue 2: SV6's proof requires explicit handling of the zeros(t) = 3 constraint

**ASN-0051, "Content Allocation and Coverage Stability" section, SV6 (CrossOriginExclusion) proof**: "For any element-level t with zeros(t) = 3, this means t has exactly three field separators at the same positions as s"

**Problem**: The proof establishes that t (in the span) agrees with s on positions 1..k-1, hence has zeros at s's zero positions p₁, p₂, p₃. For t's field decomposition to match s's, t must additionally have *no other zeros* at positions k..#t. This step relies on zeros(t) = 3 forcing exactly three zeros globally, not just at positions ≤ k-1. The proof implicitly assumes this but doesn't make it explicit.

**Required**: Add explicit argument: "Since zeros(t) = 3 (by hypothesis) and t already has zeros at p₁, p₂, p₃, t has no other zeros at any position. Therefore t's field separator positions are exactly p₁, p₂, p₃, identical to s's."

### Issue 3: SV11 conflates "fragment" definition with decomposition terms

**ASN-0051, "Partial Survival" section, SV11 (PartialSurvivalDecomposition)**: The fragment definition specifies "F is *maximal* with respect to extending j₁ downward or j₂ upward within π_text(e, d) ∩ I(β_k)", but the decomposition formula `π_text(e, d) = ⋃_{j,k} (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))` yields up to m · p terms that are contiguous but not necessarily maximal.

**Problem**: Two terms ⟦(s₁, ℓ₁)⟧ ∩ I(β_k) and ⟦(s₂, ℓ₂)⟧ ∩ I(β_k) for the same block β_k may be adjacent and coalesce into one maximal fragment. So the count of decomposition terms (≤ m · p) may exceed the count of true fragments (per the formal definition). The prose treats these as the same thing.

**Required**: Distinguish "decomposition terms" (≤ m · p bound) from "fragments" (maximal subsequences, possibly fewer). Either rename one consistently or add explicit relationship between them.

### Issue 4: SV1 and SV12 are foundation citations, not new theorems

**ASN-0051, "The Frame of Link Permanence" section, SV1**: cites L12 (ASN-0043)
**ASN-0051, "Content Fidelity" section, SV12**: cites S0 (ASN-0036)

**Problem**: Both claims are restatements of foundation invariants. SV1's "proof" is just stating L12; SV12's is just stating S0. Yet they're labeled as SV claims alongside substantive theorems like SV2–SV11.

**Required**: Either label these as corollaries of foundation invariants, restructure their content into framing prose around the substantive SVs, or drop the SV labels and cite the foundation invariants directly where needed.

### Issue 5: Empty endset edge cases under-treated

**ASN-0051, "Endset Projection" section, Bilateral Vitality definition**

**Problem**: The case `F = ∅ ∧ G = ∅` is explicitly addressed as vacuous bilateral vitality. But the asymmetric cases (`F = ∅, G ≠ ∅` and `F ≠ ∅, G = ∅`) are handled only implicitly by the disjunction structure. Additionally, the projection/discovery behavior for empty endsets is not stated: `coverage(∅) = ∅`, so `π(∅, d) = ∅` and `discover_s(A)` excludes links whose endset at s is empty (since ∅ ∩ A = ∅). These corner cases warrant brief explicit treatment.

**Required**: Add a brief paragraph after the BilateralVitality definition covering: (a) asymmetric empty cases reduce to vitality of the non-empty endset; (b) `π(e, d) = ∅` whenever e = ∅; (c) a link with all content endsets empty (only Θ populated) is bilaterally vital everywhere but resolves to nothing.

### Issue 6: K.μ⁺_L's interaction with link-referencing endsets needs depth

**ASN-0051, "Extension Preserves and May Enlarge" section, SV2**

**Problem**: SV2 covers K.μ⁺_L alongside K.μ⁺ via a single monotonicity claim. But K.μ⁺_L has distinct semantics — it adds a link-subspace mapping `v_ℓ ↦ ℓ` where ℓ is a link address (per L13/L4, endsets may reference link addresses). The ASN doesn't explicitly examine:
- When does coverage(e) contain link addresses?
- How does locate(e, d) handle V-positions in the link subspace?
- Is the projection uniformly defined across both subspaces, or does π_text in SV11 implicitly exclude link-subspace contributions?

SV11 explicitly notes "The full projection π(e, d) ... may additionally include I-addresses reached through link-subspace V-positions" and defers to a future ASN. But SV2 lumps K.μ⁺ and K.μ⁺_L together without addressing the asymmetry.

**Required**: Either (a) split SV2 into separate claims for K.μ⁺ (text-subspace extension) and K.μ⁺_L (link-subspace extension), making the link-coverage case explicit; or (b) add a note clarifying that the projection treatment in SV2 is uniform across subspaces, with concrete acknowledgment of what locate(e, d) returns when coverage(e) contains link addresses.

### Issue 7: K.λ's effect on existing links not explicit

**ASN-0051, "The Complete Guarantee" section, SV13 clause (e)**: "All other elementary transitions (K.α, K.δ, K.λ, K.ρ) preserve M in their frame, so locate(e, d) is unchanged."

**Problem**: This is correct but glosses over K.λ's dual nature: it preserves locate for existing links (since M is in frame) but creates a new link whose discoverability is governed by SV9. The relationship is mentioned only implicitly via SV9's "new links may be created" clause. A reader following SV1–SV13 in order won't see K.λ's complete behavior characterized in one place.

**Required**: Add explicit statement in SV13 or an SV between SV7 and SV8: "K.λ holds M in frame, so existing links' projection and resolution are unchanged. The new link's coverage is fixed at creation by K.λ's effect, and its discoverability follows from SV8 onward."

### Issue 8: wp analysis is implicit but not stated

**ASN-0051, throughout SV2–SV5 and SV11**

**Problem**: The ASN reasons forward from transitions to their effects on π and locate. Weakest precondition analysis would ask: given a desired postcondition (e.g., `π(e, d) ≠ ∅` after K.μ⁻, or "link discoverable through d after fork"), what must hold before? The ASN's "vitality loss condition" prose (in SV3 discussion) is essentially `wp[K.μ⁻](π(e, d) = ∅)`, but isn't labeled as such. The non-trivial cases — wp for partial survival, wp for discoverability preservation across fork — aren't computed.

**Required**: Add a brief wp section or fold wp reasoning into existing claims, particularly: (a) `wp[K.μ⁻](π(e, d) ≠ ∅)` = "the contraction does not remove all of coverage(e) ∩ ran(M(d))"; (b) `wp[fork(d_src, d_new)](∀a ∈ ran(M(d_src)) : a ∈ discover_s(ran(M(d_new))))` = "the fork's K.μ⁺ step shares all I-addresses with d_src".

## OUT_OF_SCOPE

### Topic 1: Operational semantics of link discovery (indexing, latency)

**Why out of scope**: Discovery efficiency, indexing structures, and latency guarantees belong in operational/implementation ASNs. The current ASN correctly focuses on invariant-level discovery behavior (SV8, SV9).

### Topic 2: Forking semantics (J4) detailed treatment

**Why out of scope**: J4 is referenced as a foundation invariant from ASN-0047. The ASN appropriately defers detailed fork-survival analysis to that ASN's domain, mentioning only that the same discovery reasoning applies (SV7).

### Topic 3: Dormant link reactivation and operational lifecycle

**Why out of scope**: The Open Questions section flags this as future work. A "dormant link" (vital in no document) is well-defined by the current invariants; mechanisms to "reactivate" it (e.g., re-importing content into some document) are operational and belong in a future ASN.

### Topic 4: Within-document sharing semantics for projection

**Why out of scope**: The ASN correctly observes |locate(e, d)| ≥ |π(e, d)| under S5 (UnrestrictedSharing) and notes the cover-not-partition consequence in SV11. Detailed analysis of multi-occurrence resolution belongs in a future ASN focused on within-document sharing.

VERDICT: REVISE
