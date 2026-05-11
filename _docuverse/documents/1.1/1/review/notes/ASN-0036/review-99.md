# Review of ASN-0036

## REVISE

### Issue 1: S7a/S7b textual order creates an unresolved logical dependency

**ASN-0036, S7a section**: S7a's statement uses `N(a).0.U(a).0.D(a)` (the projections supplied by T4b) before S7b establishes that `zeros(a) = 3` (the condition under which T4b's `D(a)` is well-defined for *every* `a ∈ dom(Σ.C)`).

**Problem**: The "Note on textual order" at the end of S7a's Depends list acknowledges this — "S7a's statement presupposes S7b" — but does not fix it. A reader encountering S7a in the textual order must either accept the projection as well-defined on faith or skip ahead. The alternative reading offered ("S7a could be conditioned on `zeros(a) ≥ 2`") is gestured at but not adopted.

**Required**: Either reorder so S7b is stated before S7a, or restate S7a's Axiom with the explicit conditioning `(A a : a ∈ dom(Σ.C) ∧ zeros(a) ≥ 2 :: N(a).0.U(a).0.D(a) is the allocating document)`.

### Issue 2: D-CTG-depth precondition cites S8-depth for `m ≥ 3`

**ASN-0036, D-CTG-depth Formal Contract**: "Preconditions: V_1(d) non-empty; common depth m ≥ 3 (S8-depth)."

