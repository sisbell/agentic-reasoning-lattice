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
