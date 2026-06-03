# Review of ASN-0070

I checked the heavy proof (F-canonical) line by line — Step 1's action-point case split, Step 2's consecutivity characterisation (including the inductive Reverse direction and the discreteness/irreflexivity appeals), and Step 4's V-restricted↔full bridge with left- and right-closure. The mathematics is correct and the edge cases (vacuous subspace, empty endset, empty arrangement, cross-subspace straddle, interior-offset clip, multiplicity) are genuinely exercised. My findings are confined to redundancy introduced around the in-note theorem F-canonical, which the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: F-det re-narrates F-canonical's internal proof instead of citing its result
**ASN-0070, F-det Derivation, step 4**: "Uniqueness from the *V-restricted* denotation is exactly what F-canonical's Step 4 bridge supplies: it recovers each component (s_j, c_j) from the maximal runs of ⟦Σ̂^S⟧_V (the contiguity infrastructure of Step 2)... S9 ... governs equality of normalised span-sets under *full* denotation ⟦·⟧; it applies here only after the bridge converts V-restricted equivalence to full-denotation equivalence..."

**Problem**: F-canonical already proves "given R(d, e), the canonical form is uniquely determined" — and its uniqueness is precisely *from the V-restricted denotation* (Step 4). F-det's job is only: R(d,e)|_S is determined by Σ (F0 + S3★-aux) ⟹ by F-canonical the canonical form is unique. The step-4 paragraph re-derives F-canonical's Step-4 bridge and re-litigates the S9-vs-full-denotation distinction that F-canonical already settled. Two passages in the document now establish the same uniqueness-from-V-restricted-denotation fact in different words. This is also reflected in the **Depends** list, which cites S8 and S9 directly even though both are already subsumed by the cited F-canonical dependency (F-canonical's own Depends carries them).

**Required**: Collapse step 4 to a citation: R(d,e)|_S fixed ⟹ F-canonical yields the unique canonical form. Drop the re-narration of the Step-4 bridge and the S9/full-denotation aside, and remove S8/S9 from F-det's Depends (retain F0, S3★-aux, F-canonical).

### Issue 2: F-empty re-explains F-canonical's Step 0 / Step 3 rather than citing uniqueness
**ASN-0070, F-empty Derivation**: "The representational conclusion Σ_V^S = ⟨⟩ is then immediate from F-canonical, dispatched by subspace status. *Vacuous subspace...* This is exactly F-canonical's Step 0 base case... *Populated subspace...* Here m_S(d) is defined, so F-canonical's existence construction (Step 3) applies: it partitions X := R(d,e)|_S into maximal runs and emits one span per run, so the empty target X = ∅ yields zero maximal runs..."

**Problem**: Once R(d, L(ℓ).eᵢ)|_S = ∅ is established (steps 1–4), F-canonical directly gives that the unique canonical representative of ∅ is ⟨⟩ — for both the vacuous and the populated-but-empty cases, since F-canonical's uniqueness clause already covers both. Re-walking Step 0 and Step 3's run-partition mechanics here duplicates F-canonical's proof. (The *observation* that an empty result can arise two ways — vacuous subspace vs. populated subspace coverage missed — is worth keeping as a one-line remark; the re-derivation of the construction is not.)

**Required**: Replace the per-case re-derivation with a citation to F-canonical's uniqueness of the canonical form of ∅, retaining at most a single sentence noting the two distinct provenances of an empty component.

## OUT_OF_SCOPE

### Topic 1: Cross-document consistency when endset homes overlap; replication/BEBE traversal guarantees
**Why out of scope**: Both are correctly deferred in Open Questions. The first is a relationship between multiple `follow` results across documents (new territory beyond this single-query operation); the second is explicitly the replication/inter-server protocol, which the scope list excludes. Neither is an error in this ASN.

VERDICT: REVISE
