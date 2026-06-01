# Review of ASN-0086

## REVISE

### Issue 1: WP Case 1 inconsistently drops Nullify's precondition P2 from the weakest precondition

**ASN-0086, Weakest-Precondition Analysis, Case 1**: "`wp(Nullify(Σ, d_retr, a), single-tuple scope at Σ') ≡ P0(Σ, d_retr) ∧ P1(Σ, a)`" … "Nullify's third precondition P2: `|Σ.L(a)| = 3` … is absent from the wp above."

**Problem**: The necessity argument for including P0 is "Dropping P0 admits `d_retr ∉ dom(Σ.M)`, leaving the internal Emit_R's K.λ home-precondition undischarged: Nullify does not execute, no post-state Σ' is produced, and the postcondition is unreachable." But Nullify's Definition lists P0, P1, **and** P2 coequally as "three preconditions," with "Under these preconditions, Nullify is the composition…". By the identical abort-reasoning used to justify P0, violating P2 leaves the operation undefined, no Σ' is produced, and the postcondition is unreachable — so P2 belongs in the wp too. This is not a stray choice: Case 2 of the same section includes *every* Emit_K guard by exactly this reasoning ("Dropping `K ∈ T_admissible` admits `K = ∅` … Emit_K does not execute and no Σ' exists"). Case 1 applies the methodology to P0 but silently demotes P2, with no Definition-level distinction between executing preconditions and a scope marker to license the asymmetry. (Compounding the confusion: the Nullify section itself later says nullifying an arity-4 address "would be a well-formed Emit_R," implying P2 does *not* gate the underlying emission at all — in which case P2 should not be labeled a "precondition" alongside the hard guard P0.)

**Required**: Either (a) include P2 in the Case 1 wp (`P0 ∧ P1 ∧ P2`) and then observe it is geometrically inert for this postcondition, matching the uniform guard-inclusion of Case 2; or (b) reclassify P2 in Nullify's Definition as a scope/meaningfulness condition distinct from the executing preconditions P0/P1, so that its exclusion from the wp is principled rather than ad hoc. As written the two wp cases apply contradictory standards for whether an operation's guards enter its wp.

### Issue 2: R0a-Cor1 postcondition (a) derivation stated twice

**ASN-0086, R0a-Cor1**: Under "Substantive postconditions (a)" — "*Derivation:* ChainEnumerationInjectivity (ASN-0093) is stated in the strict-order form … which forces the contiguous chain prefix `{t_1, …, t_{n_d}}` to admit `t_{n_d}` as its unique maximum…"; and again under "*Proof*" — "The substantive postcondition (a) follows from ChainEnumerationInjectivity's strict-order form chained over the contiguous prefix."

**Problem**: The same derivation (postcondition (a) from ChainEnumerationInjectivity's strict-order form over the contiguous prefix) appears in two adjacent slots in different words — the "two paragraphs say the same thing" pattern the anti-bloat classifier flags.

**Required**: Give the derivation once. Either drop the "Derivation:" sub-paragraph and let the Proof carry it, or drop the Proof's restatement.

### Issue 3: Forward-consumer prose in R0a-Cor1

**ASN-0086, R0a-Cor1**: "Beyond the index re-translation `J_d^Σ := n_d − 1`, R0a-Cor1 carries two derived consequences absorbed at this site for downstream use."

**Problem**: "absorbed at this site for downstream use" is meta-prose justifying *why* the consequences are stated here rather than advancing the claim — the "definition's introduction enumerates downstream consumers" pattern. It does not help a reader follow R0a-Cor1.

**Required**: State the two derived consequences directly without the placement justification.

## OUT_OF_SCOPE

### Topic 1: Tightening L1b to `#E = 2`
The note's own Open Questions raise whether ASN-0043/0093's `#E ≥ 2` should be narrowed to `#E = 2`. R0a-Cor2 establishes `#E = 2` *within this note's substrate*; changing the foundation invariant L1b is a foundation-ASN revision, correctly left as a question rather than acted on here.

### Topic 2: Concurrency / atomicity of Emit vs. Observe
The consistency model under concurrent Observe and the atomicity of `A_K` transitions are genuinely new territory (the note works in a sequential transition model per SequentialTransitionAxiom). Correctly deferred.

VERDICT: REVISE
