# Review of ASN-0047

I checked the elementary transitions, the K.δ allocation discipline, the K.μ⁺/K.μ⁻/K.μ~ arrangement machinery, the coupling constraints, the D-SEQ★ derivation, and the invariant-preservation matrix. The core mathematics is sound — the D-SEQ★ infinite-witness argument, the K.μ⁻ constructive/post-state equivalence, the necessity/sufficiency proof for K.μ~, and the worked examples all hold up. My findings are concentrated in meta-prose accretion (the note carries the `review-mode.anti-bloat` classifier) plus one genuine classification inconsistency.

## REVISE

### Issue 1: Mutual organizational deferral between K.δ case (ii) and its discharge section
**ASN-0047, *Elementary transitions* (K.δ case (ii)) and *K.δ case (ii) discharge and parent-allocator activation***: The K.δ definition states "This definition is the authoritative source for the per-k contract (operand-admissibility conjuncts, freshness mechanism, structural identities); the discharge section keys its additions to these same sub-cases without restating them." The discharge section mirrors this: "The operand-admissibility conjuncts, freshness mechanism, and structural identities are the contract of the K.δ definition's case (ii) and are not restated here; this section adds only the *parent-allocator activation*..."

**Problem**: This is the split-across-two-sections-with-mutual-deferral pattern. Neither paragraph advances the argument; both exist solely to negotiate which section "owns" the contract and to promise the reader the other section won't repeat it. A reader following the k=0/1/2 contract must hold both locations open and reconcile the bookkeeping. The k-keyed contract belongs in one place; the prose announcing the division is noise.

**Required**: Drop both organizational meta-paragraphs. Either keep the full per-k contract in the K.δ definition and have the discharge section add its parent-allocator material inline under the same k-labels without the "authoritative source"/"not restated here" framing, or fold the discharge content back into the definition.

### Issue 2: Defensive padding in the "Inherited from foundation" table preamble
**ASN-0047, *Properties Introduced* → *Inherited from foundation* preamble**: "preservation under those new and amended transitions cannot be supplied by the foundation — the foundation never reasoned over them — and is instead established *locally* in the Class (a) verification ... The restatements here record the foundation statements for narrative continuity; the local preservation arguments live with the per-transition verification."

**Problem**: The load-bearing point is one sentence: *preservation of these foundation invariants under K.μ⁺_L and the amended transitions is verified locally in the Class (a) matrix.* The surrounding clauses ("the foundation never reasoned over them," "for narrative continuity," "live with the per-transition verification") are defensive justification of document organization, not content that advances the claim. This is the use-site-inventory / document-ordering pattern.

**Required**: Reduce to the single substantive sentence pointing the reader to the Class (a) verification for K.μ⁺_L and the amended transitions.

### Issue 3: P4a's "transient failure within composite" conflicts with its trace-property definition
**ASN-0047, *Composite-boundary verification matrix*** vs. **P4a definition box**: The matrix row for P4a lists, under "Transient failure within composite," that P4a "Transiently fails if K.ρ precedes the matching K.μ⁺ within the composite." But P4a's definition box defines it as a *trace property* whose witness ranges over composite boundaries only: "a finite sequence of composite boundaries `Σ₀ →* Σ₁ →* ... →* Σ_n = Σ` ... `(E Σ_k ∈ {Σ₀, ..., Σ_n} : ...)`."

**Problem**: Intermediate states within a composite are not members of `{Σ₀, ..., Σ_n}` (those are boundaries) and are not valid trace endpoints. So P4a is never *evaluated* at an intermediate state — it cannot "transiently fail" there, because it is not a per-state predicate. The matrix column describes a live-witness-at-intermediate-state notion that P4a's formal quantifier does not range over. The two characterizations disagree on P4a's domain of evaluation. This is precisely the category P4a's own preamble tries to fix ("Calling them 'invariants' would be misleading in the strict state-machine sense"), yet the matrix reintroduces the per-state framing for P4a.

**Required**: Make the matrix's P4a cell consistent with the trace-property definition — e.g., "not evaluated at intermediate states; as a trace property it is discharged at the boundary Σ' which carries the witness" — rather than describing it as transiently failing at intermediate states.

## OUT_OF_SCOPE

### Topic 1: Internal well-formedness of the node tree
P8 (entity hierarchy) and TrackedEmission are explicitly restricted to non-node entities, and NodeLineage requires only `n₀ ≼ e`. Consequently a multi-component node such as `[1,2,3]` may inhabit E without `[1,2]` ∈ E (the CrossNodeAccountBase argument even relies on T4-legal node nesting). Whether intermediate node addresses along a lineage must themselves be in E is left unconstrained.

**Why out of scope**: Node addresses are minted at the network-provisioning boundary (NodeBaptism), not by docuverse transitions, and the open questions already defer the node-baptism protocol to future work. Node-tree internal well-formedness is a boundary/provisioning concern, not a defect in this ASN's transition model.

VERDICT: REVISE
