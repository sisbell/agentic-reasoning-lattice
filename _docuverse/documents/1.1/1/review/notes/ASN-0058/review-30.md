# Review of ASN-0058

## REVISE

### Issue 1: M16a applies `origin` to addresses outside S7's stated domain

**ASN-0058, M16a (OriginInvarianceUnderShift)**: "For any `a ∈ dom(C)` and any `k ≥ 0`: `origin(a + k) = origin(a)`"

**Problem**: S7 (ASN-0036) defines `origin` as a function on `dom(C)` — its explicit precondition is `a ∈ dom(Σ.C)` and its attribution postcondition (b) ties `origin(a)` to the document that allocated `a`. M16a applies `origin` to `a + k` for `k ≥ 1` without establishing `a + k ∈ dom(C)`, and the proof rationalizes the application by claiming "S7 requires T4-validity ... and zeros = 3" — but those are consequences of `a ∈ dom(C)` (via S7b's structural axiom), not alternative preconditions on `origin`'s domain. The author is implicitly using a broader "`origin`" — the structural extraction `N(a).0.U(a).0.D(a)` computed via T4b's projections on any T4-valid tumbler with `zeros = 3` — without naming it as separate from S7's `origin`. In the actual use sites (M16, M6(d)) the shifted addresses happen to be in `dom(C)`, so the issue is invisible there, but M16a's statement quantifies over all `k ≥ 0` with no precondition requiring `a + k ∈ dom(C)`.

**Required**: Either (a) introduce a named structural extraction function (e.g., `docPrefix : T ⇀ T` on the T4-valid + `zeros = 3` subset of T) and restate M16a in terms of it, with the agreement against S7's `origin` on `dom(C)` noted; or (b) add `a + k ∈ dom(C)` as a precondition to M16a and discharge it explicitly in the M16 and M6(d) applications (M16: `a + n₁ = a₂ ∈ dom(C)` by hypothesis; M6(d): `a + k ∈ I(β) ⊆ dom(C)` by B3 + S3).

### Issue 2: M12a's partition corollary is asserted in one parenthetical sentence

**ASN-0058, M12a (RunDisjointness) partition corollary**: "Every `v ∈ dom(f)` belongs to at least one maximal run (start with the trivial run `(v, f(v), 1)` and extend in both directions until conditions 2 and 3 hold; termination by finiteness of `dom(f)`); by M12a, to at most one."

**Problem**: The corollary is load-bearing — it supplies the existence half of "maximal runs partition `dom(f)`", without which M12's identification of every maximally merged decomposition with the set of maximal runs cannot close. The construction is gestured at in one parenthetical clause but three substantive parts go unverified: (a) the right-extension procedure — incrementing `n` while `v + n ∈ dom(f)` and `f(v + n) = a + n` — and its termination at condition 3; (b) the left-extension procedure — searching for a predecessor `v'` with `v' + 1 = v_current ∈ dom(f)` and `f(v') + 1 = a_current`, whose stopping criterion is existential (condition 2 is "no such `v'` exists") rather than a forward equality; (c) the termination argument, which depends on each extension strictly enlarging `V(R) ⊆ dom(f)` combined with `|dom(f)| < ∞`.

**Required**: Spell out the right- and left-extension procedures with explicit stopping conditions tied to conditions 2 and 3 of "maximal run". Establish termination from finiteness of `dom(f)` (each extension adds a new element of `dom(f)` to `V(R)`). Confirm condition 1 (correspondence run) is preserved at each extension step.

### Issue 3: M2 omits T3 from its dependency list while invoking it indirectly via M-int

**ASN-0058, M2 (DecompositionExistence)**: "M2 inherits S8's preconditions verbatim"

**Problem**: M2's reverse-inclusion proof invokes M-int, and M-int's "Component-`m` reduction" uses T3 (CanonicalRepresentation, ASN-0034) to conclude `y = x + k` from component-wise plus length agreement. The M-int proof and the M2 preconditions list both omit T3, although it is foundation and used inside M-int. This is minor (the proof works) but breaks the convention of listing foundation dependencies that the rest of the ASN follows.

**Required**: Add T3 to M-int's enumerated foundation dependencies (the prose "no block-decomposition fact ... is invoked" should be widened to enumerate which foundation facts *are* invoked — TumblerAdd, T1, T3, S8a, S8-depth, OrdinalShiftBase).

## OUT_OF_SCOPE

(none — every claim stays within the block algebra; the resolution sub-section is a natural query mechanism over decompositions and does not stray into operations, links, or versions)

VERDICT: REVISE
