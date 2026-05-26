# Review of ASN-0098

## REVISE

### Issue 1: LP-Comp introduces dangling labels LP9★, LP10★, LP11★ without formal statements

**ASN-0098, LP-Comp**: "K.μ⁺/K.μ⁺_L instances compose to cumulative growth (a closure LP9★ recovered by transitive containment), K.μ⁻ instances to cumulative shrinkage (LP10★ by transitive containment), K.μ~ instances to a cumulative bijection (LP11★ by composition in Sym(dom(Σ.M(d))) when K.μ~-FIX holds at each step)"

**Problem**: The labels LP9★, LP10★, LP11★ are introduced inline but never formally stated as claims. They appear neither as separate lemmas in the body nor in the claims table. A reader cannot determine whether they are meant to be formal claims (parallel to LP2★, LP3★, Store Monotonicity★, which ARE formally stated with proof sketches) or merely informal labels for compositions. The body of the ASN never appeals to LP9★ etc. by name — LP18 uses Store Monotonicity★ + LP3★ directly, and LP19 uses LP19a applied at a specific allocation step. The starred labels are therefore both unstated and unused.

**Required**: Either formally state LP9★, LP10★, LP11★ as labelled lemmas with statement, proof sketch (by induction on chain length / bijection composition), and entries in the claims table — matching the treatment of LP2★, LP3★, and Store Monotonicity★. Or remove the labels and use descriptive prose without the starred names. The current half-introduced state suggests claims that don't formally exist.

### Issue 2: "What is not possible" enumeration mixes positive guarantees with impossibility statements

**ASN-0098, "What the Link Holder Can Rely On" section, item 4 under "What is not possible"**: "At any state, the link is discoverable from any document whose arrangement maps to any I-address in any of its endsets' coverage (LP12)."

**Problem**: Item 4 is a positive guarantee about when discoverability holds, not a statement of impossibility. It sits in a subsection titled "What is not possible" alongside genuine "cannot" claims (endsets cannot be rewritten, slots cannot be permuted, coverage cannot be altered, boundary insertion cannot grow tight reach). The framing mismatch creates ambiguity about whether the subsection enumerates capabilities denied to external parties (the genuine "cannot" items) or system commitments about discoverability that hold conditionally.

**Required**: Either move item 4 to a separate "Where discoverability is guaranteed" subsection, or reframe it negatively to match surrounding items ("The link cannot fail to be discoverable from a document whose arrangement maps to any coverage I-address"). Item 5 is borderline — its "is not discoverable" phrasing fits the impossibility frame more naturally — but item 4 is clearly a positive statement misplaced.

## OUT_OF_SCOPE

None. The Open Questions section identifies legitimate future work — reverse discovery, projection contiguity, V-order/I-order correspondence, link-to-link references, comparative editing across documents, fork composite link-subspace behaviour — without conflating them with this ASN's scope.

VERDICT: REVISE
