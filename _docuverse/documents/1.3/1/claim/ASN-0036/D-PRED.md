**D-PRED (PredecessorExistence).** Every natural at or above `1` is a successor — it has a predecessor inside `ℕ`:

`(A j ∈ ℕ : j ≥ 1 : (E i ∈ ℕ :: i + 1 = j))`.

Equivalently, every strictly positive natural `j` (the regime `j ≥ 1`, which over `ℕ` is `j > 0`) is `i + 1` for some `i ∈ ℕ`.

*Proof.* We want, for an arbitrary `j ∈ ℕ` with `j ≥ 1`, a natural `i` whose successor is `j`. The signature of `ℕ` runs the other way: NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034) gives the *forward* successor `i ↦ i + 1`, but the foundations posit no predecessor operation and no subtraction, so there is no term to evaluate at `j`. Nor does the bare order fact `j ≥ 1` name an `i` with `i + 1 = j`; that `i` must be produced. We produce it by induction on `j`, the induction principle on `j ≥ 1` underwritten by NAT-wellorder (NatWellOrdering, ASN-0034), the least-element principle in the same role it plays for the depth inductions of ASN-0034 and the count induction of D-INJ. The induction is what carries us from the two cases below to *all* of `{j ∈ ℕ : j ≥ 1}`; we do not separately presuppose that every such `j` is a successor — that conclusion is exactly what the principle delivers.

**Base `j = 1`.** Take `i = 0`. The witness lies in the carrier — `0 ∈ ℕ` by NAT-zero (NatZeroMinimum, ASN-0034) — and `i + 1 = 0 + 1 = 1 = j` by NAT-closure's left-identity clause `0 + n = n` read at `n := 1`. So `1` is the successor of `0`, and the case `j = 1` holds.

**Step `j = k + 1`.** A positive natural presented in successor form `k + 1` with `k ∈ ℕ` is its own witness's successor: take `i = k`. The witness lies in the carrier — `k ∈ ℕ` by hypothesis — and `i + 1 = k + 1 = j` holds by the reading of `j`, the successor `k + 1` itself lying in `ℕ` by NAT-closure's successor closure `n + 1 ∈ ℕ`. (The step does not lean on the induction hypothesis; it is the induction *principle*, reaching `k + 1` from `k`, that does the carrying.) So `k + 1` is the successor of `k`, and the step holds.

By the induction principle the two cases exhaust `{j ∈ ℕ : j ≥ 1}`, so each such `j` carries a predecessor `i ∈ ℕ` with `i + 1 = j`. ∎

The lemma exports existence only — which is all its consumer needs. D-INJ's renumbering meets the lemma in its above-`k₀` surjectivity sub-case: there a punctured-segment value `j > k₀` must be exhibited as `ρ.i = i + 1 = j`, and D-PRED hands the index `i` before the bounds `k₀ ≤ i ≤ P` are read off `i + 1 = j`. That consumer needs only *some* predecessor, never a *unique* one, so we prove and export existence alone and make no uniqueness claim — keeping the lemma's footing to the three foundations the construction actually uses.

*Formal Contract:*

- *Lemma:* `(A j ∈ ℕ : j ≥ 1 : (E i ∈ ℕ :: i + 1 = j))` — every natural `j ≥ 1` (equivalently, over `ℕ`, every `j > 0`) is the successor `i + 1` of some natural `i`. Proved by induction on `j` (the induction principle underwritten by NAT-wellorder): at the base `j = 1` the predecessor is `i = 0`, with `0 ∈ ℕ` (NAT-zero) and `0 + 1 = 1` (NAT-closure's left identity `0 + n = n` at `n := 1`); at a successor `j = k + 1` with `k ∈ ℕ` the predecessor is `i = k`, with `k + 1 ∈ ℕ` (NAT-closure's successor closure). The induction principle, not the hypothesis, supplies the structural fact that every `j ≥ 1` is reached as a successor; only existence is exported — the downstream use (D-INJ) needs some predecessor, not a unique one, so the lemma makes no uniqueness claim.

- *Depends:*
  - NAT-wellorder (NatWellOrdering, ASN-0034) — supplies the induction principle on `j ≥ 1` that underwrites the proof, its least-element principle in the same meta-level role it plays for the depth inductions of ASN-0034 and the count induction of D-INJ. This is the load-bearing axiom: the order fact `j ≥ 1` does not on its own name a predecessor, and it is the induction principle — base `1`, step `k ↦ k + 1` — that licenses the passage to "every `j ≥ 1` is a successor"
  - NAT-zero (NatZeroMinimum, ASN-0034) — supplies `0 ∈ ℕ`, the base-case predecessor witness `i = 0`, so that the predecessor of `1` lies inside the carrier rather than outside it
  - NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034) — supplies the left-identity clause `0 + n = n`, instantiated at `n := 1` to read `0 + 1 = 1` and close the base case, and the successor closure `n + 1 ∈ ℕ`, which keeps the step's witness `i = k` and its successor `k + 1` ℕ-valued; it is also the foundation that furnishes the forward successor `i ↦ i + 1` while furnishing no predecessor inverse, which is why existence must be established rather than read off a term
- *Forward References:*
  - D-INJ (InjectiveImageCardinality) — downstream consumer of this lemma; its above-k₀ surjectivity sub-case draws the predecessor `i` from D-PRED and is the motivating use that bounds the lemma to existence alone
