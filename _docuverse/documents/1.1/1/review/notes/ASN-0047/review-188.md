# Review of ASN-0047

## REVISE

### Issue 1: J1'★ derivation attributes gap-closure to J0 + P2, which do not cover the general case

**ASN-0047, Scoped coupling constraints (J1'★ derivation)**: "What closes that gap is not the step-local calculus but the other constraints of ValidComposite★: J0 forbids the allocate-then-strip composites that would discard a witnessed content address, and P2 persists every R-entry, so no valid composite records (a, d) and then removes a from d's content-subspace range before reaching Σ'."

**Problem**: The step-local wp gives a witness at the K.ρ post-state; the derivation must justify why the stronger Σ'-witness form of J1'★ excludes no legitimate composite. The named closers (J0, P2) are insufficient. Construct a valid-by-clause-(1) composite on *pre-existing* content `a ∈ dom(C)` (allocated in a prior composite), where `(a,d) ∉ R` and `d` does not currently contain `a`: K.μ⁺ (transclude `a` into `d`'s content range) → K.ρ (record `(a,d)`) → K.μ⁻ (strip `a` from `d`). Every elementary precondition holds at each intermediate state, so clause (1) is satisfied. At Σ', `(a,d) ∈ R'\R` but `a ∉ ran(M'(d)|_{s_C})`. J0 does **not** forbid this (`a` is not freshly allocated in this composite), and P2 merely keeps `(a,d)` in R. The only thing excluding this composite is **J1'★ itself** (as a boundary validity condition). The derivation's claim that "J0 + P2 close the gap" is therefore false for the pre-existing-content case — exactly the case the gap discussion is about.

**Required**: State that the Σ'-witness form of J1'★, imposed as a ValidComposite★ clause-(2) constraint, is itself what renders record-then-strip composites invalid; J0 covers only the freshly-allocated sub-case. Do not attribute the general closure to J0 + P2.

### Issue 2: "P3 = P0 ∧ P1 ∧ P2 ∧ L12" is restated four times, with naming meta-prose

**ASN-0047, Destruction confinement / ExtendedTransitionInvariants / per-transition proof / Properties Introduced**: The identity is stated in the P3 definition ("P3 is the synthesis of P0 ∧ L12 ∧ P1 ∧ P2 …"), in ExtendedTransitionInvariants ("P3 is the conjunction P0 ∧ P1 ∧ P2 ∧ L12 … so naming P3 alone covers every per-transition monotonicity obligation"), in the proof's per-transition section ("P3 is the conjunction P0 ∧ P1 ∧ P2 ∧ L12; discharging each conjunct discharges P3"), and again in the Local-extensions table P3 row.

**Problem**: Two-plus paragraphs in different sections say the same thing in different words (anti-bloat pattern). Additionally, "The label carries no '★' because there is no four-component predecessor to amend …" explains a naming convention rather than advancing the argument.

**Required**: State the conjunction once at P3's definition; have the later sites reference it. Delete the "label carries no '★'" naming rationale.

### Issue 3: Repeated forward deferrals to "Content-scoped containment and provenance" / P4★

**ASN-0047, Definition (Current containment), J2, J3, J4**: P4★ is invoked as "the operative provenance bound P4★ (Contains_C(Σ) ⊆ R, *Content-scoped containment and provenance*)" before it is defined, in the Current-containment definition, J2, J3, and the post-J4 staleness paragraph — each carrying the same forward pointer and the same parenthetical restatement of the bound.

**Problem**: Multiple paragraphs in different sections defer to the same downstream location (anti-bloat pattern), each re-stating `Contains_C(Σ) ⊆ R` and re-explaining that the unscoped `Contains(Σ) ⊆ R` is unsatisfiable. The repetition compounds the forward-reference load the reader must carry.

**Required**: Introduce Contains_C and P4★ before their first use (or consolidate the unsatisfiability argument to one site), and let subsequent sections cite P4★ by name without re-deriving the scoping rationale.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The forked document's link subspace starts empty by design (J4 discharge); a link-inheritance mechanism is correctly deferred to a future operations ASN and listed in Open Questions.

### Topic 2: Interior link withdrawal / tombstoning
**Why out of scope**: K.μ⁻ admits only suffix truncation under D-CTG★/D-MIN★; a separate withdrawal mechanism reconciling Nelson's tombstoning is genuinely new territory, appropriately recorded in Open Questions, not an error here.

VERDICT: REVISE
