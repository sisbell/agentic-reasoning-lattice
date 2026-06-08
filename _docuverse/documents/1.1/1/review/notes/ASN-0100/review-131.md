# Review of ASN-0100

## REVISE

### Issue 1: "Transfers verbatim" over-reaches the I3 frame
**ASN-0100, §Effect Three (INS.I3-coincide)**: "every per-state property I3 establishes of that arrangement transfers verbatim to M'(d) restricted to those two regions."
**Problem**: INSERT grows `dom(C)` (INS.C), which contradicts ASN-0082's I3-C content frame (`dom(C') = dom(C)`). Some I3 lemmas rest on that frame — notably I3-S7 (PostInsertionAllocationInvariants), which ASN-0082 derives "trivially by I3-C," and I3-S3's inherited proof premise. A *verbatim* transfer of "every" per-state property is therefore false for the content-frame-dependent lemmas. The ASN in fact re-derives S3 (§Referential integrity) and S7 (§Post-state V-position well-formedness) independently, so the blanket universal is both over-strong and redundant with work done elsewhere.
**Required**: Scope the transfer to the content-frame-independent arrangement lemmas actually used (I3-S2, I3-VP, I3-VD, I3-fin), and state explicitly that S3/S7 are re-derived (not inherited) because INSERT violates I3-C.

### Issue 2: π is defined two incompatible ways in INS.proj
**ASN-0100, §Coverage and link discoverability**: first "`π` is the *region-aware shift map* — identity on the Left region (`v < p`) and `shift(·, n)` on the Right region (`v ≥ p`)"; later "Identifying π as the region-aware shift map (identity on Left **and link-subspace contributions**, `shift(·, n)` on Right contributions)."
**Problem**: The first definition partitions only `s_C` positions (Left/Right by `v < p`); link-subspace positions `P_0^{s_L}` are not classified by it, yet π must act on the whole `project(ℓ, i, d, Σ)` including `P_0^{s_L}`. The two statements of π disagree on domain.
**Required**: Give one definition of π covering all three contribution classes (Left, Right, link-subspace) at first use.

### Issue 3: Link/entity frame preservation verified redundantly (anti-bloat)
**ASN-0100, §Link store unchanged vs §Atomicity "Link-store invariants" bullet**: the same conclusion — `L' = L` so L0/L1/L1a/L1b/L1c/L3/L-fin/L12/CL-OWN/CL-UNIQ hold — is established twice, and the L0 content-conjunct subtlety (it ranges over the *growing* `dom(C)`, discharged per-address via the S7 bullet) is re-explained in both places. The entity-set frame (`E' = E`) is likewise re-derived in §Cross-document independence, §Frame Conditions, and the §Atomicity entity bullet.
**Problem**: The per-state-at-intermediates check is the only new content in the §Atomicity bullets; it is buried under restatements of what each invariant constrains and which component it ranges over — an inventory already covered in §Verifying the Invariants. A precise reader must skip the duplicated framing to find the intermediate-state argument.
**Required**: In §Atomicity, state the component-frame inheritance once ("invariants ranging solely over the unmodified L and E inherit from the pre-state at every intermediate"), keep only the genuinely intermediate-specific obligations (S4 at each K.α intermediate, the L0 content-conjunct per-address discharge, P6/P7 at K.α/K.ρ), and drop the per-invariant enumeration that merely repeats §Verifying the Invariants.

### Issue 4: Roadmap meta-prose in structural slots (anti-bloat)
**ASN-0100, §The Operation's Inputs**: "These preconditions are necessary; we shall verify they are jointly sufficient." — and the §Effect One residual-content paragraph ("An empty content subspace … does not entail an empty content store …") is then re-demonstrated wholesale by the "Re-insertion into a cleared content subspace" worked example, which itself announces it is "instantiating the residual-content nuance of §Effect One."
**Problem**: The sufficiency sentence is a promise, not content. The residual-content nuance is stated as essay in §Effect One and again as a full worked example; the example is the right vehicle (concrete), so the §Effect One prose beyond the bare branch-selection rule is redundant narration.
**Required**: Drop the sufficiency-promise sentence. In §Effect One keep only the branch-selection rule (subsequent-emission fires off the persisted frontier when residual `origin = d` content exists); let the worked example carry the demonstration.

## OUT_OF_SCOPE

(none — the Bounding the Scope and Open Questions sections correctly enumerate DELETE/COPY/REARRANGE/link-subspace/version/replication as future work without defining claims for them.)

VERDICT: REVISE
