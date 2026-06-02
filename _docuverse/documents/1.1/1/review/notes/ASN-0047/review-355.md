# Review of ASN-0047

## REVISE

### Issue 1: K.μ⁻ is simultaneously claimed as new and as inherited from ASN-0036

**ASN-0047, *Elementary transitions* / *Properties Introduced***: The body defines K.μ⁻ fresh — "**K.μ⁻ (Arrangement contraction).** Existing V→I mappings are removed from some d ∈ E_doc..." — and the *New properties introduced by this ASN* table lists it: "K.μ⁻ | Arrangement contraction — remove existing V→I mappings...". But the *Local extensions and strengthenings* table gives its Foundation source as "ASN-0036's K.μ⁻ stated D-CTG/D-MIN with a link-subspace exemption."

**Problem**: K.μ⁻ cannot be both a property newly introduced by this ASN and a foundation property of ASN-0036. The ASN-0036 foundation extract contains no K.μ⁻ transition at all — only the *invariants* D-CTG/D-MIN/D-SEQ and the predicates S0–S8. The operation K.μ⁻ is this ASN's; only the invariants it must preserve are ASN-0036's. The Local-extensions row attributes the operation itself to ASN-0036, which is both internally contradictory (against the New-properties table and the fresh body definition) and unsupported by the foundation.

**Required**: Make the attribution consistent. K.μ⁻ should be presented as introduced here, with the row reframed as "strengthening of *this ASN's* K.μ⁻ postconditions against ASN-0036's D-CTG/D-MIN invariants" — paralleling the K.μ⁺-amendment row, which correctly reads "Strengthening of this ASN's K.μ⁺."

### Issue 2: Document-organization meta-prose in K.μ⁻ admissible contraction shape

**ASN-0047, *Elementary transitions*, K.μ⁻ precondition**: "...are derived consequences of the restriction form M'(d) = M(d) ↾ R, proved once in *K.μ⁻ admissible contraction shape* below; that proof is the sole site stating the equivalence, and every later mention cites it rather than restating it."

**Problem**: The clause "that proof is the sole site stating the equivalence, and every later mention cites it rather than restating it" advances no part of the contraction specification — it is prose justifying how the document is organized. This is the forward-reference-accretion pattern the anti-bloat classifier targets: meta-commentary on citation discipline rather than mathematical content.

**Required**: Delete the organizational clause; the forward pointer "proved... in K.μ⁻ admissible contraction shape below" already carries the navigation.

### Issue 3: "Why this lemma exists" comparative prose in the FrontierEquivalence / ChildSpawnFreshness entries

**ASN-0047, *Properties Introduced*, ChildSpawnFreshness row**: "...reverse direction via GlobalUniqueness/T10a.6 over the spawned child allocator's base; admits node operands (no ¬Node(t) precondition), so it covers the k = 2 descents off node/account operands that FrontierEquivalence cannot."

**Problem**: The trailing comparison explains why two lemmas are needed (one covers what the other "cannot") rather than stating what ChildSpawnFreshness asserts. This is the "new prose explains why the construct is needed rather than what it says" pattern. The substantive contrast (k=0 frontier read vs. k∈{1,2} child-spawn read) is already carried where each is *used* — at K.δ case (ii).

**Required**: Trim the entry to the lemma statement and its discharge mechanism; drop the comparative justification of its existence relative to FrontierEquivalence.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal
The ASN models contraction as suffix removal only (faithful to gap-free POOM for suffix deletes), and explicitly defers interior `DELETEVSPAN`-style compaction to a future ASN (Open Question). This is correctly out of scope here — interior renumbering is operation-level (DELETEVSPAN), which the Scope section excludes.

### Topic 2: Concurrency / serialization of allocation
SequentialTransitionAxiom assumes atomic, totally-ordered transitions; the concurrent-allocation question is raised as an Open Question and belongs to a future concurrency ASN, not this one.

VERDICT: REVISE
