# Review of ASN-0047

This ASN is genuinely rigorous on correctness: the elementary transitions, the per-subspace D-CTG★/D-MIN★/D-SEQ★ regime, the K.μ~ admissibility/realisability coincidence, and the J0/J1★/J1'★ coupling discharge all hold up under case analysis, and the worked examples exercise the load-bearing boundary cases (empty-source fork, k=0 subsequent version, interior replacement, link-subspace suffix removal). I could not find a correctness gap. The findings below are noise/precision issues, surfaced under the note's `review-mode.anti-bloat` mandate.

## REVISE

### Issue 1: Circular / zero-content navigation pointers
**ASN-0047, Class (a) verification — K.μ~ shape-package paragraph**: "*K.μ~ discharge for the arrangement-shape package (uniform argument).* … Per-property K.μ~ discharge: this paragraph."

**Problem**: The closing sentence "Per-property K.μ~ discharge: this paragraph" is a pointer to the paragraph it sits in — it advances no reasoning. It compounds with a navigation loop: the matrix K.μ~ cells say "see *S8a, S8-depth, S8-fin* prose below," "see *S8★* prose below," "see *D-CTG★ / D-MIN★* prose below," "see *D-SEQ★* prose below," and each of those prose blocks then says "by the uniform shape-package discharge above" — i.e. back to this same paragraph. A reader chasing the S8a/K.μ~ discharge bounces prose→prose with no incremental content at the destination.

**Required**: Delete the self-referential sentence. State the uniform shape-package discharge once, and have the per-property prose blocks (S8a/S8-depth, D-CTG★/D-MIN★, D-SEQ★) name only their genuine per-property *delta* (e.g. S8-fin's "finite + finite = finite," D-SEQ★'s re-derivation) rather than re-deferring to the shared paragraph.

### Issue 2: Per-k freshness mechanism split across two locations
**ASN-0047, K.δ definition and "K.δ case (ii) discharge and parent-allocator activation"**: The K.δ definition states "*Per-k freshness mechanism (stated once here).*" with the full k=0 / k∈{1,2} breakdown, then the later dedicated section re-walks the same k-by-k freshness regime ("k = 0 … (Freshness is discharged by the per-k mechanism stated in the K.δ definition.) k = 1 … k = 2 …").

**Problem**: The freshness discharge is presented as "stated once here" in the definition, but the case-(ii) section re-enumerates the same per-k freshness split before getting to its genuine added content (parent-allocator activation / ParentAllocatorDispatch). The reader re-reads the FrontierEquivalence-vs-direct-uniqueness distinction twice. This is the "content relocated rather than removed" pattern the anti-bloat note flags.

**Required**: In the case-(ii) discharge section, drop the per-k freshness re-enumeration entirely and keep only the cross-reference plus the new parent-allocator-activation material that the definition does not contain.

### Issue 3: "Discharged by FrontierEquivalence" mislabels a caller-checked precondition
**ASN-0047, K.δ case (ii), k=0**: "at k = 0 the frontier check `inc(t, 0) ∉ E` is discharged by FrontierEquivalence."

**Problem**: FrontierEquivalence is a biconditional *characterization* (`inc(t,0) ∉ E ⟺ t is the frontier`); it does not establish either side. The conjunct `inc(t,0) ∉ E` is a genuine caller-checked precondition (the k=0 worked example correctly calls it "the caller-checked guard `inc(t, 0) ∉ E`"). Calling it "discharged by FrontierEquivalence" conflates "characterized by" with "established by," and is inconsistent with the worked-example phrasing.

**Required**: Reword to "characterized by FrontierEquivalence" (or "translated to the frontier condition by FrontierEquivalence"), reserving "discharged" for the k∈{1,2} direct-uniqueness axiom that genuinely establishes its conjunct.

## OUT_OF_SCOPE

None — the ASN stays within state, elementary transitions, and invariants, and correctly defers INSERT/DELETE/COPY/MAKELINK semantics, concurrency, and the node-provisioning protocol to open questions / future ASNs.

VERDICT: REVISE
