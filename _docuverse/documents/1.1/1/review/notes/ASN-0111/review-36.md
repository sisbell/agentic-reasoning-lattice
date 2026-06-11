# Review of ASN-0111

## REVISE

### Issue 1: The structural screen is not evaluable on its declared domain
**ASN-0111, "Deriving the read" / RL0**: "A reader holding a candidate tumbler can test the *necessary* structural conditions from the address alone — `zeros(a) = 3 ∧ subspace_I(a) = s_L ∧ #E(a) ≥ 2` — by T4 parsing... each conjunct is necessary by L1, L0, and L1b (ASN-0043) respectively."
**Problem**: `subspace_I` and `#E(·)` are defined only on T4-valid tumblers — ASN-0043's SubspaceI definition restricts the function to "every tumbler on which T4b's `E` projection is well-defined," and T4b's precondition is the T4 constraints. The screen, however, is offered to a caller holding an arbitrary `a ∈ T` (RL0 declares the read "defined for every `a ∈ T`"). On a tumbler with three zeros that violates T4 — e.g. `[0,1,0,2,0,3]` (leading zero) or `[1,0,0,2,0,3]` (adjacent zeros) — the second and third conjuncts have no value, so the promise "a failed screen, by contrast, guarantees `⊥` without an invocation" is not established over the screen's intended domain. Moreover T4-validity is itself a necessary condition (L0b), which the surrounding prose lists ("element-level, T4-valid tumbler... L0, L1, L1b, L0b") but the screen formula silently drops.
**Required**: Add `T4-valid(a)` as the leading screen conjunct — it is decidable from the address alone (zeros ≤ 3, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`), it is necessary by L0b, and it guards the well-definedness of `subspace_I(a)` and `#E(a)`. Update the claims-table entry for RL0 to match.

### Issue 2: The insufficiency-of-address-tests claim is misquantified and unwitnessed
**ASN-0111, "Deriving the read"**: "every condition a caller can compute from the address alone is necessary but not sufficient for membership in `dom(Σ.L)`"
**Problem**: As quantified, this is false — `#a = 8` is computable from the address alone and is not necessary for membership. What the derivation needs is two separate facts: each screen conjunct is necessary, and *no* address-computable predicate is sufficient. The second half is asserted with no witness, yet it is the deciding observation for making the read total rather than precondition-gated.
**Required**: Restate as two claims and discharge the second in one line: at the initial state `Σ₀` (ASN-0047), `dom(Σ₀.L) = ∅`, so any satisfiable address-only predicate fails sufficiency there; hence no caller can discharge a membership precondition from the address alone.

### Issue 3: False statement about the codomain
**ASN-0111, RL0**: "There is no partial-success middle state — no element of the codomain `Link ∪ {⊥}` is a fragment of a link."
**Problem**: The second clause is false. `Link` is closed under shrinking a connective slot: if `(F, G, Θ) ∈ Link` with `|F| ≥ 2`, then `(F', G, Θ)` with `F' ⊊ F` is also an element of `Link` (arity 3, all slots in `Endset`), and it is precisely a fragment of the stored value. The absence of partial success is a property of the *operation*, not of the codomain's structure: by the definition, every invocation returns either `Σ.L(a)` entire or `⊥`.
**Required**: Replace the codomain claim with the per-invocation statement: `readlink(a, Σ) ∈ {Σ.L(a), ⊥}` for every `(a, Σ)` — no execution returns a proper sub-value of the stored entry. This follows immediately from the definition and is what "no partial-success middle state" actually means.

### Issue 4: RL4's no-flattening corollary rests on an unconstructed existential
**ASN-0111, "Faithful disclosure of nesting"**: "two reachable states can agree on the entry at `a` while disagreeing on what is recorded at some `a' ∈ coverage(readlink(a, Σ₁).eᵢ)` with `a' ≠ a` — the K.λ event allocating `a'` accepts any conforming value — and RL4 forces the two reads at `a` to be equal".
**Problem**: This existential is load-bearing: if covered values were determined by the entry at `a`, a flattening reader would satisfy RL4 vacuously, and the claim "RL4 excludes this" would fail. The parenthetical "K.λ accepts any conforming value" names the key fact but is not a construction. The actual argument has real steps: the covered address `a'` must be the frontier emission of an active sub-allocator at the branching state; the two branches take K.λ at `a'` with distinct conforming values `v₁ ≠ v₂`; subsequent steps (including the allocation of the reading link, which by chain contiguity must come *after* `a'` when `a'` precedes it on the same chain, as in the worked example's `c`/`a'` pair) are enabled identically in both branches because they share `dom(L)` and differ only in the value stored at `a'`; agreement at the reading link's address then holds by the K.λ frame and L12. None of this is shown.
**Required**: Give the two-state construction explicitly. The worked example already supplies every ingredient: branch the history at the allocation of `a' = inc(a, 0)` with two distinct conforming values, then allocate `c` with the same value in both branches; conclude `Σ₁.L(c) = Σ₂.L(c)`, `Σ₁.L(a') ≠ Σ₂.L(a')`, `a' ∈ coverage(Σ₁.L(c).e₂)`.

### Issue 5: RL5 is silent on the instability of `⊥`
**ASN-0111, "Determinacy and the immutability of the recorded relationship"**: "A reader who has once read a link may rely on that reading permanently."
**Problem**: The stability theorem is correctly confined to the success branch (`a ∈ dom(Σ.L)`), but the spec never states the asymmetry: the `⊥` answer is *not* stable. `a ∉ dom(Σ.L)` does not persist across `Σ →* Σ'` — a subsequent K.λ can allocate `a` (any screen-passing address at the frontier of an active link sub-allocator), after which the read returns a link value. A caller who caches `⊥` as permanent is wrong, and nothing in RL0–RL6 warns against this; the boundary case of the determinacy claim is simply missing.
**Required**: One explicit statement under RL5 (or a labelled remark): the failure branch carries no stability guarantee — `readlink(a, Σ) = ⊥` does not entail `readlink(a, Σ') = ⊥` for `Σ →* Σ'`; only success-branch results are permanent.

### Issue 6: Duplicated meta-prose (anti-bloat)
**ASN-0111, "Deriving the read" and the paragraph following RL0; RL4 and RL5**: (a) The screen's insufficiency is argued twice in different words — "every condition a caller can compute from the address alone is necessary but not sufficient..." in the derivation, then "The screen is not sufficient: an address may parse as a well-formed link tumbler yet name no allocated link..." after RL0 — and two separate sentences forward-defer to the same downstream location ("The deciding observation comes with the structural screen below" and "their use as a pre-invocation structural screen is taken up with RL0 below"). (b) RL5's opening — "not merely of the whole link store: two reads of the same address against the same stored entry return identical values" — restates the strictly-weaker observation RL4's own note already makes ("Note that 'pure function of `(a, Σ.L)`' would be strictly weaker...").
**Problem**: Two paragraphs saying the same thing in different words, plus repeated forward pointers to one downstream location — exactly the accretion patterns this note is flagged for.
**Required**: State the screen and its insufficiency once, in the RL0 section; let the derivation cite that single statement. In RL5, cite RL4 for purity without re-arguing the whole-store distinction.

## OUT_OF_SCOPE

### Topic 1: Per-slot or per-endset read operations
**Why out of scope**: An operation reading only `Σ.L(a).e₃` (e.g., for type matching without transferring connective endsets) is a distinct operation with its own contract; this ASN correctly specifies the whole-value read and need not define projections of it.

### Topic 2: Discriminated failure reporting
**Why out of scope**: `⊥` collapses "structurally impossible address" (screen-fail, permanently unallocatable) and "well-formed but unallocated" (possibly allocatable later). A richer failure taxonomy is a protocol-surface design question for a future ASN, not an error in this one — though note its interaction with Issue 5.

VERDICT: REVISE
