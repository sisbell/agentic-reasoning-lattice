# Review of ASN-0093

## REVISE

### Issue 1: Link invariants restate ASN-0043 using `origin` where the foundation defines `home`

**ASN-0093, State model / L1a / L1c**: "The `origin(·)` function is the tumbler-projection defined in ASN-0036 (truncation to the `zeros = 2` prefix)." and L1a: "`(A a ∈ dom(L) :: origin(a) ∈ dom(M))`", L1c: "`t₀ = origin(ℓ)`".

**Problem**: ASN-0036's `origin` (S7) is defined only for content addresses (`a ∈ dom(Σ.C)`). Foundation ASN-0043 deliberately introduced a *separate* link-scoped projection — `home(a) = N(a).0.U(a).0.D(a)` — precisely because `origin` is content-scoped, and states its own L1a as `home(a) ∈ dom(Σ.M)` and L1c's seed as `home`. This note inherits ASN-0043's L1a/L1c (Properties table, Source = ASN-0043) but restates them with `origin` applied to link addresses, i.e. it stretches a content-scoped foundation function onto links while bypassing the foundation function (`home`) that already covers them. The State-model sentence attributes the generalized "truncation to the `zeros = 2` prefix" reading to ASN-0036, which does not define `origin` that broadly, and never reconciles with `home`. A precise reader comparing this note's L1a (`origin`) against ASN-0043's L1a (`home`) sees two symbols for the same quantity with no stated equivalence.

**Required**: Either use `home(ℓ)` for link addresses (matching ASN-0043's L1a/L1c verbatim) and reserve `origin` for content (matching ASN-0036 S7), or add a one-line reconciliation establishing `origin ≡ home` as the common projection and stating that the note adopts `origin` uniformly across both stores. As written the inherited invariants do not match their cited source notation.

## OUT_OF_SCOPE

None. The deferred topics (arrangement mutation, entity stratification, provenance, coupling, withdrawal) are correctly enumerated in Scope and the substrate does not stray into them.

VERDICT: REVISE
