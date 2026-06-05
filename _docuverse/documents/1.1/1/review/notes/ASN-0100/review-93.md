# Review of ASN-0100

I worked through the substrate decomposition, the three-region effect specification, every invariant in ASN-0047's ExtendedReachableStateInvariants list, the worked examples, the wp analysis, and the atomicity argument. The correctness core is genuinely strong: the closed-interval D-CTG★ reduction handles off-prefix tuples for `m ≥ 3` correctly, the projection-shift correspondence (INS.proj) tracks each elementary step soundly, P4★'s boundary-only classification is used correctly to avoid a false intermediate-state violation, and the empty/append/clearance edge cases are all covered. I found no correctness hole. The findings below are precision and prose-accretion items, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Foundation claims renamed with non-canonical aliases
**ASN-0100, Claims table and §Provenance / §Atomicity**: e.g. "J1★ (ExtensionRecordsProvenanceContentSubspace)", "J1'★ (ProvenanceRequiresExtensionContentSubspace)", "P4★ (ProvenanceBoundsContentSubspace)", "NodeLineage (NodeDescentFromBootstrap)".
**Problem**: The foundation's canonical names are J1★ "ExtensionRecordsProvenance", J1'★ "ProvenanceRequiresExtension", P4★ "ProvenanceBounds", NodeLineage "NodeLineage". The ASN appends "ContentSubspace" to several and invents "NodeDescentFromBootstrap". A reader cross-checking against ASN-0047/ASN-0093 is led to believe these are distinct claims. Standard 7: use the foundation's identifiers, do not re-label them.
**Required**: Cite the foundation claims by their canonical names; if a content-subspace scoping is being emphasized, do it in prose, not by minting a new claim name.

### Issue 2: Duplicated invariant-discharge prose between §Verifying the Invariants and §Atomicity
**ASN-0100, §Link store unchanged and §Atomicity (link-store bullet)**: The L0 content-clause discharge for each fresh `a_k` (`subspace_I(a_k) = s_C` via DisjointSubAllocatorChains; ASN-0093) is written out in full in both sections. The same double-statement occurs for S8★-via-C1a (stated in §Per-subspace span decomposition and re-derived through INS.C1a-app at the post-K.μ⁻ bullet).
**Problem**: Two paragraphs in different sections say the same thing in different words — the precise reader must verify the same argument twice and confirm they agree. This is the prose-accretion pattern the classifier targets.
**Required**: Discharge each per-fresh-address content invariant (L0 content clause, S4, C1b, C1c, L14, P6, S7a/S7b) once — the §Atomicity grouped paragraph is the natural home since it argues the intermediate states — and have §Verifying the Invariants reference it rather than re-prove it.

### Issue 3: Defensive meta-prose around the I3 inheritance
**ASN-0100, §Effect Three ("Identification with the foundation's post-insertion shift") and Claims table (INS.M-shift: "inherited not re-derived")**: "We do not re-derive this — it is the foundation result, and INS.M-shift is its instance at S = s_C."
**Problem**: The load-bearing content is the *decomposition* statement (post-state coincides with I3 on Left ∪ Shifted-right, Insertion fills the I3-vacated gap). The provenance disclaimers ("we do not re-derive", "inherited not re-derived") explain why the proof is absent rather than advancing the argument; they are skip-past text.
**Required**: Keep the decomposition sentence and the I3/I3-V citation; drop the disclaimers and the claims-table annotation.

### Issue 4: Bidirectional forward/back references for the same two claims
**ASN-0100, §Effect Two ("§Post-state V-position well-formedness extends both to the Left and Shifted-right regions") and §Post-state V-position well-formedness ("by claim S8a, established at §Effect Two")**: S8a and INS.inv.depth are split across two sections that each point at the other.
**Problem**: Neither section is self-contained for these two claims; the reader bounces between them to assemble one argument.
**Required**: Establish S8a and INS.inv.depth for all three regions in one place (Insertion is already done at §Effect Two; fold the Left/Shifted-right inheritance from I3-VP/I3-VD in alongside it).

## OUT_OF_SCOPE

### Topic 1: INSERT vs. COPY contrast (§INSERT vs. COPY)
**Why out of scope**: COPY mechanics are explicitly out of scope. The section is framing only and specifies no COPY semantics, and INS.identity / INS.identity.crossdoc are legitimate INSERT claims — so this is not an error. But the COPY-comparison framing prose could be trimmed to the corollary, since the comparison itself adds no INSERT guarantee.

### Topic 2: Partial-failure recovery, concurrent INSERTs, derived document metadata (Open Questions)
**Why out of scope**: Correctly deferred — recovery is implementation territory, concurrency is a scheduling concern beyond the single-state contract, and derived-metadata maintenance is a separate ASN.

VERDICT: REVISE
