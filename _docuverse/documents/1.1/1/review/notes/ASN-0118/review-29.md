# Review of ASN-0118

I checked every postcondition derivation against the foundation contracts, re-derived the composite exhibition step by step, and verified the worked example's arithmetic by hand. The findings from the prior cycle (CP3c closure peers; grounding of K.μ⁺'s image-membership and S8a/S8-depth obligations for the placement positions) have been addressed, and I found no remaining defect. The substantive checks:

**Resolution (CP0).** The per-position grounding of `expand` is now complete: run interiors are covered by the lockstep clause (MaximalRun condition 1 / B3 via C1a on restrictions), not just run leaders, so CP0(a) discharges S3★ for every `cᵢ`, not merely the `aⱼ`. The substitution of content-residence for ASN-0058's full-binding condition is legitimate — C1a's general restriction form needs only single-subspace `dom(f)`, which the content-residence precondition supplies directly; the ASN does not lean on C0/C0a/C2, which are the clauses that genuinely require full binding (and the C2 gap is correctly parked as an open question).

**Composite exhibition.** The case split is exhaustive over valid insertion positions (`j ∈ {0..N}`: displacing for `j < N`, append for `j = N`, ValidFirstInsertionPosition when empty). The structural argument that K.μ⁺ cannot vacate a position — forcing the contraction-then-extension decomposition — is correct. K.μ⁻'s per-subspace retention is used correctly: `n'_{s_C} = j < N` supplies the strict contraction, licensing the non-strict `n'_{s_L} = n_{s_L}` that carries CP6's non-text conjunct. The intermediate state Σ₁ obligations check out, including the `j = 0` boundary (D-MIN★ vacuous on the emptied text subspace). The placement-position observation correctly separates the gap-fill positions (not covered by I3-VP/I3-VD, which apply only to shifted content) from the displaced positions, and the empty-case depth treatment is careful — `m_{s_C}(d)` is defined by the choice of `m`, not equated with an undefined pre-state depth.

**Provenance (CP8).** The three-branch discharge is sound and complete: fresh K.ρ for range-new pairs absent from `Σ.R` (J1'★-admissible by exactly the range-new condition); P2 permanence for range-new pairs already recorded (the re-COPY-after-delete configuration, correctly identified as reachable); P4★ + P2 for not-range-new addresses, with P4★'s availability properly grounded in the composite-boundary standing precondition. J0 is correctly discharged vacuously (no K.α). The `⊆` direction follows from K.μ⁻/K.μ⁺ framing `R` and J1'★ independently confining new pairs.

**Tiling and closure (CP3).** The three-interval argument is genuine ordinal arithmetic, not hand-waving: disjointness from TS1/TS4, gaplessness from TS3/Extended Associativity (`(min+i)+W = min+(i+W)`), yielding the contiguous run `[min, max+W]`. CP3c plus CP6's domain-equality conjunct gives the range characterization `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {c₀,…,c_{W−1}}` in both directions, which the wp derivation needs and uses correctly.

**Derived consequences.** CP4's "exactly W" survives scrutiny: shifted pairs replace rather than add (injectivity of shift), non-text positions cannot bind content addresses (S3★ + SD), and the per-address occurrence-count refinement is correctly distinguished from the aggregate. The wp for link discoverability is non-trivial and correctly scoped to links not already discoverable. CP7b's LP12 application is evaluated at the post-state with coverage held by CP7a — correct.

**Worked example.** All arithmetic verified: `zeros` counts, span denotations, `act` sets, the single-run resolution of σ_A (`a₂ = a₁ + 1`), the post-state arrangement, the origin multiset `⦃d_A, d_A, d_B⦄`, and the range-new classification of all three placed addresses. The variant exhibiting the P4★/P2 branch is a genuine instance of the not-range-new case.

**Anti-bloat scan.** The CP3c closure-peer enumeration and the CP12 bounding remark were introduced deliberately in the last revision and carry content (they establish that every state component is bounded above by the operation's own clauses, which is what makes the postconditions self-sufficient); I do not count them as meta-prose. The single CP8 forward-pointer to the composite section is standard claim-then-proof organization, not compounding deferral. No paragraph imagines a precondition-excluded case; no relocated-finding residue detected.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Guarantees relating a partially-bound span's nominal extent to its placed width
**Why out of scope**: The ASN correctly admits partial binding and resolves by restriction; what COPY should promise about the silent shortfall relative to ASN-0058's C2 is design territory for a future ASN, and the document already parks it as an open question rather than claiming it.

### Topic 2: Undiscoverability of inherited links after later removal of the transcluded positions
**Why out of scope**: This is the DELETE-side contraction question (LP12a/LP12b territory applied to a successor operation), not a property of the COPY transition itself.

### Topic 3: Transclusion into the link subspace
**Why out of scope**: COPY is explicitly scoped to content placements in `s_C`; link-by-reference placement interacts with K.μ⁺_L's origin and uniqueness invariants (CL-OWN, CL-UNIQ) and needs its own operation specification.

### Topic 4: The correspondence relation among appearances of shared content
**Why out of scope**: CP2/CP4 establish shared identity and independent occurrences; the relation that lets one appearance stand for all is new machinery, not a missing conjunct here.

VERDICT: CONVERGED
