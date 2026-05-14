# Review of ASN-0042

## REVISE

### Issue 1: O10's single-step framing is too tight for the construction
**ASN-0042, O10 (DenialAsFork), Formal Contract**: "(E Σ', a' : Σ → Σ' ∧ a' ∈ dom(π) ∩ Σ'.B ∧ ω_{Σ'}(a') = π ∧ a ∈ Σ'.B)"

**Problem**: The contract uses `Σ → Σ'` (single-step, as in O3, O12), but the construction for `zeros(pfx(π)) = 0` finds `u ∈ ℕ_{>0} ∖ S` and builds `a' = pfx(π).0.u.0.1.0.1`. ASN-0040's baptism produces `c₁, c₂, ...` sequentially via `next(B, p, d)`; reaching arbitrary `u` requires baptizing siblings `1, 2, ..., u`, then descending to document and element levels. The closing paragraph says "the resulting transition produces the witnessing Σ'" — but no single transition can produce this `a'` in general. The proof actually requires `Σ →⁺ Σ'` (or `Σ →* Σ'`).

**Required**: Change `Σ → Σ'` to `Σ →⁺ Σ'` in the contract, or rephrase the construction to use the first baptizable address (e.g., `a' = inc(pfx(π), 2)` for the `zeros = 1` case is genuinely single-step; the `zeros = 0` case is not). Either way, make the proof explicit about the baptism sequence required to reach `a'` and explain why intermediate baptisms don't violate the fork's invariants (i.e., intermediate addresses `[pfx(π), 0, k]` for `k ∈ S` end up owned by sub-delegates, not by `π`, which is acceptable since `a'` itself satisfies the postcondition).

### Issue 2: T5/Prefix attribution errors
**ASN-0042, O1 (PrefixDetermination)**: "where `p ≼ a` denotes that `p` is a prefix of `a` in the sense of T5"

**Problem**: T5 is `ContiguousSubtrees`; it uses the prefix relation but does not define it. The prefix relation `≼` is defined by the foundation property `Prefix (PrefixRelation)`. The same misattribution appears in the *Covering-chain lemma* paragraph of O7's proof: "O2's proof — which derives from T5 (ContiguousSubtrees) — establishes that any two tumbler prefixes of the same address are linearly ordered by `≼`". The linear-ordering-of-covering-prefixes is a property of the `Prefix` relation (and `T3`), not of T5.

**Required**: Replace `T5` with `Prefix` (or both, where appropriate) at the definitional citations. T5 remains correctly cited where it is actually used (e.g., "By T5 (ContiguousSubtrees), every ownership domain is a contiguous interval").

### Issue 3: O1 mis-classified in the Properties Introduced table
**ASN-0042, Properties Introduced table**: "O1 | `owns(π, a) ≡ pfx(π) ≼ a` | from T4, T5"

**Problem**: O1 is a *definition* — it introduces the symbol `owns` by stipulation. It is not derived from T4 and T5. The body's prose explicitly says "O1 is a definition: we define the ownership predicate". The "from T4, T5" attribution is inconsistent with that.

**Required**: Mark O1 as "definition" (mirroring how `acct(a)`, `ω(a)`, `Delegation`, `OwnershipDomain` are marked).

### Issue 4: O3 proof does not explicitly conclude that π' came from delegation
**ASN-0042, O3 proof**: "the only way for the longest-match computation over Π_{Σ'} to yield a *different* result is for some principal in Π_{Σ'} ∖ Π_Σ to cover a with a strictly longer prefix"

**Problem**: The headline of O3 reads "changes only when **delegation** introduces a principal", but the proof only shows existence of a new principal `π'`. It never explicitly invokes O15 to conclude `π'` arrived through delegation rather than (hypothetically) some other mechanism. The conclusion is reachable — O14 + iterated O12 force `Π₀ ⊆ Π_Σ`, ruling out the bootstrap branch of O15 — but this chain is left to the reader. The same closure is made explicit in AccountLevelPermanence's Step 1; O3's proof should do the same.

