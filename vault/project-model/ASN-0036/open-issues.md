### Finding 1: [stale-label] GlobalUniqueness
**Location**: deps:S4
**Detail**: Property S4 references GlobalUniqueness which does not exist in any active ASN's export

### Finding 2: [stale-label] GlobalUniqueness
**Location**: deps:S7
**Detail**: Property S7 references GlobalUniqueness which does not exist in any active ASN's export

### Finding 3: [stale-label] T0(a)
**Location**: deps:D-CTG
**Detail**: Property D-CTG references T0(a) which does not exist in any active ASN's export

### Finding 4: [stale-label] T0(a)
**Location**: deps:D-CTG-depth
**Detail**: Property D-CTG-depth references T0(a) which does not exist in any active ASN's export

### Finding 5: [stale-label] OrdinalShift
**Location**: deps:ValidInsertionPosition
**Detail**: Property ValidInsertionPosition references OrdinalShift which does not exist in any active ASN's export

### Finding 6: [stale-label] TumblerAdd
**Location**: deps:ValidInsertionPosition
**Detail**: Property ValidInsertionPosition references TumblerAdd which does not exist in any active ASN's export

### Finding 7: [prose-only] T0 (ASN-0034)
**Location**: prose
**Detail**: Prose cites T0 (ASN-0034) but no property table entry lists it in follows_from

### 1. Stale Labels

**Finding 1.** D-CTG inline proof cites `"T1(i) (LexicographicOrdering, ASN-0034)"`:

> "The strict inequality at component j follows from v₁ < v₂ by T1(i) (LexicographicOrdering, ASN-0034): the first component at which two equal-length tumblers disagree determines their order."

The foundation labels T1 as **LexicographicTotalOrder**, not "LexicographicOrdering".

---

**Finding 2.** D-SEQ Step 3 and its Formal Contract cite `"T1(i) (TumblerOrdering, ASN-0034)"`:

> "By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1 and differ first at component m where k₁ < k₂."

Same foundation property T1 (**LexicographicTotalOrder**), different wrong parenthetical name ("TumblerOrdering").

### 2. Structural Drift

(none)

### 3. Local Redefinitions

(none)

### 4. Registry Misclassification

**Finding 3.** S8a is listed in the properties table with status `"from T4, S7b (ASN-0034)"` — implying full derivation — but the body text explicitly says **"S8a is a design requirement"** and its formal contract contains an axiom:

> "*Axiom:* V-positions are element-field tumblers — the fourth field in T4's decomposition of element-level addresses."

Every other property with an "Axiom:" in its formal contract (S0, S2, S3, S7a, S7b, S8-fin, S8-depth, D-CTG, D-MIN) is classified as "design requirement" in the table. S8a's axiomatic premise is absent from its "from" chain, making the table entry inconsistent with the body.

### 5. Missing Dependencies

(none)

### 6. Exhaustiveness Gaps

(none)

---

`RESULT: 3 FINDINGS`

I need to read the ASN and foundation carefully to find issues the structured checks couldn't catch.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0036/open-issues.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>vault/**/ASN-0036*</pattern>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>vault/project-model/ASN-0036/**</pattern>
</parameters>
</tool_call>

