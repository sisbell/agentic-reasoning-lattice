# Review of ASN-0084

## REVISE

### Issue 1: R-PRE(v) is derivable, not a precondition

**ASN-0084, R-PRE clause (v)**: "Both transposed regions are non-empty: w_α ≥ 1 and w_β ≥ 1."

**Problem**: This is derivable from R-PRE(iv) combined with CS2, CS3, CS4. CS2 gives c₀ < c₁ < c_{n−1}, so by T1 strict ordering on singleton ordinals (and NAT-discrete) ord(c₁) ≥ ord(c₀) + 1; combined with CS3+CS4 placing c₀ at depth 2 in subspace S and R-PRE(iv) placing c₀ in V_S(d), we have c₀ ∈ α (since c₀ ≤ c₀ < c₁), so w_α ≥ 1. Similarly for w_β. The ASN already proves the parallel claim w_μ ≥ 1 as a derived consequence, but lists w_α, w_β ≥ 1 as preconditions.

**Required**: Either remove R-PRE(v) and move w_α ≥ 1 and w_β ≥ 1 into "Consequences of R-PRE" (parallel to the existing w_μ ≥ 1 derivation), or annotate that R-PRE(v) restates derived consequences.

### Issue 2: Permutation Displacement carrier canonical form not stated

**ASN-0084, Definition — PermutationDisplacement**: "Δ(v) is a signed magnitude `(σ, n) ∈ {+, −, 0} × ℕ`..."

**Problem**: The encoding admits four spurious pairs — (+, 0), (−, 0), (0, n) with n ≥ 1, and any (σ, n) with σ ≠ {+,−,0} — that the case analysis never produces but the carrier admits. Equality comparison Δ(v₁) = Δ(v₂) on the raw carrier could match (+, 0) ≠ (0, 0) for two positions that both have π(v) = v under different encodings. The ASN says equality is the only operation used; without a canonical-form constraint, equality is ambiguous.

**Required**: Add a canonical-form clause: the only values produced are (0, 0), (+, n) with n ≥ 1, and (−, n) with n ≥ 1. State that equality compares these canonical forms.

### Issue 3: R-PPERM/R-SPERM piecewise definitions are silent on non-S positions

**ASN-0084, R-PPERM**: The piecewise definition lists "exterior", "α → end", "β → start" but no non-S branch. Same for R-SPERM.

**Problem**: Non-S positions (subspace > S = 1) satisfy v > c_{n−1} under T1 (divergence at position 1 with subspace value > 1), so they fall under the "exterior" branch — but this is buried in the proof prose ("the first branch ... fires on the subspace(v) ≠ S case via R-FRAME-P(a)") and not visible in the piecewise notation. A reader checking that π is total on dom(M(d)) sees three cases keyed to V_S(d)-style conditions and no apparent case for v ∈ dom(M(d)) with subspace(v) ≠ S.

**Required**: Either add an explicit non-S branch (e.g., "π(v) = v if subspace(v) ≠ S") at the top of the piecewise definitions, or annotate the "exterior" case to read "(exterior or non-S)".

### Issue 4: Maximality of the constructed canonical run is implicit

**ASN-0084, Canonical decomposition, step (a)**: "the maximal run containing v is (v_s, M(d)(v_s), r(v) + 1 + f(v)), and it is uniquely determined by the values of r(v) and f(v)."

**Problem**: The proof establishes f(v) and r(v) as maxima of bounded sets and constructs a run from them. But the claim that this run is *maximal* in the canonical-partition sense (no further extension possible) is asserted, not proved. The reader must infer that f(v) being the max forbids forward extension and r(v) being the max forbids backward extension. Step (b)'s correctness depends on (a) actually producing a maximal run.

**Required**: After the construction, add an explicit paragraph: "This run is maximal: extending forward to v + f(v) + 1 would require M(d)(v + f(v) + 1) = M(d)(v) + f(v) + 1, but the definition of f(v) as max rules this out; extending backward to [S, ord(v) − r(v) − 1] is similarly forbidden by the maximality of r(v)."

