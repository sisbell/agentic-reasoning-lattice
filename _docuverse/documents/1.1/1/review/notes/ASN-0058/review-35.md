# Review of ASN-0058

## REVISE

### Issue 1: M16a's citation of S7d for T4-validity is misplaced
**ASN-0058, M16a proof**: "T10a.4 (T4PreservationUnderDiscipline, ASN-0034) applied to S7d's allocation discipline gives T4-validity of every a ∈ dom(C)"

**Problem**: S7d (DocumentAllocationDiscipline, ASN-0036) is specifically about *document tumblers* (zeros = 2), not content addresses (zeros = 3 per S7b). S7d does not establish that content addresses are T10a-allocated; what does is the framework-level assumption "a system conforming to T10a" presupposed by ASN-0036's S4 and S7. The chain "T10a.4 applied to S7d's allocation discipline" is broken — S7d's discipline does not range over `dom(C)`.

**Required**: Replace the S7d citation with the framework-level T10a-conformance citation (S4's "within a system conforming to T10a" or S7's precondition list naming T10a directly are appropriate sources).

### Issue 2: Set D is used without formal definition
**ASN-0058, Content References section**: "Let D be the set of documents for which an arrangement is defined."

**Problem**: D is introduced casually and then used as a fixed set in `d_s ∈ D` of the ContentReference Definition. The phrase "for which an arrangement is defined" suggests state-dependence on Σ, but no dependence is made precise. ContentReference reads as a state-independent definition over a state-dependent population.

**Required**: Define D explicitly relative to a state — `D(Σ) = {d : M(Σ, d) is defined}` or similar — and thread the state through. Or declare D as a primitive of the state vocabulary up front.

### Issue 3: ContentReference precondition (iv) `m ≥ 2` is redundant
**ASN-0058, Definition (ContentReference)**: "(iv) m ≥ 2."

**Problem**: Precondition (i) requires `V_{u₁}(d_s) ≠ ∅`, so some `v ∈ V_{u₁}(d_s)` exists. By S8a (ASN-0036), `#v ≥ 2`; by S8-depth (ASN-0036), all V-positions in `V_{u₁}(d_s)` share that depth. So `m ≥ 2` is a consequence of (i), not an independent constraint. Stated as a precondition, it obscures that subspace confinement (claimed to require (iv)) is in fact licensed by the weaker (i) alone.

**Required**: Drop (iv) and derive `m ≥ 2` at the point of use, or relabel it as a derived consequence of (i) rather than an independent precondition.

### Issue 4: M-int's Component-m reduction does not handle `k = 0` explicitly
**ASN-0058, M-int proof, Component-m reduction**: "The tumbler x + k, computed via TumblerAdd at action point m, agrees with y on components 1..m−1 (by prefix agreement) and on component m (by definition of k), and shares depth m. Hence y = x + k."

**Problem**: TumblerAdd applies only to ordinal displacements `δ(k, m)` with `k ≥ 1`. The boundary case `k = 0` — which arises when `x = y`, admitted by `x ≤ y` — requires the OrdinalShiftBase convention `x + 0 = x`, not TumblerAdd's three-region rule. The proof's "computed via TumblerAdd" framing elides the case split, leaving `k = 0` only implicitly handled.

**Required**: Split the final step on `k = 0` vs `k ≥ 1`. For `k = 0`, derive `y = x` directly from prefix agreement + depth equality + `(y)_m = (x)_m` via T3, then conclude `y = x = x + 0` by OrdinalShiftBase. For `k ≥ 1`, the TumblerAdd argument as written applies.

### Issue 5: M15's supporting argument does not address the claim it supports
**ASN-0058, M15**: "(b) Splitting or merging blocks in a decomposition of M(d₁) does not alter any block in any decomposition of M(d₂)." Supported by: "If deletion — the most destructive arrangement operation — cannot affect other documents' mappings, then no arrangement operation can."

**Problem**: Split and merge are *representation operations* on block decompositions; they do not modify M(d) at all. The Nelson quote and the inference about "arrangement operations" concern operations on M(d), which is a different object than B. The argument therefore does not establish what M15(b) claims. The relevant fact is a frame condition: split and merge name a single decomposition B associated with a single M(d) and touch nothing else.

**Required**: Reformulate M15(b) as an explicit frame condition on M6f and M7f — the operation modifies only the single B (of a single M(d)) named in its precondition, and no other document's arrangement or decomposition is named, read, or modified. M15(a) is then a definitional observation; (b) follows from the frame.

### Issue 6: Forward references compromise structural ordering
**ASN-0058, M6 clause (d)**: "M16a (OriginInvarianceUnderShift, below) then gives origin(a + k) = origin(a)..."

**Problem**: M6(d) invokes M16a, which is established several sections later; the ContentReference Definition motivates precondition (iv) via C0a established below. These are not logical errors (M16a and C0a do not depend on their callers), but the reader must defer trust until the forward references resolve, and the "below" labels become brittle under reordering.

**Required**: Either move M16a before M6 (it stands on its own and is short), or factor M6's clause (d) into a corollary stated after M16a. The ContentReference motivation can similarly be deferred to a remark after C0a.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