**Required**: Add a sentence after the existence-of-π' conclusion: "By O15 (PrincipalClosure), `π' ∈ Π_{Σ'} ∖ Π_Σ` arrived via bootstrap or delegation; iterated O12 gives `Π₀ ⊆ Π_Σ`, so `π' ∉ Π₀` and `π'` was delegated by some `π_d ∈ Π_Σ`."

### Issue 5: AccountLevelPermanence's multi-step rooting argument is muddled
**ASN-0042, AccountLevelPermanence (Corollary discussion)**: "The chain of delegators inducing changes within dom(π) is therefore rooted at π — Nelson's 'forevermore' in its multi-step form."

**Problem**: The prose attempts to derive a "rooted at π" claim from the bootstrap-ancestry argument, but the argument is convoluted and conflates two senses of "rooted": (a) that the *first* delegator into dom(π) must be π itself, and (b) that bootstrap ancestors trace back to π. The formal multi-step corollary only proves the per-transition statement (each delegator has prefix extending pfx(π)); the "rooted at π" claim is informal commentary. The simpler argument: by O15, the *first* delegator into dom(π) (across the transition sequence) must be in Π that already exists before any sub-delegate of π exists; that delegator must satisfy pfx(π) ≼ pfx(delegator) (proven), and is therefore either π or a sub-delegate of π — but no sub-delegate of π exists yet, so it must be π.

**Required**: Either tighten the informal "rooted at π" prose to track this simpler chain (first delegator must be π), or strike the prose and let the formal per-transition statement carry the result.

### Issue 6: Worked example missing the self-ownership boundary case
**ASN-0042, Worked Example**

**Problem**: The worked example covers delegation, sub-account namespaces, cross-node addresses, forks, and irrevocability — but never checks the boundary case where `pfx(π) ∈ Σ.B` (the principal's own prefix is itself an allocated address). Specifically, what is `ω([1])` for the node operator `π_N` with `pfx(π_N) = [1]` once `[1]` itself is baptized? What is `ω([1, 0, 2])` once that account-prefix address itself is allocated? Both should yield the principal whose prefix equals the address, but the example does not exercise this case, leaving the reader to verify it.

**Required**: Add a short paragraph to the worked example checking that `ω(pfx(π))` for a principal whose prefix has itself been allocated yields `π` (longest match is the principal's own prefix, length equal to the address).

### Issue 7: Redundancy between O2's proof and ω(a)'s proof
**ASN-0042, O2 (OwnershipExclusivity) and ω(a) (EffectiveOwner)**

**Problem**: O2's proof and ω(a)'s proof are essentially the same four-step argument (non-emptiness via O4, total ordering of covering prefixes via Prefix-relation arithmetic, finiteness via length-uniqueness, existence/uniqueness via maximum-of-finite-chain + O1b). Presenting them twice in sequence is awkward and risks divergence under future edits.

**Required**: Merge the proofs. State O2 as the existence/uniqueness theorem, then define ω(a) as the witnessing principal — one proof, one location.

### Issue 8: `pfx(π)` formal contract lists postconditions that are not really postconditions of pfx
**ASN-0042, pfx(π) (OwnershipPrefix) Formal Contract**: "Postconditions: (c) Injectivity: stated separately as O1b. (d) Account-level boundary: stated separately as O1a."

**Problem**: A Formal Contract block lists postconditions of a primitive/definition. O1a and O1b are *separate axioms* about Π — they constrain `pfx` globally, but they are not local postconditions of the `pfx` mapping when invoked at a single principal. Listing them under "Postconditions" with "stated separately" is misleading.

**Required**: Either move (c) and (d) out of the Postconditions block (e.g., into a "Related axioms" line), or restate (c) and (d) directly as postconditions in the same block without the "stated separately" qualification (and let O1a / O1b stand as the named handles).

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanics
**Why out of scope**: Listed in Open Questions. The ASN takes the conservative reading (no transfer in the system as specified) and acknowledges Nelson's hint at transferability would require machinery outside the structural model.

### Topic 2: Authentication and session-to-principal binding
**Why out of scope**: O11 explicitly axiomatizes principal identity as external. The stated scope excludes "concrete authentication mechanisms".

### Topic 3: Delegation history reconstruction
**Why out of scope**: Listed in Open Questions. Whether the system records delegation events or reconstructs them from the address hierarchy is a future design question, not a property of the ownership model itself.

VERDICT: REVISE
