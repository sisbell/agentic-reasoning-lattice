# Review of ASN-0102

## REVISE

### Issue 1: COPY invokes ValidComposite★'s coupling machinery without admitting COPY into its closed atomic vocabulary

**ASN-0102, Definition of COPY / X14**: "we add it to the system's transition vocabulary — the operation set `𝒦` (ASN-0047)" and later "Treating COPY as the length-1 composite it is, each is discharged."

**Problem**: ASN-0047's `ValidComposite★` defines a valid composite as "a finite sequence of atomic transitions ... drawn from the atomic vocabulary K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), and K.ρ" — a **closed enumeration**. The ASN simultaneously (a) declares COPY a genuinely new atomic operation that is "deliberately *not* an instance of K.μ⁺" and is irreducible to the listed atomics (because of the `· + W` relabelling), and (b) discharges J0/J1★/J1'★ by treating COPY "as the length-1 composite it is." But J0/J1★/J1'★ are clauses of `ValidComposite★`, whose clause-1 only admits steps from the enumerated list. COPY is not in that list, so "COPY-as-length-1-composite" is not a valid composite under the definition the ASN is invoking. Adding COPY to `𝒦` does not, by itself, extend `ValidComposite★`'s fixed enumeration. This same gap underwrites the X14 Old-branch reliance on P4★ (a composite-boundary property) holding at COPY's pre-state — which is only licensed if COPY's pre/post-states are recognized composite boundaries.

**Required**: Explicitly amend `ValidComposite★`'s atomic vocabulary to admit COPY (paralleling the foundation's own "(amended)" tags), and state that COPY's pre- and post-states are composite boundaries so the P4★ appeal in X14's Old-branch is grounded. Either that, or route the coupling discharge without leaning on `ValidComposite★`'s enumeration.

### Issue 2: No worked example exercises the genuinely distinct boundary cases

**ASN-0102, A worked example / A self-transclusion scenario**: both worked tables instantiate the same interior configuration (`p = 3`, non-empty subspace).

**Problem**: The standards require boundary cases (empty, first, last) to be checked concretely, and the operation's genuinely *different* configurations are exactly the ones not worked: (i) the empty-subspace first insertion (`n_S = 0`, depth `m` chosen, no pre-state D-SEQ to inherit), and (ii) the append/prepend extremes (`p = n_S + 1`, `p = 1`, where the unmoved or displaced class is empty). X16 derives the tiling for all `p` and parenthetically specializes `n_S = 0`, but the tiling/density and the J1★/J1'★ split (where `New = A`, `Old = ∅` for the empty case) are never verified against a specific instance — and the empty case is precisely where `m_S(d)` re-pinning and ValidFirstInsertionPosition replace D-SEQ. The two existing tables are both interior, so the prose claims for the boundaries remain unexercised.

**Required**: Add at least one worked instance for the empty/first-insertion case (`n_S = 0`, `p = 1`, some `W ≥ 1`) checking X1, X16 (density, min `[s_C,1,…,1]`), and the X14 coupling split, and ideally one append-boundary instance (`p = n_S + 1`, trailing boundary absent).

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content after subsequent re-displacement
**Why out of scope**: The first Open Question (origin ↔ continued discoverability under later displacement) concerns link-projection dynamics over edited arrangements, which is ASN-0098 territory and a future operation-interaction note, not a guarantee COPY itself must state.

### Topic 2: Behavior when an allocating document becomes unreachable
**Why out of scope**: The fourth Open Question (identity when the origin document is no longer reachable) depends on replication/garbage-collection semantics not yet in the model — new territory, not a defect in COPY's contract.

VERDICT: REVISE