Let me examine the formal statements for ASN-0036 and the foundation more carefully.

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>vault/project-model/ASN-0036/*</pattern>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0034/formal-statements.md</file_path>
<offset>1</offset>
<limit>100</limit>
</parameters>
</tool_call>

Now let me trace the specific argument chains that the structured checks cannot evaluate.

### Finding 1: S7b provides insufficient precondition for T4 field extraction

**Foundation**: T4 (FieldSeparatorConstraint) — requires valid address tumblers to satisfy: `zeros(t) ≤ 3`, positive non-separator components, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`, non-empty fields. Only under these constraints does `fields(t)` yield a well-defined four-field decomposition.

**ASN**: S7b states `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`. The S7 proof then says: "By S7b, every a ∈ dom(Σ.C) satisfies zeros(a) = 3. By T4, zeros(a) = 3 means a contains exactly three zero-valued field separators, and fields(a) decomposes a into four fields." S7a's formal contract similarly cites S7b as the precondition "so that T4's fields(a) yields node, user, document, and element fields."

**Issue**: `zeros(a) = 3` is necessary but not sufficient for T4's `fields(a)` to be well-defined. A tumbler like `[0, 1, 0, 2, 0, 3, 4]` has `zeros = 3` but violates T4's leading-zero constraint (`t₁ = 0`), making the node field empty and `fields(a)` ill-defined. Similarly, `[1, 0, 0, 2, 0, 3, 4]` has `zeros = 3` with adjacent zeros, producing an empty user field. T4's bijection between zero-count and hierarchical level holds only for tumblers satisfying T4's full axiom — not for arbitrary tumblers that happen to have three zeros. The allocation mechanism (S7a + T10a + TA5) produces only T4-compliant addresses, so the gap cannot be exploited operationally, but the formal chain from S7b to T4 has an unstated premise: that every element of `dom(C)` is a valid address tumbler satisfying T4's full constraint set.

**What needs resolving**: Either strengthen S7b to assert full T4 compliance for `dom(C)` (not just `zeros = 3`), or introduce a separate property establishing `dom(C) ⊆ {valid address tumblers satisfying T4}` — derived from S7a and the foundation's allocator discipline — and cite it as a precondition in S7 and S7a.

---

### Finding 2: ValidInsertionPosition formal contract omits D-SEQ and S8-fin

**Foundation**: D-SEQ requires S8-fin (`dom(M(d))` finite) among its preconditions. OrdinalShift (used for `shift(min, j)`) requires the foundation's shift machinery.

**ASN**: ValidInsertionPosition's formal contract lists: "Preconditions: d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1." The definition body explicitly invokes D-SEQ: "v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1 (D-SEQ)" and uses `|V_S(d)| = N` as a finite natural number.

**Issue**: The definition depends on D-SEQ's characterization of V-positions as `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n}` and on the finiteness of `V_S(d)` (for `N` to be a well-defined natural number and "exactly N + 1 valid insertion positions" to be meaningful). D-SEQ itself requires S8-fin in its preconditions. Neither D-SEQ nor S8-fin appears in ValidInsertionPosition's formal contract. An operation ASN that verifies only ValidInsertionPosition's stated preconditions would not be obligated to establish finiteness, leaving the N + 1 count ungrounded.

**What needs resolving**: Add D-SEQ and S8-fin (or D-SEQ alone, which transitively requires S8-fin) to ValidInsertionPosition's formal contract preconditions.

---

### Finding 3: I-address prefix preservation attributed to TA7a exceeds its formal scope

**Foundation**: TA7a (Ordinal-only shift arithmetic) defines arithmetic on ordinals `o ∈ S` with the subspace identifier `N` held as structural context. Its frame clause states: "The subspace identifier N, held as structural context, is not an operand and is never modified by either operation."

**ASN**: S8-depth claims: "A parallel uniformity holds for I-addresses within a correspondence run: all I-addresses in a run share the same tumbler depth and prefix, differing only at the element ordinal. **This follows from TA7a** (ASN-0034): ordinal displacement [x] ⊕ [k] = [x + k] preserves the component count by construction, so the **full I-address** preserves depth and prefix when the structural context is held fixed."

**Issue**: An I-address like `1.0.1.0.1.0.1.5` has four fields; the "structural context" that must be held fixed includes the entire `node.0.user.0.document.0` prefix — seven components in this example — not just the subspace identifier `1`. TA7a's frame clause guarantees only that the subspace identifier `N` is preserved; it says nothing about the node, user, or document fields, which are outside its formal scope entirely. The conclusion (full prefix preservation) is correct — the prefix is not an operand to ordinal arithmetic, so it is trivially unchanged — but it does not follow from TA7a. It follows from the separate observation that ordinal displacement operates on a strict suffix of the I-address, leaving all preceding structure untouched. The "follows from TA7a" attribution creates a dependency chain that TA7a's formal contract does not support.

**What needs resolving**: Either extend the justification to state the prefix-preservation argument independently of TA7a (since the node/user/document prefix is simply not an operand), or establish a general structural-context principle that subsumes TA7a's subspace-specific frame clause and cite that instead.

### [REVIEW-55] [VERIFIED] S7b

### [REVIEW-55] [VERIFIED] S7a

### [REVIEW-55] [FOUND] S8-depth
Looking at S8-depth, the axiom itself is a design requirement and is cleanly stated. The issue lies in the correspondence run definition.

The narrative claims:

> ordinal displacement `[x] ⊕ [k] = [x + k]` preserves the component count by construction, **so** the full I-address preserves depth and prefix when the structural context is held fixed.

That "so" is unjustified for multi-component ordinals. By TA0, `#(a ⊕ w) = #w`. For single-component ordinals, `#([x] ⊕ [k]) = #[k] = 1 = #[x]` — depth preserved. But if ordinals have depth `m > 1` (which S8-depth permits — it guarantees uniform depth, not depth 2), then `[x₁, x₂] ⊕ [k]` yields `#result = #[k] = 1 ≠ 2`. The displacement `[k]` **destroys the ordinal depth** for multi-component ordinals.

The correct depth-preserving displacement for an `m`-component ordinal is `[0, …, 0, k]` of length `m` (action point `m`), giving `(o ⊕ w)_i = o_i` for `i < m` and `(o ⊕ w)_m = o_m + k`, with `#result = m`. This mapping `δ: (k, m) ↦ [0, …, 0, k]` is not defined in S8-depth, TA7a, or any provided dependency.

The correspondence run definition's `v + k` notation therefore has no formal semantics for the general case that S8-depth's own axiom permits.

```
RESULT: FOUND

**Problem**: The correspondence run definition uses `v + k` for natural number `k`,
referencing TA7a, but TA7a's `⊕` operates on tumbler pairs. The narrative justifies
depth preservation only for single-component ordinals (`[x] ⊕ [k] = [x + k]`), then
claims "so the full I-address preserves depth" — but this generalization fails for
multi-component ordinals. Concretely: for ordinal `o = [x₁, x₂]` and displacement
`w = [k]`, TA0 gives `#(o ⊕ w) = #w = 1 ≠ 2 = #o`, changing the depth. Since
S8-depth's axiom guarantees uniform depth without constraining the depth value,
multi-component ordinals are formally permitted, and the definition is incomplete.

**Required**: Define an ordinal displacement function δ(k, m) = [0, ..., 0, k] of
length m (where m is the ordinal depth within the subspace, as guaranteed uniform by
S8-depth). Then restate the correspondence run's `v + k` as displacement by δ(k, m),
making the depth-matching explicit. This could be added to TA7a as a corollary or
defined within S8-depth's formal contract. The formal contract's Definition should
become:

  - *Definition:* δ(k, m) = [0, ..., 0, k] of length m, with actionPoint m.
    A *correspondence run* in document d is a triple (v, a, n) with n ≥ 1 such that
    (A k : 0 ≤ k < n : Σ.M(d)(v ⊕ δ(k, mᵥ)) = a ⊕ δ(k, mₐ)), where mᵥ and mₐ
    are the uniform ordinal depths of V-positions and I-address element ordinals
    respectively.
```

### [REVIEW-56] [FOUND] S8-depth
## Verification of S8-depth

Working through the checklist against the provided property and dependencies.

**Checklist items 1–5, 7 — the k = 0 boundary in δ and the correspondence run:**

The definition states `δ(k, m) = [0, …, 0, k]` of length `m`, with `actionPoint(δ(k, m)) = m`. When `k = 0`, `δ(0, m) = [0, …, 0]` — the zero tumbler of length `m`. This has **no nonzero component**, so `actionPoint` is undefined. The claim `actionPoint(δ(k, m)) = m` is false at `k = 0`.

The correspondence run quantifies `(A k : 0 ≤ k < n : …)`, and the narrative explicitly invokes the base case:

> At `k = 0`, `δ(0, m) = [0, …, 0]` — the zero tumbler of length `m` — so `v ⊕ δ(0, mᵥ) = v` and `a ⊕ δ(0, mₐ) = a` **by TumblerAdd**

But TumblerAdd's precondition requires **`w > 0`**, and `δ(0, m)` is the zero tumbler, which is not `> 0`. TA0 has the same precondition. The operation `v ⊕ δ(0, m)` is **undefined** under the provided dependencies.

The "What tumbler arithmetic is NOT" section in the dependencies states this explicitly:

> There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition.

The narrative treats `δ(0, m)` as an identity element while the algebra it depends on explicitly denies one exists.

**Checklist item 6 — formal contract:** The definition field claims `actionPoint(δ(k, m)) = m` unconditionally, which fails at `k = 0` as shown above.

---

```
RESULT: FOUND

**Problem**: The correspondence run definition quantifies from k = 0, but δ(0, m) is 
the zero tumbler, for which (a) actionPoint is undefined (no nonzero component), and 
(b) TumblerAdd's precondition w > 0 is violated. The narrative claims 
"v ⊕ δ(0, mᵥ) = v by TumblerAdd" but TumblerAdd explicitly requires w > 0, and the 
dependencies state "the zero tumbler is a sentinel, not a neutral element for addition."

**Required**: Either (1) split the correspondence run into a separate base case and 
an inductive step — e.g., M(d)(v) = a ∧ (A k : 1 ≤ k < n : M(d)(v ⊕ δ(k, mᵥ)) = 
a ⊕ δ(k, mₐ)) — so that ⊕ is never invoked with the zero tumbler; or (2) introduce 
a convention extending ⊕ so that t ⊕ 0_m = t for any zero tumbler of matching length, 
stated as a separate stipulation (not derived from TumblerAdd). In either case, the 
definition's unconditional claim "actionPoint(δ(k, m)) = m" must be restricted to k > 0.
```

### [REVIEW-57] [VERIFIED] S8-depth

### [REVIEW-57] [RESOLVED] S8-depth

### [REVIEW-57] [VERIFIED] S8-fin

### [REVIEW-57] [VERIFIED] D-CTG

### [REVIEW-57] [VERIFIED] D-CTG-depth

### [REVIEW-57] [FOUND] D-MIN
Looking at D-MIN as an axiom (design constraint):

**Axiom statement**: Sound. D-MIN asserts `min(V_S(d)) = [S, 1, ..., 1]` as a convention, justified by Nelson's numbering-from-1 practice and T4's exclusion of zero from non-separator positions. The formal contract correctly classifies this as an axiom.

**Dependency usage**: D-CTG, D-CTG-depth, S8-depth, S8-fin, and T4 are all referenced in the justification and corollary. All are used as claimed.

**Formal contract**: Matches the narrative — axiom with the correct quantification (every d, every S with V_S(d) non-empty).

**Corollary**: The reasoning is correct — D-CTG-depth pins components 2 through m−1 to shared values, D-MIN forces those shared values to be 1, D-CTG forbids gaps in the last component, D-MIN gives minimum k = 1, and S8-fin bounds the maximum. But the text ends with:

> D-CTG restricted to the last component forbids gaps among the k values; D-MIN gives the minimum k = 1; S8-fin bounds the maximum at some finite n. Thus:

The conclusion after "Thus:" is never stated. The corollary builds the full derivation but the formal result — `V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` for some finite n ≥ 1 — is missing.

```
RESULT: FOUND

**Problem**: The corollary (general form) trails off at "Thus:" with no
conclusion. The reasoning is complete but the derived statement is absent.

**Required**: State the corollary's conclusion after "Thus:", e.g.:
`V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` for some finite `n ≥ 1`,
matching the depth-2 illustration ("addresses 1 through 100") that
the surrounding text motivates.
```

### [REVIEW-58] [VERIFIED] D-MIN

### [REVIEW-58] [RESOLVED] D-MIN

### [REVIEW-58] [VERIFIED] S2

### [REVIEW-58] [VERIFIED] S8

### [REVIEW-58] [VERIFIED] S0

### [REVIEW-58] [VERIFIED] S1

### [REVIEW-58] [VERIFIED] S3

### [REVIEW-58] [VERIFIED] S8a

### [REVIEW-58] [FOUND] ValidInsertionPosition
I need to verify the ValidInsertionPosition proof against its dependencies and the checklist.

**Working through the checklist:**

1. **Precondition completeness** — The formal contract states: `d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1`. I'll flag an issue below.

2. **Case coverage** — Two cases (non-empty, empty) are handled. Boundary cases (N=1, depth choices) are addressed. The empty case explicitly argues why m ≥ 2 is necessary.

3. **Postcondition establishment** — Four postconditions are claimed: depth preservation, subspace identity, S8a consistency, distinctness. Each is argued. The subspace identity proof states: "Since δ(j, m) has action point m ≥ 2, TumblerAdd copies component 1 unchanged." This relies on m ≥ 2.

4. **All conjuncts addressed** — All four postconditions have explicit proof paragraphs.

5. **Dependency correctness** — D-MIN (min form), OrdinalShift (result-length identity), TumblerAdd (component behavior), T3 (distinctness), S8-depth (common depth), S8a (well-formedness) — all declared and used. D-CTG is in the preconditions and used indirectly through the D-MIN corollary.

6. **Formal contract** — Has Preconditions, Definition, Postconditions. Structure matches the property type.

7. **Missing guarantees** — Here is the gap:

The non-empty case claims "m ≥ 2, since the first position placed in any subspace is established by the empty case, which requires m ≥ 2, and S8-depth preserves depth thereafter." This is an operational argument — it assumes all positions were placed through ValidInsertionPosition. But the formal contract's preconditions only say `d satisfies D-CTG, D-MIN, S8-depth, S8a`, which do not imply m ≥ 2. A document with V_S(d) = {[S]} (depth m = 1) satisfies all four: D-CTG (trivially, single element), D-MIN (min = [S], vacuously all post-first components are 1), S8-depth (trivially, single element), S8a (zeros([S]) = 0, S ≥ 1, [S] > 0). At m = 1 with N = 1, the definition yields j = 1: shift([S], 1) = [S] ⊕ δ(1,1) = [S] ⊕ [1]; action point is 1, so TumblerAdd gives r₁ = S + 1, producing [S+1] — a position with v₁ = S+1 ≠ S, violating the subspace identity postcondition.

```
RESULT: FOUND

**Problem**: The subspace identity postcondition (v₁ = S) depends on m ≥ 2 so that
δ(j, m) has action point m > 1 and TumblerAdd copies component 1 unchanged. The
non-empty case asserts "m ≥ 2" via an operational argument (the empty case requires
m ≥ 2, S8-depth preserves it), but this argument assumes positions were placed
exclusively through ValidInsertionPosition — an assumption absent from the formal
contract's preconditions. Under the stated preconditions (D-CTG, D-MIN, S8-depth,
S8a), m = 1 is consistent: V_S(d) = {[S]} satisfies all four invariants. At m = 1,
shift([S], 1) = [S+1], which has v₁ = S+1 ≠ S, falsifying the subspace identity
postcondition.

**Required**: Add m ≥ 2 to the formal contract's preconditions for the non-empty
case (e.g., "S8-depth depth m ≥ 2"), or introduce a system-level invariant that
every occupied subspace has depth m ≥ 2 and list it as a dependency. The narrative's
operational justification is sound but needs to be reflected in the formal contract.
```

### [REVIEW-59] [VERIFIED] ValidInsertionPosition

### [REVIEW-59] [RESOLVED] ValidInsertionPosition

### [REVIEW-59] [VERIFIED] D-SEQ

### [REVIEW-59] [VERIFIED] S4

### [REVIEW-59] [VERIFIED] S6

### [REVIEW-59] [VERIFIED] S5

### [REVIEW-59] [VERIFIED] S7

### [REVIEW-59] [VERIFIED] S9

### [REVIEW-59] [VERIFIED] Σ.C

### [REVIEW-59] [VERIFIED] Σ.M(d)

### Finding 1: [stale-label] GlobalUniqueness
**Location**: deps:S4
**Detail**: Property S4 references GlobalUniqueness which does not exist in any active ASN's export

### Finding 2: [stale-label] GlobalUniqueness
**Location**: deps:S7
**Detail**: Property S7 references GlobalUniqueness which does not exist in any active ASN's export

### Finding 3: [stale-label] TumblerAdd
**Location**: deps:S8-depth
**Detail**: Property S8-depth references TumblerAdd which does not exist in any active ASN's export

### Finding 4: [stale-label] T0(a)
**Location**: deps:D-CTG
**Detail**: Property D-CTG references T0(a) which does not exist in any active ASN's export

### Finding 5: [stale-label] T0(a)
**Location**: deps:D-CTG-depth
**Detail**: Property D-CTG-depth references T0(a) which does not exist in any active ASN's export

### Finding 6: [stale-label] OrdinalShift
**Location**: deps:ValidInsertionPosition
**Detail**: Property ValidInsertionPosition references OrdinalShift which does not exist in any active ASN's export

### Finding 7: [stale-label] TumblerAdd
**Location**: deps:ValidInsertionPosition
**Detail**: Property ValidInsertionPosition references TumblerAdd which does not exist in any active ASN's export

### Finding 8: [prose-only] T0 (ASN-0034)
**Location**: prose
**Detail**: Prose cites T0 (ASN-0034) but no property table entry lists it in follows_from

## Surface Check: ASN-0036 vs. ASN-0034

---

### 1. Stale Labels

**Finding 1 — "TumblerOrdering"**

D-CTG-depth formal contract preconditions cite: `T1(i) (TumblerOrdering, ASN-0034)`
D-SEQ proof: `By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1`

Foundation T1 is labeled **LexicographicTotalOrder**. No property named "TumblerOrdering" exists in ASN-0034.

**Finding 2 — "LexicographicOrdering"**

S8 proof (uniqueness within subspace): `tⱼ > vⱼ (from v ≤ t by T1(i) (LexicographicOrdering, ASN-0034))`
D-CTG-depth proof body: `The strict inequality at component j follows from v₁ < v₂ by T1(i) (LexicographicOrdering, ASN-0034)`

Foundation T1 is labeled **LexicographicTotalOrder**, not "LexicographicOrdering". Two different wrong names are used for the same property across different proof sections — "TumblerOrdering" in the formal contracts, "LexicographicOrdering" in the proof bodies.

---

### 2. Structural Drift

(none)

---

### 3. Local Redefinitions

**Finding 3 — δ(k, m) re-introduced locally**

S8-depth formal contract: `*Definition:* δ(k, m) = [0, …, 0, k] of length m; for k > 0, actionPoint(δ(k, m)) = m.`

OrdinalDisplacement in ASN-0034 already defines this: *"For natural number n ≥ 1 and depth m ≥ 1, the ordinal displacement δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m."*

The S8-depth formal contract restates OrdinalDisplacement verbatim rather than citing it. The definition also does not appear in the properties table with status `introduced`, meaning the foundation concept was absorbed into S8-depth's formal contract without acknowledgment.

---

### 4. Registry Misclassification

(none)

---

### 5. Missing Dependencies

(none)

---

### 6. Exhaustiveness Gaps

(none)

---

`RESULT: 3 FINDINGS`

I'll read the relevant files to verify current state before writing findings.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0036/open-issues.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
<offset>1</offset>
<limit>50</limit>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>zeros\(a\) = 3</pattern>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>fields\(a\)</pattern>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>S8-fin|D-SEQ</pattern>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
</parameters>
</tool_call>

Now let me verify the T4 formal contract to confirm the gap.

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>T4.*Formal Contract|Valid address tumblers satisfy</pattern>
<file_path>vault/project-model/ASN-0034/formal-statements.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
<offset>80</offset>
<limit>60</limit>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
<offset>140</offset>
<limit>60</limit>
</parameters>
</tool_call>

Now let me check the ValidInsertionPosition formal contract precisely.

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>ValidInsertionPosition.*Formal Contract|Preconditions.*D-CTG.*D-MIN</pattern>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
<offset>190</offset>
<limit>40</limit>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>vault/project-model/ASN-0036/formal-statements.md</file_path>
<offset>165</offset>
<limit>30</limit>
</parameters>
</tool_call>

Now I have the full picture. Let me write the findings.

---

## Audit Findings

### S7b provides zeros(a) = 3 but S7 requires full T4 compliance for fields(a)

**Foundation**: T4 (FieldSeparatorConstraint) — its formal contract states an *axiom* defining valid address tumblers: `zeros(t) ≤ 3`, positive non-separator components, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`, non-empty fields. Postcondition (b) — `fields(t)` well-defined — holds for tumblers satisfying this axiom.

**ASN**: S7 proof, "Well-definedness" paragraph: "By S7b (element-level I-addresses), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`. By T4 (FieldSeparatorConstraint, ASN-0034), `zeros(a) = 3` means `a` contains exactly three zero-valued field separators, and `fields(a)` decomposes `a` into four fields." S7a's formal contract similarly cites S7b as the precondition "so that T4's `fields(a)` yields node, user, document, and element fields."

**Issue**: `zeros(a) = 3` is necessary but not sufficient for T4's `fields(a)` to be well-defined. T4's postcondition (b) is conditional on the full axiom. Counterexamples with `zeros = 3` that violate T4:
- `[0, 1, 0, 2, 0, 3, 4]` — leading zero, node field empty
- `[1, 0, 0, 2, 0, 3, 4]` — adjacent zeros, user field empty
- `[1, 0, 2, 0, 3, 0]` — trailing zero, element field empty

For these tumblers, `fields(t)` is ill-defined. The allocation mechanism (S7a + T10a + TA5) produces only T4-compliant addresses, so the gap cannot be exploited operationally, but the formal chain from S7b to T4's postcondition jumps over the full axiom. The same gap propagates to S7a's formal contract, which uses `fields(a)` in its own axiom statement.

**What needs resolving**: Either strengthen S7b to assert full T4 compliance for `dom(C)` — making `zeros(a) = 3` a corollary rather than the axiom — or introduce a separate property establishing `(A a ∈ dom(Σ.C) :: a satisfies T4's valid-address axiom)` and cite it as a precondition in S7 and S7a.

---

### ValidInsertionPosition formal contract omits S8-fin and D-SEQ

**Foundation**: S8-fin (Finite arrangement) — `dom(M(d))` is finite. D-SEQ (Sequential positions) — requires S8-fin, D-CTG, D-CTG-depth, D-MIN, S8-depth, T1.

**ASN**: ValidInsertionPosition formal contract: "Preconditions: d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1 (subspace identifier); if V_S(d) ≠ ∅, common V-position depth m ≥ 2." But the definition body uses `|V_S(d)| = N` as a finite natural number (requiring S8-fin for N to be well-defined) and explicitly cites D-SEQ: "v₀ is the minimum (D-MIN) and v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1 (D-SEQ)." The postcondition "exactly N + 1 valid insertion positions" also requires N finite.

**Issue**: S8-fin is listed as a precondition in every other property that uses finiteness of `dom(M(d))` (S8, D-CTG-depth, D-SEQ all list it). ValidInsertionPosition breaks this convention. D-SEQ is acknowledged in the body text but absent from the formal contract. An operation ASN relying solely on ValidInsertionPosition's formal contract to determine its proof obligations would not know to establish S8-fin or to derive D-SEQ's sequential characterization.

**What needs resolving**: Add S8-fin to the formal contract preconditions (since `|V_S(d)| = N` requires finiteness directly), and either list D-SEQ as a dependency or note that it is derived from the listed preconditions plus S8-fin.
