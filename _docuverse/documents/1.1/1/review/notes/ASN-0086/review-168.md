# Review of ASN-0086

The mathematical core is sound: R0's invariant discharge is conjunct-complete (frame-fixed S/M/C invariants by substitution, L0/L1/L1a/L1b/L1c/L3/L5/L6/L14/L14a/L-fin individually), R0a's two-case antichain rests on the correct disjoint premise sets, the wp Case 2 biconditional is genuinely derived in both directions over a stated domain, and the worked sketch exercises each property against concrete tumblers. I found no proof-by-checkmark, no missing boundary case, and no foundation-notation reinvention. The findings below are anti-bloat (the active classifier): prose redundancy and bookkeeping deferrals that a precise reader must work around.

## REVISE

### Issue 1: Containment-chain strictness stated and cross-deferred across two definitions
**ASN-0086, Definition — substrate-conforming state**: "the converse fails — the conformance containment chain is proper, its strictness recorded once at *Definition — state-local-conforming state* above (via Remark — NestedLinkWitness)."
**ASN-0086, Definition — state-local-conforming state**: "its rightmost inclusion is strict, witnessed by the NestedLinkWitness construction above (Remark — NestedLinkWitness)."
**Problem**: The same fact (properness/strictness of `{→*-reachable} ⊆ {substrate-conforming} ⊆ {state-local-conforming}`) is asserted in both conformance definitions, with the second carrying pure bookkeeping meta-prose ("its strictness recorded once at ... above"). This is the "multiple paragraphs defer to the same location" + "prose justifies document ordering" pattern. The strictness fact has exactly one load-bearing consumer (the wp "discipline alone is insufficient" paragraph, which cites NestedLinkWitness directly).
**Required**: State the containment chain and its strictness once, at the point of use or in the Remark, and drop the cross-deferral sentence in the substrate-conforming-state definition.

### Issue 2: "K-ops satisfy clauses (a)–(c) by their ASN-0093 contracts" stated three times
**ASN-0086**: appears in (i) Definition — substrate-conforming state ("the K-op primitives K.σ/K.α/K.λ satisfy (a)–(c) by their ASN-0093 contracts"), (ii) the K-Step Conformance Preservation statement ("Every K-op →-step ... is conformance-preserving, by its ASN-0093 contract"), and (iii) that lemma's proof ("The K-op claim is the preceding observation: K.σ/K.α/K.λ satisfy (a)–(c) by their ASN-0093 contracts").
**Problem**: The identical claim is restated three times in adjacent text — "two paragraphs say the same thing." The proof's restatement (iii) adds nothing beyond the statement (ii).
**Required**: Assert it once (in the K-Step lemma, where it is used) and remove the duplicate in the definition and the proof's tautological restatement.

### Issue 3: Cross-home freshness argument duplicated verbatim across R0's two branches
**ASN-0086, R0 first-emission branch**: "if `home(ℓ') = d' ≠ d` ... `a = ℓ'` would force `d = home(a) = home(ℓ') = d'` ... a contradiction."
**ASN-0086, R0 subsequent-emission branch (Cross-home freshness)**: "Were `a = ℓ'` as tumblers, applying the home projection to both sides would force `d = home(a) = home(ℓ') = d'`, contradicting `d ≠ d'`."
**Problem**: The cross-home distinctness argument (home-projection is a function of the address, so equal addresses force equal homes) is the same in both branches; only the establishment of `home(a) = d` differs. The argument is written out twice in different words.
**Required**: Factor the cross-home distinctness step into a single statement (e.g., a one-line sub-lemma "distinct homes ⟹ distinct addresses, by the home-projection") and have both branches cite it, leaving only the branch-specific `home(a) = d` derivation in place.

## OUT_OF_SCOPE

### Topic 1: Tightening L1b (`#E ≥ 2`) to `#E = 2` at the substrate source
L-ContiguousPrefix-Cor1 proves `#E(a) = 2` for substrate-conforming states, but whether ASN-0043's L1b admission should be narrowed is correctly left to the foundation/source, not resolved here. Already logged as an Open Question.

### Topic 2: Higher-arity typed relations `L_K^{(n)}` and multi-arity projections
The note explicitly restricts to standard-triple links; the higher-arity relational construction is genuinely new territory, correctly deferred to a future ASN and the Open Questions.

VERDICT: REVISE
