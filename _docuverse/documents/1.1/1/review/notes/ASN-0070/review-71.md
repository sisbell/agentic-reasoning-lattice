# Review of ASN-0070

## REVISE

### Issue 1: Definition slot pre-states a downstream theorem's conclusion

**ASN-0070, "Result Form and the Operation" → V-Restricted Denotation → Vacuous-subspace convention**: "The postcondition `⟦Σ_V^S⟧_V = R(d, e)|_S = ∅` is then satisfied uniquely by `⟨⟩`, preserving canonical-form uniqueness when the subspace is vacuous."

**Problem**: The definitional content this paragraph needs is only the convention `Σ_V^S = ⟨⟩` and `⟦⟨⟩⟧_V := ∅`. The clause "satisfied uniquely by `⟨⟩`, preserving canonical-form uniqueness" asserts a uniqueness result that is the conclusion proved downstream in F-canonical Step 0 (the vacuous base case). Neither the definition nor the operation's postcondition (which admits any equivalent form, per "We do not commit the operation's postcondition to canonical form") requires uniqueness here. A reader following the definition does not yet need the canonical-form-uniqueness claim. This is forward-reference accretion: a theorem conclusion placed in a definition slot.

**Required**: End the convention at the definitional content (`⟨⟩`, `⟦⟨⟩⟧_V := ∅`). Drop the uniqueness/canonical-form sentence; it is established where it belongs, in F-canonical Step 0.

### Issue 2: Document-ordering meta-prose in the canonical-form proof

**ASN-0070, F-canonical, Step 0 (vacuous subspace base case)**: "...and since `⟨⟩` is the *only* admissible candidate, uniqueness holds by the convention without appeal to the run construction below."

**Problem**: The argument's substance is complete at "`⟨⟩` is the only admissible candidate, so existence and uniqueness hold." The trailing clause "without appeal to the run construction below" adds nothing to the reasoning — it is a note to the reader about which later machinery this case avoids. That is document-ordering meta-prose of the kind the anti-bloat pass targets.

**Required**: Delete "without appeal to the run construction below."

## OUT_OF_SCOPE

### Topic 1: Cross-document consistency when an endset spans multiple homes

**Why out of scope**: The first Open Question (relationship between `follow(ℓ, d, i)` and `follow(ℓ, d', i)` for shared/overlapping transclusion homes) is new territory for a future ASN, correctly parked as an open question, not an error here.

### Topic 2: Replication / multi-server (BEBE) traversal consistency

**Why out of scope**: Explicitly named in the scope exclusions; the second Open Question frames it appropriately without claiming coverage.

VERDICT: REVISE
