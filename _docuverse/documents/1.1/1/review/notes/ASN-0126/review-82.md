# Review of ASN-0126

The technical core is sound. I worked the proofs — P1's induction, the ProjectionBridge/B1/B2 split, RegisteredAdmissible, P5's manual lift, the three-move R-Scope transfer in *Retraction as an attributed Binary*, the wp refinement, and the worked illustration's addresses (`a_R = 1.1.0.1.0.1.0.2.3`, `a = g = ...2.4 ∈ coverage(G_rng)`, born-nullified) — and they hold, including the boundary cases (empty registry, `G = ∅`, `F = ∅` excluded, arity > 3 excluded, unregistered K via conditional conjunction, interior-prefix P-tgt failure). The B2 "no `→_sh`-successors" caveat is correctly observed and correctly worked around in P5. No correctness findings.

The findings below are all the residue this note's `anti-bloat` classifier names: meta-prose that the precise reader skips.

## REVISE

### Issue 1: B1 over-justifies a triviality and inventories its use-sites
**ASN-0126, The projection bridge (B1)**: "Every ASN-0086 state-indexed function this note invokes — `a_emit(·, d)`, `A_rel^·`, `L_K^·`, `A_K^·`, and `nullified(·)` — reads only the C/M/L components (in each definition only `dom(Σ.L)`, the link values `Σ.L(·)`, `coverage`, and `origin` appear — never the registry), so each takes equal values at Σ and `π(Σ)`..."
**Problem**: "An ASN-0086 state-indexed function reads only C/M/L" is trivially true — an ASN-0086 state *has* nothing else; there is no registry for it to read. The parenthetical that verifies "never the registry" per definition belabors what cannot be otherwise, and the five-function enumeration is a use-site inventory.
**Required**: State the general fact once without the parenthetical check: "Every ASN-0086 state-indexed function reads only C/M/L (an ASN-0086 state has nothing else), so each agrees at Σ and π(Σ)." Name a specific function only where B1 is actually applied.

### Issue 2: the span-count/coverage principle is asserted three times
**ASN-0126, Shape-conformance**: para 1 ends "Span-count, not coverage, is the measure."; the "One edge" para then states "**a single-span slot means a single span as emitted**" and closes "Counting spans-as-emitted keeps the measure intrinsic to the value."
**Problem**: The same principle — we count spans, not coverage — is asserted three times across two paragraphs. The two *examples* (one unit-depth span with infinite coverage; two abutting spans with one-span coverage) are genuinely complementary and worth keeping, but the principle does not need restating with each.
**Required**: Keep both examples; state the principle once.

### Issue 3: "Properties established" re-lists results with no content
**ASN-0126, Properties established**: a bulleted list of "P1 (RegistryInvariance)" … "P6 (ReachableConformance)" with no statements.
**Problem**: Each property is already stated and proved inline. The list carries no reasoning — it is a content-free inventory of the note's own results, and restating the bodies would only duplicate the inline boxes.
**Required**: Cut it.

### Issue 4: redundant closing summary in the decidability paragraph
**ASN-0126, Registry permanence**: after establishing "it has finitely many keys at *every* reachable state; deciding (i) is then deciding `coverage(K) = coverage(K_j)` against each of the finitely many stored representative endsets … decidable by CoverageEqualityDecidable", the paragraph adds: "Finiteness bounds the number of comparisons and CoverageEqualityDecidable discharges each one, so (i) — and hence the whole gate — is a terminating, applicable-at-every-emit check."
**Problem**: The final sentence restates the conclusion the preceding sentence already reached (finite keys + each test decidable). It is the same shape as the "P5 summary sentence" already dropped in the last revision.
**Required**: Delete the closing sentence; the prior sentence carries it.

## OUT_OF_SCOPE

None. The Open Questions section draws its boundaries correctly — operational semantics (idem, behavior catalog, default predicates, composition) and the `F=1`/`N=3` loosening are deferred where they belong, not skipped.

VERDICT: REVISE
