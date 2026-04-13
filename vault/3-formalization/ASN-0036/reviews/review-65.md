# Cross-cutting Review — ASN-0036 (cycle 1)

*2026-04-13 07:36*

I've read the entire ASN and foundation statements carefully, tracking every definition, precondition chain, and cross-property interaction. The document is remarkably well-constructed after 64 prior reviews. I found three cross-cutting issues.

### OrdAddHom algebraic validity vs. semantic utility for I-addresses
**Foundation**: OrdAddHom — preconditions are `v ∈ T`, `#v = m ≥ 2`, `w ∈ T`, `w > 0`, `#w = m`, `w₁ = 0`, `actionPoint(w) ≤ m`
**ASN**: S8-depth, quoted: "the OrdAddHom/OrdShiftHom chain decomposes V-position shifts via ord/subspace/vpos, but that decomposition applies to element-field tumblers (zeros(v) = 0) and cannot be applied to full I-addresses (zeros(a) = 3), where stripping the first component yields a multi-field heterogeneous sequence, not an ordinal"
**Issue**: OrdAddHom's preconditions are purely structural — they are satisfied by any tumbler of length ≥ 2 paired with a displacement whose first component is zero. For an I-address `a` with `#a = 8` and displacement `δ(k, 8)`, every precondition is met and the identity `ord(a ⊕ w) = ord(a) ⊕ w_ord` holds. What fails is not the algebra but the interpretation: `ord(a)` strips the node field's first component, yielding a heterogeneous multi-field sequence that crosses zero separators — not a meaningful "ordinal." The text says "cannot be applied" when it means "yields no semantically useful decomposition." This distinction matters: a future ASN reasoning about I-address arithmetic might incorrectly exclude OrdAddHom from its toolbox, when the identity is available — it just doesn't decompose cleanly into subspace + ordinal.
**What needs resolving**: The S8-depth text should distinguish algebraic validity (the identity holds for I-addresses) from semantic utility (the ord/subspace/vpos decomposition is not meaningful for multi-field tumblers). The current phrasing could cause a future ASN to re-derive an I-address arithmetic result from scratch when OrdAddHom's identity, applied directly, would suffice.

### D-CTG forced intermediates and S8a joint satisfiability unstated
**Foundation**: S8a — `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`; D-CTG — forces tumblers into `V_S(d) ⊆ dom(Σ.M(d))`
**ASN**: D-CTG axiom, D-CTG-depth postcondition, D-MIN axiom, S8a axiom — the interaction of these four properties across three separate sections
**Issue**: D-CTG forces tumblers into `dom(M(d))` — any tumbler with the right subspace, depth, and ordering that falls between two existing positions must also be present. S8a constrains every element of `dom(M(d))` to have all-positive components. The ASN never explicitly verifies that every tumbler D-CTG could force into `dom(M(d))` satisfies S8a. The argument exists implicitly across a five-property chain: D-CTG + S8-fin + S8-depth → D-CTG-depth (positions share pre-last components) → D-SEQ with D-MIN (all positions have the form `[S, 1, ..., 1, k]` with `k ≥ 1`) → every component is positive → S8a holds. Each step is proved, but the bridge connecting D-CTG's "forcing" to S8a's "constraining" is never assembled. A per-property verification of D-CTG checks its proof; a per-property verification of S8a checks its derivation from T4. Neither checks that they are jointly satisfiable in non-trivial states.
**What needs resolving**: The ASN should state explicitly that D-CTG and S8a are jointly satisfiable — that any tumbler forced into `V_S(d)` by D-CTG automatically satisfies S8a. The argument is straightforward (D-SEQ's characterization makes it immediate), but leaving it implicit creates a gap in the cross-property consistency story that a TLA+ formalization would need to close.

### S5 consistency scope narrower than narrative claims
**Foundation**: S0–S3 (content immutability, store monotonicity, arrangement functionality, referential integrity); S7b — `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`; S8-fin, D-CTG, D-MIN
**ASN**: S5 proof, quoted: "S0–S3 are the only invariants checked. The constructions are minimal — single I-address, trivial arrangements — to isolate the consistency claim"; narrative text: "Transclusion is recursive and unlimited"; "no counter, cap, MAX_TRANSCLUSIONS constant, or any other limiting mechanism"
**Issue**: S5's formal property proves that S0–S3 alone do not entail a finite bound on sharing multiplicity. The proof constructs standalone models — a single I-address `a` with `C(a) = w` — without verifying that `a` satisfies S7b (`zeros(a) = 3`), or that the arrangement satisfies D-CTG, D-MIN, S8-fin, or S8-depth. The narrative surrounding S5 then asserts system-wide unrestricted sharing, citing Nelson's design intent and Gregory's implementation evidence. These system-wide claims are true — a valid state satisfying all invariants can be constructed with arbitrarily high sharing multiplicity (e.g., `{[1,k] ↦ a : 1 ≤ k ≤ N+1}` with `a` element-level satisfies D-CTG, D-MIN, S8-fin, S8-depth, S8a, and S7b) — but this is not what S5 formally establishes. The gap is between S5's proved scope (S0–S3 consistency) and S5's narrative scope (system-wide unrestricted sharing).
**What needs resolving**: Either strengthen S5's proof to verify the full invariant set (the construction is straightforward — choose an element-level I-address and sequential V-positions), or narrow the narrative claims to match the formal scope. A future ASN citing S5 for "unrestricted sharing in the system" would be making an unsound argument unless the full-invariant consistency is established somewhere.

## Result

Converged after 2 cycles.

*Elapsed: 4013s*