### Issue 5: Mutual exclusivity of Δ cases not established for non-S positions

**ASN-0084, Definition — PermutationDisplacement**: The three cases (π(v) = v), (ord(π(v)) > ord(v)), (ord(π(v)) < ord(v)) are listed sequentially.

**Problem**: For V_S(d) positions at depth 2, mutual exclusivity follows from T1 trichotomy on ord (since ord determines V-position in subspace S at depth 2). For non-S positions, ord(v) is a multi-component tumbler (length m_S − 1 ≥ 1) and NAT-sub on multi-component tumblers is undefined. The cases (+) and (−) compute ord(π(v)) − ord(v) using subtraction. The ASN never resolves whether the subtraction is well-typed for non-S ordinals, or whether non-S positions trivially fall under case (a) because π = identity.

**Required**: Add an explicit clause: "For non-S positions, π(v) = v by R-PPERM/R-SPERM, so case (a) applies and Δ(v) = (0, 0); cases (+) and (−) are never reached. For V_S(d) positions, ord is single-component (depth 2) and the cases are exhaustive and mutually exclusive by T1 trichotomy on ord(π(v)) and ord(v)."

### Issue 6: Informal "sign(w_β − w_α) · |w_β − w_α|" notation suggests undefined operations

**ASN-0084, Permutation Displacement section (4-cut μ case)**: "Δ(v) = sign(w_β − w_α) · |w_β − w_α|   if v ∈ μ   (depends on width comparison; see below)"

**Problem**: The ASN explicitly states "We do *not* define addition, multiplication, or an ordering on the signed-magnitude carrier in this ASN." The notation sign(·) · |·| implies signed-integer multiplication on a carrier the ASN refuses to give multiplication on. The formal definition resolves this via case analysis correctly, but the informal commentary contradicts the carrier discipline.

**Required**: Replace the informal formula with explicit case notation: "Δ(v) on μ is determined by case analysis on w_β vs w_α; see formal cases below."

### Issue 7: TS5 label inconsistency

**ASN-0084, multiple sites**: "TS5 (AmountMonotonicity)"

**Problem**: The foundation defines this as "TS5 — ShiftAmountMonotonicity". ASN-0084 drops the "Shift" prefix in each occurrence (~5 sites).

**Required**: Use the foundation's exact label "ShiftAmountMonotonicity".

## OUT_OF_SCOPE

### Topic 1: Generalization to text subspace depth m_1 > 2

**Why out of scope**: The ASN explicitly restricts to m_1 = 2 (singleton-tumbler ordinals identified with naturals). Generalizing the displacement arithmetic to multi-component ordinals is a separate, substantial development that requires extending NAT-sub-style reasoning to tumbler-valued ordinals.

### Topic 2: k-cut rearrangements for k > 4

**Why out of scope**: The ASN itself names this as an open question; n ∈ {3, 4} is a design choice for this layer.

### Topic 3: Composition of multiple rearrangements

**Why out of scope**: Named as an open question; expressibility of a composition as a single REARRANGE is a separate result.

### Topic 4: Inverse REARRANGE operation

**Why out of scope**: The ASN defines REARRANGE; defining and proving correctness of REARRANGE⁻¹ (or showing self-inverse for swaps with equal widths) is future work.

### Topic 5: Cross-subspace transposition

**Why out of scope**: Explicitly excluded by the introduction; requires a separate operation definition with different region semantics.

### Topic 6: REARRANGE composition with INSERT/DELETE

**Why out of scope**: Requires INSERT and DELETE ASNs to be defined first, then a separate compositional analysis.

### Topic 7: Link subspace rearrangement

**Why out of scope**: The ASN restricts to text subspace (S = 1); link subspace has sparse-with-tombstones semantics (D-CTG exempts it) that the cut-point formulation does not directly support.

### Topic 8: Bound on canonical-partition run-count change

**Why out of scope**: Named as an open question; tying R-BLK Phase 2 region assignment to pre-state I-address arithmetic to predict post-merge mergeability requires separate analysis.

VERDICT: REVISE
