# Worked Examples — ASN-0034 Tumbler Algebra

## Scenario 1: Total order at the prefix boundary

**Setup.** Four tumblers in hierarchical nesting order, all within server 1 / user 3 / document 2:
- p  = [1, 0, 3] — user address (zeros=1)
- d  = [1, 0, 3, 0, 2] — document address (zeros=2)
- e₁ = [1, 0, 3, 0, 2, 0, 1, 1] — element address, text subspace, ordinal 1 (zeros=3)
- e₂ = [1, 0, 3, 0, 2, 0, 1, 5] — element address, text subspace, ordinal 5 (zeros=3)

**Operation.** Order all four by T1.

**Result.** p < d < e₁ < e₂.

**Properties exercised.**
- T1 case (ii): p < d — p is a proper prefix of d (#p=3 < #d=5, positions 1–3 agree) ✓
- T1 case (ii): d < e₁ — d is a proper prefix of e₁ (#d=5 < #e₁=8, positions 1–5 agree) ✓
- T1 case (i): e₁ < e₂ — divergence at position 8: e₁₈=1 < e₂₈=5; positions 1–7 agree ✓
- T2: each comparison reads at most min(#a,#b) component pairs; no external state consulted ✓
- T5: prefix q=[1,0,3,0,2,0,1]; any x with e₁ ≤ x ≤ e₂ must extend q — if x diverged from q at position k ≤ 7, then xₖ < qₖ would violate e₁ ≤ x or xₖ > qₖ would violate x ≤ e₂ ✓

---

## Scenario 2: T4 — Valid address and boundary violations

**Setup.** Five candidate tumblers:
- v  = [1, 0, 3, 0, 2, 0, 1, 5] — proposed element address
- x₁ = [1, 0, 0, 3] — zeros at positions 2 and 3 (adjacent)
- x₂ = [0, 1, 0, 3] — zero at position 1 (leading)
- x₃ = [1, 0, 3, 0] — zero at position 4 (trailing)
- x₄ = [1, 0, 3, 0, 2, 0, 1, 0] — zero at position 8

**Operation.** Apply T4 to classify each.

**Result.**
- v: valid. zeros(v)=3 → element address. Node=[1], User=[3], Doc=[2], Element=[1,5]. All field components strictly positive; no leading, trailing, or adjacent zeros. ✓
- x₁: invalid. zeros=2 but positions 2–3 adjacent. Parse: Node=[1] | empty User | Doc=[3]. User field empty (β=0 violates β≥1). ✗
- x₂: invalid. Position 1 is zero (leading zero). Node field empty (α=0 violates α≥1). ✗
- x₃: invalid. Trailing zero at position 4. After the separator at position 2, User=[3], and position 4 is a trailing zero — Doc field would be empty (γ=0 violates γ≥1 when present). ✗
- x₄: invalid. zeros(x₄) = 4 (positions 2, 4, 6, 8 are all zero) > 3 permitted — directly violates T4's at-most-three-zero-separators constraint. Under T4, all zeros are separators and field components are strictly positive; x₄ thus encodes four field separators, exceeding the three allowed by the four-field model. ✗

**Properties exercised.**
- T4 (valid case): v satisfies all conditions — zeros count=3, no adjacent/leading/trailing zeros, all field components positive ✓
- T4 (at-most-three-zeros): x₄ has zeros(x₄)=4 > 3 — the zero count alone determines invalidity here; x₄ encodes four separators which the four-field model cannot accommodate ✓
- T4 (structural conditions ↔ non-empty fields): x₁ shows adjacent zeros create an empty intermediate field without a leading zero; x₂, x₃ show the leading-zero and trailing-zero failure modes ✓
- T3: all five are distinct canonical tumblers; T4 invalidity is a semantic constraint on valid addresses, not a violation of canonical representation ✓

---

## Scenario 3: TA1 — Boundary between strict and weak order preservation under addition

**Setup.**
- a = [1, 0, 3, 0, 2, 0, 1, 2] (#a=8)
- b = [1, 0, 3, 0, 2, 0, 1, 5] (#b=8)
- divergence(a, b) = 8 (positions 1–7 agree; a₈=2, b₈=5, case (i) of T1)
- w_deep    = [0, 0, 0, 0, 0, 0, 0, 3] — action point k=8
- w_shallow = [3] — action point k=1

Ordering: a < b by T1 case (i).

**Operation A: w_deep, k=8 = divergence(a, b).**
- a ⊕ w_deep: copy positions 1–7 from a → [1,0,3,0,2,0,1]; position 8: 2+3=5. Result: [1,0,3,0,2,0,1,5].
- b ⊕ w_deep: copy positions 1–7 from b → [1,0,3,0,2,0,1]; position 8: 5+3=8. Result: [1,0,3,0,2,0,1,8].
- Divergence at position 8: 5 < 8. **Strict inequality** a⊕w_deep < b⊕w_deep.

**Operation B: w_shallow, k=1 < divergence(a, b)=8.**
- a ⊕ w_shallow: position 1: 1+3=4; result length = #w_shallow = 1. Result: [4].
- b ⊕ w_shallow: position 1: 1+3=4. Result: [4].
- **Equality** a⊕w_shallow = b⊕w_shallow = [4].

**Properties exercised.**
- TA0: k=8 ≤ min(#a,#b)=8 ✓ and k=1 ≤ min(#a,#b)=8 ✓ — both operations well-defined ✓
- TA-strict: [1,0,3,0,2,0,1,5] > a (position 8: 5>2) ✓; [4] > a (position 1: 4>1) ✓
- TA1 (weak): [4] ≤ [4] — equality satisfies the weak claim ✓
- TA1-strict: k=8 ≥ divergence(a,b)=8 → strict inequality holds in Operation A ✓
- TA1-strict (negative): k=1 < divergence(a,b)=8 → strict claim not guaranteed; equality observed ✓
- Result-length identity: #(a⊕w_deep)=8=#w_deep ✓; #(a⊕w_shallow)=1=#w_shallow ✓
- Tail replacement: w_shallow (k=1) overwrites everything from position 1 onward — the divergence at position 8 is erased; neither result carries any information about the original ordinal difference ✓

---

## Scenario 4: TA4 — Partial inverse at the precondition boundary

**Setup.**
- Ordinal: o = [2], w = [3] (action point k=1, text subspace, structural context N=1)
- Full address: a = [1, 0, 3, 0, 2, 0, 1, 2], w_full = [0,0,0,0,0,0,0,3] (action point k=8)

**Ordinal round-trip.**
- o ⊕ w = [2+3] = [5]. Preconditions: k=1=#o ✓; #w=1=k ✓; zero-prefix (no positions i with 1≤i<1): vacuous ✓.
- [5] ⊖ [3]: divergence at position 1 (5≠3). Result: [5−3] = [2] = o. **Round-trip succeeds.** ✓

**Full-address round-trip.**
- a ⊕ w_full: positions 1–7 copy from a; position 8: 2+3=5. r = [1,0,3,0,2,0,1,5].
- r ⊖ w_full: scan for divergence — position 1: r₁=1, (w_full)₁=0. Divergence at d=1. Result: position 1 gets 1−0=1; positions 2–8 copy from r. Result: [1,0,3,0,2,0,1,5] = r ≠ a. **Round-trip fails.** ✗

**TA4 precondition audit for the full-address case.**
- k=8, #a=8 ✓; #w_full=8 ✓
- Zero-prefix: ∀ i : 1≤i<8 : aᵢ=0? a₁=1≠0. **Violated.** ✗
- TA4 makes no claim. The subtraction finds divergence at d=1 (the node field), not at k=8; the node component 1−0=1 is reproduced unchanged, giving r back instead of a.

**TA6 ordering check.**
- If o=w (e.g. o=[3], w=[3]): o⊕w=[6], [6]⊖[3]=[3]=o ✓; but o⊖w=[3]⊖[3]=[0] — the zero-valued sentinel.
- Compare [0] with positive tumbler [1,0,3,0,2,0,1,1]: position 1: 0 < 1 → [0] < [1,0,3,0,2,0,1,1] by T1 case (i).
- General principle: any zero tumbler has 0 at every position; any positive tumbler has tₖ > 0 at some first k. T1 case (i) at that k gives zero tumbler < positive tumbler. This is what makes zero tumblers usable as strict lower bounds in span arithmetic.

**Properties exercised.**
- TA4: ordinal case — all preconditions met → round-trip holds ✓
- TA4 (precondition necessity): zero-prefix condition violated → no guarantee; round-trip concretely fails ✓
- TA2: r=[1,0,3,0,2,0,1,5] ≥ w_full=[0,0,0,0,0,0,0,3] (position 1: 1>0) → subtraction well-defined ✓
- TA7a: ordinal-only formulation is the correct representation for element-local shifts; N=1 (text subspace identifier) is structural context, not an operand — o=[2] after round-trip remains a length-1 ordinal within text subspace context ✓
- TA6 (sentinel): o⊖o=[0] — a zero-valued sentinel of length 1, not a valid address ✓
- TA6 (ordering): [0] < [1,0,3,0,2,0,1,1] by T1 case (i) at position 1 (0 < 1) — every zero tumbler is strictly less than every positive tumbler ✓

---

## Scenario 5: T10 + TA5 — Allocation streams, child-spawning, and partition independence

**Setup.** Node address n = [1] (zeros=0). We trace allocation of two user accounts and their documents.

**Operation 1: Node allocator spawns user accounts.**
- inc(n, 2): k=2, #n'=1+2=3. Position 2 ← 0, position 3 ← 1. u₁ = [1, 0, 1]. zeros=1. T4: Node=[1], User=[1]. ✓
- inc(u₁, 0): sig(u₁)=3 (last nonzero at position 3). Position 3: 1+1=2. u₂ = [1, 0, 2]. zeros=1. ✓

**Operation 2: Each user allocator spawns a document.**
- inc(u₁, 2): k=2, #u₁'=3+2=5. Position 4 ← 0, position 5 ← 1. d₁ = [1, 0, 1, 0, 1]. zeros=2. T4: Node=[1], User=[1], Doc=[1]. ✓
- inc(u₂, 2): k=2. d₂ = [1, 0, 2, 0, 1]. zeros=2. T4: Node=[1], User=[2], Doc=[1]. ✓

**Operation 3: Document allocator spawns an element; boundary violation.**
- inc(d₁, 2): k=2, result = [1, 0, 1, 0, 1, 0, 1]. zeros=3. T4: element address. ✓
- inc([1,0,1,0,1,0,1], 2): would produce [1,0,1,0,1,0,1,0,1]. zeros=4 > 3. T4 **violated** — four separators exceed the three-field-separator maximum. ✗

**Result.**
- Sibling order: u₁=[1,0,1] < u₂=[1,0,2] (position 3: 1<2). Neither is a prefix of the other (same length, differ at position 3). By the prefix ordering extension lemma, every extension of u₁ < every extension of u₂; so d₁=[1,0,1,0,1] < d₂=[1,0,2,0,1] ✓
- Partition independence: d₁ ≠ d₂. Allocators under u₁ and u₂ produce addresses with distinct prefixes diverging at position 3; by T10 they cannot coincide. ✓
- T4 enforces the ceiling at three separators; k=2 at zeros=3 would introduce a fourth, which the hierarchy disallows. ✓

**Properties exercised.**
- TA5(a): u₁=[1,0,1] > n=[1] (n is a proper prefix of u₁ → T1 case ii) ✓; u₂ > u₁ (position 3: 2>1 → T1 case i) ✓
- TA5(c): inc(u₁, 0) → #u₂=3=#u₁; differs only at sig(u₁)=3 ✓
- TA5(d): inc(n, 2) → #u₁=3=1+2; position 2=0, position 3=1 ✓
- TA5 T4 preservation: k=2 valid when zeros(t)≤2 — n: 0≤2 ✓; u₁: 1≤2 ✓; d₁: 2≤2 ✓; [1,0,1,0,1,0,1]: 3>2 → blocked ✓
- T10: u₁ and u₂ are non-nesting (same length 3, differ at position 3) → all u₁-outputs ≠ all u₂-outputs ✓
- T10a: node allocator uses inc(·,0) for sibling accounts (u₁→u₂), inc(·,2) for child-spawning ✓
- T9: within u₁'s document stream — inc(u₁,2)=d₁=[1,0,1,0,1]; inc(d₁,0)=[1,0,1,0,2] > d₁ — strictly monotone ✓
- T6(a): d₁ and d₂ share node field [1] ✓; T6(b): d₁ user=[1], d₂ user=[2] — same node, different account, decidable from addresses alone ✓

---

## Scenario 6: T12 — Span well-formedness at the action-point boundary

**Setup.**
- s = [1, 0, 3, 0, 2, 0, 1, 2] (#s=8)
- ℓ_valid = [0,0,0,0,0,0,0,3] — action point k=8
- ℓ_deep  = [0,0,0,0,0,0,0,0,3] — action point k=9

**Operation A: Well-formed span.**
- s ⊕ ℓ_valid: positions 1–7 copy from s → [1,0,3,0,2,0,1]; position 8: 2+3=5. Result: [1,0,3,0,2,0,1,5].
- Span: {t ∈ T : [1,0,3,0,2,0,1,2] ≤ t < [1,0,3,0,2,0,1,5]}. Non-empty — contains s itself.

**Operation B: Malformed span.**
- ℓ_deep has action point k=9 > #s=8. TA0 precondition k ≤ #s fails. s ⊕ ℓ_deep is **undefined**. Span ill-formed.

**Result.**
- (s, ℓ_valid): well-formed span over text-subspace ordinals 2 through 4 within document [1,0,3,0,2].
- (s, ℓ_deep): ill-formed — a displacement with 8 leading zeros requires 8 "levels of stay" but position 9 does not exist in s.

**Properties exercised.**
- T12: ℓ_valid > 0 ✓ and k=8 ≤ #s=8 ✓ → well-formed. ℓ_deep: k=9 > #s=8 → ill-formed ✓
- TA0: k ≤ #a is a hard precondition; violations make the span endpoint undefined, not merely ill-typed ✓
- TA-strict: s⊕ℓ_valid=[1,0,3,0,2,0,1,5] > s (position 8: 5>2) → span non-empty ✓
- T5: all t with s ≤ t < s⊕ℓ_valid share prefix [1,0,3,0,2,0,1] — the span stays within the text subspace of document 2 ✓

---

## Scenario 7: T0 — Unbounded component values and unlimited depth

**Setup.** Node address n=[1] (zeros=0). User address u₁=[1,0,1] (zeros=1).

**Operation A: T0(a) — Unbounded component values within a single level.**

Starting from u₁=[1,0,1], apply inc(·,0) repeatedly. sig(uₖ)=3 for all k (last nonzero at position 3):
- u₁ = [1,0,1]: user component = 1
- u₂ = inc(u₁,0) = [1,0,2]: user component = 2
- u₃ = [1,0,3], u₄ = [1,0,4], u₅ = [1,0,5]
- uₖ = [1,0,k]: user component = k, for any k ≥ 1.

For any bound M, uₘ₊₁=[1,0,M+1] has user-field component M+1 > M. The user field at position 3 is inexhaustible. No ceiling.

**Operation B: T0(b) — Unlimited nesting depth within a single field.**

Starting from t₀=[1] (#t₀=1), apply inc(·,1) (within-field child) repeatedly:
- t₁ = inc([1],1): #t₁=2, append [1]. Result [1,1].
- t₂ = inc([1,1],1): #t₂=3. Result [1,1,1].
- t₃=[1,1,1,1], t₄=[1,1,1,1,1], t₅=[1,1,1,1,1,1].
- tₙ = [1,1,...,1] (n+1 ones), #tₙ = n+1.

For any bound n, tₙ has length n+1 ≥ n. Tumblers of arbitrary length exist. All are node-level addresses (zeros=0) demonstrating unlimited within-field nesting.

**Result.**
- T0(a): uₖ=[1,0,k] — the user-field component at position 3 grows to k for any k; siblings within one level are inexhaustible.
- T0(b): tₙ has length n+1 — nesting depth within a field is unlimited; levels themselves are inexhaustible.

These are distinct guarantees: T0(a) ensures unlimited siblings at one level; T0(b) ensures unlimited nesting depth. Gregory's implementation violates both: the 32-bit user-field component overflows silently after 2³²−1 users; the 16-slot depth limit caused fatal crashes when version chains exceeded it (the NPLACES comment records a bump from 11 to 16 to defer the failure).

**Properties exercised.**
- T0(a): uₘ₊₁=[1,0,M+1] has component M+1 > M at position 3 for any M ✓
- T0(b): tₙ has length n+1 ≥ n for any n ✓
- TA5(c): each inc(u,0) preserves length (#uₖ=3) and increments only position sig(u)=3 ✓
- TA5(d): each inc(t,1) adds one component (#tₙ₊₁=#tₙ+1), new position set to 1 ✓

---

## Scenario 8: T7 — Subspace disjointness and its ordering consequence

**Setup.** Document d=[1,0,3,0,2]. Two element addresses within the same document:
- e_text = [1,0,3,0,2,0,**1**,3] — text element, subspace identifier 1, ordinal 3
- e_link = [1,0,3,0,2,0,**2**,1] — link element, subspace identifier 2, ordinal 1

Both have zeros=3 (element addresses). T4: e_text element field=[1,3] ✓; e_link element field=[2,1] ✓. All field components strictly positive.

**Step 1: T3 — canonical distinctness.**

Compare position by position: positions 1–6 both give [1,0,3,0,2,0] — agree. Position 7: e_text₇=1, e_link₇=2 — differ. By T3 (canonical representation): a single position mismatch is sufficient. **e_text ≠ e_link.**

**Step 2: T1 — ordering consequence.**

Position 7 is the first divergence; 1 < 2 → e_text < e_link by T1 case (i). This is a consequence of the lexicographic order, not a separate assumption: every text address in document [1,0,3,0,2] has value 1 at position 7; every link address has value ≥ 2 at position 7; T1 case (i) at position 7 places all text addresses before all link addresses within the same document.

**Step 3: T7 — permanent disjointness.**

Apply inc(e_text, 0): sig(e_text)=8; e_text' = [1,0,3,0,2,0,1,4]. Position 7 remains 1. Any sequence of inc(·,0) increments within the text subspace changes only position 8 onward — position 7 (the subspace identifier) is never touched. By T7 (corollary of T3+T4): since e_text.E₁=1 ≠ 2=e_link.E₁, the addresses are permanently in disjoint subspaces. Arithmetic within subspace 1 cannot produce an address in subspace 2.

**Result.**
- e_text ≠ e_link (T3, position-7 mismatch).
- e_text < e_link (T1 case i, 1 < 2 at position 7).
- e_text' = [1,0,3,0,2,0,1,4] remains in subspace 1; subspace identifier is invariant under element-local arithmetic.

**Properties exercised.**
- T3: position-7 disagreement → e_text ≠ e_link ✓
- T1 case (i): 1 < 2 at position 7 → e_text < e_link; all subspace-1 addresses precede all subspace-2 addresses within the same document ✓
- T7: E₁ values differ → permanently disjoint subspaces; arithmetic within one subspace cannot produce addresses in another ✓
- TA5(c): inc(e_text, 0) differs from e_text only at sig(e_text) = 8; position 7 (the subspace identifier) is unchanged, confirming that allocation increments within a subspace do not cross subspace boundaries ✓

---

## Scenario 9: T8 — Allocation permanence and monotone growth

**Setup.** Element allocator for document [1,0,1,0,1], text subspace. Starting address: a₁=[1,0,1,0,1,0,1,1] (zeros=3, element address, subspace 1, ordinal 1). We track the allocated set A through three allocation events.

**State at t₁:** Allocate a₁.
- A₁ = {a₁} = {[1,0,1,0,1,0,1,1]}.

**State at t₂:** Allocate a₂ = inc(a₁, 0).
- sig(a₁)=8; a₂₈=1+1=2. a₂=[1,0,1,0,1,0,1,2].
- A₂ = {a₁, a₂}. A₁ ⊆ A₂.

**State at t₃:** Allocate a₃ = inc(a₂, 0).
- a₃=[1,0,1,0,1,0,1,3].
- A₃ = {a₁, a₂, a₃}. A₂ ⊆ A₃.

**T8 check.** a₁ ∈ A₁ ⊆ A₂ ⊆ A₃. Even if content stored at a₁ is subsequently deleted — a₁ becomes a ghost element in Nelson's sense — a₁ remains permanently in the allocated set. No allocation or content operation removes it. The tumbler [1,0,1,0,1,0,1,1] irrevocably occupies its position on the tumbler line.

**Ghost element.** Suppose at t₃ the content at a₁ is deleted. The content mapping changes, but A₃ does not: a₁ ∈ A₃ still. a₁ occupies its position as a ghost — an allocated address with no stored content. T8 asserts that the address, not the content, is permanent.

**T6(c) — same document-lineage fields.** Parse a₁ and a₂ via fields(·): both yield node=[1], user=[1], doc=[1], with element fields [1,1] and [1,2] respectively. The node, user, and document fields are identical. T6(c) confirmed — a₁ and a₂ belong to the same document family, and this is computable from the addresses alone without consulting any index or version graph.

**Result.**
- A₁ ⊆ A₂ ⊆ A₃: monotone growth, no element ever removed.
- a₁ < a₂ < a₃ (position 8: 1<2<3): within-allocator ordering strictly monotone (T9).
- The content at a₁ may vanish; the address a₁ never does.

**Properties exercised.**
- T8: A₁ ⊆ A₂ ⊆ A₃ — monotone non-decreasing; a₁ not removable at any step ✓
- T9: a₁ < a₂ < a₃ — within-allocator strictly monotone, no gaps ✓
- TA5(a): each inc(·,0) produces a strictly greater address ✓
- TA5(c): #aᵢ=8 for all i — length preserved by inc(·,0) ✓
- T6(c): fields(a₁).node=[1]=fields(a₂).node, fields(a₁).user=[1]=fields(a₂).user, fields(a₁).doc=[1]=fields(a₂).doc — same document lineage, computable from addresses alone ✓

---

## Scenario 10: TA3 — Order preservation under subtraction

**Setup.** Two sub-scenarios illustrating the boundary between TA3-strict (equal-length) and TA3 weak (prefix-related operands).

**Sub-scenario A: Same length — TA3-strict.**
- a=[1,0,3,0,2,0,1,2], b=[1,0,3,0,2,0,1,5], w=[1,0,3,0,2,0,1,1].
- #a=#b=8. a<b (position 8: 2<5). a≥w (position 8: 2≥1). b≥w (position 8: 5≥1).

Compute a⊖w: scan for first divergence between [1,0,3,0,2,0,1,2] and [1,0,3,0,2,0,1,1].
- Positions 1–7: both give [1,0,3,0,2,0,1] — agree.
- Position 8: 2 vs 1 → diverge at k=8.
- r₁=...=r₇=0, r₈=2−1=1. Result: **[0,0,0,0,0,0,0,1]**.

Compute b⊖w: same scan, diverge at k=8 (b₈=5 vs w₈=1).
- r₈=5−1=4. Result: **[0,0,0,0,0,0,0,4]**.

Compare: position 8: 1 < 4 → **a⊖w < b⊖w** (strict). TA3-strict: #a=#b=8 → strict inequality guaranteed.

**Sub-scenario B: Prefix-related — TA3 weak only.**
- a=[1,0,3,0,2] (proper prefix of b=[1,0,3,0,2,0,1,2]), w=[1,0,3,0,1].
- #a=5, #b=8. a<b (T1 case ii: a is proper prefix of b). a≥w (position 5: 2≥1). b≥w (position 5: 2≥1, w zero-padded to [1,0,3,0,1,0,0,0]).

Compute a⊖w: scan [1,0,3,0,2] against [1,0,3,0,1].
- Positions 1–4: [1,0,3,0]=[1,0,3,0] — agree.
- Position 5: 2 vs 1 → diverge at k=5.
- r₁=r₂=r₃=r₄=0, r₅=2−1=1. Result: **[0,0,0,0,1]** (length 5).

Compute b⊖w: scan [1,0,3,0,2,0,1,2] against [1,0,3,0,1,0,0,0] (w zero-padded to length 8).
- Positions 1–4 agree; position 5: 2 vs 1 → diverge at k=5.
- r₁=r₂=r₃=r₄=0, r₅=2−1=1; positions 6–8 copy from b: 0,1,2. Result: **[0,0,0,0,1,0,1,2]** (length 8).

Compare: [0,0,0,0,1] is a proper prefix of [0,0,0,0,1,0,1,2] → **a⊖w < b⊖w** by T1 case (ii). Weak inequality satisfied.

TA3-strict does NOT apply: #a=5 ≠ #b=8. The equal-length precondition excludes prefix-related pairs, and this scenario shows concretely why: the strict inequality comes not from the subtracted values at the divergence point but from the length difference of the results — a structure-level inequality that TA3-strict is not designed to capture.

**Result.**
- Sub-scenario A: [0,0,0,0,0,0,0,1] < [0,0,0,0,0,0,0,4] (strict, same length).
- Sub-scenario B: [0,0,0,0,1] < [0,0,0,0,1,0,1,2] (weak, by prefix rule T1 case ii).

**Properties exercised.**
- TA3 (weak): both sub-scenarios satisfy a⊖w ≤ b⊖w ✓
- TA3-strict: Sub-scenario A (#a=#b=8) → strict; Sub-scenario B (#a≠#b) → strict form inapplicable — demonstrates why equal-length precondition exists ✓
- TA2: all four subtractions well-defined: a≥w and b≥w verified in both sub-scenarios ✓
- T1 case (ii): Sub-scenario B uses prefix rule for the result comparison ✓

---

## Scenario 11: T6(d) — Structural subordination within a document family

**Setup.** Server 1, user 3. Four document-level addresses with multi-component document fields:
- p = [1, 0, 3, 0, 2] — doc field [2], zeros=2
- q = [1, 0, 3, 0, 2, 1] — doc field [2, 1], zeros=2
- r = [1, 0, 3, 0, 3] — doc field [3], zeros=2
- s = [1, 0, 3, 0, 3, 1] — doc field [3, 1], zeros=2

T4 parse of q = [1,0,3,0,2,1]: zeros at positions 2 and 4 (zeros=2); Node=[1], User=[3], Doc=[2,1]. Components 2 and 1 of the doc field are strictly positive; no adjacent zeros, no leading/trailing zero. ✓

T4 parse of s = [1,0,3,0,3,1]: zeros at positions 2 and 4 (zeros=2); Node=[1], User=[3], Doc=[3,1]. Both doc-field components strictly positive. ✓

**Operation.** Apply T6(d) to three pairs: (p, q), (p, r), and (p, s).

**Result.**

*Pair (p, q):* fields(p).doc = [2]; fields(q).doc = [2, 1]. Prefix check: #[2]=1 < 2=#[2,1]; position 1: 2=2. [2] is a proper prefix of [2,1]. T6(d) **confirmed** — q (version 1) is structurally subordinate within p's document family. This reflects that version 2.1 was spawned from document 2 by the allocation hierarchy.

*Pair (p, r):* fields(p).doc = [2]; fields(r).doc = [3]. Prefix check: position 1: 2 ≠ 3. [2] is not a prefix of [3]. T6(d) **fails** — p and r are distinct documents (document 2 vs. document 3) with no subordination relationship.

*Pair (p, s):* fields(p).doc = [2]; fields(s).doc = [3, 1]. Prefix check: position 1: 2 ≠ 3. [2] is not a prefix of [3, 1]. T6(d) **fails** — s is version 1 of document 3, not of document 2. The mismatch at the base document component (2 ≠ 3) is sufficient to determine non-subordination regardless of s having a version suffix.

Note: T6(d) detects allocation ancestry (who baptised whom), not derivation history. Nelson: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Version q=2.1 was allocated under document 2, but the content of q may have been derived from any other source. Formal derivation history requires the version graph, not just the addresses.

**Properties exercised.**
- T4: p, q, r, s all parse correctly — doc-field components strictly positive, non-adjacent zeros, no leading/trailing zeros ✓
- T6(d): (p,q) → [2] ≼ [2,1] (proper prefix) → structural subordination confirmed; T4 parsing extracts both doc fields; prefix check is computable from addresses alone ✓
- T6(d) (negative, single-component): (p,r) → [2] ⋠ [3] (component mismatch at position 1) → no subordination ✓
- T6(d) (negative, multi-component): (p,s) → [2] ⋠ [3,1] (same mismatch at position 1 despite s having a version suffix) → no subordination ✓
- T6 decidability: all three determinations are made from addresses alone via T4 parsing; no version graph or external state is consulted ✓

---

## Coverage

| Property | Scenario | Vacuous? |
|----------|----------|----------|
| T0(a) | S7 | No |
| T0(b) | S7 | No |
| T1 | S1, S3, S5, S8, S10 | No |
| T2 | S1 | No |
| T3 | S2, S8 | No |
| T4 | S2, S5, S11 | No |
| T5 | S1, S6 | No |
| T6(a), T6(b) | S5 | No |
| T6(c) | S9 | No |
| T6(d) | S11 | No |
| T7 | S8 | No |
| T8 | S9 | No |
| T9 | S5, S9 | No |
| T10 | S5 | No |
| T10a | S5 | No |
| T12 | S6 | No |
| TA0 | S3, S4, S6 | No |
| TA1 (weak) | S3 operation B | No |
| TA1-strict | S3 operation A | No |
| TA-strict | S3, S6 | No |
| TA2 | S4, S10 | No |
| TA3 (weak) | S10 sub-B | No |
| TA3-strict | S10 sub-A | No |
| TA4 | S4 | No |
| TA5 | S5, S7, S8, S9 | No |
| TA6 | S4 | No |
| TA7a | S4 | No |

---

## Backlog

- **Global uniqueness Case 4 (parent/child length separation)**: Needs two simultaneous allocator streams — parent using inc(·,0) at length γ₁, child using inc(·,0) at length γ₁+k' — to concretely exhibit that no output of the parent can equal any output of the child. Depends on S5's groundwork; requires extending S5 to track two generations simultaneously, verifying that the length separation γ₁ < γ₁+k' accounts for all four uniqueness cases in the global uniqueness theorem.