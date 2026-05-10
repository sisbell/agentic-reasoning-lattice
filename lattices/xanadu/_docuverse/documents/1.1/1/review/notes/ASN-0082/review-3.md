# Review of ASN-0082

## REVISE

### Issue 1: Region disjointness not derived
**ASN-0082, Post-Insertion Shift**: I3, I3-L, I3-X, and I3-D jointly assign values to positions in M'(d).

**Problem**: For M'(d) to be a well-defined partial function, the positions covered by these four assignments must be pairwise disjoint — no position can receive two conflicting values. The ASN does not verify this. The argument is short but load-bearing:

- *Shifted vs left*: For v ≥ p in subspace S, shift(v, n) > v ≥ p by TS4, so shift(v, n) > p > u for every u < p. No collision with I3-L positions.
- *Shifted vs shifted*: TS2 (injectivity) guarantees distinct v's produce distinct shift(v, n)'s.
- *Shifted vs cross-subspace*: Subspace preservation (shift(v, n)₁ = v₁ = S when m ≥ 2) ensures shifted positions remain in subspace S, disjoint from I3-X positions (subspace ≠ S).

This is a three-line derivation, but without it the reader cannot verify that the postconditions are jointly satisfiable.

**Required**: Add a consistency paragraph deriving pairwise disjointness of the four assignment regions.

---

### Issue 2: Gap region unacknowledged
**ASN-0082, Post-Insertion Shift**: I3 and the frame conditions partition existing V-positions into four regions (left, shifted, cross-subspace, cross-document), but the *output* domain of M'(d) contains a region no postcondition addresses: positions in [p, shift(p, n)) within subspace S.

**Problem**: Position p itself is not covered by any condition (p is not < p for I3-L; shift(v, n) > p for all v ≥ p by TS4, so p is not a shifted image for I3). The n − 1 positions between p and shift(p, n) are likewise unspecified. The worked example implicitly shows new content occupying these positions, but no formal statement addresses them.

Frame conditions carry the standard connotation "everything not explicitly modified is preserved." Their silence about the gap could be misread as: old positions in the gap (if any existed in dom(M(d))) are preserved with their original values — contradicting the operation's purpose.

**Required**: Add an explicit note that I3 and the frames are partial constraints on M'(d), with the gap region [p, shift(p, n)) reserved for a content-placement postcondition to be specified by a future INSERT operation ASN. Alternatively, include the content-placement postcondition in this ASN.

---

### Issue 3: No span-level derived property
**ASN-0082, introduction**: "This ASN extends ASN-0053 (Span Algebra)..."

**Problem**: The ASN claims to extend ASN-0053 but cites no ASN-0053 definition or result — every cited result (OrdinalDisplacement, OrdinalShift, TS1, TS2) is from ASN-0034. I3 is about arrangement mappings (M(d) : T ⇀ T), not about spans. The claim that I3 belongs in the span algebra domain is asserted in prose but not supported by any formal connection to ASN-0053's framework.

A natural span-level property exists and should be derived. For a level-uniform span σ = (s, ℓ) in the shifted region (s ≥ p) with actionPoint(ℓ) = m = #s:

```
reach(σ') = shift(reach(σ), n)     — shifted endpoint
width(σ') = ℓ                       — width preserved
```

where σ' = (shift(s, n), ℓ). The derivation: by TA-assoc, shift(s, n) ⊕ ℓ = (s ⊕ δₙ) ⊕ ℓ = s ⊕ (δₙ ⊕ ℓ). Since both δₙ and ℓ have action point m, δₙ ⊕ ℓ = [0, …, 0, n + ℓₘ] and ℓ ⊕ δₙ = [0, …, 0, ℓₘ + n]; same result. So reach(σ') = s ⊕ (δₙ ⊕ ℓ) = (s ⊕ ℓ) ⊕ δₙ = shift(reach(σ), n). Width recovery: shift(reach(σ), n) ⊖ shift(s, n) = ℓ by direct computation (both agree at positions 1..m−1, differ at m by ℓₘ). This uses ASN-0053's SpanReach definition and bridges I3's point-level shift to the span framework.

**Required**: Derive span width preservation (or an equivalent span-level property) and cite ASN-0053's SpanReach definition. This justifies the "extends ASN-0053" categorization.

---

### Issue 4: M(d) and subspace(v) absent from statement registry
**ASN-0082, Statement Registry**

**Problem**: The arrangement function M(d) : T ⇀ T is introduced inline and is the central concept in I3, I3-L, I3-X, and I3-D, but has no statement registry entry. Similarly, subspace(v) = v₁ is used in VD, VP, I3, I3-L, and I3-X but is only implicitly defined within VP's formal statement — it lacks its own entry.

**Required**: Add both as definition entries in the statement registry with status "introduced (local)."


## OUT_OF_SCOPE

### Topic 1: Complete INSERT operation specification
**Why out of scope**: I3 specifies the shift aspect of insertion. A complete INSERT also requires: a content-placement postcondition (what the n new elements map to at positions in the gap), an I-space postcondition (new I-addresses appended), and a domain characterization (exactly which positions constitute dom(M'(d))). These are operation-level concerns that belong in a future INSERT ASN, not this shift-property ASN.

### Topic 2: Post-deletion contraction
**Why out of scope**: The reverse operation — shifting positions backward after deletion — has distinct edge cases (shift amount vs. start position, gap collapse) and warrants its own analysis. This ASN correctly scopes itself to insertion-direction shifts.


VERDICT: REVISE
