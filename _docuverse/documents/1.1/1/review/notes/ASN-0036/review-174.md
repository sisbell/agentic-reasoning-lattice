# Review of ASN-0036

## REVISE

### Issue 1: S5's "genuine strand state" checklist omits several always-on invariants
**ASN-0036, Sharing (S5 proof, preamble and conclusion)**: "the always-on well-formedness invariants the model imposes on every state — S7b (`zeros(a) = 3`...), the domain-restriction axiom..., and S8-fin (finite arrangements)."
**Problem**: This enumeration claims to list the invariants "the model imposes on every state," but the ASN also states S8-depth, D-CTG, and D-MIN as *Axiom (design requirement)* / "design constraint on well-formed document states," and S7a, S7d as always-on design requirements. None of these appear in the checklist, and neither construction verifies them. The proof then asserts the witnesses are "genuine strand states, not bare models of S0–S3" — but a genuine well-formed state must satisfy *all* always-on requirements, not the subset chosen here. (The constructions do happen to satisfy D-CTG/D-MIN/S8-depth/S7a/S7d, which makes the omission fixable, not fatal — but it is unverified.) A downstream operations ASN that relies on S5's "genuine strand state" notion would inherit an incomplete definition.
**Required**: Either (a) verify S7a, S7d, S8-depth, D-CTG, D-MIN against both witness states alongside the existing checks, or (b) define "genuine strand state" precisely once and justify why these specific invariants are excludable for the witness purpose. Note that D-CTG/D-MIN/S8-depth are introduced *after* S5 in document order; the forward dependency is part of why the enumeration drifted out of sync.

### Issue 2: S8a is a renamed restatement of the domain-restriction axiom, with re-derivation prose
**ASN-0036, Singleton span partition (S8a) and Properties table**: "This is the per-component form of the domain-restriction axiom... `zeros(v) = 0` iff every component is positive"; table: "from the domain-restriction axiom, T0... equivalent by T0."
**Problem**: S8a and the domain-restriction axiom (`zeros(v) = 0 ∧ #v ≥ 2`) are logically equivalent given T0, by the ASN's own admission. Maintaining two named forms with a paragraph re-deriving their equivalence is the "same thing in different words" pattern the anti-bloat pass targets. The proofs cite "S8a" repeatedly where they could cite the axiom directly.
**Required**: Keep at most one canonical statement. If the per-component form is retained for proof ergonomics, present it as a one-line cited reformulation, not a re-derived sibling axiom.

### Issue 3: S7a axiom buried under justification prose
**ASN-0036, Structural attribution (S7a)**: "Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction... is computable only because I-addresses are scoped under their originating documents. Gregory's implementation corroborates this..."
**Problem**: This is multi-sentence prose explaining *why the axiom is needed* rather than *what it says* — exactly the accretion pattern flagged for this note. The axiom itself ("every I-address is allocated under the originating document's prefix") is already clear; the surrounding justification does not advance the formal content.
**Required**: Reduce to a single motivating line (or the one Nelson quote that states the principle) and let the formal contract carry the claim.

## OUT_OF_SCOPE

### Topic 1: Preservation of D-CTG/D-MIN/S2 under editing operations
**Why out of scope**: This is correctly deferred — the ASN's open questions explicitly ask what INSERT/DELETE/COPY/REARRANGE must guarantee to preserve the contiguity invariants. Operation frame/postconditions belong in a future ASN per the stated scope.

VERDICT: REVISE
