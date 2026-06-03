# Review of ASN-0070

The mathematical core is sound. F0's inverse-image definition is clean, F-subspace's biconditional is correctly derived, and the F-canonical existence/uniqueness proof (including the new Step 0 vacuous base case) is rigorous and complete. The six worked configurations correctly exercise the catalogued properties, and the weakest-precondition analysis is genuine. All cross-ASN references are to foundation ASNs (0034/0036/0043/0047/0053/0058) — no rule-7 violation. My findings below are accretion/duplication under the anti-bloat classifier, not correctness gaps.

## REVISE

### Issue 1: Contiguity proof duplicated between prose section and lemma
**ASN-0070, "Computation via Decomposition" and F-contig**: The "Contiguity claim" is proved in full inline (ending in ∎: "the intersection therefore contains every index between its minimum and maximum") in the prose section; then F-contig restates the same argument — "strict monotonicity of `k ↦ a + k` (M1) places any index between two qualifying indices into an order-interval... T12's order-convexity then places that index in `⟦σ⟧`."
**Problem**: The same proof appears twice in different words — once as an inline claim, once as a catalogued lemma derivation. This is the "two paragraphs say the same thing" pattern.
**Required**: Make F-contig the single home of the proof and have the Computation section cite F-contig, or keep the inline proof and reduce F-contig's Derivation to a bare pointer with no re-summary.

### Issue 2: Roadmap meta-prose in the F-canonical proof
**ASN-0070, F-canonical, Steps 0/3/4**: Several sentences narrate proof structure rather than prove:
- Step 0: "This base case is independent of Steps 1–5, which presuppose `m_S(d)` defined."
- Step 3: "Steps 1 and 2 constrain the *shape* any canonical form must take and supply the contiguity notion; we now exhibit one, discharging the existence half of the theorem."
- Step 4: "S9 ... governs equality under the full denotation `⟦·⟧`, not the V-restricted denotation `⟦·⟧_V`. We bridge..."
**Problem**: These are navigational/defensive framing the reader must skip past to reach the argument; they restate the step's role rather than advance it.
**Required**: Delete the structural-commentary sentences; let each step's first mathematical sentence carry it. The Step 4 bridge can open directly with the lemma ("For a single component span `σ = (s, δ(c, m_S(d)))`: ...").

### Issue 3: Per-configuration justification prose in worked examples
**ASN-0070, worked-example configurations 5 and 6**: Each new configuration is prefaced by an inventory of what prior configurations did and did not cover — "Every configuration so far meets each block at offset `j = 0`... We exercise that case directly" (fifth); "Configurations 1–5 keep both subspaces of `d` populated... We now exercise the Vacuous-subspace convention directly" (sixth).
**Problem**: This is use-site/coverage-inventory prose justifying the example's existence rather than running it. The example's purpose is evident from the property labels (F-contig, F-empty's vacuous branch) it checks.
**Required**: Drop the retrospective "configurations so far" framing; state the configuration and the properties it exercises directly.

### Issue 4: Documentation-convention meta in Derived Properties intro
**ASN-0070, Derived Properties**: "`follow` is a query; per-lemma Frame slots are omitted unless an across-transition observation is involved."
**Problem**: Explains a formatting convention rather than advancing content; the absence of a Frame slot is self-evident where it is absent.
**Required**: Remove the sentence. Similarly trim F-multi's "Two arguments, kept separate." to let the two labelled sub-arguments stand on their own.

## OUT_OF_SCOPE

### Topic 1: Cross-document resolution relationship for shared homes
**Why out of scope**: The first Open Question (relating `follow(ℓ, d, i)` and `follow(ℓ, d', i)` for documents transcluding overlapping homes) is genuine future territory; F-multidoc correctly establishes only that no document is privileged. Not an error here.

### Topic 2: Multi-server / BEBE traversal consistency
**Why out of scope**: Replication and inter-server consistency are explicitly out of scope; the second Open Question correctly defers them.

VERDICT: REVISE
