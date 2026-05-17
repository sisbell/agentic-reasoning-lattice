# Review of ASN-0086

## REVISE

### Issue 1: Seed-independence proof relies on an unestablished contiguous-prefix claim

**ASN-0086, Emit_K Definition, "Case B's seed-independence" paragraph**: "combined with the IH-derived fact that every `incʲ'(d.0.s_L.1, 0)` for `j' ∈ {0, …, k}` is in `dom(Σ.L)` (R0a's invariant applied at Σ to all such `j'`, since the stream is monotonically extended by every prior disciplinary emission under `d`)"

**Problem**: The claim that `incʲ'(d.0.s_L.1, 0) ∈ dom(Σ.L)` for *every* `j' ∈ {0, …, k}` is load-bearing for the conclusion that `j = i + k` is the global least `j ≥ 0` with `incʲ(d.0.s_L.1, 0) ∉ dom(Σ.L)`. But this fact does *not* follow from R0a's sibling-stream invariant as stated. R0a's invariant says each existing link is in the stream at *some* `j ≥ 0`; it does not say all positions `{0, …, k}` are occupied. The set `{0, 5}` would satisfy R0a's invariant (each element is in the stream) but violate the implicit contiguous-prefix claim. Under the discipline, contiguous-prefix does hold, but R0a's proof establishes only the sibling-stream invariant, not contiguous-prefix. The parenthetical "since the stream is monotonically extended by every prior disciplinary emission under `d`" gestures at the missing argument but does not derive it.

**Required**: Either (a) strengthen R0a's stated invariant to "every link is at `j ≥ 0` *and* `dom(Σ.L) ∩ stream(d) = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J}` for some `J`", proving the stronger form by the same induction; or (b) add a brief sub-lemma between R0a and Emit_K (e.g., R0a' — ContiguousPrefixUnderDiscipline) deriving contiguous-prefix from the discipline by induction on emission count; or (c) inline the inductive argument in Emit_K's Case-B seed-independence remark. Without one of these, the seed-independence proof (which licenses calling Emit_K a *function* rather than a relation) is incomplete.

### Issue 2: R0a's "Symmetrically a' ⊀ a" remark is mislabeled

**ASN-0086, R0a's Case 2 sub-argument**: "By L1a's definition `home(·) = N(·).0.U(·).0.D(·)` — exactly this prefix — `home(a') = home(a) = d`, contradicting `d' ≠ d`. Symmetrically `a' ⊀ a`."

**Problem**: The antichain conclusion as stated is `a ≼ a' ⟹ a = a'`, which is *already* bidirectional via universal quantification over the pair `(a, a')`: instantiating at `(a', a)` covers the reverse direction. The "Symmetrically" remark is therefore unnecessary, but more confusingly, it is mislabeled — Case 2's hypothesis is `d ≠ d'`, and what is "symmetric" is the argument with roles swapped, not the conclusion. As written, the remark suggests a separate fact (`a' ⊀ a` under `d ≠ d'`) is being asserted, which is true but redundant.

**Required**: Either drop the remark (since universal quantification gives bidirectionality), or rephrase to clarify that it is exhibiting the same argument applied to the swapped pair (`(a', a)` with `d' ≠ d`), not a distinct claim.

### Issue 3: R0a's antichain conclusion in Case 1 uses T10a.2 without verifying its sibling-stream precondition

**ASN-0086, R0a "Antichain conclusion as corollary"**: "the sibling-stream invariant places both `a` and `a'` at `incʲ(d.0.s_L.1, 0)` and `incʲ'(d.0.s_L.1, 0)` for some `j, j' ≥ 0` — both are siblings in the depth-2 link allocator rooted at `d.0.s_L.1`... by T10a.2 (NonNestingSiblingPrefixes, ASN-0034) any two distinct siblings are prefix-incomparable"

**Problem**: T10a.2's precondition is "`tᵢ, tⱼ` are distinct siblings from the same allocator". The corollary needs to establish that `a` and `a'` are siblings of the *same* allocator before invoking T10a.2. The note asserts they are "siblings in the depth-2 link allocator rooted at `d.0.s_L.1`" but does not explicitly establish that both `a` and `a'` belong to that one allocator's domain. Under R0a's sibling-stream invariant, both lie on the stream anchored at `d.0.s_L.1`, but stream membership and allocator-domain membership require an extra step (the stream IS the allocator's enumeration, but this identification is implicit). The Worked Sketch instantiates this concretely (`a₁`, `b₁`, `a₂` are first three emissions of `A_{a₁}`), so the chain is sound, but R0a's general proof leaves the bridge from "in the stream" to "siblings in A_{d.0.s_L.1}" implicit.

