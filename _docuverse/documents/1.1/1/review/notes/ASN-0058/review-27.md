# Review of ASN-0058

## REVISE

### Issue 1: M16a omits T4-validity verification for the shifted address
**ASN-0058, M16a (OriginInvarianceUnderShift)**: "By TumblerAdd (ASN-0034), every component at indices `i < #a` is copied unchanged from `a` to `a + k`, including the entire document prefix `N.0.U.0.D`. Therefore `origin(a + k) = origin(a)`."

**Problem**: The proof concludes `origin(a + k) = origin(a)` without establishing that `a + k` lies in `origin`'s domain. The S7 origin (ASN-0036) is defined as `N(a).0.U(a).0.D(a)`, where N, U, D are T4b's partial projections — applicable only when their input is T4-valid with `zeros ≥ 2`. The proof secures T4-validity of `a` (via S7d → T10a → T10a.4) and shows the document prefix is preserved at indices `< #a`, but it never verifies the four T4 conjuncts for `a + k`: `zeros(a + k) ≤ 3` (the last component shifts from `a_{#a} ≥ 1` to `a_{#a} + k ≥ 1`, introducing no new zero); no adjacent zeros (only the last component changes, and it stays positive); `(a + k)_1 ≠ 0`; `(a + k)_{#a} = a_{#a} + k ≥ 1`. These follow straightforwardly, but the proof should make the step explicit. Downstream proofs depend on M16a — M16 (CrossOriginMergeImpossibility) and M6(d) (SplitPreservation, origin traceability) both cite it — so the gap propagates.

**Required**: Add an explicit T4-validity check for `a + k` (or factor it into a companion lemma cited by M16a). Equivalently, the proof could define origin syntactically in terms of component indices and show preservation, then bridge to S7's projection-based definition once T4-validity is in hand.

### Issue 2: Title and body use inconsistent terminology
**ASN-0058, Title**: "Bundle Algebra"
**ASN-0058, Body**: The body uses "mapping block" exclusively. The term "bundle" never appears in any definition, claim, proof, table entry, or section heading. The Properties Introduced table lists only mapping-block and content-reference claims.

**Problem**: The title names an algebraic structure that the body neither defines nor uses. A reader entering the ASN cannot determine whether "bundle" is a synonym for "block decomposition", a higher-order aggregate, or a stale name from earlier drafting. The ASN itself coherently develops a *mapping block algebra* — the title misdirects.

**Required**: Either (a) rename the ASN to match the body terminology (e.g., "Mapping Block Algebra"), or (b) formally introduce "bundle" as a defined term used in subsequent material.

## OUT_OF_SCOPE

### Topic 1: Composite resolution with overlapping references
`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)` concatenates without deduplication. When two references resolve to overlapping I-address regions, the meaning of the resulting redundancy is unspecified.

**Why out of scope**: Composition behavior of references is placement-level structure, beyond the bundle-algebra focus.

### Topic 2: Synthesis (inverse of resolution)
Given an I-address sequence `⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`, can one recover a content reference resolving to it? Under what conditions is an inverse unique?

**Why out of scope**: This is the synthesis problem — constructing arrangements from I-address data — which belongs to operations ASNs, not the bundle algebra.

### Topic 3: Resolution against arrangement operations
How does resolution interact with INSERT/DELETE/COPY/REARRANGE on the source document? Specifically, what stability guarantees does resolve(d_s, σ) carry across operations on `M(d_s)`?

**Why out of scope**: Operation effects on arrangements are out of scope per the scope statement.

VERDICT: REVISE
