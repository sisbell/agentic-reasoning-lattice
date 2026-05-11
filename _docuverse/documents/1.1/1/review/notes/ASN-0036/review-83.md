# Review of ASN-0036

## REVISE

### Issue 1: S7 proof misattributes "zeros = 3 preservation" to T10a.4

**ASN-0036, S7 proof, Well-definedness paragraph**: "By T10a.4 (T4PreservationUnderDiscipline, ASN-0034), every address produced by an allocation event under T10a's discipline is a well-formed T4 tumbler — zeros = 3 is preserved as a structural invariant, so T4's field-decomposition machinery applies."

**Problem**: T10a.4 preserves T4-validity, which includes `zeros(t) ≤ 3`, no adjacent zeros, `t₁ ≠ 0`, and `t_{#t} ≠ 0`. It does NOT establish `zeros(t) = 3` as a structural invariant — that strict equality is supplied by S7b's axiomatic commitment that `dom(Σ.C)` contains only element-level tumblers. T10a is consistent with allocation at any zero count satisfying T4 (node-level at zeros=0, user-level at zeros=1, document-level at zeros=2 are all T4-valid). The depends list correctly states "T10a.4 — guarantees that the `zeros = 3` invariant carried by S7b is preserved by every T10a allocation event," but the proof prose conflates "T10a.4 preserves T4-validity" with "T10a.4 preserves zeros = 3."

**Required**: Reword to clarify that `zeros(a) = 3` is supplied by S7b axiomatically, while T10a.4 ensures the T4-validity that allows S7b's invariant to be preserved across allocations. The two contribute different things.

### Issue 2: S5 proof's constructions don't address strand-model well-formedness

**ASN-0036, S5 proof, both constructions**: "N + 1 documents `d₁, …, d_{N+1}`, with `M_N(dᵢ) = {vᵢ ↦ a}` for an arbitrary V-position `vᵢ`" / "N + 1 pairwise distinct V-positions `v₁, …, v_{N+1}`."

**Problem**: The constructions select V-positions as "arbitrary" or "pairwise distinct" tumblers without verifying they satisfy S8a (zeros = 0, `#v ≥ 2`, componentwise positivity). The verification step explicitly covers S0, S1, S2, S3 only. The contract reads "There exists a state Σ satisfying S0–S3..." — but the word "state" in the strand model implies a well-formed strand-model state satisfying all invariants. As written, the constructed `Σ_N` and `Σ'_N` may be (C, M) pairs that satisfy S0–S3 but are not strand-model states (V-positions of depth 1, or with zero components, would fail S8a).

This is technically consistent with the narrow contract but reads as if the constructed states are fully well-formed.

**Required**: Either (a) explicitly note that S5 claims S0–S3 consistency in isolation, not strand-model well-formedness, or (b) refine the constructions to use V-positions satisfying S8a (e.g., depth-2 positions `[1, k]` in subspace 1 for the within-document case, all with positive components).

### Issue 3: S8 proof — "Conjunct (b)'s postcondition" misidentified, and general argument misplaced

**ASN-0036, S8 proof, "Subspace preservation under shifts (k ≥ 1)" paragraph**: "Conjunct (b)'s postcondition asserts that for every run `(vⱼ, aⱼ, nⱼ)` and every `k` with `0 ≤ k < nⱼ`, the image `shift(aⱼ, k)` preserves the I-address subspace identifier..."

**Problem**: Conjunct (b) as stated in the contract is `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` — an equality, not a subspace-preservation claim. The subspace-preservation property `subspace_I(shift(aⱼ, k)) = subspace_I(aⱼ)` is a separate postcondition listed after (a) and (b) in the contract.

Beyond the mislabelling, the argument is for general `k ≥ 1` but the existence proof constructs only singletons (`nⱼ = 1`), where the only valid `k` is 0 and `shift(a, 0) = a` makes subspace preservation trivially true. The S7c-based prefix-position argument is doing work that's not needed for the constructed decomposition. It would be more honest as a standalone property of correspondence runs that any future coarser decomposition would inherit.

**Required**: (a) Rename "Conjunct (b)'s postcondition" to something like "The subspace-preservation postcondition" to match the contract. (b) Either move the general `k ≥ 1` argument into a separate paragraph that explicitly frames it as a property of any correspondence run (relevant when coarser decompositions arise), or restrict the proof to the trivial `k = 0` case actually needed for the singleton decomposition.

## OUT_OF_SCOPE

None. The ASN's scope is explicit and consistently honored — operations, subspace alignment, link-subspace semantics, subtraction homomorphism, and the canonical choice of `m` for empty subspaces are all properly deferred via the open-questions section, not erroneously claimed.

VERDICT: REVISE
