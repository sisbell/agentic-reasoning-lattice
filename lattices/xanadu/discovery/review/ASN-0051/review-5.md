# Review of ASN-0051

## REVISE

### Issue 1: SV6 implicit element-level precondition on span start
**ASN-0051, SV6 (CrossOriginExclusion)**: "For a span (s, ℓ) in an existing endset and a newly allocated address b with origin(b) ≠ origin(s), when the action point of ℓ falls within the element field"
**Problem**: The proof uses `origin(s)`, which requires `s` to be element-level (`zeros(s) = 3`, per the origin definition in ASN-0036). The phrase "action point within the element field" implicitly requires `s` to have an element field, hence to be element-level — but this is never stated as a precondition. Since L4 (EndsetGenerality) permits endset spans with non-element-level starts, the claim needs to explicitly restrict to element-level `s`. Without this, a reader could wonder whether SV6 applies to a span starting at a document-level tumbler (`zeros(s) = 2`), where `origin(s)` would be ill-formed.
**Required**: Add explicit precondition `zeros(s) = 3` (element-level start), or equivalently state that both `s` and `b` are element-level tumblers and that the action point falls beyond the third field separator of `s`.

### Issue 2: SV3 asymmetric resolution treatment
**ASN-0051, SV3 (ContractionReduction)**: States `π_{Σ'}(e, d) ⊆ π_Σ(e, d)` but omits the resolution claim.
**Problem**: SV2 includes an explicit "For resolution" paragraph proving `resolve_Σ(e, d) ⊆ resolve_{Σ'}(e, d)` for extension. SV3 has no corresponding paragraph for contraction. SV13(e) later claims "Contraction of M(d) can only shrink resolve(e, d)" without derivation. The argument is straightforward (`v ∈ resolve_{Σ'}(e, d)` implies `v ∈ dom(M'(d)) ⊂ dom(M(d))` with `M'(d)(v) = M(d)(v) ∈ coverage(e)`, giving `v ∈ resolve_Σ(e, d)`), but by the standard the ASN sets in SV2, it should be stated.
**Required**: Add a "For resolution" paragraph to SV3 parallel to SV2's.

### Issue 3: SV7 is a definitional tautology
**ASN-0051, SV7 (DiscoveryByContentIdentity)**: The formal statement asserts that if `{M(d₁)(v) : v ∈ V₁} = {M(d₂)(v) : v ∈ V₂}`, then `discover_s` applied to both yields the same result.
**Problem**: This is `f(A) = f(B)` when `A = B` — a property of all functions, not a specific property of the discovery function. The conceptual point (discovery depends on content identity, not document identity) is valid, but it is a consequence of how `discover_s` was *defined* (parameterised by I-addresses rather than by document-V-region pairs), not a theorem derivable from the system's axioms. Labeling it as a named property and including it in the properties table inflates the formal content.
**Required**: Either reframe SV7 as a definitional observation / design remark (removing it from the formal properties table), or strengthen the formal statement to express a non-trivial consequence — for example, formalising the transclusion discovery guarantee: that `K.μ⁺` mapping a V-position in `d₂` to an I-address `a ∈ ran(M(d₁))` immediately makes all links discoverable through `d₁`'s content also discoverable through `d₂`, with no additional coupling step required.

### Issue 4: SV13(e) imprecise about reordering and resolution
**ASN-0051, SV13(e)**: "Reordering of M(d) preserves π(e, d) but changes resolve(e, d). [SV5]"
**Problem**: The unqualified "changes" implies reordering *always* changes resolution. SV5 in the body correctly says "resolve_{Σ'}(e, d) ≠ resolve_Σ(e, d) in general." The worked example confirms this qualifier is needed: the swap of v₂ ↔ v₄ (both mapping to I-addresses within coverage(F)) leaves the resolution set {v₂, v₄} unchanged. The first two bullets of SV13(e) use directional bounds that allow for no change ("can only enlarge," "can only shrink"); the third bullet should follow the same pattern.
**Required**: Change to "may change resolve(e, d)" to match SV5's "in general" qualifier and the worked example's evidence.

### Issue 5: SV13(f) blends proved and architectural claims
**ASN-0051, SV13(f)**: "Same-origin coverage growth depends on the allocation regime — closed at the byte level by sequential sibling allocation, open at broader address levels by design."
**Problem**: SV6 (cross-origin exclusion) is formally proved from the foundations. The byte-level closure claim is not — it is argued from Nelson's design intent ("append-only storage system" [LM 2/14]) and Gregory's allocator implementation (`tumblerincrement(&lowerbound, rightshift=0, 1, isaptr)`). The body section correctly labels this as "architectural, not definitional." But SV13, labeled "SurvivabilityTheorem," presents both claims side by side as components of "the complete guarantee," obscuring which parts are formally established and which rest on architectural assumptions outside the current axiom set.
**Required**: In SV13(f), explicitly mark the boundary: state the proved claim (SV6, cross-origin exclusion) separately from the architectural observation (byte-level closure by allocation discipline). A parenthetical like "(the byte-level closure follows from allocation discipline assumptions not formalised in this ASN)" would suffice.

## OUT_OF_SCOPE

### Topic 1: Allocation regime formalisation for byte-level coverage closure
**Why out of scope**: The current foundations (T8, T9, T10a) describe allocation in general terms. Proving that same-origin coverage growth cannot occur at the byte level would require a formal invariant constraining text-content allocation to sibling increment exclusively — a new axiom about the allocation regime, not an error in this ASN.

### Topic 2: Link-subspace V-positions and their effect on projection
**Why out of scope**: SV11 explicitly restricts to text-subspace projection and defers the link-subspace contribution. The ASN correctly notes that no currently defined operation creates non-text V-positions, so the restriction is non-lossy for all reachable states. Extending to link-subspace V-positions is new territory for a future Link Subspace ASN.

### Topic 3: Cross-document fragment ordering guarantees
**Why out of scope**: The ASN asks in its open questions whether there is a canonical ordering of fragments that all implementations must respect. This is a legitimate design question for a future ASN on resolution presentation, not a gap in the current survivability analysis.

VERDICT: REVISE
