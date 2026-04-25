# Regional Review — ASN-0034/Divergence (cycle 2)

*2026-04-24 05:14*

### T1 paragraph defending its NAT-closure declaration is meta-prose
**Class**: REVISE
**Foundation**: (internal)
**ASN**: T1 (LexicographicOrder), paragraph beginning "The Definition invokes two primitives not introduced here. The literal `1` — in the witness constraint `1 ≤ k`, …" through "…matching T0's precedent of naming NAT-closure directly for the single `1` in `1 ≤ #a` and NAT-cancel's articulated rule that a symbol supplied only by NAT-closure is named directly rather than reached transitively through downstream NAT-* axioms that themselves depend on it."
**Issue**: The paragraph does not develop the claim — it justifies a slot in the Depends list. It enumerates every use site of `1` and `+ 1` in the Definition and proof, names NAT-closure as the supplier, then invokes precedent (T0's `1 ≤ #a`, NAT-cancel's "articulated rule") to argue why NAT-closure is declared directly rather than transitively. This is the reviser-drift pattern flagged in the instructions: new prose around an axiom citation that explains why the axiom is declared rather than what the claim says. The matching material is already inside the Formal Contract's NAT-closure citation (which itself runs to two full sentences of precedent-invocation). The prior REVISE finding (T1 missing NAT-closure) required declaring NAT-closure in Depends; it did not require prose elaboration of the declaration.
**What needs resolving**: Either remove the justification paragraph (retain only a compact NAT-closure citation in Depends that names the supplied symbols) or collapse to a single sentence stating the dependency without use-site inventory and precedent appeal.

### NAT-cancel's "non-minimality / matching the precedent" meta-commentary
**Class**: REVISE
**Foundation**: (internal)
**ASN**: NAT-cancel, two locations: (a) the trailing sentence "Each form uses the cancellation axiom on the side where `m` already stands free … recording either form as an axiom would make the set non-minimal, so both are listed here as consequences of this ASN's cancellation axioms together with NAT-closure." (b) Formal Contract → Depends → NAT-zero citation: "named directly rather than reached transitively through NAT-closure, following the same precedent NAT-closure uses to declare NAT-zero as the supplier of the literal `0` in its identity clauses `0 + n = n` and `n + 0 = n`."
**Issue**: Sentence (a) explains a bookkeeping choice about axiom-vs-consequence placement; the preceding derivations already carry the mathematical weight. Sentence (b) is a precedent appeal embedded in a Depends line that ought to name the supplied symbol and stop. Both are meta-commentary about how the ASN is organized, not about what it claims. NAT-addcompat's similar closing ("Both foundations are declared in the Depends slot so that the axiom body can be read without silently importing them") exhibits the same pattern. These defensive justifications compound across axioms.
**What needs resolving**: Remove the axiom-minimality commentary and the "named directly rather than reached transitively, matching the precedent…" language from NAT-cancel (and the parallel NAT-addcompat closing); keep Depends citations to the supplied symbol and its use.

### Divergence prose on NAT-wellorder's role vs. uniqueness argument
**Class**: REVISE
**Foundation**: (internal)
**ASN**: Divergence, paragraph beginning "Case (i)'s value `k` is unique from the characterization alone, without appeal to NAT-wellorder: suppose…" and continuing "NAT-wellorder plays a distinct role — not in uniqueness, but in *existence* of a witness: when case (i) is entered from the weaker hypothesis that `S := {i ∈ ℕ : …}` is nonempty, NAT-wellorder supplies `min S`…"
**Issue**: Case (i)'s Definition already quantifies `∃ k` over the full conjunction `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`, so existence of a witness for case (i) is the premise, not something that requires NAT-wellorder. The "when case (i) is entered from the weaker hypothesis that `S` is nonempty" clause imagines a reformulation the current Definition does not use. The paragraph reads like a relocated argument for why NAT-wellorder remains in Depends after uniqueness was shown not to need it — a defensive justification, not claim development. The Depends citation for NAT-wellorder already discharges this need in a single line.
**What needs resolving**: Either rewrite the Definition to make "least index satisfying the shared-position mismatch conjunction" the defining characterization (in which case NAT-wellorder supplies existence and the mismatch set `S` enters the Definition, not the prose), or drop the "distinct role" paragraph and let the NAT-wellorder Depends citation stand alone.

### T1 trichotomy Case 3 re-derives the ordering it already has from the clause
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: T1 (LexicographicOrder), proof part (b) Case 3: "Both clauses force `m ≠ n`: (β) gives `m + 1 ≤ n`, hence `m < n` via NAT-addcompat's `m < m + 1`; (γ) gives `n < m` symmetrically. So `a ≠ b` by T3. NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`. If `m < n`, then `k = m + 1 ≤ n`…"
**Issue**: In clause (β) we already have `k = m + 1 ≤ n` (hence `m < n`) directly; in clause (γ) we already have `k = n + 1 ≤ m` (hence `n < m`). The step "NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`" introduces a branching disjunction that the case split already specifies, then recovers the facts clause (β) / clause (γ) supplied. The "if `m < n`" / "if `n < m`" branches correspond exactly to (β) / (γ) — the trichotomy invocation adds a layer of indirection without sharpening the argument.
**What needs resolving**: —

### T1 transitivity case `k₁ < k₂` leans on "`cₖ₁` exists" without stating the index bound explicitly
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: T1, proof part (c) Case `k₁ < k₂`: "If `a < b` via T1(i): `aₖ₁ < bₖ₁ = cₖ₁` with `k₁ ≤ m`, and the existence of `cₖ₁` gives `k₁ ≤ p`; position `k₁` witnesses `a < c` via T1(i). If `a < b` via T1(ii): `k₁ = m + 1 ≤ n`, and `cₖ₁` exists, so `m + 1 ≤ p`; `k₁` witnesses `a < c` via T1(ii)."
**Issue**: The bound `k₁ ≤ p` (resp. `m + 1 ≤ p`) needed for the T1(i) / T1(ii) witness is justified by "the existence of `cₖ₁`" / "`cₖ₁` exists". The operative chain is `k₁ < k₂ ≤ p` (from the `b < c` witness, case (i) via `k₂ ≤ p` or case (ii) via `k₂ = n + 1 ≤ p`), which yields `k₁ < p` and thus `k₁ ≤ p`. That the component `cₖ₁` is well-defined follows from that bound, not the reverse — the proof elsewhere walks `≤`-vs-`<` chains in full detail, so the informal shortcut reads out of register with the surrounding style.
**What needs resolving**: —

VERDICT: REVISE
