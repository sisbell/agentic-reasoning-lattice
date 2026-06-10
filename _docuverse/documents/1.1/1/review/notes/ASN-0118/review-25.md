# Review of ASN-0118

I worked the proofs carefully — the resolution grounding (CP0), the composite decomposition (K.μ⁻ + K.μ⁺ + K.ρ), the three-branch provenance discharge, the tiling arithmetic, and the worked example. The core is sound: the displacing-case composite is faithful (K.μ⁺ cannot vacate a position, so contraction-then-extension is the right shape), the J0/J1★/J1'★ couplings are discharged correctly initial-to-final, the three provenance branches are exhaustive and each reachable, and the wp for link discoverability is genuinely non-trivial and correctly pulled back. The findings below are precision, one elided derivation, and the meta-prose the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: CP7(c) states prior-content link survival without the LP12 chain CP7(b) is careful to supply
**ASN-0118, "Survival of links anchored to the reused content"**: "Third, links anchored to the destination's *prior* content survive untouched, because that content's I-addresses are unchanged by the displacement (CP3) — the strap stays on the same bytes even as their V-positions slide forward."

**Problem**: CP7(b) derives discoverability the right way — placed addresses enter `ran(Σ'.M(d))`, then LP12 at the post-state with `Σ'.L = Σ.L`. CP7(c) makes the parallel claim for *prior* content in one clause and stops at "I-addresses unchanged." The actual obligation is two steps the reader must supply: (i) the displaced images are retained in the range — `a = Σ.M(d)(v) = Σ'.M(d)(v+W) ∈ ran(Σ'.M(d))` by CP3a — and (ii) LP12 then preserves discoverability since coverage is unchanged. "I-addresses unchanged" alone does not reach "links survive"; it needs the range-membership fact plus LP12. Depth is mandatory, and CP7(b) sets the standard for this very claim.

**Required**: State the range-preservation step (`ran(Σ'.M(d)) ⊇ {Σ.M(d)(v) : v ∈ V_{s_C}(d)}` via CP3a/CP3b) and invoke LP12 explicitly, as CP7(b) does.

### Issue 2: bare S3 (ASN-0036) cited for post-state referential integrity where S3★ (ASN-0047) governs
**ASN-0118, "The transclusion frame"**: "referential integrity (S3) demands its image lie in the content store, `cᵢ ∈ dom(Σ'.C)`" — and **"The substrate we build on"**: "whose every image lies in the content store (S3 ReferentialIntegrity)".

**Problem**: COPY operates in ASN-0047's extended state (it uses K.μ⁻, K.ρ, `Σ.R`, the link subspace, P4★, and cites S3★ in CP0(a)). In that state S3★ *supersedes* S3, and bare S3 — "*every* image lies in the content store" — is false for `s_L` positions (whose images lie in `dom(Σ.L)`). The conclusion `cᵢ ∈ dom(Σ'.C)` is correct only because the binding is at an `s_C` position; it is licensed by S3★'s `s_C` branch, not by the superseded ASN-0036 S3. The note already uses S3★ correctly in CP0(a), so the bare-S3 citations are slips.

**Required**: Cite S3★ (its `s_C` branch) consistently for the extended-state referential-integrity steps, or note explicitly that the strand-model S3 is being read through its S3★ refinement.

### Issue 3: defensive and comparison meta-prose in CP0(a)
**ASN-0118, CP0(a)**: "The interior addresses `aⱼ + k` are covered because that grounding identifies each with the image of the bound position `vⱼ + k`, not left as bare arithmetic on `aⱼ`. The conclusion coincides with ASN-0058 C1 (ResolutionIntegrity); here it is grounded in S3★ over the bound subset, per the resolution basis fixed above."

**Problem**: The grounding paragraph immediately before CP0 already establishes "every `cᵢ` the flat sequence lists, run-leading **or interior**, is the image of a bound active position." The first sentence here re-states that with a defensive tail ("not left as bare arithmetic on `aⱼ`") that answers an anticipated objection rather than advancing the argument. The second sentence is a coincidence-with-C1 note plus a back-reference ("per the resolution basis fixed above") — neither moves the proof. This is the anti-bloat finding-residue and use-of-foundation-comparison pattern.

**Required**: Delete the defensive clause and the C1-coincidence sentence; the per-position grounding sentence already discharges CP0(a) via S3★.

### Issue 4: modeling-choice meta-commentary in the content-residence precondition and the resolution prose
**ASN-0118, precondition "content residence"**: "This promotes the resolution section's "content spec-set" restriction to an explicit precondition of the operation. By content-residence every active position is in `s_C`, so S3★ gives each resolved `cᵢ ∈ dom(Σ.C)` (CP0(a)), and the destination bindings of CP2 land content addresses in content-subspace positions (S3★ in the post-state)." And **"What a spec-set names"**: "We reuse ASN-0058's construct rather than reinvent it."

**Problem**: "This promotes the … restriction to an explicit precondition" is commentary on the modeling move, not content of the precondition. The following sentence is a use-site inventory enumerating downstream consumers (CP0(a), CP2) before they are reached — the "definition's introduction enumerates downstream consumers" pattern. "We reuse ASN-0058's construct rather than reinvent it" is a bare modeling-choice aside; the sentence before it already establishes that a V-spec *is* an ASN-0058 ContentReference, which is the substantive content. These are skip-past sentences.

**Required**: State the precondition (`(A ρ ∈ R, v ∈ act(ρ, Σ) : subspace(v) = s_C)`) and let CP0(a)/CP2 cite it where they use it; drop the consumer inventory and the "reuse rather than reinvent" aside.

## OUT_OF_SCOPE

### The five Open Questions are correctly deferred, not gaps in this ASN
Partial-binding width shortfall vs. nominal extent, level-uniformity across mixed-depth source spans, conditions for later loss of discoverability, the correspondence relation across appearances, and link-subspace transclusion are all genuine future territory. COPY is well-defined and invariant-preserving on whatever the boundaries bind (`W = |resolve(R,Σ)|`); none of these questions is needed for the operation's correctness, and the ASN is right to list them rather than answer them here.

### One observation, not a required fix
The abutting-of-ranges arithmetic (`(min+i)+W = min+(i+W)` via TS3 / Extended Associativity) is derived inline in the displacing-case composite *and* again, more elaborately, in "The destination's prior arrangement is preserved." The two overlap on contiguity; the latter additionally carries the disjointness/no-double-binding (S2, CP3c) argument, so it is not pure duplication. Worth consolidating the shared contiguity step if a future cycle touches either section, but I am not flagging it as a defect.

VERDICT: REVISE
