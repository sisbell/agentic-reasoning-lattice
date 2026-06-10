# Review of ASN-0118

The technical core is sound and unusually careful: the resolution bridge reaches run-interior addresses (not just run leaders); the composite decomposition correctly splits append/empty vs. displacing and fixes both subspaces' retention counts in the K.μ⁻ step; the three-way provenance discharge (J1'★ fresh record / P2 carry-forward / P4★+P2) is exhaustive and the standing composite-boundary precondition that licenses P4★ is stated; the self-transclusion and empty-destination boundaries are handled explicitly. The wp for link discoverability is a genuine non-trivial analysis. I found no correctness gap.

The findings below are (1) one derivation-completeness gap on the hardest invariant, and (2) accreted meta-prose around forward references — the patterns this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: No-gap half of the tiling relies on an uncited multi-step shift identity
**ASN-0118, "The destination's prior arrangement is preserved" (CP3 tiling)**: "Disjointness is ordinal arithmetic, not I3 — shift is strictly order-preserving (ASN-0034, TS1) and a strict advance (`v + W > v`, TS4) ... Their union is the single contiguous run `[min, max+W] = {min + i : 0 ≤ i < N+W}`."
**Problem**: The *disjointness* half is carefully cited (TS1, TS4); the *no-gap* half — that the shifted region `{(min+i)+W : j ≤ i < N}` fills consecutive ordinals `[p+W, max+W]` with no interior hole — is asserted in one sentence. At depth 2 this is trivial (`[1,1+i]+W = [1,1+i+W]`), but the section is stated for general depth (abstract `+`, D-CTG★ is depth-general), where contiguity of the shifted run needs `(min+i)+W = min+(i+W)` (shift composition). That step is uncited. Tiling-without-gaps is the invariant most often hand-waved, and this is exactly where it is. The same uncited no-gap claim recurs in the displacing-case composite ("The resulting text run is the contiguous block `[min, max+W]`, discharging K.μ⁺'s D-CTG★/D-MIN★ precondition").
**Required**: Cite TS3 (ShiftComposition, ASN-0034) / Extended Associativity (ASN-0084) for `(min+i)+W = min+(i+W)`, so the contiguity argument carries the same rigor as the disjointness argument it sits beside.

### Issue 2: The I3-scope caveat is stated and then recapped verbatim
**ASN-0118, "The COPY operation" (CP3a) and "The destination's prior arrangement is preserved"**: CP3a: "from it we borrow, *for the shifted positions*, that they remain well-formed (I3-VP), preserve depth (I3-VD) ... The function-ness, no-holes, contiguity, and sequentiality of COPY's actual `Σ'.M(d)` rest instead on CP3c's domain closure and K.μ⁺'s strict-extension contract." Later: "As CP3a noted, I3 establishes only the *shifted* positions' well-formedness, depth, and finiteness; the function-ness and no-holes ... rest instead on CP3c's domain closure and K.μ⁺'s strict extension."
**Problem**: Two near-verbatim statements of the same scoping fact, the second explicitly flagged as a recap ("As CP3a noted"). The substantive work — distinguishing the I3-VP/I3-VD route (shifted) from the OrdShiftHom route (gap-fill) — is done in the displacing-case composite; these two framings add nothing to it.
**Required**: State the I3 scope once, at the displacing-case derivation where the distinction does work; drop the CP3a-intro and prior-arrangement recaps.

### Issue 3: Content-residence and `act ⊆ V_{s_C}(d_s)` are forward-referenced twice in the resolution section
**ASN-0118, "What a spec-set names, and what resolution recovers"**: "is single-subspace by content-residence (`act(ρ, Σ) ⊆ V_{s_C}(d_s)`, the operation's precondition below) and single-depth by S8-depth"; and later "COPY's content-residence precondition (stated with the operation below) ... confines the resolved domain `act(ρ, Σ) ⊆ V_{s_C}(d_s)` to a *single subspace* directly, and S8-depth (ASN-0036) gives that subspace a *common depth*."
**Problem**: The same not-yet-stated precondition is gestured at twice, each time re-asserting `act ⊆ V_{s_C}` + single-depth-by-S8-depth. Two paragraphs in one section deferring to the same downstream location and stating the same fact.
**Required**: Assert the single-subspace/single-depth consequence once; let the formal precondition statement below carry it.

### Issue 4: CP0's grounding is wrapped in defensive meta-framing
**ASN-0118, "What a spec-set names..." (CP0)**: "That per-position grounding is the bridge CP0(a) leans on — it must reach the *interior* addresses `aⱼ+1, …, aⱼ+(nⱼ−1)` that `expand` produces, not only the run-leading `aⱼ` — so we exhibit it rather than assert it."
**Problem**: The substantive derivation that follows (each `aⱼ+k` is `M(d_s)(vⱼ+k)` for a bound active position, via S8 lockstep) is correct and sufficient. The sentence preceding it is defensive commentary about *why* the proof is shown — it doesn't advance the argument and reads as a reply to a prior reviewer concern.
**Required**: Drop the "the bridge CP0(a) leans on ... so we exhibit it rather than assert it" framing; the interior-address derivation stands on its own.

### Issue 5: CP3c's role ("dischargeable from the postconditions alone") is restated within adjacent sentences
**ASN-0118, "The COPY operation" (CP3c prose)**: "it pins the extent of `d`'s text-subspace domain so that `d`'s per-state invariants are dischargeable from the postconditions alone ... CP3c closes the text-subspace domain to the three disjoint, abutting ordinal ranges ... so each text V-position carries exactly one binding and S2 is dischargeable from the postconditions alone."
**Problem**: "dischargeable from the postconditions alone" appears twice in the same paragraph; the paragraph also threads a forward pointer to the tiling ("given later under prior-arrangement preservation") and a parenthetical CP6 cross-reference. (The I3-V/D-DOM analogy in the same paragraph is legitimate content — flag only the duplication.)
**Required**: State CP3c's domain equation and its single role (S2 dischargeable) once.

## OUT_OF_SCOPE

The five Open Questions (partial-binding width shortfall, mixed source depths, post-removal link undiscoverability, the correspondence relation, link-subspace transclusion) are correctly deferred: none names an invariant COPY's post-state can violate (e.g., heterogeneous I-address depth leaves V-positions uniform-depth, so S8-depth is untouched). No further out-of-scope topics to add.

VERDICT: REVISE
