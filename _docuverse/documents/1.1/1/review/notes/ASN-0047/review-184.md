# Review of ASN-0047

## REVISE

### Issue 1: Dangling forward reference to a nonexistent "Rationale (k = 0 conjuncts)" subsection, motivating FrontierEquivalence
**ASN-0047, Properties Introduced (FrontierEquivalence row)**: "...'frontier' is well-defined by T10a.7. See the K.δ *Rationale (k = 0 conjuncts)* for why T4b-based identification does not suffice."

**Problem**: No subsection titled "Rationale (k = 0 conjuncts)" exists in the body. The K.δ definition and the §*K.δ case (ii) discharge and parent-allocator activation* section discuss the k = 0 guard and its FrontierEquivalence rewrite, but **neither argues why a T4b-based structural identification would fail to discharge the frontier check** — which is precisely the claim the pointer promises. FrontierEquivalence is the lemma that converts the operational guard `inc(t,0) ∉ E` into the allocator-frontier predicate, so the justification that this *operational* check cannot be replaced by a *structural* one is load-bearing for the lemma's necessity. As written, the lemma is motivated by an assertion that the document never establishes, and the reader is sent to a section that does not exist.

**Required**: Either supply the missing argument (state, in one place, why `inc(t,0) ∉ E` is not recoverable from a T4b parse of `t` alone — presumably because the frontier depends on prior K.δ history, not on `t`'s component structure) and point the reference at it, or delete the dangling clause and let FrontierEquivalence's proof stand on its own.

### Issue 2: "S7a–S7d" range notation implies a nonexistent S7c
**ASN-0047, Properties Introduced (ExtendedReachableStateInvariants row)**: "Every reachable state satisfies the *per-state invariants* S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a–S7d ∧ S8a ∧ ..."

**Problem**: The foundation defines S7a, S7b, S7d — there is no S7c. The authoritative per-state conjunction in the *Extended reachable-state invariants* section correctly spells "S7a ∧ S7b ∧ C1b ∧ S7d" (note C1b, not S7c). The contracted range "S7a–S7d" both invents a phantom S7c and silently drops C1b, so the summary row no longer matches the conjunction it summarizes.

**Required**: Replace "S7a–S7d" with the explicit "S7a ∧ S7b ∧ C1b ∧ S7d" to match the body, or otherwise make the abbreviation consistent with the actual invariant set.

### Issue 3: Epistemic hedge in the J1'★ derivation does not advance the argument
**ASN-0047, Scoped coupling constraints (J1'★ derivation)**: "J1'★ is accordingly an imposed coupling whose step-local wp is intuition, not a complete derivation of its composite-Σ' form."

**Problem**: This note carries the `review-mode.anti-bloat` classifier. The surrounding paragraph already does the substantive work (it identifies J0 + P2 as the ValidComposite★ constraints that close the gap between the step-local wp and the composite-Σ' form). The quoted sentence then editorializes about the derivation's epistemic status — "intuition, not a complete derivation" — which restates the gap a third time without adding a step. This is the "new prose explaining why the coupling is imposed rather than what it states" pattern. The reader has to absorb the meta-commentary to reach the operative content.

**Required**: Drop the hedge sentence; the preceding "What closes that gap is ... J0 ... and P2 ..." already states both the limitation and its resolution. If a status label is wanted, one clause ("J1'★ is imposed, not derived; J0 + P2 discharge it") suffices.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The J4 discussion notes that "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred — the elementary set and fork composite are complete without it.

**Why out of scope**: Defining a link-inheritance composite is new territory (it would introduce a fork variant that populates the link subspace), not an error in the current fork definition, which is internally consistent for the content-only case.

### Topic 2: Interior link withdrawal / tombstoning
The D-CTG★/D-MIN★ strengthening restricts K.μ⁻ to per-subspace suffix truncations, so withdrawing an interior link requires withdrawing every later-allocated link. The ASN catalogues this in Open Questions as requiring a separate mechanism outside K.μ⁻'s contract.

**Why out of scope**: A tombstone/withdrawal mechanism is a distinct operation, not a gap in the present contraction transition, whose suffix-only semantics are proved sound.

META: (none — the ASN defines abstract state, elementary transitions, and their invariants; the findings are a broken pointer, a notation slip, and one meta-prose sentence, all fixable.)

VERDICT: REVISE
