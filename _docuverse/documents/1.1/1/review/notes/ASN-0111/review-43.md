# Review of ASN-0111

## REVISE

### Issue 1: The worked read's reachability route is not a sequence of valid composites — J1★ is violated
**ASN-0111, "A worked read"**: "each enters dom(C) inside a J0-satisfying composite — K.α coupled with a K.μ⁺ arranging it at the boundary. A subsequent K.μ⁻ on each document with content-subspace retention n'_{s_C} = 0 then empties the content V-positions while dom(C) retains all three entries (P0)."
**Problem**: Validity of a composite (ValidComposite★, ASN-0047) requires J0 ∧ J1★ ∧ J1'★ between initial and final states, and composite boundaries must satisfy P4★ and P7a. The exhibited composite K.α + K.μ⁺ makes each fresh I-address range-new to `M'(d)`'s content subspace, so J1★ demands `(a, d) ∈ R'` — but the route contains no K.ρ step and `R₀ = ∅`, so J1★ fails, P4★ fails at the boundary (`Contains_C(Σ') ⊄ R'`), and P7a fails for all three addresses. The note explicitly promises "we exhibit the route rather than assume it," and the exhibited route is not reachable as written. The same gap does not affect the RL4 construction (no K.α steps there), but the worked example's central stipulation — three allocated, content-bearing, unarranged I-addresses — currently rests on an invalid composite.
**Required**: Extend each content-allocating composite to K.α + K.μ⁺ + K.ρ (the shape J4 already uses), and note that the provenance entries persist through the later K.μ⁻ by P2, so P4★/P7a hold at every subsequent boundary.

### Issue 2: The depth family re-derives a foundation result (LP-Sub) instead of citing it
**ASN-0111, "Determinacy and the immutability of the recorded relationship"**: "*Depth:* under the standing precondition's transition vocabulary, every address that ever enters dom(L) lies on the chain A_L(d) of its origin (ChainMembershipForOrigin, ASN-0093), and every element of such a chain has element-field depth exactly 2. The first emission [d.0.s_L.1] has #E = 2, and each subsequent emission is inc(·, 0); length preservation alone would not fix #E … the element-field boundary is undisturbed, and #E = 2 is preserved along the chain."
**Problem**: This ~10-line chain-induction (TA5(b), TA5(c), TA5-SigValid, ChainElementT4Validity, T4's trailing-component clause) reconstructs what the foundation already packages. LP-Sub (ASN-0098) gives `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` at every reachable state, and the SubstrateEmittableAddresses definition fixes `#E(a) = 2` for every member of `F`. The entire depth-family permanence proof is: `#E(a) = 3 ⟹ a ∉ F ⟹ a ∉ dom(Σ'.L)` at every reachable `Σ'`. The ASN should use the foundation, not reinvent its derivation — and under the anti-bloat classifier this re-derivation is exactly the accretion the cycle is meant to remove.
**Required**: Replace the chain-preservation argument with a direct application of LP-Sub plus `F`'s `#E = 2` structural form; the Gregory corroboration sentence can stay.

### Issue 3: The lineage family's permanence proof is a multi-step argument stated as a clause
**ASN-0111, "Determinacy and the immutability of the recorded relationship"**: "no entity chain through P8 can ever place home(a) in dom(M), and L1a then excludes a from dom(Σ'.L) at every reachable Σ'."
**Problem**: "X follows from P8 + NodeLineage + L1a" is a claim, not a proof. The actual chain has five steps that are nowhere shown: (1) suppose `a ∈ dom(Σ'.L)`; L1a gives `home(a) = [2.0.1.0.1] ∈ dom(Σ'.M) = E'_doc`; (2) P8 at the document gives `parent(home(a)) = N·0·U = [2.0.1] ∈ E'`; (3) P8 at the account gives `parent([2.0.1]) = N = [2] ∈ E'`; (4) `zeros([2]) = 0` so `Node([2])`, and NodeLineage gives `n₀ ≼ [2]`; (5) `[2]₁ = 2 ≠ 1` refutes `n₀ ≼ [2]` — contradiction. The two distinct P8 applications (document→account, account→node) and the Node-classification step are load-bearing, since the caching rule (ii) licenses permanent ⊥-caching on exactly this argument.
**Required**: Show the two P8 parent steps and the Node/NodeLineage contradiction explicitly (three to four lines suffice).

### Issue 4: The same one-sidedness point is stated three times in one paragraph
**ASN-0111, "Determinacy and the immutability of the recorded relationship"**: First as "the screen settles nothing in either direction: the screen-passing class contains addresses of both fates, so permanence of ⊥ is not derivable from the screen alone," then as "The screen is therefore a one-sided test: failure proves permanent absence; passage, by itself, proves nothing about the future," then as "What passage withholds is thus permanence derivable from the screen alone; the address may still carry a permanence proof under the finer tests."
**Problem**: Three formulations of one fact inside a single paragraph — exactly the "same thing in different words" accretion the anti-bloat classifier flags. The RL5 claims-table row then restates nearly the full paragraph, including the three-part caching rule, rather than summarizing it.
**Required**: State the one-sidedness once (the "one-sided test" formulation is the sharpest), let the two families and the three-part caching rule carry the rest, and compress the RL5 table row to the claim plus a pointer to the caching discipline.

### Issue 5: The signature conflates the state metavariable with the state space
**ASN-0111, "Deriving the read"**: "`readlink : T × Σ → Link ∪ {⊥}`"
**Problem**: `Σ` is used in the signature as the *type* of the second argument while simultaneously serving as the bound state variable in `readlink(a, Σ)`. The foundation explicitly reserves a distinct symbol for the state space — ASN-0034 (AllocatedSet, NoDeallocation) introduces `𝒮` precisely "to keep the state-space symbol distinct" — and ASN-0036/0043/0047 use Σ only as a state, never as the space. The ASN reinvents (misuses) notation the foundation already settles. The same form recurs in the claims table.
**Required**: Write the signature over the foundation's state space (e.g., `readlink : T × 𝒮 → Link ∪ {⊥}`, with the domain restricted to reachable states per the standing precondition), here and in the claims table.

## OUT_OF_SCOPE

### Topic 1: Disclosure of retraction status for links read as relational tuples
A reader of a link that participates in a typed relation (ASN-0086) cannot tell from `readlink` alone whether the address is in `nullified(Σ)` — the read returns the frozen value either way, by design. Whether a read variant should disclose active-subset status is relational-layer business.
**Why out of scope**: Nullification is an overlay defined by ASN-0086's layer conventions, not a property of the link store; readlink correctly reads the store, and active-status queries belong with Observe_K's view machinery.

### Topic 2: A cache as a system component
RL5 establishes the caller-side soundness rule for caching results and ⊥. Specifying an actual caching facility — shared caches, invalidation across nodes, interaction with replication — is new territory.
**Why out of scope**: The ASN proves what makes caching sound; a cache component's state and operations are a separate specification (and touch the excluded BEBE territory).

VERDICT: REVISE
