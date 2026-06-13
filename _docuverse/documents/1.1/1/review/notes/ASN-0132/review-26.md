# Review of ASN-0132

I checked each introduced claim against its cited foundations, re-derived the worked example end to end (static counts 2/4/2/0 and the dynamic 2→3→3→2 sequence), and traced the two-case CN-MONO weakest-precondition argument. The note is sound:

- **CN-DEF / well-definedness** — the counted set is a subset of `dom(Σ.L)` (finite by L-fin, ASN-0093) and `sat` is decidable per link (FL-DEC, ASN-0121), so `countlinks_FTT(q, Σ) ∈ ℕ`. The frame is `Σ` (a query, not a transition). Sound.
- **CN-LOC** — `sat` reads only `Σ.L(a)` and the address projection `home(a)`; `nullified` (hence `addressable`) is an `Σ.L`-function (FL-LOC, ASN-0121). The count never consults `Σ.C`, `Σ.M`, `Σ.E`, `Σ.R`. Sound.
- **CN-UNIT** — the three rejected units are correctly disposed: anchoring collapses inside the existential `touch`; transclusion and appearance live in `Σ.M`, excluded by CN-LOC. The version-refraction sub-case correctly routes through J4 (ASN-0047) — the fork composite performs no `K.λ` and no `K.μ⁺_L` ("no other elementary steps"), so `Σ.L` is untouched and cross-version surfacing is appearance multiplicity, not link copying. Sound.
- **CN-ENUM / CN-ZERO / CN-SNAP / CN-STAB / CN-RETRACT / CN-ORPHAN / CN-OBT** — each follows from its cited lemma. CN-ZERO's empty-store/empty-request distinction (FL-EMP) is correctly drawn; the biconditional holds in both cases. CN-ORPHAN's superset relation `|C| = |U| + |orphans|` against FL-REACH is correct. The reverse-orphaning instance under CN-STAB (home-bounded count unmoved because `home(a)` projects the permanent address) checks out.
- **CN-MONO** — the ordinary-case wp matches FL-WP(a) (with the standing-retraction conjunct correctly inherited from ASN-0086's disciplined-domain simplification + R0a, not re-derived); the retraction-case wp matches FL-WP(b) with the self-retraction conjunct `b ∉ coverage(G')`. I separately confirmed the retraction case's sum-preservation is complete: the body shows counted-stays-counted under the hypothesis, and the missing "no previously-uncounted link becomes counted" direction follows trivially from nullified-monotonicity (R6a) + sat-fixity (CN-LOC), so the conclusion is established. The 3→2 dynamic step correctly demonstrates the *boundary* — the hypothesis fails and the count falls.

I also confirmed Standard 7 is satisfied (every load-bearing citation is to a foundation; ASN-0108/0111/0114/0120/0125/0129 appear only in the scope-exclusion list), and that the note specifies abstract system guarantees (unit of counting, locality, snapshot/stability/monotonicity semantics) rather than implementation mechanics — the Gregory back-end remarks are clearly marked as deviation-from-spec observations. Not META.

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: V-to-I resolution of content-pointing queries into address-set requests
The note takes `q` as already resolved over addresses and treats the front-end's V-to-I resolution against an arrangement as upstream of the operation. The invariant connecting an address-set count to an arrangement-position (V-spec) count is correctly deferred to Open Question 1 — it is new territory (the resolution boundary / ASN-0127's layer), not a gap in this ASN.

### Topic 2: count↔enumeration cross-state consistency under concurrency
CN-ENUM's "at one state" qualifier correctly scopes the equality; the discipline under which a count and a *later* enumeration observe one consistent state is a concurrency concern deferred to Open Question 2. Appropriately out of scope.

### Topic 3: count as a planning primitive (cost asymmetry)
The specification fixes the count *value* and is deliberately silent on *cost* (Open Question 5). Whether "how many" can be answered more cheaply than "which ones" is a quality-of-service concern, correctly not a correctness obligation here.

### Topic 4: federated counting across independently administered stores
Open Question 6 raises this; it belongs to the replication / inter-server layer (BEBE), explicitly excluded by the scope list. Appropriately out of scope.

VERDICT: CONVERGED
