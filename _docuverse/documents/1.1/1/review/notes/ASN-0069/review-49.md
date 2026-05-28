# Review of ASN-0069

## REVISE

### Issue 1: V4b's derivation invokes V6 with an unstated chain through S3★-aux

**ASN-0069, V4b structural support paragraph**: "K.ρ does not modify arrangements. By V6 every position in `dom(M'(d_new))` lies in the content subspace, so: V4b"

**Problem**: V6 alone (`V_{s_L}(d_new) = ∅`) does not establish "every position in dom(M'(d_new)) lies in the content subspace". That conclusion requires also invoking S3★-aux (SubspaceExhaustiveness, ASN-0047) — "every v ∈ dom(M(d)) has subspace s_C or s_L" — to conclude by elimination that every position must be in subspace s_C. S3★-aux is not cited here and does not appear in the Dependency Audit.

**Required**: Either cite S3★-aux explicitly (and add to Dependency Audit), or replace the V6 appeal with the more direct K.μ⁺ amendment (KMuPlusContentSubspaceRestriction, ASN-0047) — already implicitly referenced via ValidComposite★'s "K.μ⁺ (amended)" — which requires `subspace(v) = s_C` for all new V-positions added, yielding the content-subspace conclusion in one step without indirection.

### Issue 2: V11a's prefix-chain derivation is over-elaborated

**ASN-0069, V11a "Derivation of prefix chain"**: Uses an outer induction on chain length k (base from V2, step from V2 + transitivity composing IH `d_src ≼ d^k_new`) to establish `d_src ≼ d^k_new`, then an inner induction on `k − i` (base from reflexivity, step from V2 + transitivity composing IH `d^{i+1}_new ≼ d^k_new`) to establish `d^i_new ≼ d^k_new` for each intermediate i.

**Problem**: After transitivity of ≼ is established at the opening, the full chain `d_src ≼ d¹_new ≼ ... ≼ d^k_new` follows directly from k applications of V2 (one per chain step) plus transitivity composed `k − 1` times. The two named inductions formalize what is a direct conjunction. The inner induction is structurally identical to the outer one with different bookkeeping.

**Required**: State the chain as the direct conjunction `d_src ≼ d¹_new` (V2 at step 1) ∧ `d¹_new ≼ d²_new` (V2 at step 2) ∧ ... composed via transitivity. The recovery argument (Length identity + Prefix identity + T3) is the substantive content and remains as written.

### Issue 3: V9a's parenthetical excursion is tangential to its main claim

**ASN-0069, V9a**: "via direct allocation (if `origin(a) = d_new`, which cannot occur in a fresh fork: by V3, `C' = C`, so the inherited I-addresses are exactly those already in `dom(C)` before the fork, none of which can have `origin(a) = d_new` because `d_new ∉ E_doc` pre-fork means `A_C(d_new)` had not been activated by SubAllocatorAxiom and so had emitted nothing into `dom(C)` prior to the fork)"

**Problem**: V9a's primary claim is that provenance records containment, not derivation path. The parenthetical asserts a separate, distinct fact about content sub-allocator activation timing. The two are independently true but the parenthetical interrupts V9a's sentence mid-enumeration of acquisition paths, mixing two claims that would each benefit from standalone statement.

**Required**: Either promote the activation-timing observation to a separate corollary (e.g., V9b — "fresh forks inherit only externally-allocated I-addresses"), or move it to a footnote, separating V9a's containment-vs-derivation claim from the fresh-allocator observation.

### Issue 4: Worked example "vignette point" labels lack prior definition

**ASN-0069, Worked Example "Empty source (V7)" paragraph**: Uses inline labels "vignette point (i)", "vignette point (ii)", "vignette point (iii)", "vignette point (iv) first half", "vignette point (iv) second half" as mid-sentence annotations.

**Problem**: The labeling convention is unusual and not introduced anywhere in the ASN. The reader must infer from context that these labels enumerate properties being verified against the empty-source case. Without prior definition, the labels read as opaque trailing annotations whose role is ambiguous.

**Required**: Either enumerate the four points up front before the paragraph (e.g., "We verify four properties: (i) M' initialises empty, (ii) R unchanged, (iii) V9 vacuous, (iv) V6 via emptiness") with the inline labels referring back, or restructure the paragraph as a bulleted enumeration.

## OUT_OF_SCOPE

None. The ASN's Open Questions section appropriately flags future-work topics (concurrent modification, snapshot vs living, transcludent sources, version-space coherence, source-deletion-after-fork) without trying to address them.

VERDICT: REVISE
