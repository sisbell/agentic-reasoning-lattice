# Review of ASN-0064

## REVISE

### Issue 1: DiscoveryQuery allows arbitrary Q ⊆ T, but decidability proof requires finite span-set representation

**ASN-0064, The Satisfaction Predicate**: "A discovery query is a tuple Q = (H, F_Q, G_Q, Θ_Q) where... F_Q ⊆ T is the *from-constraint*"

**ASN-0064, F3 proof**: "Each overlap test reduces to pairwise span intersection (the biconditional above), which is decidable by T2 (IntrinsicComparison) applied to the four endpoint tumblers. Since each endset is finite (ASN-0043, Endset), there are finitely many span pairs to test."

**Problem**: The DiscoveryQuery definition admits arbitrary subsets of the infinite tumbler space T as constraints. The decidability proof assumes these constraints are given as finite span-sets so that overlap can be tested by pairwise span comparison. For an arbitrary Q ⊆ T, the test `coverage(e) ∩ Q ≠ ∅` is not decidable by enumeration or pairwise comparison — you cannot iterate over an arbitrary infinite subset. The proof's "finitely many span pairs" argument requires both the endset and the query to be finite collections of spans.

**Required**: Either constrain DiscoveryQuery so that F_Q, G_Q, Θ_Q are finite span-sets (matching the user-facing specification, where queries are V-span-sets resolved through M(d)), or revise the decidability proof to handle the stated generality. The natural fix is the former: the definition should require each constraint to be either T (unrestricted) or a finite span-set — which matches the resolution pipeline described in prose.

---

### Issue 2: F5 (CrossDocumentIdentity) is formally broken

**ASN-0064, Cross-Document Discovery**: 
```
(A d₁, d₂ ∈ E_doc, a ∈ T :
  a ∈ ran(M(d₁)) ∧ a ∈ ran(M(d₂))
  ⟹ (A ℓ : overlaps(Σ.L(ℓ).from, {a}) : ℓ ∈ findlinks((E_doc, {a}, T, T))))
```

**Problem**: Three defects.

(a) *Hypothesis unused.* The quantification over d₁, d₂ and the hypothesis `a ∈ ran(M(d₁)) ∧ a ∈ ran(M(d₂))` are never used in the conclusion. The conclusion quantifies over arbitrary ℓ with the overlap property — no reference to d₁ or d₂.

(b) *Missing assumption.* Expanding findlinks: `ℓ ∈ findlinks((E_doc, {a}, T, T))` requires `home(ℓ) ∈ E_doc ∧ overlaps(Σ.L(ℓ).from, {a})`. The guard gives the overlap condition. The home condition `home(ℓ) ∈ E_doc` is assumed but never established — no foundation states that `origin(ℓ) ∈ E_doc` for all `ℓ ∈ dom(Σ.L)`. (P6 establishes this for dom(C), not dom(L); no foundation defines the link creation transition that would establish it for dom(L).)

(c) *Formal statement doesn't match the derivation.* The prose derivation correctly argues that `resolve(d₁, {v₁}) = {a} = resolve(d₂, {v₂})` implies both queries produce identical findlinks results. This is the actual cross-document property. But F5's formal statement says something different — it says "any link overlapping {a} is in findlinks," which is (modulo the home gap) a restatement of findlinks' definition, not a cross-document identity claim.

**Required**: Reformalize F5 to match the prose. The property is: for any two documents d₁, d₂ both arranging I-address a, any query resolved through d₁ to {a} and any query resolved through d₂ to {a} produce the same findlinks result. Additionally, either state `home(ℓ) ∈ E_doc` as an explicit assumption (with a note that the link-creation transition must establish it), or derive it from the foundations.

---

### Issue 3: F10 (ReverseSilentOmission) is tautological

**ASN-0064, Reverse Resolution**: "F10 — ReverseSilentOmission (LEMMA). `reverse(d, e) ⊆ {v : M(d)(v) ∈ coverage(e)}`"

**Problem**: By the definition on the same page, `reverse(d, e) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`. The right-hand side of F10, `{v : M(d)(v) ∈ coverage(e)}`, is only well-defined for v ∈ dom(M(d)) (since M(d) is partial). So the right-hand side equals reverse(d, e), and F10 states A ⊆ A. The intended property — that coverage(e) may contain I-addresses absent from ran(M(d)), producing a partial result with no indication of the omitted addresses — is described clearly in prose but not captured by the formal statement.

