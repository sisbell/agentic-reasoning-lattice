# Review of ASN-0047

## REVISE

### Issue 1: S8★ K.μ⁻ preservation argument is split across three locations with a back-pointing deferral chain
**ASN-0047, S8★ definition (closing paragraph) vs. Class (a) verification prose vs. verification matrix**: The S8★ definition closes with "S8★ is a per-state invariant carried through the verification matrix; each transition preserves it, as the matrix records," immediately followed by a *full* K.μ⁻ discharge ("Under a K.μ⁻ contraction, S8★ is discharged per subspace by the same two routes... *Content subspace:* ... *Link subspace:* ..."). The matrix S8★/K.μ⁻ cell says "see *S8★* prose below"; the verification *S8★* prose then says "Established per-subspace by the two routes specified at S8★'s definition."
**Problem**: A reader chasing the K.μ⁻ discharge is bounced matrix → verification prose → back to the definition. The substantive preservation argument (a verification obligation) lives in the *definition* slot, while the verification prose and matrix cell both defer elsewhere. The definition also asserts "the matrix records it" and then records it again. This is a multi-hop deferral to the same content plus preservation prose misplaced into a definition.
**Required**: Put the K.μ⁻ S8★ discharge once, in the verification prose where the matrix cell already points, and have the definition define S8★ only.

### Issue 2: Full-clearance form box carries a downstream-consumer / use-site inventory
**ASN-0047, *Decomposition of K.μ~*, "Full-clearance form (canonical statement)"**: "...This form realises *every* admissible π without per-π precondition checks... **Step (A), Step (B), and the sufficiency construction below all reference this single form; the *Decomposition* paragraph at the end of the section gives the concrete K.μ⁻ + K.μ⁺ write set that realises it.**"
**Problem**: The bolded sentence is a use-site inventory — it enumerates which later passages consume the form rather than advancing what the form *is*. It matches the flagged accretion pattern ("a definition's introduction enumerates downstream consumers"). The reader must skip past it to reach the operative content.
**Required**: Keep the operative claim (the full-clearance form realises every admissible π, with vacuous K.μ⁻ suffix-removal and fresh K.μ⁺ writes) and drop the inventory of downstream references.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal / tombstoning mechanism reconciling Nelson's LM 4/9 with D-CTG★
The ASN's own open questions correctly identify that D-CTG★/D-MIN★ confine K.μ⁻ to link-subspace *suffix* truncation, so interior-link withdrawal would require a separate mechanism (status flag / tombstone). This is new territory, not a defect in the present transition model.
**Why out of scope**: A withdrawal/tombstone primitive and its invariants are a future ASN; the present ASN's contraction contract is internally consistent.

### Topic 2: Concurrency / serialization of link and content allocation under a shared home document
Raised in the open questions. The ASN assumes SequentialAtomicTransitions (inherited axiom); concurrent allocation coordination is outside the sequential model.
**Why out of scope**: Concurrency is explicitly deferred and the sequential model is self-consistent.

I checked the substantive proof obligations — K.δ case-(ii) freshness discharge across k∈{0,1,2}, the D-SEQ★ derivation (including the m=3 boundary of the u_M construction), K.μ~ link-subspace fixity and K.μ~-FIX, S3★/P7a/J1★ chaining, FrontierEquivalence, and the worked-example arithmetic — and found no correctness gaps; boundary cases (empty arrangement, full clearance, first/last insertion, single-position contraction) are covered.

VERDICT: REVISE
