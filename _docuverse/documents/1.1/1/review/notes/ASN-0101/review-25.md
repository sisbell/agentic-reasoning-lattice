# Review of ASN-0101

## REVISE

### Issue 1: D8 cites foundation invariants and lemmas that do not exist in the named foundations
**ASN-0101, D8 Group (ii) and Group (iii)**: "All of M0, **S4, S7a, S7b, S7c, S7d**, C1, ..." ; "*S7a, S7b, **S7c** (ASN-0036)* predicate over `dom(C)` (... element-field depth `≥ 2`)" ; "*S9 (TwoStreamSeparation, ASN-0036)*" ; "the substrate-level chain-discipline lemmas — ChainElementT4Validity, **ChainUniformLength**, ChainEnumerationInjectivity, **ChainUniformZeroCount**, ..."

**Problem**: Several labels do not occur in the cited foundations as provided.
- ASN-0036 defines S7, S7a, S7b, S7d — there is **no S7c** and **no S9**. The claimed "S7c = content element-field depth ≥ 2" is actually **C1b of ASN-0093**, not an ASN-0036 invariant; "S9 (TwoStreamSeparation)" is invented (the ASN even constructs an antecedent `Σ'.M(d) ≠ Σ.M(d)` for it).
- ASN-0093's chain lemmas are ChainElementT4Validity, ChainEnumerationInjectivity, ChainPrefixExtension, ChainMembershipForOrigin, etc. — there is **no ChainUniformLength** and **no ChainUniformZeroCount**.
- Store disjointness is labeled **SD** in ASN-0093, but D8 cites "L14 (StoreDisjointness, ASN-0093)"; CrossDocumentDisjointness is cited as "CrossDocDisjointness."

D8's central claim is "every foundation invariant the pre-state satisfied holds at the post-state." Asserting preservation of invariants that the foundation does not define makes the catalogue uncheckable and, in the S7c/S9 cases, vacuously names nonexistent obligations.

**Required**: Correct each label to the actual foundation invariant (content element-field depth → C1b of ASN-0093; remove or rename S9; fix SD/L14 and CrossDoc names), and either supply the real references for the uniform-length / uniform-zero-count properties or drop them.

### Issue 2: D11 weakest preconditions omit the enabledness conjunct
**ASN-0101, D11**: "`wp(DEL[d, σ], Q_disc(ℓ, d)) ≡ (E i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊄ X)`"

**Problem**: The foundation's analogous lemma, LP12a (ASN-0098), writes its wp as `enabled(K.μ⁻[d, R]) ∧ (E i : ...)` — the operation's guard is an explicit conjunct. D11 drops the DEL guard (`d ∈ dom(M)`, span well-formedness, containment) from all four wps. As written, a pre-state in which DEL is not applicable can satisfy `(E i : project ⊄ X)`, so the stated predicate is not the weakest precondition for total correctness; it is at best the wp *given* enabledness. This is a depth gap precisely where the ASN advertises wp analysis.

**Required**: Conjoin the DEL enabledness predicate to each wp (as LP12a does), or state explicitly that each wp is computed under the assumption that DEL is enabled.

### Issue 3: K.μ~ precondition mischaracterized, making the "killer case" characterization too narrow
**ASN-0101, "The operation"**: "K.μ~ (ASN-0047) requires `|dom_C(M(d))| ≥ 2` as a formal precondition" ; "The genuine killer case ... is therefore exactly: link-subspace interior deletion in a document with `|V_{s_C}(d)| < 2`."

**Problem**: ASN-0047's K.μ~ precondition is "`M(d)|_{dom_C}` takes at least two distinct *values*," not a cardinality bound on `dom_C`. By S5/M13 (UnrestrictedSharing / SharedContent), a document may have `|V_{s_C}(d)| ≥ 2` while every content V-position maps to a *single* I-address; there K.μ~ is unavailable despite `|V_{s_C}(d)| ≥ 2`. So the composite is unavailable in cases beyond the one named, and the word "exactly" is false.

**Required**: Restate K.μ~'s precondition as "≥ 2 distinct content-subspace image values," and widen (or re-justify) the killer-case characterization to include the shared-single-value configurations.

### Issue 4: LinkVPositionDepthAxiom referenced but undefined; m_L = 2 asserted, not derived
**ASN-0101, reduction justification and link-subspace example**: "At `m_S = 2` (the depth fixed for the link subspace by **LinkVPositionDepthAxiom** ...)" ; "(`S = s_L`, depth `m_L = 2` by **LinkVPositionDepthAxiom**)"

**Problem**: No LinkVPositionDepthAxiom appears in the foundations. S8a gives `#v ≥ 2` and S8-depth fixes a *common* per-subspace depth, but nothing pins the link-subspace depth to exactly 2. The link example's `m_L = 2` is therefore an example-local choice presented as an axiomatic derivation.

**Required**: Cite the actual foundation that fixes link depth if one exists, or present `m_L = 2` as an assumption of the worked example (the reduction proof is already general in `m_S` and needs no such axiom).

## OUT_OF_SCOPE

None. The recoverability discussion touches version creation (J4 ForkComposite) only as motivating context and does not define out-of-scope operations.

VERDICT: REVISE