**Required**: Either formalize the omission property (e.g., as an existential: there exist states where `coverage(e) ⊄ ran(M(d))` and the result contains no information about `{a ∈ coverage(e) : a ∉ ran(M(d))}`), or demote F10 from a LEMMA to an observation with a precise prose description acknowledging that the silent-omission property is an interface constraint rather than a mathematical lemma.

---

### Issue 4: F7 (VisibilityFiltering) depends on undefined predicates

**ASN-0064, Visibility and Access Control**: "`accessible(d, u) ≡ published(d) ∨ authorized(u, d)`"

**Problem**: `published(d)` and `authorized(u, d)` are not defined in any foundation ASN, nor are they defined in this ASN. F7 is stated as a formal invariant with two sub-properties (no-omission and no-leakage), but both depend on undefined predicates. The ASN acknowledges the gap: "Private documents. (Currently all documents are visible to all users.)" and "An implementation must add access-control filtering on top of the satisfaction predicate." But the formal invariant is presented alongside fully-grounded properties (F0–F6), with no indication that F7's formal status is different.

**Required**: Either define the predicates (at least axiomatically — stating their types, monotonicity properties, and relationship to E_doc), or restructure the section to clearly separate the formal properties (F0–F6, F8–F11, which are grounded) from the design intent (F7, which is not). A "Design Requirement" label rather than INV would be honest about the status.

---

### Issue 5: No concrete worked example

**ASN-0064, throughout**

**Problem**: The ASN defines resolution, overlap, satisfaction, findlinks, reverse resolution, and pagination without verifying any of them against a specific scenario. The review standards require: "the ASN should verify its key postconditions against at least one specific scenario." The Implementation Observations section discusses Gregory's code but never traces through the formal definitions with concrete tumblers.

**Required**: Add a worked example. For instance: a document d with two mapping blocks β₁ = ([1,1], [2.0.3.0.1.1], 3) and β₂ = ([1,4], [2.0.5.0.1.1], 2); a link ℓ with from-endset {([2.0.3.0.1.2], [0,2])}; a query selecting V-positions [1,2] through [1,5]. Trace through: resolve produces two I-runs; the overlap test against ℓ's from-endset succeeds on the first I-run; satisfaction holds; findlinks returns ℓ. Verify each step against the formal definitions. Show at least one case where the V-span crosses a block boundary (the F1 fragmentation scenario) and one case where a link does NOT satisfy the query.

---

### Issue 6: Pagination cursor domain is inconsistent

**ASN-0064, Result Ordering and Pagination**: "For a result set R = findlinks(Q), a cursor c ∈ dom(Σ.L), and a count n ≥ 1..." followed by "The first page uses a cursor below all possible link addresses (such as the zero tumbler)."

**Problem**: The definition constrains c ∈ dom(Σ.L). The zero tumbler is not in dom(Σ.L) — by TA6, zero tumblers are not valid addresses, and by L1, link addresses are element-level tumblers. So the suggested initial cursor violates the definition's own type constraint. This leaves the first page undefined.

**Required**: Either relax the cursor domain to T (all tumblers, including the zero tumbler used as a sentinel), or define a separate first-page case where c is not required. The former is cleaner — the cursor is just a position in the total order, not necessarily a link address.

---

## OUT_OF_SCOPE

### Topic 1: Link creation state transition
**Why out of scope**: No foundation ASN defines how links enter dom(Σ.L). ASN-0047 defines K.α (content allocation) but has no analogous K.λ (link allocation). This gap means properties like `home(ℓ) ∈ E_doc` for all ℓ ∈ dom(Σ.L) cannot currently be derived. A future link-creation ASN (presumably ASN-0063) should establish this as a postcondition. ASN-0064 may need to state it as an explicit assumption until that foundation is in place.

### Topic 2: Link-subspace query interactions
**Why out of scope**: The ASN defines resolution generically over all V-positions, including link-subspace positions (subspace 0). Whether users can or should query the link subspace — and what it means for the overlap test when the query's resolved I-addresses are themselves link addresses — is a question about the interaction between link-subspace arrangement and link discovery. This belongs in the arrangement layer, not in the discovery specification.

VERDICT: REVISE
