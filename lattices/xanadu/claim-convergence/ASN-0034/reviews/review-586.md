# Cone Review — ASN-0034/TA1-strict (cycle 1)

*2026-04-26 01:18*

### NAT-carrier use-site inventory in axiom prose
**Class**: OBSERVE
**ASN**: NAT-carrier — "Every Cartesian product `ℕ × ℕ` (NAT-order's `< ⊆ ℕ × ℕ`, NAT-closure's `+ : ℕ × ℕ → ℕ`), every membership `x ∈ ℕ` (NAT-zero's `0 ∈ ℕ`, NAT-closure's `1 ∈ ℕ`), and every set-builder `{j ∈ ℕ : ...}` (T0's index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}`) presupposes this primitive commitment."
**Issue**: The axiom body explains *why* the axiom is needed (by enumerating downstream use sites) rather than *what* it says. The first paragraph's "irreducible at this level" framing — "not constructed from a more elementary substrate, not extracted from the meta-language by ambient definability" — is essay content defending the choice of primitive rather than carrying argumentative load. The axiom itself ("`ℕ` is a set") is one line; the prose is a use-site inventory and a defensive justification.

### NAT-sub axiom-vs-consequence defenses
**Class**: OBSERVE
**ASN**: NAT-sub — "Strict monotonicity ... is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from the right-inverse together with NAT-addcompat's right order compatibility and NAT-order's at-least-one trichotomy with irreflexivity. Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form `m < n ⟹ m ≠ n` from being separately exported..."; and analogous prose preceding the strict-positivity derivation.
**Issue**: Two paragraphs defend the design choice of recording the two facts as Consequences rather than as additional axiom clauses. The defense is meta-content about axiomatic minimality, not part of the derivation. The Consequence slot itself already records "derived from ... as shown in the preceding prose"; the additional sentences ("Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept...") are defensive justification a precise reader must skip past.

### NAT-sub trailing use-site inventory
**Class**: OBSERVE
**ASN**: NAT-sub — "The axiom body invokes symbols beyond ℕ's primitive membership. The strict order `<` together with its non-strict companion `≤` ... appear in the signature's domain condition... The binary addition `+` closed over ℕ by NAT-closure appears in the sums `(m − n) + n`, `n + (m − n)`, `m + n`, and `n + m`. NAT-addbound's right-dominance clause ... discharges the conditional-closure precondition ... NAT-addcompat is declared in the Depends slot accordingly. ... NAT-zero and NAT-discrete are declared in the Depends slot accordingly."
**Issue**: A long paragraph that re-states the contents of the Depends list in prose form, listing each cited dependency and where it is used. The Depends slot already carries this information per dependency. The paragraph is a use-site inventory in a structural slot.

### TumblerAdd "characterizations" appendix
**Class**: OBSERVE
**ASN**: TumblerAdd — the post-proof section labelled "Three properties of this definition — characterizations of what ⊕ does rather than postconditions to discharge — require explicit statement," followed by "No carry propagation," "Tail replacement, not tail addition," and "The many-to-one property."
**Issue**: The "characterizations of what ⊕ does rather than postconditions to discharge" framing is a defensive disclaimer that pre-emptively explains why these paragraphs are not proof obligations. The three subsections themselves (concrete examples, the `[1,1] ⊕ [0,2] = [1,3]` worked instances, the contrast between tail replacement and tail addition) are statements of what the operation does and so are not noise; the surrounding meta-frame is. Flag the framing sentence, not the content.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 795s*
