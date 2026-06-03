# Review of ASN-0070

## REVISE

### Issue 1: Three defined behaviors are never exercised by any worked example

**ASN-0070, A Worked Example (five configurations) vs. Derived Properties / V-Restricted Denotation**

The note builds five elaborate configurations and checks F-sound, F-complete, F-multi, F-subspace, F-contig, F-empty, F-state, F-persist against them. But three pieces of defined behavior receive no concrete scenario:

1. **Vacuous-subspace convention.** Every configuration keeps both subspaces populated (`β_L = ([2,1], ℓ₀, 1)` is present throughout), so `m_{s_L}(d)` is always defined. The case `V_S(d) = ∅` with `m_S(d)` *undefined* — where the V-Restricted Denotation convention forces `Σ_V^S = ⟨⟩` and F-canonical's uniqueness depends on that forcing — is never instantiated.
2. **F-slot (SlotUniformity).** Every configuration uses `i = 1`. No example follows a second slot (e.g. the type endset `e₃`) to show identical routing with a differing endset.
3. **F-multidoc (NoPreferredDocument).** No example evaluates `follow(ℓ, d, i)` and `follow(ℓ, d', i)` for distinct documents.

**Problem**: Standard 6 requires key postconditions verified against a concrete scenario. The vacuous-subspace convention in particular is load-bearing for canonical-form uniqueness, and it is precisely the corner the prose distinguishes ("distinct from a vacuous subspace `V_S(d) = ∅`" in F-empty) yet never shows.

**Required**: Add at least one configuration with a genuinely empty subspace (a document holding content but no links, so `V_{s_L}(d) = ∅` and `m_L(d)` undefined), verifying that `follow` returns `Σ_V^{s_L} = ⟨⟩` by the convention rather than by missed coverage. Optionally extend an existing configuration to a second slot index and a second document to exercise F-slot and F-multidoc.

### Issue 2: Transitive-dependency tracing in F-det's Depends slot

**ASN-0070, F-det — DenotationalDeterminism, Depends**: "F0 (InverseImageRelation, this ASN — its Well-definedness clause, which itself rests on S2 ArrangementFunctionality, ASN-0036)"

**Problem**: The `Depends` line cites F0, then traces F0's own upstream dependency back to S2. F0 already discharges S2 in its own Well-definedness clause; re-threading it through F-det's Depends is accreted meta-prose, not advancement of F-det's derivation. The anti-bloat classifier flags exactly this kind of dependency-chain restatement.

**Required**: Cite F0 alone; drop the "which itself rests on S2" parenthetical.

### Issue 3: F-slot introduces an undefined `followAll` operation

**ASN-0070, F-slot — SlotUniformity**: "Uniformity makes the operation composable: `followAll(ℓ, d) = (follow(ℓ, d, 1), ..., follow(ℓ, d, |L(ℓ)|))` is the positionally-aligned tuple..."

**Problem**: `followAll` appears in no signature, no claims table, and is not part of this operation's specification. It is essay content in a lemma slot about slot uniformity — a composability aside that does not advance F-slot's stated postcondition.

**Required**: Remove the `followAll` digression, or reduce the closing remark to the substantive point already made (resolution mechanism is slot-independent; differing results reflect differing endsets).

## OUT_OF_SCOPE

### Topic 1: Cross-document resolution relationships and concurrency
**Why out of scope**: The two Open Questions (relationship between `follow(ℓ, d, i)` and `follow(ℓ, d', i)` under shared transclusion homes; concurrency semantics under concurrent modification) are genuinely new territory belonging to future ASNs, correctly parked rather than half-specified here.

VERDICT: REVISE