**Problem**: S8-depth only guarantees a common depth `m ≥ 2` (via S8a's lower bound), not `m ≥ 3`. The bound `m ≥ 3` is an additional restriction that bounds when D-CTG-depth's claim is non-trivial — at `m = 2` the index range `2 ≤ j ≤ m − 1` is empty, so the claim is vacuous. The parenthetical citation makes it look like S8-depth supplies `m ≥ 3`, which it does not.

**Required**: Decouple the citation, e.g.: "Preconditions: V_1(d) non-empty; common depth m supplied by S8-depth, with `m ≥ 3` (the additional bound under which the claim is non-trivial; at `m = 2` the claim is vacuous since positions 2 through `m − 1` form an empty range)."

### Issue 3: Within-subspace incompatibility lemma elides `v ≤ t ⟹ v < t`

**ASN-0036, S8 proof, within-subspace incompatibility lemma, Case `j < m`**: "Then `tᵢ = vᵢ` for `i < j` and `tⱼ > vⱼ` (from `v ≤ t` by T1(i), since `j ≤ m = min(m, m)`)."

**Problem**: T1(i) applies to *strict* orderings (`v < t`), not non-strict (`v ≤ t`). The bridge step — `v ≤ t` combined with `t ≠ v` (from the lemma's hypothesis) gives `v < t`, which T1(i) then dispatches — is implicit. A reader has to reconstruct the move from `v ≤ t` to `v < t`.

**Required**: Make the bridge explicit: "Since `t ≠ v` (lemma hypothesis) and `v ≤ t` (from `t ∈ [v, shift(v, 1))`), we have `v < t`. T1(i) applied to `v < t` at first divergence position `j ≤ min(m, m)` yields `tⱼ > vⱼ`."

### Issue 4: D-CTG-depth alternative construction cites strict successor as `0 < i + 1`

**ASN-0036, D-CTG-depth proof**: "(Equivalently — and without invoking T0(a) more than once — the map i ↦ (v₁)ⱼ₊₁ + i + 1 is injective… and the image lies above `(v₁)ⱼ₊₁` because NAT-addcompat's strict successor inequality `0 < i + 1` combined with left order compatibility gives `(v₁)ⱼ₊₁ < (v₁)ⱼ₊₁ + (i + 1)` for every `i ∈ ℕ`.)"

**Problem**: NAT-addcompat's strict successor is `(A n ∈ ℕ :: n < n + 1)`, not `0 < i + 1` for arbitrary `i`. The cited inequality `0 < i + 1` is derived (NAT-zero gives `0 ≤ i`; strict successor at `n = i` gives `i < i + 1`; mixed `≤`/`<` transitivity composes them to `0 < i + 1`), but the proof presents it as if it were a direct axiom instantiation. Additionally, left order compatibility on `≤` doesn't directly produce a strict inequality — bridging to `(v₁)ⱼ₊₁ < (v₁)ⱼ₊₁ + (i + 1)` requires NAT-cancel to rule out equality, or use of right additive identity to rewrite `(v₁)ⱼ₊₁ + 0 = (v₁)ⱼ₊₁` and then the strict promotion.

**Required**: Either replace the parenthetical with a single citation to T0(a) (which the main argument already supplies) and drop the alternative, or spell out the derivation chain: NAT-zero `0 ≤ i`, strict successor at `n = i` giving `i < i + 1`, mixed `≤`/`<` transitivity giving `0 < i + 1`, then strict left order compatibility (NAT-addcompat plus NAT-cancel) giving `(v₁)ⱼ₊₁ < (v₁)ⱼ₊₁ + (i + 1)`.

### Issue 5: S8 auxiliary lemma conclusion (ii) wording understates the prefix-copy argument

**ASN-0036, S8 proof, auxiliary lemma, Conclusion (ii)**: "The three field-separator zeros of `aⱼ` (between `N`, `U`, `D`, and `E`, sitting at positions `< #aⱼ`) are copied unchanged into `shift(aⱼ, k)` by the prefix rule, and no additional zero is introduced at position `#aⱼ`, so `zeros(shift(aⱼ, k)) = zeros(aⱼ) = 3`."

**Problem**: The argument as stated only addresses the three field-separator zeros and position `#aⱼ`. It does not explicitly rule out new zeros being introduced at *non-separator* positions strictly before `#aⱼ`. The TumblerAdd prefix rule copies *every* component at positions `i < #aⱼ` unchanged from `aⱼ` — including non-separator components whose nonzero status is therefore preserved. The reader has to reconstruct this from the citation alone.

**Required**: State explicitly: "By TumblerAdd's prefix rule, every component of `shift(aⱼ, k)` at position `i < #aⱼ` equals `(aⱼ)ᵢ`, so the zero/nonzero status of each such position is preserved. The three field-separator zeros (at positions 2, 4, 6 in the canonical N.0.U.0.D.0.E pattern) are therefore inherited unchanged, and no new zero appears at any position `i < #aⱼ`. At position `#aⱼ`, the value `aⱼ_{#aⱼ} + k > 0`, so no zero is introduced there either. Hence `zeros(shift(aⱼ, k)) = zeros(aⱼ) = 3`."

## OUT_OF_SCOPE

### Topic 1: Whether DELETE/INSERT/COPY/REARRANGE preserve D-CTG and D-MIN

**Why out of scope**: Explicitly listed in the ASN's Scope: "Operation-specific effects (INSERT, DELETE, COPY, REARRANGE frame conditions and postconditions)". The ASN correctly delegates preservation of the contiguity invariants to each operation's own ASN. The open question is recorded.

### Topic 2: Link-subspace contiguity semantics

**Why out of scope**: The ASN deliberately binds D-CTG, D-MIN, D-CTG-depth, and D-SEQ to the text subspace `S = 1` and notes that link-subspace semantics (sparse, append-only with tombstones) are deferred. The remark following S8a and the Frame notes throughout make this explicit.

### Topic 3: Subspace alignment between V-positions and I-addresses

**Why out of scope**: The ASN explicitly defers this to the operations layer ("Remark (subspace alignment deferred)"). The open question is recorded. Gregory's implementation evidence (cited in the remark) supports the design choice.

### Topic 4: Canonical decomposition uniqueness

**Why out of scope**: S8 asserts existence of *some* finite decomposition, not uniqueness or canonical form. The ASN labels this as Non-canonicality and routes the question to operations-layer behavior. The open question is recorded.

### Topic 5: Specific value of `m` for the first-placement depth

**Why out of scope**: The strand model fixes only the lower bound `m ≥ 2` for `ValidFirstInsertionPosition`. The specific value (Nelson's "subdivision by further digits") is an operation-layer convention. The open question is recorded.

VERDICT: REVISE
