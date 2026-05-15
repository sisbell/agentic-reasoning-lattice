# Review of ASN-0082

## REVISE

### Issue 1: PositiveOffsetExceeds derivation invokes commutativity not present in the foundation

**ASN-0082, "Ordinal Extraction" section, Lemma PositiveOffsetExceeds**: "For the left-summand form `a + b > b`: ... the cleaner path is to invoke commutativity of `+` on ℕ — a derived property of the natural-number monoid available under NAT-closure, NAT-addcompat, and NAT-wellorder's induction — to rewrite `a + b` as `b + a` and reduce to the right-summand form just proved."

**Problem**: The foundation (ASN-0034) does not include commutativity of `+` on ℕ as an axiom. Every directional property in the NAT-* axiom set is stated independently — left/right additive identity (NAT-closure), left/right cancellation (NAT-cancel), left/right order compatibility (NAT-addcompat), left/right dominance (NAT-addbound) — a structural signal that commutativity is *not* assumed. The phrase "a derived property... available under NAT-closure, NAT-addcompat, and NAT-wellorder's induction" claims derivability but exhibits no derivation, and commutativity is not a trivial consequence of those axioms. This is hand-waving in a load-bearing lemma cited at D-SHIFT well-definedness, D-BJ order-preservation, D-S span derivation, and S8a-post wp analysis.

**Required**: Replace the commutativity-based step with a foundation-derivable chain. The cleaner alternative does not need commutativity: NAT-addbound's right-dominance clause `(A m, n ∈ ℕ :: m + n ≥ n)` instantiated at `(m, n) := (a, b)` gives `a + b ≥ b`. NAT-cancel's mirror form `(A m, n ∈ ℕ : n + m = m : n = 0)` (already cited as a NAT-cancel Consequence) instantiated at `(m, n) := (b, a)` gives `a + b = b ⟹ a = 0`; by contrapositive with `a ≥ 1 ⟹ a ≠ 0` (from NAT-closure's `0 < 1`, NAT-order's transitivity and irreflexivity), conclude `a + b ≠ b`. Compose `a + b ≥ b` with `a + b ≠ b` via NAT-order's `≤`-defining clause to yield `a + b > b`. The right-summand form `b + a > b` derives independently as the ASN already shows. Update the Depends section accordingly.

## OUT_OF_SCOPE

### Topic 1: Boundary-crossing spans under D-SHIFT

**Why out of scope**: D-S handles spans whose start lies in R (entirely within the shifted region). Spans straddling region boundaries — start ∈ L with reach ∈ R, or start ∈ X — require additional decomposition: the X portion is deleted (and a span starting in X has its start position eliminated). Specifying how spans transform across the contraction boundary is the proper job of a downstream DELETE operation ASN that composes D-SHIFT with span-set semantics.

### Topic 2: Higher-depth contraction (#p > 2)

**Why out of scope**: The depth scoping axiom restricts contraction to #p = 2 with a rigorous TA4-incompatibility derivation. Generalizing to #p > 2 requires either a strengthened TA4-style partial-inverse lemma admitting non-zero prefixes, or a direct derivation from TumblerAdd/TumblerSub primitives — substantive new foundation work. This is acknowledged in the ASN's Open Questions.

### Topic 3: Link-subspace contraction semantics

**Why out of scope**: The subspace scoping axiom restricts contraction to S = 1. The link subspace V_2(d) admits tombstoning rather than gap-closure (foundation D-CTG/D-MIN/D-SEQ frame notes), so a different mutation discipline applies. A future ASN on link-mutation operations is the right venue.

### Topic 4: Full INSERT operation composition

**Why out of scope**: I3 is explicitly scoped as the shift sub-operation; content placement into the vacated gap [p, shift(p, n)) is deferred. The ASN correctly defers re-deriving D-CTG/D-MIN/D-SEQ in the text-subspace case to a composing INSERT ASN.

VERDICT: REVISE
