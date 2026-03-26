### [REVIEW-25] [FOUND] TA0
Looking at this more carefully, I see that the "Property Section" contains both the statement and its justification paragraph. Let me evaluate this as the proof.

The property states: Given `a, w ∈ T` where `w > 0` and `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The justification paragraph explains **why the precondition is needed** — it describes the constructive definition (copy `a₁, ..., aₖ₋₁`, add `wₖ` to `aₖ`) and why `k > #a` would be undefined. But it does **not** establish the postcondition.

```
RESULT: FOUND

**Problem**: The proof explains why the precondition `k ≤ #a` is necessary but never establishes that the result `a ⊕ w` is actually a well-defined tumbler in `T`. Specifically, it does not show:

1. **Component well-formedness**: That each component of the result is a positive rational (or satisfies whatever membership condition `T` requires). The operation adds `wₖ` to `aₖ` — the proof must show `aₖ + wₖ` remains a valid tumbler component (e.g., positive). It must also show that appending the tail components `wₖ₊₁, ..., w_{#w}` (if any exist beyond position `k`) yields valid components.

2. **Result structure**: The constructive definition produces `(a₁, ..., aₖ₋₁, aₖ + wₖ, wₖ₊₁, ..., w_{#w})`. The proof does not verify this is a valid tumbler — e.g., that it has at least one component, that all components are positive, or that trailing zeros are handled correctly.

3. **Positivity of the sum**: Since `w > 0`, we know `wₖ > 0` (the action-point component is the first nonzero component). Combined with `aₖ > 0` (since `a ∈ T`), this gives `aₖ + wₖ > 0`. This step is straightforward but must be stated.

The second paragraph is an explanation of the precondition's motivation, not a proof of well-definedness.

**Required**: A constructive proof that shows the output `(a₁, ..., aₖ₋₁, aₖ + wₖ, wₖ₊₁, ..., w_{#w})` satisfies the membership conditions of `T`. This requires: (a) each copied prefix component `aᵢ` for `i < k` is positive (inherited from `a ∈ T`); (b) the sum `aₖ + wₖ` is positive (both summands are positive); (c) any appended tail components `wⱼ` for `j > k` are positive (inherited from `w ∈ T` and `j > k` meaning these are past the action point, so their positivity needs justification from the tumbler definition); (d) the result has finite length. If `T` has additional structural invariants, those must be checked too.
```

### [REVIEW-26] [VERIFIED] TA0

### [REVIEW-26] [RESOLVED] TA0

### [REVIEW-26] [VERIFIED] T3

### [REVIEW-26] [VERIFIED] TA1

### [REVIEW-26] [VERIFIED] T1

### [REVIEW-26] [VERIFIED] Divergence

### [REVIEW-26] [VERIFIED] TA4

### [REVIEW-26] [VERIFIED] TumblerAdd

### [REVIEW-26] [VERIFIED] TA1-strict

### [REVIEW-26] [FOUND] TA3
Now I have the full picture. Let me verify the TA3 proof.

**TA3 Claim**: `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`

**Proof text**: "Immediate from TA2: `a ⊖ w < b ⊖ w` implies `a ⊖ w ≤ b ⊖ w`, since `<` ⊂ `≤`."

**Verification:**

1. **Precondition completeness** — TA3's preconditions (`a < b ∧ a ≥ w ∧ b ≥ w`) exactly match TA2's preconditions. ✓

2. **Case coverage** — The precondition is `a < b` (strict), so only the strict-inequality case arises. No need for a separate `a = b` case. ✓

3. **Postcondition establishment** — TA2 gives `a ⊖ w < b ⊖ w`; weakening `<` to `≤` is elementary. ✓

4. **All conjuncts addressed** — Single conclusion, addressed. ✓

5. **Dependency correctness** — The proof cites TA2 and uses it correctly. However, the appeal to TA2 is only valid if `a ⊖ w` and `b ⊖ w` are well-formed tumblers (otherwise the `<` comparison is undefined). Well-formedness of these differences follows from **TA0** (tumbler subtraction closure) applied to the preconditions `a ≥ w` and `b ≥ w`. TA0 is not cited.

---

```
RESULT: FOUND

**Problem**: The proof invokes TA2 to obtain `a ⊖ w < b ⊖ w`, but this comparison presupposes that both differences are well-formed tumblers. That guarantee comes from TA0 (tumbler subtraction closure), which is used but not declared as a dependency. Without TA0, the expressions `a ⊖ w` and `b ⊖ w` are not known to be valid tumblers, and the ordering relation `<` between them is undefined.

