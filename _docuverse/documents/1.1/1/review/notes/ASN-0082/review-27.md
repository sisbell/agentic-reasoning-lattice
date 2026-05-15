# Review of ASN-0082

## REVISE

### Issue 1: D-DP(a) proof skips the R = ∅ case

**ASN-0082, D-DP proof**: "By D-SEP(b), when R ≠ ∅ the minimum ordinal in Q₃ is ord(p), and by D-BJ every other element of Q₃ has ordinal strictly greater than ord(p). So every element of L has ordinal strictly less than ord(p) and every element of Q₃ has ordinal ≥ ord(p), giving L ∩ Q₃ = ∅."

**Problem**: The proof appeals to D-SEP(b), which is itself conditioned on R ≠ ∅. When R = ∅, Q₃ = ∅ by definition and the intersection is trivially empty, but this case is not addressed. The conclusion holds in both cases (the universal "every element of Q₃ has ord ≥ ord(p)" is vacuously true when Q₃ = ∅), but the proof structure leaves a reader to deduce this. D-SEP(b)'s own proof, by contrast, splits into Case 1 (v = r) and Case 2 (v > r) and handles them explicitly. D-MIN-post handles three cases explicitly. D-DP(a) should match that level of rigor.

**Required**: Insert a case split at the start of the (a) argument: "*Case R = ∅:* Q₃ = ∅ by definition, so L ∩ Q₃ = ∅ trivially. *Case R ≠ ∅:* [current proof]."

### Issue 2: I3-S2 wp Case 1's "contrapositive" reasoning conflates two transformations

**ASN-0082, wp analysis for I3-S2, Case 1**: "*(shift) ∩ (shift):* `(A u₁, u₂ : both in shifted source : shift(u₁, n) = shift(u₂, n) ⟹ M(d)(u₁) = M(d)(u₂))`. The hypothesis simplifies via the contrapositive to `u₁ ≠ u₂ ⟹ shift(u₁, n) ≠ shift(u₂, n)` — exactly TS2 (ShiftInjectivity, ASN-0034)."

**Problem**: The contrapositive of the obligation `shift(u₁, n) = shift(u₂, n) ⟹ M(d)(u₁) = M(d)(u₂)` is `M(d)(u₁) ≠ M(d)(u₂) ⟹ shift(u₁, n) ≠ shift(u₂, n)`, not the form quoted. The form `u₁ ≠ u₂ ⟹ shift(u₁, n) ≠ shift(u₂, n)` is the contrapositive of *TS2 itself*, not of the obligation. The actual discharge is: assume shift(u₁,n) = shift(u₂,n); apply TS2 to get u₁ = u₂; conclude M(d)(u₁) = M(d)(u₂) by reflexivity. This works, but the "simplifies via the contrapositive" framing misidentifies which proposition is being transformed.

**Required**: Rewrite as: "Discharged by TS2 (ShiftInjectivity, ASN-0034): from `shift(u₁, n) = shift(u₂, n)`, TS2 gives `u₁ = u₂`, hence `M(d)(u₁) = M(d)(u₂)` by reflexivity of equality. The wp surfaces TS2 as the precise obligation: without injectivity of shift, two distinct pre-state positions could map to the same post-state V-position with conflicting I-addresses."

### Issue 3: Worked-example verification lists for contraction omit D-DP

**ASN-0082, "Boundary case: R = ∅" verification list**: D-L, D-SHIFT, D-DOM, D-CTG-post, D-MIN-post, S8-depth-post, S8a-post, S2-post, S3-post are checked, but D-DP is not listed. Same omission in "Boundary case: L = ∅ and R = ∅". The non-boundary cross-subspace contraction example also omits D-DP from its tick-list.

**Problem**: D-DP is one of the three lemmas (D-BJ, D-SEP, D-DP) the proof structure relies on. The boundary cases are precisely where D-DP becomes interesting (Q₃ empty, L empty). Omitting D-DP from these checks leaves the boundary verification incomplete and reinforces the impression from Issue 1 that D-DP is treated as "trivial in degenerate cases" without being shown.

**Required**: Add `D-DP: L ∩ Q₃ = ∅ (Q₃ = ∅ since R = ∅). ✓` to the R = ∅ and full-deletion boundary cases. The cross-subspace example is non-degenerate; add the analogous check there too.

## OUT_OF_SCOPE

### Topic 1: Depth > 2 contraction

**Why out of scope**: The depth scoping axiom restricts contraction to #p = 2. The ASN explicitly identifies generalization to deeper ordinals as an open question with substantive new analysis required (a strengthened TA4 or first-principles derivation). This is correctly deferred to a future ASN if Xanadu ever needs it; the udanax-green implementation evidence and Literary Machines design intent confirm depth-2 suffices for byte-stream INSERT/DELETE/REARRANGE.

### Topic 2: Composition with content placement

**Why out of scope**: The "Scope" paragraph clearly delimits I3 to the shift sub-operation of INSERT, deferring content allocation, gap-filling, and re-derivation of D-CTG/D-MIN/D-SEQ to a future INSERT ASN. Likewise, contraction here is the gap-closure dual; full DELETE composition is a separate concern. Both are properly scoped out.

### Topic 3: Link-subspace mutation discipline (tombstoning)

**Why out of scope**: The cross-subspace examples touch on link-subspace exemption from D-CTG/D-MIN/D-SEQ but tombstone semantics for link mutation are not specified here. The ASN correctly notes link mutation "uses tombstoning instead, deferred to a future ASN."

VERDICT: REVISE