**Required**: Add one sentence after "siblings in the depth-2 link allocator" naming the allocator (e.g., `A_{d.0.s_L.1}`, the allocator opened by R0 Step 2's child-spawn `(d.0.s_L, 1)`) and explicitly identifying its enumeration with the sibling stream `{incʲ(d.0.s_L.1, 0) : j ≥ 0}` via T10a.7. Then T10a.2's "same allocator" precondition is discharged on `j ≠ j'`.

### Issue 4: R6b "proof" is a single observation rather than a derivation

**ASN-0086, R6b — SingleDepthRetraction**: "Justification. Direct from the Definition of `nullified(Σ)`: the existential quantifier ranges over `L_R^Σ`, not `A_R^Σ`."

**Problem**: R6b is labeled a LEMMA but its proof is a single observation about the definition. The subsequent paragraph (the "(1) Emit (b, F', G_a, R)..." / "(2) Emit (c, F'', G_b, R)..." analysis) is illustrative but is presented as a distinguishing-from-R6a discussion, not as derivation steps. Either R6b is so direct from the definition that it should be marked DEF or COROLLARY rather than LEMMA, or the proof should be slightly expanded to show the chain `(b, F', G_a) ∈ L_R^Σ' ∧ a ∈ coverage(G_a) ⟹ a ∈ nullified(Σ')` from the Definition, independent of `b`'s `A_R` status.

**Required**: Either redesignate R6b (a DEF or direct corollary of the Definition is more honest than a LEMMA whose proof is "see the definition"), or expand the justification to a 2–3 step derivation showing how the quantifier's range gives the conclusion mechanically.

### Issue 5: R0 Step 4's S-invariants summary argument cites preservation by "definitional identity of inputs"

**ASN-0086, R0 Step 4 final bullet**: "ASN-0036 S-invariants (uniform argument). Every ASN-0036 invariant is a predicate over `(Σ.C, Σ.M)`; none references `Σ.L` or its values... For any predicate `P` whose free variables range only over `(Σ.C, Σ.M)`, `P(Σ'.C, Σ'.M)` and `P(Σ.C, Σ.M)` are the same proposition: preservation holds by definitional identity of inputs, not by re-verification of `P`."

**Problem**: The claim that "every ASN-0036 invariant is a predicate over `(Σ.C, Σ.M)`; none references `Σ.L`" should be verified, not asserted. The S-invariant catalog in the reference material (S0–S9, including S7a, S7b, S7c, S7d) is over `Σ.C` and `Σ.M` — but the verification that none touches `Σ.L` is the load-bearing premise of the "definitional identity" argument. A skeptical reader cannot verify this premise without enumerating the S-invariants. The bullet asserts it; ideally it would cite the property of ASN-0036's transition vocabulary (Scoping note, Σ.L is not in ASN-0036's signature) that makes this true uniformly.

