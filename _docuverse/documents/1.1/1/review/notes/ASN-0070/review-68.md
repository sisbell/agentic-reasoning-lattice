# Review of ASN-0070

I checked the central proofs (F-canonical's five steps, F-subspace, F-contig), the six worked configurations, and boundary coverage (empty document, zero reach, interior clip `j>0`, cross-subspace straddle, multiplicity, vacuous subspace). The mathematics is sound and the boundary coverage is unusually complete. One precision gap remains.

## REVISE

### Issue 1: F-canonical and F-empty rely on the vacuous-subspace convention without dispatching it in the proofs

**ASN-0070, F-canonical (CanonicalExistenceAndUniqueness)**: the proof opens "we show each subspace component admits exactly one canonical representation," then "*Step 1.* ... Fix a **non-empty** subspace `S`, write `m := m_S(d)`." Steps 1–5 never return to the case `V_S(d) = ∅` (where `m_S(d)` is undefined).

**ASN-0070, F-empty derivation**: "The representational conclusion `Σ_V^S = ⟨⟩` is then immediate from F-canonical, with no further argument needed: F-canonical's existence construction (Step 3) partitions `X := R(d, e)|_S` into maximal runs ... so the empty target `X = ∅` yields ... `⟨⟩`."

**Problem**: Both arguments presuppose a non-empty subspace (Step 3 needs `m_S(d)` defined to form depth-`m_S` runs). The vacuous case — `V_S(d) = ∅`, so `m_S(d)` undefined and `R(d, e)|_S = ∅` unconditionally — is reachable under F-empty's precondition (e.g. a document with no links, as in the sixth configuration's `d'`). For that subspace, the unique representative `⟨⟩` is supplied only by the *Vacuous-subspace convention* stated in F-canon-form, not by F-canonical's proven existence/uniqueness argument. F-canonical therefore does not actually establish "exactly one per-subspace family" for documents with a vacuous subspace, and F-empty cites Step 3 for a case Step 3 excludes. The two claims lean on the convention as if it were a proven sub-case.

**Required**: Give F-canonical an explicit base case — when `m_S(d)` is undefined, `R(d, e)|_S = ∅` and the only admissible span-set is `⟨⟩` (existence and uniqueness by the convention `⟦⟨⟩⟧_V := ∅`) — before "Fix a non-empty subspace `S`." Then have F-empty cite that base case (the convention) for the vacuous subspace and Step 3 only for a populated-but-unreached subspace, rather than attributing both to Step 3.

## OUT_OF_SCOPE

### Topic 1: Cross-document resolution relationships under shared/overlapping transclusion homes
**Why out of scope**: The note's first Open Question — what relationship `follow(ℓ, d, i)` and `follow(ℓ, d', i)` must satisfy when `d`, `d'` transclude overlapping home subsets — is genuinely new territory. F-multidoc and F-origin establish per-document home-independence; a positive cross-document relation is a future ASN, not a gap here.

### Topic 2: Concurrency/consistency obligations for traversal under BEBE
**Why out of scope**: Replication/inter-server protocol is excluded by the stated scope; SequentialTransitionAxiom makes `follow` a pure single-state query, so no obligation arises in this model.

VERDICT: REVISE
