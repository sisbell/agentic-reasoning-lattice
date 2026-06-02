# Review of ASN-0047

The ASN is technically strong: the D-SEQ★ derivation (both m=2 and m≥3 cases), the K.μ~ admissibility/realisability coincidence, the necessity/sufficiency proof of the K.μ~ precondition, and the seven worked examples are genuinely rigorous and self-checking. My findings are confined to forward-reference accretion (the `review-mode.anti-bloat` patterns) and one classification concern.

## REVISE

### Issue 1: Defensive forward-reference prose in K.δ case (ii), k = 2

**ASN-0047, *K.δ case (ii) discharge and parent-allocator activation*, k = 2 closing paragraph**: "For the node rows, 'based at its own node' is not by itself the non-lineage of two distinct nodes' account sub-allocators: that non-lineage — required when distinctness is compared across distinct node bases, even under node nesting N₁ ≼ N₂ — is established by CrossNodeAccountBase (*Entity distinctness*), not asserted from boundary baptism."

**Problem**: The activation discharge at this site concerns a *single* K.δ k = 2 event. Cross-node non-lineage (comparing two distinct nodes' sub-allocators) is a different concern, handled in the *Entity distinctness* corollary. This sentence imagines that downstream comparison purely to warn the reader off conflating it, and defers to CrossNodeAccountBase. It is meta-prose the reader must skip to follow the activation discharge — the reviser-drift pattern "a paragraph imagines a case the claim's carrier already excludes" plus a non-circularity forward pointer.

**Required**: Delete the sentence. CrossNodeAccountBase stands on its own at its definition site; the activation discharge does not need to pre-disclaim it.

### Issue 2: Multiple paragraphs defer to the same link-subspace-fixity location

**ASN-0047, *Decomposition of K.μ~***: clause (v) of the admissibility list points forward twice — "(*Link V-position permanence* below)" and "(*Link-subspace fixity and realisation* below)"; Step (A) Case `s_L` defers with "Pointwise link fixity (clause (v), `π(v) = v`) for these sources holds by *Link-subspace fixity and realisation* below"; and the LRP lemma plus sub-step (4) are themselves that location.

**Problem**: The same link-subspace-fixity fact is announced in clause (v), re-announced in Step (A), and finally proved in *Link-subspace fixity and realisation* via LRP + CL-UNIQ. Three separated paragraphs route to one downstream proof — the "multiple paragraphs in different sections defer to the same downstream location" pattern. The reader cannot follow clause (v) or Step (A) without jumping ahead, then back.

**Required**: State link-subspace fixity once (LRP is already the single named fact). Have clause (v) and Step (A) cite LRP directly rather than each forward-pointing to the prose block; remove the duplicate "below" deferrals.

### Issue 3: K.δ definition defers its discharge inventory downstream

**ASN-0047, *Elementary transitions*, K.δ case (ii) preamble**: "The parent entity-level sub-allocator on which each step acts, the spawn-admissibility conjuncts (for the child-spawn regimes k ∈ {1, 2}), and the allocator-discipline properties the guard maintains are discharged uniformly in §*K.δ case (ii) discharge and parent-allocator activation*."

**Problem**: This is a use-site inventory ("the X, the Y, and the Z are discharged in §W") that enumerates downstream consumers rather than advancing the K.δ definition. Combined with the per-sub-case "discharged per the per-k freshness mechanism above / discharged uniformly in §…" pointers, the K.δ definition reads as a routing table to its own discharge section.

**Required**: Replace the inventory with a single pointer ("Discharge of the parent-allocator and spawn-admissibility conditions: §K.δ case (ii) discharge…"), and let the downstream section enumerate what it discharges.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering (DELETEVSPAN compaction)

**Why out of scope**: K.μ⁻ models link-subspace contraction by suffix removal only; interior withdrawal with V-position renumbering is the implementation's `DELETEVSPAN` behaviour. This is correctly flagged as an open question, and named operations (DELETEVSPAN) are explicitly out of scope. No revision needed — the ASN handles this appropriately by deferring it.

META: not applicable — the ASN defines extended state, elementary transitions on that state, and their invariants at the abstract level; it has not drifted into implementation mechanics.

VERDICT: REVISE
