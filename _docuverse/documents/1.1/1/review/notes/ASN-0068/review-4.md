# Review of ASN-0068

## REVISE

### Issue 1: Sign convention in Worked Example 2

**ASN-0068, "Worked Examples" section, Example 2**: "different lockstep offsets (δ = 0 for the first, δ = 2 for the second)"

**Problem**: The CV-MAX uniqueness proof defines δ as a signed difference (`δ := j²_a − j¹_a = j²_b − j¹_b`). For the second run ([1,3], [1,1], 1), the per-side last-component offset is j_b - j_a = 1 - 3 = -2 (or +2 if the convention is reversed). The text states δ = 2 without specifying which convention is in use, and the chosen sign is inconsistent with the proof's "WLOG δ ≥ 0 (else swap)" convention applied to the natural reading "j²_a − j¹_a".

**Required**: State the sign convention explicitly (e.g., "absolute per-side offset" or "j_a − j_b") to match either +2 or be consistent with the proof. The example's structural conclusion is correct; only the labeling needs to align with the proof's notation.

### Issue 2: CV-LINK-DEGEN self-comparison subclaim is informal

**ASN-0068, CV-LINK-DEGEN justification**: "The same reasoning, applied to the self-comparison case d_a = d_b, combines with CL-UNIQ (ASN-0047) — M(d)|_{dom_L} is injective — to leave only the identity correspondences in s_L."

**Problem**: This subclaim asserts a non-trivial consequence (self-comparison in s_L collapses to a diagonal) but the reasoning is invoked by reference rather than derived. The d_a ≠ d_b case uses CL-OWN + S7 (function-valued origin); the d_a = d_b case requires a different mechanism (CL-UNIQ injectivity). "Same reasoning" obscures that the proof structure differs.

**Required**: Either promote the self-comparison s_L case to an explicit subclaim with proof — "for v¹, v² ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_L}(d) with M(d)(v¹) = M(d)(v²): by CL-UNIQ, v¹ = v²" — or remove the informal claim from CV-LINK-DEGEN's justification.

### Issue 3: Self-comparison case lacks worked example

**ASN-0068, "Worked Examples" section**: Both examples are cross-document comparisons in s_C. The self-comparison case (d_a = d_b) is discussed abstractly after CV-PROV-FORGOTTEN but never exemplified.

**Problem**: The text describes the maximal-run structure for self-comparison ("the identity-diagonal runs over ⟦R_a⟧ ∩ ⟦R_b⟧ ... together with off-diagonal width-1 runs for each self-transclusion pair"). This claim is non-trivial — the identity diagonal collapses into multi-byte runs while off-diagonal entries remain width-1 — but is asserted rather than verified. The non-trivial interaction between CV-ATOM (width-1 admissibility), CV-MAX (uniqueness), and self-transclusion deserves concrete demonstration.

**Required**: Add a third worked example for self-comparison with self-transclusion (e.g., `M(d): [1,1]→a, [1,2]→a` with `R_a = R_b` = full). Show the four pairs in `corr_{a,a}` and the resulting `MaxRuns = {([1,1],[1,1],2), ([1,1],[1,2],1), ([1,2],[1,1],1)}`, verifying that the diagonal pairs aggregate into a single width-2 run while off-diagonal pairs remain width-1.

### Issue 4: Result finiteness not stated

**ASN-0068, CV-MAX and Result type**: `Result := P(T × T × ℕ⁺)`.

**Problem**: The result of compareversions is always finite — by S8-fin (ASN-0036), `dom(M(d_a))` and `dom(M(d_b))` are finite, so `corr_{a,b}` is finite, so `|MaxRuns| ≤ |corr_{a,b}| < ∞`. This finiteness is load-bearing: it justifies treating `MaxRuns` as a concrete enumerable set and underwrites termination of the walks in the CV-MAX existence proof. The existence proof cites S8-fin for walk termination but never lifts finiteness to a result-level property.

**Required**: Add an explicit finiteness postcondition to CV-MAX or as a separate claim: `|MaxRuns(d_a, R_a, d_b, R_b)| ≤ min(|dom(M(d_a))|, |dom(M(d_b))|) < ∞`, cited to S8-fin.

### Issue 5: CV-IN m_σ notation is awkward

**ASN-0068, CV-IN**: "σ is level-uniform (S6, ASN-0053) at the document's V-position depth m_σ ∈ {m_a, m_b} (with m_a := m_{d_a, S} for σ ∈ R_a and m_b := m_{d_b, S} for σ ∈ R_b, both supplied by S8-depth, ASN-0036); and actionPoint(width(σ)) = m_σ"

**Problem**: The notation m_σ as "depending on which span-set σ belongs to" forces the reader to resolve side-membership within a quantifier over R_a ∪ R_b. If a span literal happens to appear in both R_a and R_b with m_a ≠ m_b, the constraint silently becomes unsatisfiable. The notational economy obscures the underlying structure.

**Required**: State CV-IN as two separate clauses — "for every σ ∈ R_a: ... at depth m_a := m_{d_a, S}" and "for every σ ∈ R_b: ... at depth m_b := m_{d_b, S}" — rather than as a single quantifier with conditional depth resolution.

## OUT_OF_SCOPE

### Topic 1: Concurrent modification semantics

CV-DETERM and CV-RO are stated for a stable state. The Open Question "What invariants must the correspondence relation preserve when one or both documents undergo concurrent arrangement modification mid-comparison?" belongs to a future ASN on transaction/concurrency, not an error in this one.

### Topic 2: Sub-allocator boundary semantics for runs

The Open Question about runs whose I-addresses span sub-allocator boundaries (different origins at consecutive V-offsets) is exploratory and belongs to a future ASN on attribution composition.

VERDICT: REVISE
