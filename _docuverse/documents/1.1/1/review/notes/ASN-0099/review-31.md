# Review of ASN-0099

## REVISE

### Issue 1: F10's well-orderedness terminology overstates the requirement
**ASN-0099, F10 proof**: "the least element exists by well-orderedness of `T1`'s restriction, the second-least is the least of the remainder, and so on by finite induction"

**Problem**: "Well-orderedness" is a stronger property than needed. T1 restricted to an arbitrary subset of T is not in general well-ordered (consider `{[1, 1], [1, 2], [1, 3], …}` viewed under T1 — every finite subset has a least element by totality alone, but the infinite ordinal here requires no further well-ordering claim). The argument actually rests on finiteness (just established via L-fin) combined with totality of T1. For finite totally-ordered sets, least-element existence is trivial without needing well-orderedness.

**Required**: Replace "well-orderedness of T1's restriction" with explicit invocation of finiteness: "the least element exists in any non-empty finite totally-ordered set" — or cite NAT-wellorder applied via the bijection between the finite result set and an initial segment of ℕ, making the well-ordering route explicit. The same fix applies in F10-filt and F10-sco where the F10 argument is referenced.

### Issue 2: A1b relies on Nelson and Gregory as load-bearing premises
**ASN-0099, A1b**: "the closed-world interpretation of the silent frames is exactly the discipline that the implementation honors" and "(1) Design intent (Nelson, Literary Machines)... (2) Implementation evidence (Gregory, udanax-green)"

**Problem**: A1b cites Nelson's Literary Machines and Gregory's udanax-green codebase as evidence grounding a load-bearing structural lemma. A1b feeds F9, F9★, F9-cor, F9★-cor, F17, F18, F19, F19-filt, F19-sco for the K.μ⁺/K.μ⁻/K.ρ sub-cases. An abstract specification should not have load-bearing premises grounded on external design documents or implementation artifacts. The reader cannot verify "Nelson's design intent" against the foundation ASNs supplied in this review, and "udanax-green honors this discipline" is implementation evidence, not specification reasoning. The closed-world reading is a reasonable convention, but as currently presented, A1b makes the spec's correctness depend on accepting interpretive claims about sources outside the foundation.

**Required**: Either (a) restate A1b as adopting the closed-world convention purely as a methodological choice ("This ASN reads ASN-0047's effect-clause convention as closed-world: components absent from both effect and frame are preserved") without grounding it on external sources, or (b) defer the question to a foundation revision (ASN-0047 publishing `L' = L` in the three silent frames, or a foundation axiom explicitly stating the closed-world convention). The Nelson and Gregory discussions belong in design notes, not in a load-bearing structural lemma.

### Issue 3: F4 strengthening/weakening framing is imprecise about which conformance contract is being violated
**ASN-0099, F4 strengthening direction**: "Any such alternative defines a different match predicate and therefore (via F2 with `matches` read as F1) a different — and, with respect to F1, incomplete — conforming result set."

**Problem**: The phrase "conforming result set" is ambiguous. If the alternative implementation uses P_s as its match predicate, its output is conforming to F2 with `matches := P_s`, not conforming to F2 with `matches := F1`. The "incomplete with respect to F1" reading is what's intended, but the prose "conforming result set" suggests the alternative is somehow conforming-but-different, which conflates two conformance contracts. The weakening direction below ("the alternative implementation fails the conformance test") is clearer.

**Required**: Rephrase to make explicit that conformance is evaluated against F2 ∧ F3 with `matches := F1` (the F1-fixed contract), and any predicate other than F1 yields an output that violates this contract. Match the explicitness of the weakening direction's "fails the conformance test at the realized state".

### Issue 4: The chain-index argument in F10 cites SubAllocatorAxiom.ChainDiscipline at A_doc, but the axiom covers only A_C and A_L
**ASN-0099, worked example**: "By SubAllocatorAxiom.ChainDiscipline and T10a (ASN-0093, ASN-0034), `d_a < d_b` under T1."

**Problem**: SubAllocatorAxiom in ASN-0093 covers `A_C(d)` and `A_L(d)` — content and link sub-allocators rooted at documents. Document sub-allocators `A_doc(A)` rooted at accounts are defined in ASN-0047's allocator hierarchy. The citation should target T10a.7 (EnumerationInjectivity, ASN-0034) for the general principle that any T10a-conforming `inc(·, 0)` chain is strictly T1-increasing — this is the load-bearing fact, applicable uniformly across A_C, A_L, A_doc, A_account, A_v.

**Required**: Replace "SubAllocatorAxiom.ChainDiscipline and T10a" with a direct citation to T10a.7 (EnumerationInjectivity), which gives the strict T1-increase across any T10a-conforming chain regardless of which allocator hosts it.

### Issue 5: F10's "between" claim for version-extension blocks is asserted but the general (n > 3) iteration is only gestured at
**ASN-0099, F10 derivation**: "a version's link block sits between its parent's block and the parent's siblings' blocks. The general nesting structure follows from applying the pairwise case analysis above iteratively"

**Problem**: The claim says "iteratively" but the only worked instance is three documents (`d_a`, `d_v`, `d_b` exhibited in the example). The leap from three pairwise comparisons to "any nesting structure" needs more than "iteratively" — what's the inductive argument? Specifically, for n documents related by an arbitrary pattern of sibling/version-of relationships, how does the case analysis compose into a single strictly increasing sequence? "T1's transitivity" is named but the full chaining argument isn't supplied.

**Required**: Either (a) state the general claim formally as a separate lemma with explicit inductive proof, or (b) restrict the claim to "any pair of documents" (matching what the pairwise case analysis actually establishes) and let downstream specs build on the pairwise form for n-document orderings. The iterative claim as stated is the kind of "by similar reasoning" hand-wave the review standards warn against.

## OUT_OF_SCOPE

### Topic 1: Inverse direction (FOLLOWLINK/RETRIEVEENDSETS)
**Why out of scope**: The ASN explicitly notes "We have not specified the inverse direction — the resolution of the result's endsets back to V-positions". This belongs in a separate operation specification, not in FINDLINKS.

### Topic 2: Phantom-address query semantics
**Why out of scope**: The ASN flags the open question of "what FINDLINKS returns when the query I-set includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`". The match predicate mechanically handles any `I ⊆ T`, but operational semantics for phantom-address queries belongs in a follow-up.

### Topic 3: Replication, partition tolerance, and multi-server consistency
**Why out of scope**: The ASN's single-state setting is explicit, and replication/partition tolerance for the link store belongs in BEBE-layer specs.

### Topic 4: Access control composition
**Why out of scope**: The ASN notes access control "composes with discovery rather than altering its semantics" and leaves formalization for a separate spec.

### Topic 5: Combined filtered-and-scoped operation
**Why out of scope**: The ASN explicitly leaves `findlinks_filtered_scoped` implicit, deriving its determinism/survivability/monotonicity by composition. A future spec extending the query vocabulary could formalize it.

VERDICT: REVISE
