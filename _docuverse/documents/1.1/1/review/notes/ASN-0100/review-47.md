# Review of ASN-0100

## REVISE

### Issue 1: §Effect One re-derives a foundation lemma instead of citing it
**ASN-0100, "Background... Discovering the Three Effects → Effect One: Allocation"**: "The `a_k ∉ dom(Σ_k.C)` clause holds by ChainEnumerationInjectivity (ASN-0093)... By ChainMembershipForOrigin (ASN-0093)... and cross-origin elements... are distinct... by SubAllocatorBundle (ASN-0047)... The `a_k ∉ dom(Σ_k.L)` clause is discharged by subspace separation. By DisjointSubAllocatorChains (ASN-0093)... L0... SC-NEQ..."
**Problem**: This is a step-by-step reconstruction of exactly ASN-0093's **SubsequentEmissionFreshness** lemma, whose statement is "the subsequent emission... `a = inc(a_prev, 0)`... is fresh against `dom(C) ∪ dom(L)`. Freshness splits three ways: Within-document... Cross-document... Cross-subspace..." — the identical three-way split, with the identical citations. The foundation already proves this; the ASN reinvents it. The same re-derivation is then invoked again twice ("by the chain-injectivity and subspace-disjointness arguments of §Effect One" in both §Provenance and §Atomicity).
**Required**: Cite ASN-0093's SubsequentEmissionFreshness (and FirstEmissionFreshness for the `m_d = 0` boundary) for the K.α freshness discharge; delete the manual reconstruction and the two later back-references to it.

### Issue 2: Open Question 6 is already answered in the body
**ASN-0100, "Open Questions"**: "What abstract guarantee constrains the order in which the K.α firings of step 1 of the substrate composite may be interleaved with the K.ρ firings of step 4, and does any such reordering produce an externally observable difference?"
**Problem**: §Atomicity already derives this in full: "The only forced ordering on K.ρ(a_k, d) is that it follow its own K.α(a_k)... relative to K.μ⁺ it commutes," and on observability: "External observers see the composite boundary; the intermediate states are not externally observable" together with the uniqueness-of-Σ' derivation. An "Open Question" whose answer the ASN proves is not open.
**Required**: Remove the question, or restate it as something the body does not resolve.

### Issue 3: Duplicated D-CTG★ closed-interval argument
**ASN-0100, "Sequential text-subspace structure (D-CTG★, D-MIN★, D-SEQ★)"**: the non-empty paragraph "For D-CTG★ we must discharge the full closed-interval form... if some `z_j > 1` for a least `j`... `z > max` by T1 case (i) — contradicting `z ≤ max`..." and the empty-case bullet "we discharge the full closed-interval form over the entire depth-`m`... if some `z_j > 1` for a least `j`... `z > max` by T1 case (i)... contradicting `z ≤ max`."
**Problem**: The two paragraphs are the same argument verbatim with `min`/`max` relabeled. Two paragraphs saying the same thing.
**Required**: State the closed-interval reduction once (e.g., as a one-line lemma over the generic extremes `[s_C,1,…,1]` and `[s_C,1,…,1,K]`) and apply it to both cases by instantiating `K`.

### Issue 4: Forward-reference accretion and meta-prose (anti-bloat)
The note carries `review-mode.anti-bloat`; the following are meta-prose that does not advance the argument:

- **§Effect Three, "The foundation's frozen-store frames do not transfer."**: "Every post-state invariant those frames would have supplied — S2, S3★, S8a, S8-depth, S8-fin, the S7 family — is therefore re-derived directly in §Verifying the Invariants." A use-site inventory plus a forward pointer; the warning that I3-C/I3-S7 cannot be imported can be made in one clause without enumerating consumers and re-derivation sites.
- **Repeated deferral**: "this first insertion fixes `m_C = m` for `d` (§The Operation's Inputs)" appears in §Discovering the Three Effects (empty case), §Sequential text-subspace structure, the empty-case S8-depth bullet, and the INS.inv.depth table row — the same fact deferred to the same location ≥4 times.
- **INS.chain-shift introduction**: "admits an equivalent ordinal-shift reading that is **load-bearing wherever a contiguous run of `A_C(d)`'s emissions is treated as a single mapping block**." A downstream-consumer justification; state the identity, not where it will be used.
- **§Per-subspace span decomposition (S8★)**: "its existence guaranteed by C1a applied to the restriction `M'(d)|_{V_{s_C}(d')}` **(preconditions discharged below)**" — the preconditions are discharged *above* (opening paragraph of the same section), not below; the pointer is mis-directed and accreted. The section also repeats the parallel construction "supplied not by M2 ... but by C1a" / "supplied not by M12 ... but by C1a" — fold into one statement.

**Required**: Strip the use-site inventories and downstream-consumer justifications; state each fact once at its home and reference by claim label only; fix the "discharged below" mis-pointer.

### Issue 5: Coupling-discharge prose duplicated across sections
**ASN-0100, "The Operation: Formal Contract → Effect — Provenance"** fully argues J1★/J1'★/J0 ("For Insertion positions, the K.α-allocated `a_k` is freshly placed... so J1★ requires `(a_k, d) ∈ R'`... Conversely, J1'★... J0... requires..."), and **§Provenance (R, P4★, P4a, P7a)** re-proves the same three couplings in the same terms.
**Problem**: The contract slot should state the effect; the dedicated proof section should prove it. Proving it in both is duplicate prose. (The worked-example discharge is a concrete instance and is fine.)
**Required**: In the Formal Contract, state `R' = R ∪ {(a_k,d)}` and assert the couplings hold; move the argument solely to §Provenance.

## OUT_OF_SCOPE

### Topic 1: Partial-failure recovery of canonical order (Open Question 1)
**Why out of scope**: Implementation crash-recovery semantics are below this ASN's abstraction level (the ASN itself flags concurrency control as such); a legitimate future question, not a defect here.

### Topic 2: Link-subspace insertion (Open Question 2)
**Why out of scope**: K.μ⁺_L / K.λ insertion is explicitly bounded out and belongs to a separate operation ASN.

META: not applicable — the ASN stays at the level of state, operations, and invariants, keeping concurrency mechanism and the "knife" implementation below its abstraction line.

VERDICT: REVISE
