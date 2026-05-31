# Review of ASN-0093

## REVISE

### Issue 1: Inconsistent naming of the document-prefix projection for links (`home` vs `origin`)

**ASN-0093, StoreT4Validity corollary proof**: "The link case is symmetric, using L1c for the chain and **L1a (in place of C2) to land the seed `home(ℓ) ∈ dom(M)`**, whence M0 gives the seed's T4-validity."

**Problem**: Everywhere else the note uses `origin(·)` for the document-level prefix of *both* content and link addresses — L1a is itself stated as `origin(a) ∈ dom(M)`, ChainMembershipForOrigin quantifies over `origin(ℓ') = d`, and the entire worked example writes `origin(ℓ) = d`. This single occurrence of `home(ℓ)` (ASN-0043's name for the same `N(a).0.U(a).0.D(a)` formula) contradicts the note's own restatement of L1a. A reader must verify that `home` and `origin` denote the same projection to follow the step.

**Required**: Replace `home(ℓ)` with `origin(ℓ)` to match L1a's statement and the rest of the note, or state once that the note adopts `origin` for both stores and use it uniformly.

### Issue 2: SD matrix row restates "covers both allocation transitions" in both cells

**ASN-0093, Discharge matrix, SD row**: K.α cell — "...This single argument covers both allocation transitions (K.α and K.λ)." K.λ cell — "As the K.α cell — same standing consequence, **covering both allocation transitions**."

**Problem**: The K.α cell already declares that its single T7 derivation covers both K.α and K.λ. The K.λ cell's "As the K.α cell" pointer is sufficient; re-appending "covering both allocation transitions" repeats the same claim in different words — the duplicated-prose pattern the anti-bloat classifier targets.

**Required**: Reduce the K.λ cell to the bare pointer ("As the K.α cell"); drop the second "covering both allocation transitions."

## OUT_OF_SCOPE

None. The note correctly defers arrangement mutation (K.μ family), entity stratification, provenance, coupling, and link withdrawal, and defines no claims that intrude on those topics. M2's fixing of `M(d) = ∅` is the substrate's own stance, not an arrangement-mutation claim.

VERDICT: REVISE
