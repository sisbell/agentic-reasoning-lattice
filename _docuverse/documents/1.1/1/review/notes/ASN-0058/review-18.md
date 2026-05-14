# Review of ASN-0058

## REVISE

### Issue 1: V_{u₁}(d_s) notation extends ASN-0036 without explicit definition

**ASN-0058, Definition (ContentReference)**: "(i) V_{u₁}(d_s) ≠ ∅ — the subspace contains at least one V-position"

**Problem**: ASN-0036 defines V_1(d) (in D-CTG) for the text subspace specifically. It does not define V_S(d) for general subspace identifier S. This ASN uses V_{u₁}(d_s) throughout the content reference section (precondition (i), the inclusion argument after C0a is cited, and the C2 proof's exhaustiveness step) as if V_S(d) were already defined in the foundation. Since foundation reuse is permitted but inventing new notation in this ASN should be explicit, the generalization should be stated.

**Required**: Either add an explicit definition near the top of the content-references section — `V_S(d) := {v ∈ dom(M(d)) : subspace(v) = S}` — or annotate the first use as a generalization of ASN-0036's V_1(d) to arbitrary subspace identifiers.

### Issue 2: M6(d) origin-traceability claim implicitly requires a ∈ dom(C)

**ASN-0058, M6 (SplitPreservation) clause (d)**: "Each I-address a + k carries its origin permanently in its tumbler structure — origin(a + k) = origin(a), since a + k = a ⊕ δ(k, #a) and TumblerAdd with action point #a copies aᵢ for all i < #a, preserving the document prefix N.0.U.0.D (S7, ASN-0036)."

**Problem**: The `origin` function (S7, ASN-0036) is defined only on dom(Σ.C); the document-prefix structural argument requires S7b's `zeros(a) = 3` and S7c's `#E(a) ≥ 2`, neither of which is stated as a precondition of a mapping block. Although blocks in any decomposition of M(d) have I-starts in ran(M(d)) ⊆ dom(C) by S3, the block definition β = (v, a, n) admits arbitrary tumblers as a. The argument that #(N.0.U.0.D) < #a is what makes the document prefix lie in TumblerAdd's prefix-copy region — that derivation isn't visible at M6, only emerges in M16.

**Required**: State explicitly that M6(d) is conditional on a ∈ dom(C) (or that the algebra is understood to range over blocks drawn from decompositions of arrangements), and either inline the #(N.0.U.0.D) < #a step or forward-reference M16's worked-out version.

### Issue 3: M16 hypothesis on I-address structure is implicit in the claim text

**ASN-0058, M16 (CrossOriginMergeImpossibility)**: "If origin(a₁) ≠ origin(a₂) — the I-addresses in two blocks were allocated by different documents — then the blocks cannot satisfy I-adjacency"

**Problem**: The proof's first move is "For element-level I-addresses, S7b (ASN-0036) gives zeros(a₁) = 3..." — but the *claim* does not state element-level membership as a hypothesis. The reader has to infer that `origin` being defined on a₁, a₂ implicitly constrains them to dom(C). For a property labelled as a structural impossibility theorem of the algebra, the precondition should be explicit.

**Required**: Add `a₁, a₂ ∈ dom(C)` (or equivalently, "the I-addresses in two blocks of any decomposition of some M(d)") to M16's preconditions, so the proof's "for element-level I-addresses" qualifier becomes a discharge of a stated hypothesis rather than a hidden assumption.

### Issue 4: M7's overlap case has a small gap at k = 0

**ASN-0058, M7 (MergeCondition) necessity proof**: "So v₂ = v₁ + k for k = (v₂)_m − (v₁)_m ∈ [0, n₁), placing v₂ ∈ V(β₁). Combined with v₂ ∈ V(β₂), this gives v₂ ∈ V(β₁) ∩ V(β₂), violating B2 of the original decomposition."

**Problem**: The case v₂ < v₁ + n₁ is being ruled out. The derivation concludes k ∈ [0, n₁). At k = 0 the conclusion v₂ = v₁ contradicts the hypothesis v₁ < v₂ directly — there is no need to invoke B2 at all. At k ≥ 1, v₂ ∈ V(β₁) at a non-zero offset, and then B2 fires. The proof states "k ∈ [0, n₁)" without separating the two subcases, leaving slightly imprecise the conclusion that B2 is the violated invariant (when at k=0 the direct contradiction with v₁ < v₂ is what fires).

**Required**: Either restrict the range to k ∈ [1, n₁) by noting k = 0 contradicts the case hypothesis v₁ < v₂, or explicitly say "either k = 0 contradicting v₁ < v₂, or k ≥ 1 placing v₂ in V(β₁) at offset k and violating B2."

### Issue 5: C0a's interpretation of J at indices beyond #t is unstated

**ASN-0058, C0a (PrefixConfinement) proof**: "Suppose for contradiction that J = {j : 1 ≤ j < m ∧ tⱼ ≠ uⱼ} is non-empty, and let j₀ = min(J). ... Moreover, #t ≥ m: if #t < m, then J = ∅ forces tⱼ = uⱼ for all 1 ≤ j ≤ #t, making t a proper prefix of u..."

**Problem**: J's defining predicate `tⱼ ≠ uⱼ` is well-formed only when tⱼ is defined, i.e., j ≤ #t. The proof's J non-empty branch silently assumes j₀ ≤ #t (used implicitly when it writes t_{j₀} > u_{j₀}). The J = ∅ branch then re-interprets the same condition over the range 1 ≤ j ≤ #t. The reader is left to figure out which convention is in force, and the case where #t < m and J as written might include j > #t (depending on convention) is never addressed.

**Required**: Add one sentence stating that J's membership predicate requires tⱼ to be defined (equivalently, j ≤ #t), making the J non-empty / J = ∅ split exhaustive, and the conclusion #t ≥ m of the second branch unambiguous.

## OUT_OF_SCOPE

(No items — the Open Questions section explicitly defers further algebraic questions, which is appropriate.)

VERDICT: REVISE
