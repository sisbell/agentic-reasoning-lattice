## Review

I worked through every scenario independently, redoing all arithmetic from the constructive definitions and checking all preconditions.

### Part 1: Correctness

**Scenario 1.** All three comparisons verified directly: p<d by T1(ii) (proper prefix, 3<5 components), d<e₁ by T1(ii), e₁<e₂ by T1(i) at position 8 (1<5). T5 argument: any x between e₁ and e₂ with prefix divergence from q=[1,0,3,0,2,0,1] before position 8 would contradict one of the bounds. ✓

**Scenario 2.** x₁: positions 2-3 adjacent zeros → empty user field. x₂: leading zero → empty node field. x₃: trailing zero → empty doc field. x₄: zeros at positions 2,4,6,8 gives zeros(x₄)=4>3, also trailing zero at position 8. All four invalidity arguments are correct. v: zeros at positions 2,4,6 only, all field components strictly positive. ✓

**Scenario 3.** Operation A: a⊕w_deep copies positions 1-7 from a → [1,0,3,0,2,0,1]; position 8: 2+3=5. Result [1,0,3,0,2,0,1,5]. b⊕w_deep: position 8: 5+3=8. Result [1,0,3,0,2,0,1,8]. Compare position 8: 5<8 — strict. k=8=divergence(a,b)=8 satisfies TA1-strict. Operation B: a⊕w_shallow: k=1, position 1: 1+3=4, length=#w_shallow=1. Result [4]. Same for b. Equality. k=1<divergence(a,b)=8 — TA1-strict doesn't apply. Result-length identity: 8=8 and 1=1. ✓

