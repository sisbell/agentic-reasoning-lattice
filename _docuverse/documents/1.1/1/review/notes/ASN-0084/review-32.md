# Review of ASN-0084

## REVISE

### Issue 1: TS2 cited where TS5 is needed

**ASN-0084, Canonical decomposition step (c), Forward extension case**: "Under b = c, we have v_c = v_b and n_c = n_b, so v_b + n_b = v_c + k_c = v_b + k_c, and TS2 gives n_b = k_c (using n_b ≥ 1 from S8 and k_c ≥ 1 from the contradiction assumption)"

**Problem**: TS2 (ShiftInjectivity) is "shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂" — same shift amount, different bases. Here we have the same base v_b with two potentially different shift amounts (n_b and k_c). Concluding n_b = k_c from shift(v_b, n_b) = shift(v_b, k_c) requires TS5 (AmountMonotonicity) contrapositively, not TS2. The author cites TS5 correctly elsewhere in the same proof (step (b), "v₁ = v₂" sub-case), so this is a citation slip.

**Required**: Change "TS2 gives n_b = k_c" to "TS5 gives n_b = k_c" (the contrapositive of strict monotonicity over the same base).

### Issue 2: R-WP and Q quantify over V_S(d) where they should quantify over dom(M(d))

**ASN-0084, R-WP statement**: "wp(REARRANGE_C, Q) ⇐ R-PRE(C) ∧ ASN-0036-invariants(Σ, d) ∧ (B is a correspondence-run partition of V_S(d) under M(d))" and Q's description "a correspondence-run partition of V_S(d) under M'(d) obtained from the pre-state partition B via Phases 1–3"

**Problem**: ASN-0036's S8 partitions dom(M(d)), not just V_S(d). R-BLK's proof itself works with "B = {b₁, ..., bₘ} a run partition of M(d) ... including runs whose V-extents lie in V_S(d) and runs whose V-extents lie in subspaces other than S," and its S8(a) discharge covers all of dom(M'(d)). The precondition's "of V_S(d)" is therefore too narrow to feed R-BLK, and Q's "of V_S(d)" claims less than R-BLK actually delivers (and less than S8 requires of an S8-witness on M'(d)).

**Required**: Restate both the precondition and Q in terms of dom(M(d)) / dom(M'(d)), so they align with ASN-0036's S8 statement and with R-BLK's actual input/output scope.

### Issue 3: "Order-reversal" appeal is not derived from NAT-sub axioms

**ASN-0084, existence-of-maximum helper lemma in canonical decomposition**: "For every s ∈ S, m ≤ B − s gives s ≤ B − m (by the involution and order-reversal of x ↦ B − x on {0, ..., B})"

**Problem**: The involution B − (B − s) = s is derived explicitly via NAT-sub right-inverse and NAT-cancel; good. But "order-reversal of x ↦ B − x" is then invoked as a generic property, not as a NAT-sub consequence. The needed step "m ≤ B − s ⟹ s ≤ B − m" requires (i) adding s to both sides to get m + s ≤ B (using NAT-sub right-inverse on (B − s) + s = B), then (ii) subtracting m from both sides — which itself needs a non-strict-monotonicity-of-(− m) argument with a case split on m + s = B versus m + s < B (since NAT-sub only ships *strict* monotonicity).

**Required**: Replace the "order-reversal" phrase with the explicit two-step NAT-sub derivation, so the proof rests on the foundation's named primitives rather than a generic algebraic intuition.

### Issue 4: Premature "every invariant is maintained" claim

**ASN-0084, State and Vocabulary, end of Invariant preservation paragraph**: "Every ASN-0036 invariant is therefore maintained by an arrangement rearrangement."

**Problem**: At the point this sentence appears, the audit has covered the content-store invariants (via C' = C), the dom-only invariants (via dom(M'(d)) = dom(M(d))), S2 (via bijectivity of π), S3 (via R-RI), and S5 (via multiset preservation) — but **not** S8(a)/(b), the existence/consistency of a correspondence-run decomposition under M'(d). Preservation of S8 requires R-BLK and is only discharged in R-WP, several sections later. The sweeping closing sentence overstates what has actually been established here.

**Required**: Restrict the closing sentence (e.g., "Every ASN-0036 invariant except S8(a)/(b) is therefore maintained; preservation of S8 is established constructively in R-WP via R-BLK"), or move the sentence to after R-WP. As written, it claims the conclusion before its load-bearing lemma has been introduced.

## OUT_OF_SCOPE

None beyond the Open Questions the ASN already lists (k-cut generalization, composition of rearrangements, run-count bounds, cut/run-boundary interaction).

VERDICT: REVISE
