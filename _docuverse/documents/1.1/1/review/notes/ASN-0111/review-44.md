# Review of ASN-0111

## REVISE

### Issue 1: The caching discipline's residual-class prohibition and exactness claim are falsified by a permanence family the note misses
**ASN-0111, "Determinacy and the immutability of the recorded relationship" (RL5)**: "(iii) `⊥` must not be cached at the residual class — screen-passing, `#E(a) = 2`, `N(a)₁ = 1` — which contains the frontier addresses a future K.λ allocates, and for whose members the tests established here yield no permanence proof. Caching `⊥` is sound exactly where such a proof is in hand." Also the claims-table entry: "`⊥` is cacheable exactly where an address-computable permanence proof is in hand," and the earlier sentence "The two families show that the screen-passing class is heterogeneous, split by finer tests that are still address-computable: depth (...) and lineage (...)."

**Problem**: The residual class contains permanently absent members, so both the class-level prohibition and the "exactly" biconditional are false. Witness: `a = [1.0.1.1.0.1.0.2.1]`, parsing as `N(a) = [1]`, `U(a) = [1, 1]`, `D(a) = [1]`, `E(a) = [2, 1]`. It is T4-valid (zeros at positions 2, 5, 7 — none adjacent, first and last components nonzero), passes every screen conjunct, has `#E(a) = 2` and `N(a)₁ = 1` — squarely in the residual class. Yet it is permanently absent, by the note's own P8-chain method from the lineage family: `a ∈ dom(Σ'.L)` would give `home(a) = [1.0.1.1.0.1] ∈ E'_doc` (L1a), whence `parent(·) = [1.0.1.1] ∈ E'` (P8) — an account with two-component user field. No such account is ever creatable: accounts enter `E` only via K.δ case (ii) with `k = 2` from a node, producing `inc(t, 2) = t.[0, 1]` with single-component user field, or via `k = 0` from an existing account, which modifies only the terminal component (TA5(c), TA5-SigValid) and so preserves `#U = 1`; the `k = 1` and case (i) branches produce documents and nodes. So `#U(e) = 1` for every account in every reachable `E'`, the supposition fails, and `a ∉ dom(Σ'.L)` throughout the future. Caching `⊥` at `a` is therefore sound, and the test `#U(a) ≥ 2` that proves it is address-computable — contradicting "must not be cached at the residual class," contradicting the exactness of "sound exactly where such a proof is in hand," and showing the depth/lineage split of the screen-passing class is incomplete.

**Required**: Either (a) weaken: replace the class-level prohibition with a proof-relative one ("`⊥` must not be cached without a permanence proof in hand"), drop or qualify "exactly," and state explicitly that the screen/depth/lineage tests are sufficient but not exhaustive over the permanently-absent class; or (b) complete: add the user-field family (`#U(a) ≥ 2 ⟹` permanent absence, by the K.δ-vocabulary argument above) and re-draw the residual class as screen-passing `∧ #E(a) = 2 ∧ N(a)₁ = 1 ∧ #U(a) = 1`. Option (b) appears to make the prohibition and the exactness claim true — every member of the four-conjunct class looks reachable as a future K.λ frontier (nodes by NodeBaptism under `n₀`, accounts by sibling advance, documents by sibling/version steps, link ordinals by chain advance) — but that closure claim must then be argued, not assumed. The RL5 table entry must be updated to match whichever fix is taken.

### Issue 2: Inaccurate citation of J4's composite shape in the worked read
**ASN-0111, "A worked read"**: "each enters `dom(C)` inside a valid composite of the shape J4 already uses — K.α coupled with a K.μ⁺ arranging the fresh address at the boundary (discharging J0) and a K.ρ recording `(a, d)` for the range-new address..."

**Problem**: J4's fork composite consists of K.δ + K.μ⁺ + K.ρ (ASN-0047); it contains no K.α step, so the composite used here is not "the shape J4 already uses." The route's validity is in fact established by the J0/J1★/J1'★ discharge the sentence itself performs, so the J4 appeal is both inaccurate and doing no work — it reads as precedent-invocation rather than proof.

**Required**: Drop "of the shape J4 already uses," or correct it to claim only the shared coupling pattern (arrangement extension plus provenance recording discharging J0/J1★), not a shared composite shape.

### Issue 3: The address-insufficiency observation and its consequence are stated twice
**ASN-0111, "Deriving the read"**: "The deciding observation is the insufficiency of address-only tests: no satisfiable predicate computable from the address alone is sufficient for membership in `dom(Σ.L)`, so a caller cannot in general discharge a membership precondition before invoking." — and later in the same section: "*No satisfiable address-computable predicate is sufficient* — at the initial state `Σ₀` ... Hence no caller can discharge a membership precondition from the address alone; only the outcome — `Link` versus `⊥` — settles membership."

**Problem**: The claim and its consequence appear twice in nearly the same words — once unproven as motivation, once with the `Σ₀` witness. Two passages in one section saying the same thing in different words is exactly the accretion pattern this note is flagged for; the reader hits the conclusion before the proof and again after it.

**Required**: State the consequence once. Keep the proof at the screen paragraph; in the totality derivation, retain only the bare observation that motivates the total-function shape (or a forward gesture), without restating the caller-cannot-discharge conclusion.

### Issue 4: Defensive notation-provenance clause in the signature paragraph
**ASN-0111, "Deriving the read"**: "Writing `𝒮` for the state space — the symbol ASN-0034 (AllocatedSet, NoDeallocation) reserves precisely to keep the space distinct from a state `Σ` — with the second argument restricted to reachable states..."

**Problem**: The appositive explains why the foundation chose the symbol rather than what the symbol denotes here — provenance justification interposed mid-signature, which the reader must skip past to reach the definition. The signature needs only the identification.

**Required**: Reduce to "Writing `𝒮` for the state space (ASN-0034), with the second argument restricted to reachable states..."

## OUT_OF_SCOPE

### Topic 1: A complete address-computable decision procedure for permanent absence versus eventual allocatability
**Why out of scope**: If Issue 1 is resolved by weakening rather than completing the discipline, the full partition of `T` into permanently-`⊥` and possibly-allocated classes (covering node, user, document, and element fields uniformly) is new territory — a future ASN's characterization theorem, not an error here. This note only needs its own claims about its established tests to be true.

VERDICT: REVISE