**Scenario 4.** Ordinal round-trip: o=[2], w=[3]. o⊕w=[5]. [5]⊖[3]: diverge at position 1 (5≠3), result 5-3=2=[2]. Preconditions met (k=1=#o, #w=1, zero-prefix vacuous). ✓ Full-address round-trip: r=[1,0,3,0,2,0,1,5]. r⊖w_full: position 1: 1≠0, diverge at d=1. Result: position 1 gets 1-0=1, positions 2-8 copy from r → [1,0,3,0,2,0,1,5]=r≠a. Precondition failure: a₁=1≠0 violates zero-prefix condition. TA4 makes no claim. [3]⊖[3]: no divergence → zero tumbler [0]. [0]<[1,0,3,0,2,0,1,1] at position 1 (0<1). ✓

**Scenario 5.** inc(n=[1],2): #t'=1+2=3, positions 2→0, 3→1. u₁=[1,0,1]. inc(u₁,0): sig(u₁)=3, position 3: 1+1=2. u₂=[1,0,2]. inc(u₁,2): result [1,0,1,0,1]=d₁. inc(u₂,2): [1,0,2,0,1]=d₂. inc(d₁,2): [1,0,1,0,1,0,1], zeros=3. inc([1,0,1,0,1,0,1],2): would give zeros=4>3, blocked. T4 ceiling enforced. d₁<d₂: position 3: 1<2. T10: u₁,u₂ same length and differ at position 3 → non-nesting → all extensions distinct. ✓

**Scenario 6.** s⊕ℓ_valid: copy positions 1-7, position 8: 2+3=5. Result [1,0,3,0,2,0,1,5]. TA-strict: position 8 5>2. ℓ_deep: action point k=9>#s=8 → TA0 violated → undefined. ✓

**Scenario 7.** uₖ=[1,0,k] for any k — component at position 3 unbounded. tₙ=[1,1,...,1] length n+1 — length unbounded. TA5(c) and TA5(d) verified mechanically. ✓

**Scenario 8.** e_text₇=1, e_link₇=2. Position 7 is first divergence (positions 1-6 agree). 1<2 → e_text<e_link by T1(i). inc(e_text,0): sig=8 (position 8, value 3, is last nonzero). e_text'=[1,0,3,0,2,0,1,4]. Position 7 unchanged. ✓

**Scenario 9.** a₁=[1,0,1,0,1,0,1,1]. inc(a₁,0): sig=8, position 8: 1+1=2. a₂=[1,0,1,0,1,0,1,2]. a₃=[1,0,1,0,1,0,1,3]. A₁⊆A₂⊆A₃. T6(c): both a₁ and a₂ parse to node=[1], user=[1], doc=[1]. ✓

**Scenario 10, Sub-A.** a⊖w: positions 1-7 agree (both [1,0,3,0,2,0,1]), position 8: 2≠1, diverge at k=8. Result zeros 1-7, position 8: 2-1=1. [0,0,0,0,0,0,0,1]. b⊖w: position 8: 5-1=4. [0,0,0,0,0,0,0,4]. Compare position 8: 1<4 — strict. #a=#b=8 → TA3-strict applies. ✓

**Scenario 10, Sub-B.** a=[1,0,3,0,2], w=[1,0,3,0,1]. Diverge at k=5 (position 5: 2≠1). a⊖w: zeros 1-4, position 5: 2-1=1. [0,0,0,0,1] length 5. b⊖w: w zero-padded to length 8 = [1,0,3,0,1,0,0,0]. Diverge at k=5 (b₅=2≠w₅=1). Result: zeros 1-4, position 5: 1, positions 6-8 copy from b: 0,1,2. [0,0,0,0,1,0,1,2] length 8. [0,0,0,0,1] is proper prefix of [0,0,0,0,1,0,1,2] → a⊖w<b⊖w by T1(ii). #a=5≠#b=8 → TA3-strict inapplicable. ✓

**Scenario 11.** q=[1,0,3,0,2,1]: zeros at positions 2,4, zeros=2. Doc=[2,1], all components positive. s=[1,0,3,0,3,1]: zeros at positions 2,4, zeros=2. Doc=[3,1]. (p,q): [2] is proper prefix of [2,1] (position 1: 2=2, length 1<2). T6(d) confirmed. (p,r): position 1: 2≠3. Not a prefix. (p,s): position 1: 2≠3. Not a prefix. ✓

---

### Part 2: Coverage

Every property in the Properties Introduced table is exercised non-vacuously:

| Property | Scenario | Non-vacuous? |
|----------|----------|--------------|
| T0(a), T0(b) | S7 | Yes — concrete sequences uₖ and tₙ exceeding any bound |
| T1, T2 | S1 | Yes — comparisons terminate within min(#a,#b) pairs, no external lookup |
| T3 | S2, S8 | Yes — position-7 mismatch is sufficient for distinctness |
| T4 | S2, S5, S11 | Yes — valid case and three distinct failure modes |
| T5 | S1, S6 | Yes — bounded interval argument applied to specific endpoints |
| T6(a,b,c,d) | S5, S9, S11 | Yes — each sub-clause exercised with concrete field extraction |
| T7 | S8 | Yes — subspace identifiers 1 vs 2 produce permanently distinct addresses |
| T8 | S9 | Yes — ghost element after content deletion, address persists in A₃ |
| T9 | S5, S9 | Yes — a₁<a₂<a₃ within single allocator stream |
| T10, T10a | S5 | Yes — u₁ and u₂ non-nesting by equal length + position-3 divergence |
| T12 | S6 | Yes — well-formed vs. ill-formed span at the action-point boundary |
| TA0 | S3, S4, S6 | Yes — precondition checked and violated case shown |
| TA1 (weak) | S3-B | Yes — equality satisfies ≤, showing maximum degeneration |
| TA1-strict | S3-A | Yes — k=divergence(a,b) produces strict inequality |
| TA-strict | S3, S6 | Yes — position 8 increases strictly in both cases |
| TA2 | S4, S10 | Yes — a≥w confirmed before each subtraction |
| TA3 (weak) | S10-B | Yes — prefix-related operands, result by T1(ii) |
| TA3-strict | S10-A | Yes — same-length operands, strict inequality at divergence point |
| TA4 | S4 | Yes — ordinal case satisfies all three preconditions, round-trip holds; full-address case fails precondition concretely |
| TA5 | S5, S7, S8, S9 | Yes — k=0 and k>0 cases, T4-preservation boundary, sig computation |
| TA6 | S4 | Yes — [3]⊖[3]=[0], ordering [0]<positive tumbler by T1(i) |
| TA7a | S4 | Yes — ordinal [2]→[5]→[2] stays within text subspace, identifier N=1 held as context |

```
VERDICT: CONVERGED
```