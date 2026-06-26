S7 is the load-bearing claim here. I'll trace each step of the proof before reporting.

**Well-definedness:** The order of derivation is correct — T4-validity of `a` is established first (S7a + T10a.4), then T4b's projections are invoked, then T4a gives field non-emptiness, then T0's comprehension places `origin(a) ∈ T`, then NAT-card computes `zeros(origin(a)) = 2`. The NAT-card invocation is sound: the zero-index set `{#N(a)+1, #N(a)+#U(a)+2}` ⊆ `{1,...,p}`, and the strictly-increasing enumeration of length 2 witnesses `|S| = 2`. The step `#N(a)+#U(a)+2 > #N(a)+1` follows from `#U(a) ≥ 1` (T4a), and the proof correctly assembles this before invoking NAT-card.

**Identification:** Grounded axiomatically in S7a. No derived step is needed.

**Uniqueness:** S7d separates distinct documents at the event level; GlobalUniqueness lifts event-distinctness to address-distinctness. The preconditions of GlobalUniqueness (allocation events under T10a, outputs in T) are met through S7d + S7a. The chain is valid.

**Permanence:** Grounded in S0 plus the deterministic computation of `origin(a)` from tumbler components alone. Correct.

The cross-claim dependency graph is acyclic and all cited foundations are used. No missing case, no broken precondition chain, no unsound proof step found.

---

### S7b: "all four fields present" interpretation attributed to T4 but belongs to T4b

**Class**: OBSERVE
**Foundation**: T4b (UniqueParse) — `dom(E) = {t ∈ dom(N) : zeros(t) = 3}` is the site that licenses the reading "zeros = 3 ↔ all four projections defined." T4 alone supplies the Exhaustion Consequence `zeros(t) ∈ {0,1,2,3}` and the zero-count definition, but not the four-projection domain characterisation.
**ASN**: S7b — "By T4's field correspondence, zeros(a) = 3 means all four identifying fields — node, user, document, element — are present"
**Issue**: A reader following the T4 citation to understand this gloss will not find the four-projection domain characterisation there — it lives in T4b's postconditions. T4b is in S7's (not S7b's) dependency list, so the gloss's sourcing is misattributed.
**What needs resolving**: The gloss should cite T4b (or T4 + T4b) rather than T4 alone, since the specific claim that `zeros = 3 ↔ dom(E)` is defined is T4b's postcondition.

---

### S7: S4 cited parenthetically in proof prose without formal dependency or use

**Class**: OBSERVE
**Foundation**: Not a listed foundation — S4 does not appear in the foundation statements.
**ASN**: S7 (StructuralAttribution), Permanence step — "Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable."
**Issue**: S4 is cited parenthetically but is absent from S7's formal dependency list. No proof step invokes S4; the formal Permanence argument rests on S0 and the fixed-point property of tumbler components. The informal citation creates a dangling reference: a reader trying to locate S4 finds no declaration in the provided content.
**What needs resolving**: Either add S4 to S7's dependency list and exhibit the formal step that consumes it, or remove the `(S4)` parenthetical so the informal prose matches the formal dependency set.

---

### S7 postcondition implies T4-validity of origin(a) without formally stating it

**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing) — T4-validity requires zeros ≤ 3, no adjacent zeros, nonzero first, nonzero last; the proof establishes only `zeros(origin(a)) = 2` and `origin(a) ∈ T` as explicit conclusions.
**ASN**: S7 formal postconditions — "zeros(origin(a)) = 2 obtained by applying T4's zero-count definition … placing origin(a) at the document level in T4's hierarchy"
**Issue**: "At the document level in T4's hierarchy" carries an implicit claim of T4-validity of `origin(a)`. The proof establishes the zeros count and T-membership, but never states the remaining T4 conditions for `origin(a)` as conclusions. They are derivable from assembled material — nonzero-first/last from T4b's `ℕ⁺` postcondition on `N(a)` and `D(a)`, no-adjacent-zeros from `#U(a) ≥ 1` (T4a) giving separator separation ≥ 2 — but a downstream consumer applying T4b to `origin(a)` on the basis of S7's postconditions alone will find T4-validity unestablished.
**What needs resolving**: Either (a) add T4-validity of `origin(a)` as an explicit postcondition, grounded by the no-adjacent-zeros and nonzero-boundary conditions already implicit in the proof, or (b) rephrase "at the document level in T4's hierarchy" as a gloss on `zeros = 2` only, so the postcondition makes no implicit T4-validity claim.

---

VERDICT: OBSERVE