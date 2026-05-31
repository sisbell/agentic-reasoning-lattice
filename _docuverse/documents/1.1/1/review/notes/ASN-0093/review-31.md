# Review of ASN-0093

This note has clearly been through many cycles and the underlying proofs are sound — I checked the C1c/L1c chains, FirstEmissionFreshness, Cross-document disjointness, and the worked example, and the structural arguments hold. The carrier classifier is `review-mode.anti-bloat`, and that is where the remaining problems are: the argument is buried under duplicate statements, use-site inventories, and dependency preambles that the precise reader must skip past.

## REVISE

### Issue 1: Duplicate statement — chain-indexed properties need no per-transition discharge

**ASN-0093, Simultaneous-induction framing & Discharge of stated invariants**:
- Framing: "Each is a direct ASN-0040 citation (B6(a), the SiblingStream postconditions, S0, B5a, S1, B7) applied to the sibling stream `S(b_·(d), 1)`... No induction over substrate-level transitions is required."
- End of matrix: "The chain-indexed disciplines (...) are not state-dependent in their conclusions and so require no per-transition discharge; their once-and-for-all status as ASN-0040 citations is established in *Per-chain disciplines* above."

**Problem**: Two paragraphs in different sections assert the same thing (chain disciplines are state-independent ASN-0040 citations, no induction needed). The second also forward/back-points to a third location.

**Required**: Keep one statement. The discharge matrix is the natural home; delete the framing-section restatement or reduce it to a pointer.

### Issue 2: Dependency-inventory preamble in FirstEmissionFreshness

**ASN-0093, FirstEmissionFreshness**: "The proof below derives freshness from L0, SC-NEQ, ChainPrefixExtension, ChainMembershipForOrigin, Cross-document disjointness, StoreT4Validity, ChainElementT4Validity, and T7, all consumed at the pre-state Σ. ChainMembershipForOrigin, StoreT4Validity, and Cross-document disjointness are established under the same simultaneous-induction discipline."

**Problem**: This enumerates the lemma's dependencies immediately before a proof that cites each of them inline anyway — a use-site inventory. The second sentence is meta-prose about proof architecture, not about the freshness claim.

**Required**: Delete the preamble; the four-step proof body already names its premises at point of use.

### Issue 3: Parameter-semantics paragraph duplicates the binding preconditions

**ASN-0093, Substrate primitive operations**: "the first-emit predicate forces `a = [d.0.s_C.1]` (resp. `ℓ = [d.0.s_L.1]`); the subsequent-emit predicate forces `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`..."

**Problem**: The pinning formulas restated here appear verbatim again in K.α's and K.λ's *Binding precondition* blocks. The same two formulas are stated twice.

**Required**: Reduce the paragraph to the single load-bearing point ("address parameters are not free; `(d, Σ)` determines them per the preconditions below") and drop the formula restatement.

### Issue 4: ChainDiscipline use-site clause and narrative overlap

**ASN-0093, "Sub-allocator chains are ASN-0040 sibling streams"**: "In particular, each chain's closure under `inc(·, 0)` — used downstream to place a freshly emitted sibling `inc(a_prev, 0)` (resp. `inc(ℓ_prev, 0)`) onto the chain — is exactly the SiblingStream recurrence."

**Problem**: The em-dash clause is a use-site inventory ("used downstream to place...") describing where the property is consumed rather than advancing the identity being stated. The surrounding paragraph also re-exhibits `t_1^C(d) = [d.0.s_C.1]`, which the FirstEmission lemma immediately below re-derives a third time.

**Required**: Drop the "used downstream" clause; state the closure identity once and let FirstEmission cite it.

### Issue 5: Properties Introduced table carries full derivations instead of index hooks

**ASN-0093, Properties Introduced**: the rows for ChainMembershipForOrigin, FirstEmissionFreshness, Cross-doc disjointness, ChainDiscipline, and FirstEmission each contain multi-clause derivation sketches (e.g. ChainMembershipForOrigin: "Proved by induction over transitions using the FirstEmission lemma (first-emit branches placing `t₁`) and ChainDiscipline + ChainEnumerationInjectivity...").

**Problem**: A properties index should be a one-line hook per entry. These rows reproduce the body proofs, so any future edit must be kept in sync in two places.

**Required**: Collapse each Source cell to the property's premises (a citation list), not its proof.

### Issue 6: TA5a anchor-admissibility argument restated three times

**ASN-0093, FirstEmission lemma / C1c chain exhibition / L1c chain exhibition**: each independently re-derives "`t₁ = inc(d, 2)`: TA5a at `k = 2` requires `zeros(d) ≤ 2`; M0 gives `zeros(d) = 2`... `t₂ = inc(·, 1)`: TA5a at `k = 1` requires `zeros ≤ 3`, discharged by T4..."

**Problem**: The identical per-step admissibility chain appears in the FirstEmission proof and again in both C1c and L1c exhibitions. (The worked-example repetitions are acceptable as a concrete trace, but the three lemma-level copies are not.)

**Required**: Establish the anchor-construction admissibility once (FirstEmission is the natural site) and have the C1c/L1c exhibitions cite it, retaining only what is genuinely chain-specific (e.g. L1c's extra `inc(b_C(d), 0)` step).

### Issue 7: "K.σ admissibility scope" restates the precondition

**ASN-0093, K.σ**: "*K.σ admissibility scope.* K.σ's precondition is structural-only: it makes no commitment about *which* document addresses are admissible beyond T4-validity and `zeros(d) = 2`."

**Problem**: This subsection restates the precondition list verbatim under its own heading; it adds no constraint and no consequence.

**Required**: Delete the subsection.

## OUT_OF_SCOPE

### Topic 1: Arrangement mutation, entity stratification, provenance, link withdrawal
**Why out of scope**: The ASN correctly defers these via the Scope section and discharges the would-be arrangement invariants (S2, S3, S8a, etc.) as vacuous under `M(d) = ∅`. The vacuity notes are appropriate and need no expansion here.

VERDICT: REVISE
