# Review of ASN-0043

## REVISE

### Issue 1: PrefixSpanCoverage cites the wrong foundation axiom for `n < n + 1`

**ASN-0043, PrefixSpanCoverage lemma, *Inclusion* direction**: "we have `c_{#x} = x_{#x} < x_{#x} + 1 = shift(x, 1)_{#x}` (strict successor by NatDiscreteness (NAT-discrete, ASN-0034))"

**Problem**: The strict successor inequality `(A n ∈ ℕ :: n < n + 1)` is the third Axiom clause of NAT-addcompat (NatAdditionOrderAndSuccessor), not NAT-discrete. NAT-discrete supplies `m < n ⟹ m + 1 ≤ n`, which requires a *prior* strict inequality as antecedent — it cannot produce `n < n + 1` directly. The lemma later cites NAT-discrete correctly in the exclusion direction at `j = #x` ("`t_{#x} > x_{#x}` ⟹ `t_{#x} ≥ x_{#x} + 1`"), where the antecedent is a separate strict inequality from T1(i), confirming that NAT-discrete is the wrong axiom for the inclusion step.

**Required**: Replace "(strict successor by NatDiscreteness (NAT-discrete, ASN-0034))" with "(strict successor by NatAdditionOrderAndSuccessor (NAT-addcompat, ASN-0034))" in the inclusion direction. The exclusion direction citation is correct and should be left alone.

## OUT_OF_SCOPE

### Topic 1: Relocation of PrefixSpanCoverage to span/tumbler algebra

The PrefixSpanCoverage lemma proves a span-coverage identity that is independent of the link model — it consumes only tumbler-algebra primitives (T1, OrdinalShift, TA-strict, Divergence, NAT-discrete). Its current placement in ASN-0043 is structural; the lemma would serve link, content, and arrangement models alike. This is restructuring work for a future tumbler/span algebra ASN, not a correctness issue in this ASN.

### Topic 2: State-transition discipline for `dom(Σ.M)`

L1a's strengthening to require `home(a) ∈ dom(Σ.M)` is sound as a per-state invariant, but the ASN does not address whether state transitions may remove documents from `dom(Σ.M)`. If a document could be removed while links pointing under its prefix persist, L1a would be violated. Either an `Σ.M`-monotonicity axiom parallel to S1/L12a, or an operations-layer constraint forbidding document removal in the presence of dependent links, is needed. This belongs in the operations layer or a separate document-lifecycle ASN.

### Topic 3: Whether "conforming" in L9/L11b includes all ASN-0036 invariants

L9 and L11b formally quantify over "states satisfying L0–L14, L-fin, and S0–S3" — a strict subset of ASN-0036's invariants. The witness constructions implicitly preserve S4–S9, D-CTG, D-MIN, D-SEQ, S8a, S8-depth, S8-fin, S7a–d, but this is not made explicit. Whether to tighten the L9/L11b precondition to include the full ASN-0036 invariant set, or to keep the minimal conformance set, is a design decision for cross-ASN consistency, not a defect in this ASN's claims.

VERDICT: REVISE