**Required**: Cite the structural property of ASN-0036 (its state signature `(Σ.C, Σ.M)` excludes `Σ.L`, so any S-invariant well-formed in ASN-0036's signature cannot mention `Σ.L`) rather than asking the reader to inspect each invariant. One sentence: "Each S-invariant is well-formed in ASN-0036's signature `(Σ.C, Σ.M)`, which by construction excludes `Σ.L`, so the substitution argument applies uniformly without case-by-case enumeration."

### Issue 6: The Definition of `nullified(Σ)` allows a degenerate case the note doesn't address

**ASN-0086, Definition of Nullified**: "`nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}`"

**Problem**: The Definition restricts to `a ∈ A_rel^Σ`. But `coverage(G')` is a subset of `T` (not of `A_rel^Σ`); it may contain tumblers in `A_doc^Σ`, ghost tumblers, or addresses in neither. The intersection-with-`A_rel^Σ` is what limits `nullified(Σ)` to relational addresses. Under Setup + L14, content addresses are subspace-separated from link addresses, so retractions whose `G'` covers content addresses (e.g., a retraction with to-span `(c, δ(1, #c))` for content `c`) produce *no* nullification effect — the coverage hits content but the `A_rel^Σ` filter excludes it. The note doesn't comment on whether this is intended. The corresponding case for higher-arity links (`|Σ.L(a)| > 3`) is similarly ambiguous: a retraction targeting a higher-arity link nullifies it (the address is in `A_rel^Σ`), but since `A_K` is defined only over standard-triple links, no `A_K` reflects the change. The Open Questions mention this for the multi-arity case but not for the content-targeting case.

**Required**: Add one sentence noting that retractions whose `coverage(G')` falls entirely outside `A_rel^Σ` (e.g., targeting content addresses or ghosts) are well-formed but operationally inert (they leave `nullified(Σ)` unchanged), or constrain `Nullify` to require its target be in `A_rel^Σ` (which P1 already does, but other `Emit_R` calls with crafted spans escape this constraint). Either way, the asymmetry between "what retractions are syntactically permitted" and "what they nullify operationally" deserves explicit treatment.

### Issue 7: R7 Step 3's closure argument scope-shifts mid-paragraph

**ASN-0086, R7 Step 3**: "Therefore every relational-layer-initiated state-affecting transition is a class-(iii) `→`-step, and every *relational-layer-initiated* class-(iii) `→`-step is — by the operational commitment that all relational-layer state changes route through `Emit_K` — an `Emit_K` call."

**Problem**: The argument first derives (from L12, L12a, Frame) that every state-affecting transition affecting `Σ.L` is a class-(iii) `→`-step. This is rigorous. Then it asserts that every relational-layer-initiated class-(iii) step is an `Emit_K` call "by the operational commitment". This second step is not a derivation — it's a stipulation. The Scoping note acknowledges this, but the surrounding paragraph reads as if Step 3 *proves* closure, when in fact it proves half (class (iii) is the only L-affecting class) and stipulates the other half (relational-layer commitments route through `Emit_K`). The "no additional relational-layer operation exists" conclusion conflates the proven and stipulated halves.

**Required**: Separate the two halves explicitly. "From L12, L12a, and Frame: any L-affecting transition is class (iii). From the operational commitment (definitional, not derived) that relational-layer state-changes route through `Emit_K`: every relational-layer class-(iii) step is an `Emit_K` call. Therefore: under that commitment, the relational-layer state-affecting operations are exactly `{Emit_K}` ∪ {definitional shorthands for `Emit_K` invocations}." The current wording elides the asymmetry.

### Issue 8: Worked Sketch's Step 2 chain reuse claim needs explicit IH

**ASN-0086, Worked Sketch, Step 2 (concrete) L1c verification**: "the witness chain reuses `a₁`'s through the depth-2-allocator-opening child-spawn `(d.0.2, 1)` (which created `A_{a₁}`) and then takes *two* sibling steps within `A_{a₁}`"

**Problem**: The chain for `a₂` reuses the prefix of `a₁`'s chain through step (iii). But L1c (LinkAllocatorConformance) asserts existence of *a* chain, not the uniqueness or reusability of any particular chain. The argument that `a₂`'s chain extends `a₁`'s assumes (without saying so) that the T10a-conforming chain through a given address is essentially unique (in the sense that any chain to `a₂` must pass through the same allocator-spawning events). This is true under T10a's at-most-once axiom — each `(t, k')` pair fires at most once, so the chain through the depth-2 allocator's opening is forced — but the Worked Sketch doesn't cite this.

**Required**: Add a brief remark: "By T10a's at-most-once axiom on `(d.0.2, 1)`, the depth-2 allocator `A_{a₁}` is opened by a unique spawn event, so any L1c chain to `a₂` (which lies in `A_{a₁}`'s sibling stream) passes through that same opening; the chain shown is the canonical witness." This makes the chain-reuse explicit rather than implicit.

VERDICT: REVISE
