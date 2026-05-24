# Review of ASN-0094

## REVISE

### Issue 1: NAT-card termination measure cites the wrong axiom

**ASN-0094, "Locally derived NAT primitives (NAT-card, NAT-sub)"**: "the residual `S' := S \ {m}` is a strictly smaller finite subset of ℕ (NAT-discrete ensures the size-decrease is well-founded: the IH applies because `|S'|` corresponds to the predecessor `k − 1` under the recursive descent)"

**Problem**: NAT-discrete states `m ≤ n < m + 1 ⟹ n = m` — it forbids naturals strictly between consecutive successors. This says nothing about well-foundedness of subset removal. Worse, the parenthetical "|S'| corresponds to the predecessor k − 1" is circular: `|·|` is what NAT-card is in the process of defining, so it cannot serve as the decreasing measure. The cleanest correct argument inducts on `max(S)` (well-defined for nonempty S via NAT-wellorder applied to `S` itself, since `S ⊆ ℕ` is bounded above only after finiteness is assumed — better, induct on a parameter `n` with `S ⊆ {0, ..., n}`, well-founded by NAT-order on ℕ). Cited by AllocatedAddressAntichain Step 3.1 and RetractionTargetNotOnChain Step II.1, both of which inherit the unsoundness in their NAT-card invocations.

**Required**: Replace the well-foundedness argument with one that uses an external measure. Strong induction on `n` with `S ⊆ {0, ..., n}` (justified by `S` finite ⟹ S has an upper bound in ℕ, which NAT-wellorder gives via min on `{m : (A x ∈ S :: x ≤ m)}`) is the most direct. The NAT-sub derivation has the same defect — "well-founded by NAT-wellorder applied to the residual gap" is also unjustified; the residual gap `m − n` is what's being defined.

### Issue 2: Walkthroughs introduce K's after `Σ_init` without discharging the lifetime-constancy escape clause

**ASN-0094, "Tuple-Classifier", "Provenance (partial G-slot)", "Attributed Retraction"**: "Register `K = endorsed` with shape `(0, 1, -, A_rel, ⊤)`... Working from Σ_4 of the Comment example..." (similar phrasings in other walkthroughs).

**Problem**: The framework's "Lifetime constancy of `T_cat`" paragraph requires every `K ∈ T_cat` to be declared at `Σ_init`. The walkthroughs introduce new K's mid-stream (at Σ_4, at Σ_P0, etc.) and then invoke Sh0–Sh4 preservation theorems whose base case discharges against `L_K^{Σ_init} = ∅`. Either (a) the walkthrough relies on implicit `Σ_init` registration of `K` alongside `comment`, `K_res`, `R` — in which case the walkthrough's `T_cat` should be augmented to list `endorsed`, `attributed_by`, etc. at its preamble (as the Comment walkthrough does via its "Registered catalog for this walkthrough" callout) — or (b) the walkthrough is exercising the escape clause "verify `L_K^{Σ_registered} = ∅` at the registration point", in which case the verification is not exhibited. The Comment walkthrough is the model: state `T_cat` explicitly. Other walkthroughs are silent.

**Required**: Add a "Registered catalog for this walkthrough" preamble to each walkthrough, listing every K used (Tuple-Classifier: `{comment, K_res, R, endorsed}`; Provenance: `{..., attributed_by}`; etc.) and noting they are all declared at the framework's `Σ_init`.

### Issue 3: SHCD's "Coverage and Comment both use `idem = ⊥` but for different reasons" justification is informal

**ASN-0094, end of Coverage instantiation section**: "Coverage's `idem = ⊥` is principled — coverage tuples by design supersede each other (the `latest_K_for_addr` opt-in template surfaces this directly). Comment's `idem = ⊥` is incidental — comments differ in F or G even when 'looking the same' in content"

**Problem**: This is a design justification, not a formal property. The shape registry has no axis distinguishing "principled `idem = ⊥`" from "incidental `idem = ⊥`"; both rows carry the same shape tuple and Sh0–Sh4 treat them identically. If the distinction is operationally meaningful — and it appears so since only the principled case admits SHCD — that constraint should be made structural rather than left in commentary. Currently the catalog allows SHCD registration at any `(1, 1, A_doc, A_doc, ⊥)` K, including K's intended for Comment-style semantics where ordering by emission_order is semantically incoherent.

**Required**: Either accept that SHCD applies uniformly to all `(1, 1, A_doc, A_doc, ⊥)` K's (drop the "principled vs incidental" distinction), or introduce a structural marker (e.g., a `ordered` flag, or split Coverage and Comment into distinct catalog rows) so that the layer's choice of opt-in is constrained by registry-checkable shape components rather than by commentary.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link shapes
**Why out of scope**: The framework restricts to arity-3 standard triples per the *Arity scope* paragraph. Generalization to N-ary shapes requires extending the cardinality and target-domain vocabulary per extra slot; documented as future work.

### Topic 2: Cross-process / distributed substrate consistency
**Why out of scope**: Single-process substrate scope is explicitly committed under the *Sh4 idempotency contract*'s *Scope* clause and acknowledged in Open Questions. Multi-process generalization would require a coordination protocol outside the current framework.

### Topic 3: Mechanical derivation of template families from shape
**Why out of scope**: Sh5 is honestly framed as META — manual curation with mechanical *falsification* but not mechanical *derivation*. The cost is acknowledged in the catalog-extension paragraph.

### Topic 4: Ghost-targeting slot semantics
**Why out of scope**: The framework restricts slot addresses to allocated targets (rejecting ghosts via Sh-conf clause (d)), with the design question flagged in Open Questions. A future state-dependent conformance rule for ghost slots would extend the framework's scope rather than fix a defect in it.

VERDICT: REVISE
