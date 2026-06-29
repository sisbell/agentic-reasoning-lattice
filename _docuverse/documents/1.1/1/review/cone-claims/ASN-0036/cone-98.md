The foundation chain (NAT-carrier → NAT-order → NAT-zero → NAT-closure → NAT-discrete → NAT-addcompat → NAT-cancel → NAT-card → NAT-wellorder → NAT-induction → T0 → T0(a) → T1 → T3 → T4) is internally consistent and every exported consequence is used within its stated scope.

**D-INJ** — The induction on P is correctly structured. Base P = 1: the vacuously-increasing singleton enumeration is exhibited. Step P → P+1: the renumbering ρ is injective (three exhaustive cases covering a < b < k₀, a < k₀ ≤ b, k₀ ≤ a < b) and surjective onto {1,…,P+1}\{k₀} (both below-k₀ and above-k₀ sub-cases grounded by NAT-discrete + NAT-cancel + D-PRED). The composite h′ = h∘ρ supplies S′ = S\{μ}, IH gives |S′| = P, and prepending μ to g′ yields a strictly-increasing length-(P+1) enumeration of S. The three strict-increase obligations (across-seam, beyond-seam, spanning-seam) are all discharged. NAT-card's uniqueness clause then reads |S| = P+1. ✓

**D-PRED** — The induction set H = {n ∈ ℕ : n = 0 ∨ (E i ∈ ℕ :: i+1 = n)} contains 0 (left disjunct) and is closed under successor (witness i = k for the step k+1). NAT-induction gives H = ℕ. For j ≥ 1, the zero alternative is excluded by 0 < 1 ≤ j (NAT-addcompat + NAT-order transitivity + irreflexivity). ✓

**D-CTG-depth** — The proof by contradiction is sound. Agreement before position j is established (subspace component by membership in V_1(d); interior components by NAT-addcompat + NAT-order transitivity + NAT-discrete descending i < m to i+1 ≤ m, then j-minimality). The T1 witness is pinned to k = j by two-sided exclusion. The explicit witness w satisfies all of D-CTG's inner-quantifier guards (w ∈ T by T0 comprehension; subspace(w) = 1 from j ≥ 2; zeros(w) = 0 from S8a's positivity consequence + NAT-order transitivity on the new component + NAT-closure's 0 < 1 for the constant-1 tail). D-CTG forces w ∈ V_1(d). The N+1 witnesses are built by N+1 fixed applications of T0(a) (a finite iteration of fixed length drawn from S8-fin's N, not a choice-principle argument). D-INJ reads the pulled-back index set's cardinality as N+1; NAT-card's upper bound caps it at N; NAT-addcompat + NAT-order transitivity + irreflexivity yield the contradiction N < N. ✓

---

### Mixed-transitivity form cited as a named NAT-order consequence
**Class**: OBSERVE
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: D-PRED Depends ("NAT-order … supplies the mixed transitivity a < b ∧ b ≤ c ⟹ a < c"); D-INJ Depends ("its transitivity (both the pure < form and the mixed a < b ∧ b ≤ c ⟹ a < c form)"); D-CTG-depth Depends (same)
**Issue**: The form `a < b ∧ b ≤ c ⟹ a < c` is cited as something NAT-order "supplies" — implying it is an exported consequence — but NAT-order's Formal Contract exports only exactly-one trichotomy and ≤-transitivity. The mixed form is not named there. It is derivable from the ≤-definition by a two-case split (`b < c` gives `a < c` by pure transitivity; `b = c` gives `a < c` by Leibniz substitution), but that derivation is inline and uncited, not a postcondition a downstream consumer can name. A formal verifier targeting the exported contract has no named lemma to invoke here.
**What needs resolving**: Either add the mixed form `(A m, n, p ∈ ℕ : m < n ∧ n ≤ p : m < p)` (and symmetrically `m ≤ n ∧ n < p ⟹ m < p`) as a named Consequence in NAT-order's Formal Contract with its two-case derivation, or expand each citation site to show the inline two-case split from the existing exported tools.

---

### D-CTG-depth Depends entries for D-PRED and NAT-cancel attribute D-INJ's ρ construction to D-CTG-depth
**Class**: OBSERVE
**Foundation**: D-INJ (InjectiveImageCardinality); D-CTG-depth (SharedPrefixReduction)
**ASN**: D-CTG-depth Formal Contract Depends — D-PRED entry: "supplies the existence of the predecessor i ∈ ℕ … that the renumbering ρ's above-k₀ surjectivity sub-case turns on"; NAT-cancel entry: "to settle the renumbering ρ's injectivity in its same-branch upper case"; NAT-discrete entry describes "both sub-cases of the renumbering ρ's surjectivity onto the punctured segment" exclusively, omitting D-CTG-depth's own direct use (i < m ⟹ i+1 ≤ m for the interior range bound)
**Issue**: D-CTG-depth has no renumbering ρ and no index k₀; those are internal to D-INJ's proof. D-PRED and NAT-cancel appear in D-CTG-depth's Depends explaining D-INJ's proof steps as if they were D-CTG-depth's direct steps — making them false direct-dependency entries (they are only transitive through D-INJ). NAT-discrete is correctly a direct dependency (D-CTG-depth uses it at `(i, m)` for the interior range), but the Depends explanation entirely describes D-INJ's ρ-surjectivity use and omits D-CTG-depth's own application. A reader or formal verifier consulting D-CTG-depth's Depends would search for a ρ construction that does not exist in D-CTG-depth's proof, and would miss the actual direct use of NAT-discrete.
**What needs resolving**: Remove D-PRED and NAT-cancel from D-CTG-depth's Depends (they are transitive through D-INJ, which is already listed). Rewrite the NAT-discrete Depends entry to describe D-CTG-depth's direct use — instantiation at `(m, n) := (i, m)` to derive `i+1 ≤ m` from `i < m` in the interior-range placement step — rather than D-INJ's ρ-surjectivity sub-cases.

---

### Proof-internal witness construction placed in the *Definition* slot of D-CTG-depth's Formal Contract
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: D-CTG-depth Formal Contract — *Definition* field: "For positions u, x ∈ V_1(d) (u < x, both depth m) whose first disagreement is at component j … the intermediate witness w of depth m is constructed by …"
**Issue**: The *Definition* slot in a claim's Formal Contract is the site for terms exported for downstream citation. The intermediate witness w is a proof-internal existential object; it is not exported, no downstream claim cites it by name, and it does not appear in the Postconditions as a defined symbol. Placing it in the *Definition* slot implies a status it does not have, and may cause a pipeline tool to treat the construction as a named export.
**What needs resolving**: Relocate the witness construction to the proof body or to a clearly-labelled *Proof note* field; remove it from the *Definition* slot unless the construction is genuinely intended as an exported, citable object.

VERDICT: OBSERVE