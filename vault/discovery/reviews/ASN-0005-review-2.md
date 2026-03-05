# Review of ASN-0005

## REVISE

### Issue 1: DEL1 clause 3 contradicts clause 2

**ASN-0005, DELETE as V-space surgery**: DEL1 states three clauses:
- "(A q : q < p : poom'(d).q = poom(d).q)"
- "(A q : q ≥ p ⊕ w : poom'(d).(q ⊖ w) = poom(d).q)"
- "(A q : p ≤ q < p ⊕ w : q ∉ dom.poom'(d))"

**Problem**: Clauses 2 and 3 are jointly inconsistent whenever content exists beyond the deletion range. Clause 2 says that for old position q = p ⊕ w, the new mapping at position (p ⊕ w) ⊖ w = p is defined: `poom'(d).p = poom(d).(p ⊕ w)`. Clause 3 says p ∉ dom.poom'(d), since p ∈ [p, p ⊕ w). The position p is simultaneously in and not in dom.poom'(d).

The ASN's own concrete example demonstrates the contradiction. After DELETE(d, 3, 2) on a five-position document, the ASN correctly derives poom'(d) = {1 ↦ a₁, 2 ↦ a₂, 3 ↦ a₅} — position 3 IS in dom.poom'(d), mapping to a₅ via the shift. Yet clause 3 asserts 3 ∉ dom.poom'(d) since 3 ∈ [3, 5).

The contradiction vanishes only in the degenerate case where the deletion removes all content from position p onward (nothing to shift), making clause 2's quantifier vacuous. But the clause is stated universally.

**Required**: Reformulate DEL1. The three clauses should characterize dom.poom'(d) and poom'(d) without contradiction. One correct formulation:

- dom.poom'(d) restricted to text subspace = {q : q < p, q ∈ dom.poom(d)} ∪ {q ⊖ w : q ≥ p ⊕ w, q ∈ dom.poom(d)}
- For q < p: poom'(d).q = poom(d).q
- For q ≥ p ⊕ w: poom'(d).(q ⊖ w) = poom(d).q

This says: positions before the deletion are unchanged, positions after the deletion shift left by w, and the deleted positions are not represented in the new domain — captured implicitly by the domain definition rather than by a contradictory third clause. The concrete example must then be rechecked against the corrected formulation.

### Issue 2: Ambiguous and incorrect expression in DEL6 case (c)

**ASN-0005, I-dimension invariance, case (c) middle split**: "The right fragment maps [p ⊕ w, v₂) → [i₁ + (p ⊕ w − v₁), i₂), with I-displacement offset by (p ⊕ w − v₁) and width (v₂ − p ⊕ w)."

**Problem**: The expression "v₂ − p ⊕ w" is ambiguous and wrong under standard left-to-right evaluation. Reading left to right: (v₂ − p) ⊕ w, which is the opposite of the intended v₂ − (p ⊕ w). Additionally, the expression mixes plain minus (−) with tumbler addition (⊕) without precedence rules. The intended width is v₂ ⊖ (p ⊕ w), using tumbler arithmetic consistently.

**Required**: Parenthesize the expression: "width (v₂ ⊖ (p ⊕ w))". Use consistent arithmetic operators throughout — either plain arithmetic or tumbler arithmetic, not a mix within a single expression.

### Issue 3: "V↔I bijection" is the wrong characterization

**ASN-0005, I-dimension invariance**: "The V↔I bijection is maintained through the split."

**Problem**: The POOM is defined as a function `poom(d) : Pos → Addr`. The ASN never establishes that this function is injective (one-to-one) — two V-positions could map to the same I-address (as would happen with transclusion within a single document). Claiming a "bijection" is maintained requires first establishing that one exists. What the ASN actually demonstrates is something weaker and different: correspondence preservation — each surviving V-position maps to the same I-address it mapped to before, just at a shifted V-coordinate. This is a faithfulness property, not a bijectivity property.

**Required**: Replace "V↔I bijection" with the property actually established: that for every surviving position, the I-address mapping is preserved through the shift. State this precisely — it is the conjunction of DEL1 (clauses 1 and 2, once corrected) and DEL6's invariance of I-displacement fields. Do not claim bijectivity without either establishing it as a precondition or proving it.

### Issue 4: Journal as reversal source is claimed but unspecified

**ASN-0005, The sources of reversal**: DEL14(b) lists three sources for naming deleted I-addresses, the third being "a journal record naming the deleted I-addresses." The ASN then hedges: "the journal's utility for reversal depends on what detail the records contain — a property we do not fully specify here."

**Problem**: DEL14 claims three sufficient sources for identity-preserving reversal, but one of those sources — the journal — is not shown to be sufficient because the necessary record detail is unspecified. The formal summary repeats the claim: "a journal record naming them (DEL13, DEL14)." A claim of sufficiency requires showing sufficiency; "it depends on details we don't specify" is not showing sufficiency.

**Required**: Either (a) specify what the journal record for DELETE must contain (minimally: the document id, the deleted I-address range, and the original V-positions) and prove this suffices for COPY-based restoration, or (b) remove the journal from DEL14's list of proven reversal sources and relegate it to an open question about what journal records must contain for reversal to work. Do not claim sufficiency without demonstrating it.

## OUT_OF_SCOPE

### Topic 1: Position arithmetic formalization

The ASN introduces ⊕ and ⊖ as "position arithmetic (tumbler addition and subtraction within a subspace)" but never formalizes these operators. Properties like commutativity, whether p ⊕ w ⊖ w = p always holds, or how arithmetic interacts with the subspace prefix structure, are assumed throughout. A dedicated treatment of tumbler position arithmetic would place DEL1's shift clauses on firmer ground.

**Why defer**: The ASN uses these operators consistently within its scope. Formalizing position arithmetic is foundational work that precedes this ASN's concerns and would serve all operations, not just DELETE.

### Topic 2: Atomicity of multi-entry DELETE

The ASN describes what the POOM looks like after DELETE but does not specify whether the removal of entries and the leftward shift of survivors is an atomic transformation or whether intermediate states (some entries removed, others not yet shifted) may be visible. The Open Questions section raises this. It is a concurrency/observability concern that belongs in a future ASN on operation semantics.

**Why defer**: The ASN specifies the before/after relation, which is the correct level of abstraction for a sequential specification. Atomicity is a property of the execution model, not of the operation's definition.

### Topic 3: POOM domain contiguity as system invariant

DEL1 (text subspace) produces a contiguous text domain only if the pre-state domain was contiguous. The ASN never states contiguity as an invariant of the text subspace, though the shift arithmetic implicitly assumes it. Whether contiguity is a system invariant maintained by all operations, or whether gaps in the text subspace are structurally possible, should be established independently.

**Why defer**: This is an invariant about POOMs in general, not specific to DELETE. It would need to be established across INSERT, COPY, and DELETE jointly.

### Topic 4: Per-document vs. global link discoverability

DEL7 classifies link discoverability globally (quantifying over all documents' POOMs), while the concrete example and DEL8 discuss resolution through a specific document. A link can be "live" globally but "ghost" relative to a particular document. The relationship between the global classification and per-document resolution is discussed informally ("ghost link relative to d") but not formalized.

**Why defer**: The global classification in DEL7 is well-defined and correct. The per-document refinement is a useful extension for link query semantics, which is new territory rather than an error in this ASN.
