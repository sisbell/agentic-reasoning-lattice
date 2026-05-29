# Review of ASN-0053

## REVISE

### Issue 1: S7 title overclaims — covering is not representation
**ASN-0053, S7 (FiniteRepresentability)**: "Every finite set of positions P ⊂ T admits a span-set Σ with |Σ| ≤ |P| and ⟦Σ⟧ ⊇ P."
**Problem**: The formal claim is `⟦Σ⟧ ⊇ P` (a *cover*), but the label "FiniteRepresentability" asserts P is *represented*. The constructed span `(t, [0,…,0,1])` covers the entire half-open interval `[t, t⊕[0,…,0,1])`, which by T0(b) always contains deeper points (e.g. `t.0.1`) — so `⟦Σ⟧ ≠ P` in general, and no span denotes a single position. Exact representation of an arbitrary finite P is *impossible*, yet the title implies it is achieved. The bound `|Σ| ≤ |P|` is also proved only as `|Σ| = |P|`.
**Required**: Rename to reflect a covering claim (e.g. CoveringExistence) and state explicitly that exact representation of a finite point-set is generally impossible because spans are subtree-convex. Note this contrast rather than letting the title imply more than the proof gives.

### Issue 2: Restated prose in "The reach function"
**ASN-0053, reach function**: "When a = b, no displacement is needed… D0 ensures the displacement is well-defined; D1 ensures the round-trip is faithful for a < b."
**Problem**: This paragraph restates the earlier passage ("D0 ensures the displacement b ⊖ a is a well-defined positive tumbler… It does not guarantee round-trip faithfulness — the identity… additionally requires #a ≤ #b (D1)"). Two paragraphs in the same section say the same thing in different words — a flagged anti-bloat pattern. The reader must skip the second to confirm it adds nothing.
**Required**: Delete the restatement; the `a = b` degenerate handling is the only new content and can be a single clause.

### Issue 3: "Observations from the implementation" is implementation-mechanics essay
**ASN-0053, Observations from the implementation**: "These observations do not affect the abstract properties — S0 through S11 hold for any correctly-implemented span algebra over the tumbler space."
**Problem**: The section's framing is defensive ("do not affect the abstract properties") and its body (silent cross-depth degeneration, width-encoding precision, fatal-abort behavior) describes implementation mechanics rather than advancing any abstract property of the algebra. The defensive disclaimer is itself meta-prose justifying why the section is present. Concrete encoding examples are fine, but the surrounding "this doesn't affect abstraction" scaffolding is noise.
**Required**: Cut the defensive framing and any prose that only explains implementation behavior. Retain at most a concrete encoding example if it illustrates a stated property; otherwise remove.

### Issue 4: S6 carries motivational essay in a definition slot
**ASN-0053, S6 (LevelConstraint)**: "The constraint is not merely technical — it reflects the tree structure… In a flat address space (integers), every interior point would admit a valid split… The subspace closure TA7a from ASN-0034 captures the favorable case… This is the abstract guarantee that span operations work for the common case…"
**Problem**: The flat-address analogy is permissible, but its placement and the surrounding essay ("not merely technical", "captures the favorable case", "abstract guarantee… for the common case") inflate a definition with rationale that does not advance the meaning of `level_compat`. The "Mutually level-compatible" definition similarly defers with "by the argument given in S6" rather than stating its content.
**Required**: Reduce S6 to the definition plus the one load-bearing fact (same length ⇒ type-(i) divergence, D0 satisfied). Move or drop the motivational essay; keep the analogy only if tightened to one sentence.

### Issue 5: Label collision on "D2"
**ASN-0053, Properties Introduced table**: "D2 | Width recovery: for level-uniform σ, reach(σ) ⊖ start(σ) = width(σ) — follows from DisplacementUnique (D2, ASN-0034) | cited"
**Problem**: The local row is labeled **D2**, the same label as foundation ASN-0034's DisplacementUnique, but it states a *different* (span-level, derived) claim. Reusing a foundation label for a locally-derived consequence invites confusion about which "D2" a later citation means.
**Required**: Give the span-level width-recovery consequence its own label (or cite it inline as a consequence of ASN-0034 D2 without minting a colliding "D2" row).

## OUT_OF_SCOPE

### Topic 1: Splitting at a span boundary
S4 defines split only for an *interior* point (start < p < reach). Behavior when p = start or p = reach (degenerate split into empty + whole) is excluded by definition; if a future operation needs boundary splits, that belongs in a later ASN.

### Topic 2: Span-set difference bound
The final Open Question asks for the tight bound on `|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|`. S11–S11d bound only single-span difference; set-level difference is genuinely new territory, correctly deferred.

VERDICT: REVISE