**Required**: Cite TA0 as a dependency and add a sentence noting that TA0 + the preconditions `a ≥ w` and `b ≥ w` guarantee `a ⊖ w` and `b ⊖ w` are well-formed, making the appeal to TA2 legitimate.
```

### [REVIEW-27] [VERIFIED] TA3

### [REVIEW-27] [RESOLVED] TA3

### [REVIEW-27] [VERIFIED] TumblerSub

### [REVIEW-27] [VERIFIED] D1

### [REVIEW-27] [VERIFIED] D0

### [REVIEW-27] [VERIFIED] TA-LC

### [REVIEW-27] [VERIFIED] D2

### [REVIEW-27] [VERIFIED] T10a

### [REVIEW-27] [VERIFIED] T4

### [REVIEW-27] [VERIFIED] TA5

### [REVIEW-27] [VERIFIED] T10

### [REVIEW-27] [FOUND] T8
I've searched the entire repository and cannot find any proof text for T8 in the codebase — the label doesn't appear in any proof file or formal-statements file.

Looking at what you've provided: the "Monotonic allocation" section is not a proof of T8. It **assumes** T8 ("T8 tells us that addresses, once allocated, are permanent") and then pivots to a different question ("in what order are new addresses assigned?"). The property is restated as a premise, not established by argument.

```
RESULT: FOUND

**Problem**: No proof exists for T8. The "Monotonic allocation" section assumes T8 
rather than proving it. The text "T8 tells us that addresses, once allocated, are 
permanent. We now ask: in what order are new addresses assigned?" treats the property 
as given and transitions to discussing allocation order — it does not establish the 
claim that no operation removes an allocated address.

**Required**: Either (a) declare T8 as an axiom/design requirement that holds by 
construction (e.g., by showing the system's state transition functions only add to 
the allocated set, never remove), or (b) provide an inductive proof over all 
operations that mutate allocation state, showing each preserves the invariant 
`allocated(s) ⊆ allocated(s')` for any successor state s'. This would require 
listing the operations as dependencies and checking each one individually.
```

### [REVIEW-28] [VERIFIED] T8

### [REVIEW-28] [RESOLVED] T8

### [REVIEW-28] [VERIFIED] T9

### [REVIEW-28] [VERIFIED] GlobalUniqueness

### [REVIEW-28] [VERIFIED] OrdinalDisplacement

### [REVIEW-28] [VERIFIED] OrdinalShift

### [REVIEW-28] [VERIFIED] T5

### [REVIEW-28] [VERIFIED] PrefixOrderingExtension

### [REVIEW-28] [VERIFIED] PartitionMonotonicity

### [REVIEW-28] [VERIFIED] PositiveTumbler

### [REVIEW-28] [VERIFIED] TA3-strict

### [REVIEW-28] [VERIFIED] ReverseInverse

### [REVIEW-28] [VERIFIED] T0(a)

### [REVIEW-28] [VERIFIED] T0(b)

### [REVIEW-28] [VERIFIED] TA-strict

### [REVIEW-28] [VERIFIED] T12

### [REVIEW-28] [FOUND] T2
I need to find and read the actual proof for T2 before I can verify it. Let me locate it.

<tool_call>
{"name": "Grep", "arguments": {"pattern": "T2.*[Ii]ntrinsic", "path": "/Users/shane/Documents/github/claude/xanadu-spec/vault/5-proofs", "include": "*.md"}}
</tool_call>
<tool_call>
{"name": "Glob", "arguments": {"pattern": "vault/5-proofs/**/tumbler*"}}
</tool_call>

<tool_call>
{"name": "Glob", "arguments": {"pattern": "vault/5-proofs/**/*034*"}}
</tool_call>

<tool_call>
{"name": "Grep", "arguments": {"pattern": "## T2", "path": "/Users/shane/Documents/github/claude/xanadu-spec/vault/5-proofs", "include": "*.md"}}
</tool_call>

<tool_call>
{"name": "Glob", "arguments": {"pattern": "vault/5-proofs/**/*.md"}}
</tool_call>

### [REVIEW-29] [VERIFIED] T2

### [REVIEW-29] [RESOLVED] T2

### [REVIEW-29] [VERIFIED] T6

### [REVIEW-29] [FOUND] T7
Now I have the full T7 proof. Let me verify it carefully.

The proof splits into two cases based on whether `pₐ = pᵦ` (position of the first element-field component in each tumbler).

**Case 1** (`pₐ = pᵦ`): Straightforward — the tumblers differ at position `pₐ` because `Eₐ₁ ≠ Eᵦ₁`, so `a ≠ b` by T3. Sound.

**Case 2** (`pₐ ≠ pᵦ`): This is where the problem lies.

The proof's Case 2(ii) claims that when position `pₐ` in `b` is a field component (not a separator), then `b[pₐ − 1] > 0`. The parenthetical argues this by saying: "if `b[pₐ − 1]` were a separator, then `pₐ` would be the start of a field in `b`, but `pₐ < pᵦ` means `pₐ` is not the start of `b`'s element field, and the only field that starts after the third separator is the element field."

This reasoning fails to rule out `b[pₐ − 1]` being b's **first or second** separator. The parenthetical only addresses the third separator (element field start), but `pₐ` could be the start of b's user or document field.

**Concrete counterexample to the intermediate claim:**

```
a = [1, 0, 1, 0, 1, 0, 1, 2, 3, 4, 5]   (α=1, β=1, γ=1, δ=5)
    zeros at positions 2, 4, 6.  pₐ = 7.  Eₐ₁ = 1.

