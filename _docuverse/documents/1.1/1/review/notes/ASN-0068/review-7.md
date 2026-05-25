# Review of ASN-0068

## REVISE

### Issue 1: CV-SPAN-VIEW signature is type-inconsistent
**ASN-0068, CV-SPAN-VIEW**: "`π_{m_a, m_b} : MaxRuns → P(Span × Span)`" with body `π_{m_a, m_b}(v_a, v_b, n) = ((v_a, δ(n, m_a)), (v_b, δ(n, m_b)))`.
**Problem**: The signature's codomain `P(Span × Span)` denotes the power set (sets of span-pairs), but the body returns a single span-pair — an element of `Span × Span`, not of `P(Span × Span)`. The function as written does not type-check. The Well-formedness postcondition reinforces this: "the output pair (σ_a, σ_b) ... consists of two level-uniform V-spans" — the output is named as a pair, not a set.
**Required**: Change the codomain to `Span × Span`. The per-run projection returns a single span-pair; the set-level lift (sending sets of runs to sets of span-pairs) follows by the standard image construction.

### Issue 2: Introduction's "bijection" claim conflates element-level and set-level
**ASN-0068, "The Input"**: "Equivalently, given a fixed admissible input `(d_a, R_a, d_b, R_b)` that determines `m_a, m_b` by S8-depth (ASN-0036), `Result` is in bijection with a subset of `P(Span × Span)` via the projection formalized below as CV-SPAN-VIEW."
**Problem**: `Result := P(T × T × ℕ⁺)` is a type whose elements are sets of runs. `P(Span × Span)` is a type whose elements are sets of span-pairs. CV-SPAN-VIEW (under any correct reading) provides a per-run projection π, not a `Result → P(Span × Span)` map. The claimed bijection requires lifting π to sets. The introduction states the bijection but does not name the lift; CV-SPAN-VIEW does not state it either. The relation between the per-run π and the set-level bijection is left to the reader.
**Required**: Either state the lifted map π* : P(T × T × ℕ⁺) → P(Span × Span) explicitly and derive its injectivity from per-run injectivity, or move the bijection claim to CV-SPAN-VIEW and state it there as a corollary. The "subset of P(Span × Span)" reading further requires specifying that the image is `π*(Result)`, not all of `P(Span × Span)`.

### Issue 3: "Exactly n_σ V-positions" claim ignores arrangement truncation
**ASN-0068, "The Input" (commentary following the CV-IN action-point analysis)**: "The exact constraint `actionPoint(width(σ)) = m_σ` forces `reach(σ)` to agree with `start(σ)` at all positions `1 ≤ i < m_σ` and differ only at position `m_σ`, yielding `⟦σ⟧ ∩ V_S(d)` as exactly `n_σ` consecutive depth-`m_σ` V-positions starting at `start(σ)`."
**Problem**: The intersection `⟦σ⟧ ∩ V_S(d)` is bounded both by n_σ (the span's V-extent at depth m_σ) and by `n_S(d) − s_m + 1` (the count of arrangement positions from start(σ) onward, with `s_m = start(σ)_{m_σ}` and `n_S(d) = |V_S(d)|`). When `s_m + n_σ − 1 > n_S(d)`, the span overshoots the arrangement and the intersection contains fewer than n_σ V-positions. The "exactly n_σ" claim holds only conditionally; admissibility (CV-IN) does not require the span to fit within the arrangement.
**Required**: Either (a) qualify with "exactly `min(n_σ, n_S(d) − s_m + 1)` consecutive V-positions", or (b) separate two claims: the span's V-extent at depth m_σ contains exactly n_σ tumblers (a property of the span alone, not depending on the arrangement); the intersection with V_S(d) may be truncated when the span exceeds the arrangement.

### Issue 4: CV-PRED's "valid V-position" predicate is implicitly restricted to D-SEQ★ form
**ASN-0068, CV-PRED**: "For a V-position `v` of depth `m` in subspace `S` (D-SEQ★, ASN-0047) and `j ≥ 0`..."; existence clause: "the candidate predecessor `v − j = [S, 1, ..., 1, v_m − j]` is a valid V-position precisely when its last component `v_m − j ≥ 1`".
**Problem**: The existence clause computes `v − j` assuming the D-SEQ★ form `[S, 1, ..., 1, v_m]`. Without D-SEQ★, a general depth-m positive-component tumbler in subspace S could have form `[S, 3, 7, 2, ...]`, and the predecessor expression `[S, 1, ..., 1, v_m − j]` would not be `v − j`. The text references D-SEQ★ in the precondition parenthetically but does not state that the definition is meaningful only on the D-SEQ★-structured V-positions. This matters because the candidate predecessor's S8a validity check (`v_m − j ≥ 1`) is necessary but not sufficient if `v` does not have the D-SEQ★ form.
**Required**: State explicitly that CV-PRED applies to V-positions in `V_S(d)` (which have the D-SEQ★ form by ASN-0047), or alternatively define `v − j` as the tumbler-level inverse of `+ j` (via TS2) without committing to a specific component form, and let the form follow from D-SEQ★ when `v ∈ V_S(d)`.

### Issue 5: Self-comparison admissibility derivation is informal
**ASN-0068, "The Input"**: "*Self-comparison is admissible.* CV-IN does not exclude `d_a = d_b`."
**Problem**: The text asserts self-comparison admissibility but does not work through the CV-IN clauses under `d_a = d_b`. The interesting clause is the per-span constraints: when `d_a = d_b = d`, `V_S(d_a) = V_S(d_b) = V_S(d)`, and the constraint `start(σ) ∈ V_S(d_a)` for `σ ∈ R_a` is independent of the constraint `start(σ') ∈ V_S(d_b)` for `σ' ∈ R_b`. The depths `m_a` and `m_b` collapse to a single `m_d`, so no `m_a ≠ m_b` complication arises. The "single span literal lies in R_a ∩ R_b" caveat becomes vacuous. None of this is stated.
**Required**: Add a brief paragraph (parallel to the existing self-comparison discussion) explicitly verifying CV-IN's clauses under `d_a = d_b`: confirm that the per-side constraints collapse cleanly, that `m_a = m_b = m_d`, and that the "single span literal" admissibility caveat is automatically satisfied.

### Issue 6: CV-PROV-FORGOTTEN's "exactly one" claim leans on S7 without invoking attribution-uniqueness
**ASN-0068, CV-PROV-FORGOTTEN**: "By S7 (ASN-0036), `a` was allocated by exactly one document `origin(a)`."
**Problem**: S7 establishes `origin(a)` as well-defined (a function of `a`) and invariant. The claim "allocated by exactly one document" is correct, but the load-bearing fact for the three-case lineage enumeration (origin = d_a, origin = d_b, origin = neither) is that `origin` is a *function* — a single-valued map. The text invokes S7 to support this without unpacking which postcondition of S7 supplies the single-valuedness.
**Required**: Cite S7 postcondition (b) explicitly: "origin(a) is the tumbler of the document that allocated a" — which combined with S7 postcondition (c) (cross-allocator distinctness for distinct documents) gives the function property. Alternatively, cite S7 postcondition (d) (invariance) and (b) together to establish single-valuedness across the system's history.

VERDICT: REVISE
