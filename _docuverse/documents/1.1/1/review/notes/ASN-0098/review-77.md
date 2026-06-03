# Review of ASN-0098

## REVISE

### Issue 1: "State Components" claims only three components matter, but E and R are used materially

**ASN-0098, "State Components"**: "We work over the state structure inherited from the foundations. Three components matter here." — followed by descriptions of only `Σ.C`, `Σ.M`, and `Σ.L`.

**Problem**: The note materially uses two further components of ASN-0047's extended state `Σ = (C, L, E, M, R)`:
- **E** (entity set) — LP8 (Document-Registration Invariance) is stated for "K.δ in the `Document(e)` case," which registers an entity and grows `dom(M) = E_doc`.
- **R** (provenance) — LP14 is "K.ρ (provenance recording)… only adds a pair to `Σ.R`," and the worked trace explicitly records `(i₄, d₂) ∈ R`.

A reader is told three components matter, then meets `E`, `R`, `K.δ`, `K.ρ`, `S3★`, and `S3★-aux` with no prior grounding of the operative state model. Relatedly, the section grounds `Σ.C` immutability in "S0, S1 of ASN-0036" and `dom(Σ.M)` monotonicity in "M1 of ASN-0093," yet the operative transition vocabulary (K.δ, K.ρ, K.μ⁺_L, S3★) is ASN-0047's, where these invariants are restated as P0 and ASN-0047's own M1. The ASN does not pin down which foundation model it is instantiated over.

**Required**: State up front that the note operates over ASN-0047's extended state `Σ = (C, L, E, M, R)`; either describe `E` and `R` in State Components or drop "Three components matter here." Cite the operative model's invariants (P0, M1 of ASN-0047) where that model is in force.

### Issue 2: Prose restatement of the `tight` definition (anti-bloat)

**ASN-0098, "Boundary and Width Behaviour"**: immediately after the formal definition of tightness — "The first conjunct says the span starts at an allocated address; the second says every substrate-emittable address in the span's reach is already allocated."

**Problem**: This sentence restates the two formal conjuncts verbatim in words; the formal definition is one line above. It is the "two statements say the same thing" pattern the anti-bloat classifier targets — a precise reader must skip it to reach the load-bearing prose ("The first conjunct gives `s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)`, whence `s ∈ F`…").

**Required**: Delete the restating sentence; the formal conjuncts already carry it. The decidability/`F`-confinement argument that follows is the content worth keeping.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order reflection, link-to-link induced discovery, cross-document operation comparison

**Why out of scope**: These are already correctly deferred in the note's own Open Questions and concern primitives/guarantees this ASN does not define. They are future-ASN territory, not gaps in the projection-displacement model stated here.

### Topic 2: Link-canonical contraction discoverability (link-subspace span class)

**Why out of scope**: LP12b proves the wp result for the content-canonical class; the symmetric link-canonical case (where the LP-Fin Corollary disjointness argument inverts) is explicitly listed as an Open Question. Proper to leave for a follow-on; not an error in LP12b's stated scope.

META: not applicable — the ASN defines projection as live state-dependent computation, its displacement under each operation, and survival/discoverability invariants, all stated abstractly; it has not drifted into implementation mechanics.

VERDICT: REVISE