b = [1, 2, 3, 4, 5, 0, 1, 0, 1, 0, 2]   (α'=5, β'=1, γ'=1, δ'=1)
    zeros at positions 6, 8, 10. pᵦ = 11. Eᵦ₁ = 2.
```

Here `pₐ = 7 < 11 = pᵦ`. Position 7 in `b` is `b[7] = 1` (user field component), so we are in Case 2(ii). The proof claims `b[pₐ − 1] = b[6] > 0`, but `b[6] = 0` — it is b's **first** separator. Both `a[6] = 0` and `b[6] = 0`, so the proof's argument that they differ at position `pₐ − 1` fails.

(The tumblers are still distinct — they differ at position 2 where `a[2] = 0` and `b[2] = 2` — but the proof's stated reasoning doesn't establish this.)

```
RESULT: FOUND

**Problem**: Case 2(ii) incorrectly claims `b[pₐ − 1] > 0`. The parenthetical only rules out `b[pₐ − 1]` being the third separator (which would make `pₐ = pᵦ`), but `b[pₐ − 1]` can be b's first or second separator. Counterexample: `a = [1,0,1,0,1,0,1,2,3,4,5]` and `b = [1,2,3,4,5,0,1,0,1,0,2]` — both have `a[6] = 0 = b[6]`, defeating the argument at position `pₐ − 1 = 6`.

**Required**: Replace the Case 2(ii) argument. A correct approach: if `pₐ ≠ pᵦ`, the three zero-position sets of `a` and `b` cannot all agree (equal zero positions at `α+1, α+β+2, α+β+γ+3` would force `α=α', β=β', γ=γ'`, hence `pₐ = pᵦ`, contradicting the case hypothesis). Therefore there exists a position where one tumbler has a separator (0) and the other has a field component (> 0, by T4's positive-component constraint), giving `a ≠ b` by T3.
```

### [REVIEW-30] [VERIFIED] T7

### [REVIEW-30] [RESOLVED] T7

### [REVIEW-30] [VERIFIED] TA-MTO

### [REVIEW-30] [VERIFIED] TA-RC

### [REVIEW-30] [VERIFIED] TA-assoc

### [REVIEW-30] [FOUND] TA2
Let me find and read the proof for TA2.

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>TA2</pattern>
<path>/Users/shane/Documents/github/claude/xanadu-spec/vault/5-proofs</path>
<include>*.md</include>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>TA2</pattern>
<path>/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model</path>
<include>*.md</include>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>Well-defined subtraction</pattern>
<path>/Users/shane/Documents/github/claude/xanadu-spec/vault</path>
<include>*.md</include>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>/Users/shane/Documents/github/claude/xanadu-spec/vault/5-proofs/**/tumbler*</pattern>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>/Users/shane/Documents/github/claude/xanadu-spec/vault/5-proofs/**/*</pattern>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>TA2</pattern>
<path>/Users/shane/Documents/github/claude/xanadu-spec/vault</path>
<include>*.md</include>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>TA2</pattern>
<path>/Users/shane/Documents/github/claude/xanadu-spec</path>
<include>*.md</include>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>/Users/shane/Documents/github/claude/xanadu-spec/vault/5-proofs/**/*.md</pattern>
</parameters>
</tool_call>

### [REVIEW-31] [VERIFIED] TA2

### [REVIEW-31] [RESOLVED] TA2

### [REVIEW-31] [FOUND] TA6
TA6 had no formal proof. The informal paragraph before the statement sketched the ordering argument without citing T1 or splitting into cases, and never addressed the validity conjunct (which derives from T4).

### [REVIEW-32] [VERIFIED] TA6

### [REVIEW-32] [RESOLVED] TA6

### [REVIEW-32] [VERIFIED] TA6

### [REVIEW-32] [RESOLVED] TA6

### [REVIEW-32] [VERIFIED] TA7a

### [REVIEW-32] [VERIFIED] TS1

### [REVIEW-32] [VERIFIED] TS2

### [REVIEW-32] [VERIFIED] TS3

### [REVIEW-32] [VERIFIED] TS4

### [REVIEW-32] [VERIFIED] TS5
