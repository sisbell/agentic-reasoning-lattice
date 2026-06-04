# Review of ASN-0099

## REVISE

### Issue 1: The two meta-lemmas' relationship is stated twice, wrapped in use-site inventory

**ASN-0099, "Determinism and Comprehension Invariance"**: The paragraph introducing `PerLinkInvarianceUnderValuePreservation` ("We also factor out the per-link primitive that grounds the chain above. It applies under a strictly weaker hypothesis... This is the load-bearing tool precisely when `dom(Σ'.L)` has grown via K.λ... the comprehension-level meta-lemma is unavailable there... Citing claims invoke the per-link primitive directly.") and the paragraph immediately following it ("ComprehensionInvariantUnderΣL is the comprehension-level composition of PerLinkInvarianceUnderValuePreservation: full `Σ.L = Σ'.L` contributes domain equality... and licenses PerLinkInvarianceUnderValuePreservation at every `a`...").

**Problem**: Both paragraphs state the same containment relationship between the two lemmas in different words (two-paragraphs-say-the-same-thing). The first also carries use-site inventory prose ("the load-bearing tool precisely when...", "Citing claims invoke the per-link primitive directly") that catalogs where the lemma will be consumed rather than advancing its statement.

**Required**: State the relationship once. The lemma bodies are self-contained; downstream sites (F9-λ, F11, F19-filt) already cite whichever lemma they use, so the use-site inventory is redundant and should be deleted.

### Issue 2: F2-V ∧ F3-V carries defensive justification and re-explains the conformance-pair structure

**ASN-0099, "Completeness"**: "Each labeled pair `F2-X ∧ F3-X` denotes the conjunction of two individual containments analogous to F2 and F3... The two halves remain independently citable, so a non-conforming implementation that violates one direction (e.g., a filtered/scoped implementation with a deferred-index obligation that breaks F3-filt while satisfying F2-filt) can be pinned to the specific half at fault." Also: "An implementation may compute the V-side result by routing through `result` internally or by a direct procedure — but the conformance contract is fixed at F2-V ∧ F3-V."

**Problem**: The conformance pairs F2/F3 already establish the "containment in each direction, conjunction forces equality" pattern; re-explaining it "analogously" for each variant is restatement. The "independently citable / pinned to the specific half at fault" sentence is a defensive justification for why the claims were split, not content the reader needs to follow the claims.

**Required**: State the variant pairs (F2-filt/F3-filt, etc.) with their predicates and drop the meta-commentary about citability and fault-pinning. The "may compute by routing or directly" sentence is implementation rationale; remove or compress.

### Issue 3: F4(b) and the "Realizability discharge" repeat the same realizability framing

**ASN-0099, F4 and the paragraph beginning "Realizability discharge"**: F4's closing ("Any P diverging from F1's overlap test produces a result(I, Σ) that disagrees with findlinks(I, Σ) on at least one realizable (a, I) pair, hence non-conformance with F2 ∧ F3 as written") and the separate "Realizability discharge" paragraph ("Any predicate `P` disagreeing with F1 on some pair `(a, I)` defines a different operation provided the disagreement is realizable. It always is: K.λ admits...") plus the closing sentence after the five witnesses ("Each of the five witnesses is realizable... therefore wiring F2 ∧ F3 with any of them produces an operation different from `findlinks`").

**Problem**: The realizability argument is stated three times around the same five witnesses. The witnesses themselves are object-level and valuable; the surrounding "any diverging P is a different operation because the disagreement is realizable" claim is the same point repeated at F4's tail, at the discharge paragraph's head, and at the witnesses' tail.

**Required**: State the realizability principle once (it applies uniformly to all five witnesses), then list the witnesses. Remove the duplicate framings in F4's tail and the closing recap.

### Issue 4: Implementation-mechanics rationale lodged in "Local Atomicity"

**ASN-0099, "Local Atomicity and the Single-State Setting"**: "Implementations that defer index maintenance to a background process create a window in which the index lags the link store; during that window, results from the index would violate F2. The abstract specification permits no such window. Nelson's design intent at LM 2/46... no foundation invariant of this ASN formalises a timing bound beyond 'next query after K.λ commitment reflects the link'."

**Problem**: This is implementation-mechanics rationale (background index processes, lag windows) explaining *why* an implementation might fail F2, not a statement of system guarantee. The abstract content — "the next query at any state succeeding the K.λ must include `a` if `a` matches" — is already stated one sentence earlier. The deferred-index discussion restates F2's force in implementation terms.

**Required**: Keep the atomicity statement grounded in SequentialTransitionAxiom and the "next query reflects the commit" guarantee; move or drop the background-index narrative, which adds no invariant.

## OUT_OF_SCOPE

### Topic 1: Semantics for query I-sets outside `dom(Σ.C) ∪ dom(Σ.L)`
**Why out of scope**: The ASN correctly defers this to its Open Questions; `findlinks` is defined for arbitrary `I ⊆ T` and the match predicate is well-defined regardless, so no error exists in this ASN.

### Topic 2: Partition tolerance, consistency models, access-control composition
**Why out of scope**: These are future-ASN territory (replication/protocol layer), already enumerated under "What We Have Not Specified" and Open Questions.

META: The ASN defines abstract state-derived operations (`findlinks`, `image`, filtered/scoped/V-side forms) and their invariants, so it remains in-spec; the findings are accreted meta-prose, not drift into implementation territory.

VERDICT: REVISE
