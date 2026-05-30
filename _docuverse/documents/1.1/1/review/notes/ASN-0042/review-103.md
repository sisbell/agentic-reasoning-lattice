# Review of ASN-0042

## REVISE

### Issue 1: Notation-justification prose in the `delegated` definition does not advance the definition
**ASN-0042, State Axioms, Definition (delegated)**: "Because `π'` is newly introduced — `π' ∈ Π_{Σ'} ∖ Π_Σ`, so `pfx_Σ(π')` is undefined — every occurrence of `pfx(π')` in conditions (i)–(v) denotes `pfx_{Σ'}(π')`... This reading is well-defined: O15's membership clause places `π' ∈ Π_{Σ'}`, so `pfx_{Σ'}(π')` exists; and O13 fixes it for all subsequent states, so the choice of `Σ'` as the evaluation state is immaterial to the value."
**Problem**: This is meta-prose explaining the evaluation-state semantics of a symbol rather than stating what the predicate means. It is the kind of "well-definedness of the notation" essay the precise reader must read past to reach conditions (i)–(v). The four-place/subscript abbreviation apparatus is similarly machinery, not content.
**Required**: Reduce to at most one clause fixing the convention (delegator prefix read at `Σ`, delegate prefix at `Σ'`); delete the justification chain.

### Issue 2: `acct(a)` well-formedness duplicates FieldStructure
**ASN-0042, The Account-Level Boundary**: the `FieldStructure` paragraph and the subsequent "Well-formedness of `acct(a)` follows from FieldStructure" derivation both perform the same `zeros(a) ∈ {0, 1, ≥2}` case split to conclude `zeros(acct(a)) ≤ 1`.
**Problem**: Two paragraphs in the same section say the same thing — the second re-walks the cases the first already established. Compounded by the forward pointer "The formal case definition is given in the Formal Contract below," which defers the definition the reader is currently looking for.
**Required**: State the case definition once, in the Formal Contract; let postcondition (b) cite FieldStructure in one line rather than re-deriving the cases.

### Issue 3: Freshness-(v) is restated at every consumer rather than cited
**ASN-0042**: the fact "(v) discharges both `T4(pfx(π'))` and freshness `pfx(π') ∉ Σ.B` via Freshness-(v)" is rewritten at O15 condition (v), the *Delegation* summary-table entry, O7(c), O10's B6 verification, and DelegatorAllocatesPrefix.
**Problem**: This is the same downstream fact deferred-to/restated in five places — exactly the multi-site repetition pattern. Freshness-(v) is already a named derived lemma; consumers should cite it, not paraphrase its content.
**Required**: Replace each restatement with a bare citation "(by Freshness-(v))."

### Issue 4: Essay paragraphs occupy argument slots without advancing reasoning
**ASN-0042, Subdivision Authority**: "O5 interacts with O2. Because ownership is exclusive, exactly one principal may allocate... no external intervention, no administrative override, no 'root user'..." — and **Permanence**: "The combination of O3, O8, O12, O13, and B0 means the ownership structure is monotonically growing... The tree of ownership deepens but never prunes." — and the entire **Summary of the Model** section.
**Problem**: These restate already-proved results in prose, deriving nothing. They are the meta-commentary a reader must skip to follow the chain.
**Required**: Delete, or fold any genuinely new claim into the relevant formal contract.

### Issue 5: O1a is invoked before it is proved, and `Π` is used unqualified in a state-relativized contract
**ASN-0042, O9 Formal Contract**: "`(A Σ reachable from Σ₀, π ∈ Π, a ∈ Σ.B : owns(π, a) ⟹ N(pfx(π)) ≼ N(a))`" — bare `Π`. Separately, O1a is stated in *The Account-Level Boundary* and used in O6, O9, O10, but its inductive proof appears only later, in *Delegation* ("Each of O1a, T4, and O1b is a reachable-state invariant proved by the same induction").
**Problem**: O9's quantifier should be `π ∈ Π_Σ`; bare `Π` is ambiguous in a function whose whole point is state-relativization, and the proof relies on O1a/O17 which are `Π_Σ`-invariants. And O6/O9/O10 each invoke "O1a, a derived reachable-state invariant" whose establishment the reader cannot check until a much later section — a forward dependency that is asserted, not signposted at the use sites.
**Required**: Write `π ∈ Π_Σ` in O9. At O1a's introduction, state explicitly that it is established by the induction in *Delegation*, so the earlier uses are not circular.

### Issue 6: Worked example applies single-transition lemmas across milestone arrows
**ASN-0042, Worked Example**: the convention note says "Subscript labels `Σ_0, Σ_1, Σ_2, …` denote trajectory milestones, not single transitions; each segment may comprise multiple `Bop` calls." Yet the O3 verification reasons over "the transition `Σ₀ → Σ₁`," and O3 is a single-transition lemma.
**Problem**: O3's postcondition is proved for one edge `Σ → Σ'`; if a milestone arrow bundles several transitions, applying O3 to it is unjustified (the multi-step refinement corollary, not O3, is what governs bundled arrows). The example does not establish that `Σ₀ → Σ₁` is the lone delegation edge.
**Required**: State that `Σ₀ → Σ₁` is the single delegation transition (no bundling), or invoke the multi-step corollary instead of O3.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and provenance/owner divergence
**Why out of scope**: The ASN correctly confines transfer to an Open Question (Gregory's codebase has no transfer path); modification rights and transfer semantics are new territory, not an error here.

### Topic 2: Cross-node identity federation invariants
**Why out of scope**: O9 establishes node-locality; federation consistency is explicitly future work and listed under Open Questions, not a gap in this ASN.

VERDICT: REVISE
