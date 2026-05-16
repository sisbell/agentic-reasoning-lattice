# Review of ASN-0051

I checked each SV claim against its proof, verified the cross-origin exclusion argument with the worked tumbler example, and traced SV11's decomposition through the worked example.

## REVISE

### Issue 1: SV6 proof typo — "first four fields"
**ASN-0051, SV6 proof, paragraph after "Restricting to element-level t"**: "The first four fields (server, account, document) of t are identical to those of s, so origin(t) = origin(s)."
**Problem**: The prose says "first four fields" but the parenthetical lists only three: server, account, document. A T4-valid tumbler with zeros(t)=3 has exactly four fields (N, U, D, E); origin(t) = N(t).0.U(t).0.D(t) uses only the first three. The proof shows t and s agree on positions 1..k−1 ⊇ 1..p₃, which establishes agreement on N, U, D but says nothing about E (where t and s typically differ since t ∈ ⟦(s,ℓ)⟧). The "four" appears to be a slip — the conclusion origin(t) = origin(s) requires three-field agreement, not four.
**Required**: Change "first four fields" to "first three fields" (and consider replacing "server" with "node" for consistency with the rest of the ASN, which uses N(a) notation per the S7 definition).

### Issue 2: SV7 name understates the claim's scope
**ASN-0051, SV7 statement and surrounding prose**: SV7 is named "TransclusionCouplingAbsence" and framed around K.μ⁺ transclusion. But the formal statement is "for any transition Σ → Σ' that holds L in frame and any set of I-addresses A", and the proof "depends solely on L being invariant". The ASN itself notes: "The same equality holds for every elementary transition that holds L in frame — K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, and K.ρ — since the proof depends solely on L being invariant."
**Problem**: The name biases the claim toward one application (transclusion) when the claim is about discovery invariance under every L-preserving transition. Future cites of "SV7" may apply it narrowly and miss its general scope — particularly for forking (J4), where the ASN already relies on SV7's general form in the line "Same reasoning applies to forking".
**Required**: Either rename SV7 to reflect general applicability (e.g., "DiscoveryInvarianceUnderLFrame"), or split into a general claim plus a "TransclusionCouplingAbsence" corollary that specializes it. The label appearing in SV13 and elsewhere should match the broader claim.

### Issue 3: Bilateral vitality silently scoped to standard triples
**ASN-0051, Bilateral Vitality definition**: "A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when each non-empty content endset is vital in d..."
**Problem**: The definition assumes triple notation (F, G, Θ) throughout, but foundation L3 (ASN-0043 version) admits |Σ.L(a)| ≥ 3. The ASN never states that it works in the standard-triple framework, leaving readers to infer this from the (F, G, Θ) notation. Bilateral vitality for a 4-arity or 5-arity link is undefined as written — should additional slots count as content endsets requiring vitality, or as analogues of the type endset, exempt from the condition? The ASN-0043 StandardTriple convention designates slot 3 as type; positions 4+ have no such convention.
**Required**: Add one sentence scoping the analysis: "Throughout this ASN we work in the standard-triple framework of ASN-0047 (|Σ.L(a)| = 3); extension to higher-arity links per ASN-0043 is deferred." Alternatively, generalize bilateral vitality to "each non-empty endset other than slot 3 is vital in d", noting that the higher-arity treatment is a corollary.

## OUT_OF_SCOPE

### Topic 1: Same-origin coverage growth invariants
**Why out of scope**: The "Content Allocation and Coverage Stability" section identifies two mechanisms (sequential overshoot, child-depth entry) by which same-origin I-addresses can enter existing endset spans, and gives a concrete counterexample. The architectural resolution (byte-level sequential closure, broader-level intentional growth) is informal. A formal characterization belongs in an allocation-regime ASN that pins down which allocation disciplines close which span types.

### Topic 2: Endsets over entity-level (non-element) addresses
**Why out of scope**: L4 permits endset spans over node, account, or document tumblers, but SV6 is restricted to element-level coverage and the ASN as a whole assumes content endsets reference element-level I-addresses. The hierarchical address case — Nelson's "A span that contains nothing today may at a later time contain a million documents" [LM 4/25] — is mentioned but not treated. This belongs in a future ASN on hierarchical address semantics.

### Topic 3: Endsets referencing link-subspace addresses
**Why out of scope**: The ASN explicitly defers reflexive addressing analysis: "We defer the detailed analysis of link-referencing endsets and reflexive addressing to the Link Subspace ASN." SV2's unified treatment (covering both K.μ⁺ and K.μ⁺_L) is sound for the monotonicity it claims; the structural implications of links over links are appropriately future work.

VERDICT: REVISE
