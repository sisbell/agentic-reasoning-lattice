**Dependency trace.** The six ASN-0036 claims form a layered structure: Σ.C is the primitive; S0, S7b, S7a, S7d are axioms over it; S7 is the main theorem that composes them. I read each axiom for internal consistency, then traced S7's proof step by step — well-definedness, identification, uniqueness, permanence — against the cited dependencies and the foundation statements.

---

**Well-definedness chain check.** S7's proof correctly establishes T4-validity via S7a→T10a.4 before invoking T4b's projections, and invokes S7b only afterwards for the zero count. The ordering is sound. T0's comprehension is correctly applied: the component map r is total and ℕ-valued (field components in ℕ⁺ ⊆ ℕ, separators 0 ∈ ℕ), so origin(a) ∈ T follows. The identification, uniqueness (S7d → GlobalUniqueness), and permanence (S0) steps are each individually sound.

**NAT-card application.** The zeros(origin(a)) = 2 computation turns on applying NAT-card to the set {#N(a)+1, #N(a)+#U(a)+2}. NAT-card's axiom requires exhibiting a strictly increasing enumeration — specifically that f(1) = #N(a)+1 < f(2) = #N(a)+#U(a)+2. The proof discharges this by computing the difference (#N(a)+#U(a)+2) − (#N(a)+1) = #U(a)+1, bounding it below by 2 from #U(a) ≥ 1, and concluding the strict inequality. That arithmetic chain — whether framed as subtraction (NAT-sub, right-telescoping) or as addition-monotonicity (#N(a)+1 + (#U(a)+1) = #N(a)+#U(a)+2, then right NAT-addcompat at #U(a)+1 > 0) — requires foundations not present in S7's Depends.

---

### NAT-card strict-ordering prerequisite ungrounded in S7's Depends
**Class**: REVISE
**Foundation**: NAT-card (NatFiniteSetCardinality) — cited in S7's Depends; its axiom requires a strictly increasing enumeration f with f.i < f.j for 1 ≤ i < j ≤ k
**ASN**: S7 (StructuralAttribution), well-definedness step — "These two indices are distinct: they differ by (#N(a)+#U(a)+2) − (#N(a)+1) = #U(a)+1, and T4a's non-emptiness of the U field — #U(a) ≥ 1, already established above — bounds that difference below by #U(a)+1 ≥ 2 > 0, so #N(a)+#U(a)+2 > #N(a)+1."
**Issue**: NAT-card is explicitly cited, signalling the cardinality step must be formally grounded. But the strict-ordering prerequisite f(1) < f(2) — i.e., #N(a)+1 < #N(a)+#U(a)+2 — is discharged by an arithmetic chain (difference computation, numeral bound, order conclusion) whose components require either NAT-sub (right-telescoping (m+n)−n = m) or NAT-addcompat (right strict-compatibility p ≤ n → p+m ≤ n+m), plus NAT-closure (for the numeral 2 := 1+1 used in #U(a)+1 ≥ 2), none of which appear in S7's Depends. The foundation claims T4a and T4b cite every arithmetic step at this granularity; S7's proof targets the same standard but leaves this step floating. The cited T4a supplies #U(a) ≥ 1 correctly; it is the arithmetic transformation from that bound to the strict inequality that lacks a grounding dependency.
**What needs resolving**: Add the missing arithmetic foundations to S7's Depends to ground the step. At minimum: NAT-addcompat (for the monotonicity reasoning #N(a)+1 < #N(a)+1+(#U(a)+1) = #N(a)+#U(a)+2 because #U(a)+1 > 0) and NAT-closure (for the numeral 2 := 1+1 and the bound 1+1 ≥ 1+1 = 2). Alternatively NAT-sub (right-telescoping for the difference form) plus NAT-order (for order from positive difference) suffice. The same additions ground the parallel `p ≥ 5` arithmetic earlier in the same step.

---

### S7b gloss drops T4-validity from dom(E) membership implication
**Class**: OBSERVE
**Foundation**: T4b (UniqueParse) — `dom(E) = {t ∈ dom(N) : zeros(t) = 3}` where `dom(N)` is the T4-valid subset of T
**ASN**: S7b (ElementLevelIAddresses) — "Hence `zeros(a) = 3` places `a` in `dom(E)`, so all four fields are present, the element field `E(a)` carrying the content-level address."
**Issue**: T4b defines dom(E) as requiring both zeros(t) = 3 and t ∈ dom(N) (T4-validity). S7b's axiom supplies only zeros(a) = 3. The gloss presents the dom(E) membership as a consequence of the zero count alone, silently dropping the T4-validity conjunct. A reader consulting S7b in isolation would infer that the zero count suffices, which is incorrect; T4-validity is established only in S7's well-definedness step via S7a → T10a.4. The formal axiom (zeros(a) = 3) is correct; the error is in the explanatory inference connecting it to dom(E).
**What needs resolving**: Qualify the gloss to note that dom(E) membership follows from zeros(a) = 3 together with T4-validity, the latter supplied by S7a → T10a.4 in S7's well-definedness step rather than by S7b itself.

---

VERDICT: REVISE