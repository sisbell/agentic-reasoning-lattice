# Review of ASN-0030

## REVISE

### Issue 1: A3 terminology collision with formal definition of `reachable`
**ASN-0030, Accessibility Transitions**: "A3 classifies which state-pairs are reachable, not single-step transitions." and transition `(f) (iii) → (ii): reachable — via (a) then (b)`.

**Problem**: The word "reachable" is used here to mean "achievable by the transition system," but `reachable(a, d)` is a formally defined predicate in this same ASN meaning V-space membership. Two uses of the same word with different meanings in a formal document. Transitions (a)–(e) use "permitted" or "forbidden"; transition (f) switches to "reachable" without explanation for the vocabulary change.

**Required**: Replace "reachable" in the A3 note and transition (f) label with "achievable" or "attainable." The note becomes: "A3 classifies which state-pairs are achievable…" and (f) becomes: `(f) (iii) → (ii): achievable — via (a) then (b)`.

### Issue 2: A4, A4a, A5 omit document-set frame condition
**ASN-0030, A4/A4a/A5 frame conditions**: None of the three specification requirements states `Σ'.D = Σ.D`.

**Problem**: D2 (DocumentPermanence) ensures no document is *removed*, but nothing in the foundations or in A4/A4a/A5 prevents these operations from *adding* documents. An implementation that satisfied A4 while also creating a spurious empty document on every DELETE would not violate any stated condition. The frame conditions quantify over `Σ.D` ("for all d' in Σ.D with d' ≠ target…") but are silent about documents in `Σ'.D \ Σ.D`. Since these properties are labeled "specification requirements" — intended as complete statements of correct behavior — the document-set frame belongs.

**Required**: Add `Σ'.D = Σ.D` to the frame condition of each of A4, A4a, and A5. One sentence covering all three would suffice (e.g., a paragraph before the operations section stating that DELETE, REARRANGE, and COPY preserve the document set).

## OUT_OF_SCOPE

### Topic 1: MAKELINK specification
**Why out of scope**: The ASN analyzes address permanence for content operations. Link creation modifies a separate state component (link storage / spanfilade) not yet formalized. The ASN correctly derives link *stability* consequences (A7, A7a, A7b) without needing to specify link *creation*. Future ASN territory.

### Topic 2: Historical backtrack mechanism
**Why out of scope**: The ASN honestly identifies that transition (ii)→(i) for truly unreferenced addresses is permitted by invariants but not achievable by any defined operation. The recovery mechanism (historical trace enfilade) is a new operation with its own invariants. Correctly deferred.

### Topic 3: Content authentication
**Why out of scope**: A10 correctly identifies the gap between "the invariant holds" and "a client can verify the invariant holds." Closing this gap requires cryptographic mechanisms outside the current architecture. New design territory.

VERDICT: REVISE
