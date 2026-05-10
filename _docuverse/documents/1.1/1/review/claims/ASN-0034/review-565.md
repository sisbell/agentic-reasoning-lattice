# Cone Review — ASN-0034/T4b (cycle 4)

*2026-04-25 20:46*

I'll review the ASN as a whole, focusing on internal consistency and any new issues not already in Previous Findings.

After careful reading, here are my new findings:

### T4 prose "purely definitional" framing clashes with derived Consequence slot
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4 (HierarchicalParsing) prose: "T4 is purely definitional: it characterises T4-valid as a predicate on `T` (the four-conjunct conjunction above) without asserting which `t ∈ T` satisfy it"
**Issue**: T4's Formal Contract has a *Consequence:* slot (Exhaustion) that is genuinely derived — not definitional. A precise reader sees "purely definitional" and reaches for the slot inventory, where Definition + derived Consequence don't fit the framing. The intended meaning ("T4 makes no unconditional assertion about which tumblers exist") is defensible, but the surface phrasing reads as if T4 has only Definition slots.

### T4c uses "Injectivity" for what is pairwise mutual exclusivity
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4c (LevelDetermination) proof body: "*Injectivity.* The values `0, 1, 2, 3` are pairwise distinct in ℕ ... Since `zeros(t)` is single-valued, distinct zero counts induce distinct labels."
**Issue**: There is no function whose injectivity is at issue here. The argument establishes that the four label predicates have pairwise-disjoint extensions — i.e., no T4-valid `t` receives two labels — by the joint facts that `zeros(t)` is single-valued and `{0,1,2,3}` are pairwise distinct. Calling this "Injectivity" treats the assignment-of-labels as a function from `T4-valid` to `{labels}`; that function is implicit, never named in the contract. The Postcondition more precisely calls it "Pairwise distinctness," but the body proof uses the looser term.

### T4b Postconditions slot duplicates Definition slot
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4b (UniqueParse). The Definition slot fixes `dom(N), dom(U), dom(D), dom(E)`, the per-`k` projection values, and the four-case partitioning. The Postconditions slot then restates the function signature, the dom() characterisations, the per-`k` presence pattern, and the `t.X₁` notation.
**Issue**: A precise reader gets the projection-domain characterisation twice and the per-`k` case enumeration twice. Postconditions ought to name what the proof established that the Definition didn't — primarily *uniqueness*, *image lying in `T` with `ℕ⁺`-valued components*, and *exhaustion of `dom(N)` by the four cases*. The current Postconditions slot mixes those genuine outputs with verbatim restatement of the Definition slot.

### T4c Definition's "t is T4-valid" predicate referenced in quantifier domain
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4c Definition slot: "(A t ∈ T : t is T4-valid :: (zeros(t) = 0 ↔ t is a node address) ∧ ...)"
**Issue**: The quantifier restricts to "t is T4-valid", but T4 introduces *T4-valid* in its body as a Definition sub-bullet without giving it a contract-level *symbol*. A reader walking T4c's contract sees the predicate referenced and must visit T4's body (not its Formal Contract slot) to confirm its content. T4 has a *Definition: T4-valid predicate* sub-bullet — so the reference is legitimate — but a glance at T4's Formal Contract surface doesn't make T4-valid prominent as the canonical predicate name. Naming the predicate at the slot level (e.g., a `T4Valid(t)` symbol) would let T4c quote the canonical name rather than a prose phrase.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 4224s*
