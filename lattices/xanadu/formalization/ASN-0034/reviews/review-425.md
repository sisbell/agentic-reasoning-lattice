# Regional Review — ASN-0034/T6 (cycle 2)

*2026-04-23 03:37*

### T6 "T3-canonical" precondition has no operational content
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T6 intro: "For any T3-canonical, T4-valid tumblers `a, b ∈ T`, the following are decidable…" and Preconditions: "`a, b ∈ T` satisfy T3 (CanonicalRepresentation) and T4 (HierarchicalParsing)."
**Issue**: T3's formal statement is a universal biconditional `a = b ⟺ #a = #b ∧ …` — a theorem about all elements of `T`, not a predicate that some tumblers satisfy and others fail. No `a ∈ T` can "fail T3". The phrase "T3-canonical" therefore carves out no sub-domain and the Precondition slot's "satisfy T3" is vacuous. The phrase seems to gesture at Gregory's normalization routine (discussed in T3's body) but the formal T3 never introduces a "canonical tumbler" predicate. A reader trying to discharge the precondition has nothing to check.

### T3 forward direction leans on sequence extensionality not furnished by T0
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T3 proof: "Since `a` and `b` are finite sequences of the same length `n` agreeing at every position, they are identical as sequences by extensional equality."
**Issue**: T0's Axiom says `T` is "the set of finite sequences over ℕ" equipped with `#·` and `·ᵢ`, but does not axiomatize *what makes two sequences equal*. The forward direction silently invokes a sequence-extensionality principle — "a sequence is determined by its length and component projection" — that is not stated in T0's Axiom. The reverse direction is fine (Leibniz from `a = b`), but forward is where the mathematical content lives, and it is being attributed to T0 without T0 actually carrying it. Either T0's Axiom should make extensionality explicit (e.g., fix sequences as functions on initial segments and cite function extensionality), or T3 should declare the extensionality principle as an additional dependency.

### T6 Ingredient 3 cites NAT-discrete redundantly for ℕ-equality decidability
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T6 Ingredient 3: "Decidability of equality on ℕ follows from NAT-order's trichotomy together with NAT-discrete." T6 Depends: "NAT-discrete (NatDiscreteness) — … forecloses density for Ingredient 3."
**Issue**: Equality on ℕ is decidable from trichotomy alone: given `m, n ∈ ℕ`, exactly-one trichotomy tells us whether `m < n`, `m = n`, or `n < m` — equality is the middle branch. NAT-discrete's anti-density content does not enter the argument; it would be needed if we were constructing successors or bounding gaps, but componentwise comparison does not do that. The "forecloses density" gloss in Depends is hand-wave. Either drop NAT-discrete from this ingredient's justification (keeping it elsewhere in T6 where it is load-bearing, e.g., Ingredient 1's `tᵢ ≠ 0 ⟹ tᵢ ≥ 1`), or explain what density would otherwise break.

### T4 Axiom slot both posits positional constraints and the per-`k` written-form schema
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T4 Axiom: "Valid address tumblers satisfy: `zeros(t) ≤ 3`; [adjacency]; `t₁ ≠ 0`; `t_{#t} ≠ 0`. … The canonical written form of a T4-valid address tumbler is given by the following schema, quantified per-`k`: … `k = 3`: `t = N₁. … .Nₐ . 0 . … .Eδ`. In every case, `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present."
**Issue**: The per-`k` written-form schema is not an independent axiomatic commitment — it is a rendering of what the positional constraints already determine (via T4a's forward/reverse between positional form and segment non-emptiness). Placing both in the Axiom slot makes the axiom over-determined and makes T4a's theorem (positional ≡ segmental) sit between two clauses of the same axiom. Either the per-`k` schema belongs in a Definition/Consequence slot (derivable, not posited), or its appearance in the Axiom should be acknowledged as a notation-fixing stipulation rather than a constraint.

### T6 Depends omits NAT-card despite Ingredient 2 invoking `|·|`
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T6 Ingredient 2: "Let `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` as in T4 (with `|·|` the cardinality of a finite subset of ℕ, distinct from T0's tumbler-length `#·`), computable by one scan." T6 Depends lists T0, NAT-zero, NAT-discrete, NAT-order, T3, T4, T4a, T4b — no NAT-card, NAT-closure, or NAT-sub.
**Issue**: Other claims in this ASN that mention `zeros(t) = |{…}|` (T4, T4a, T4b) cite NAT-card directly. T6 re-states the same definition but does not carry the citation. Uniformity would be served by either citing NAT-card explicitly here too, or acknowledging transitive inheritance through T4 once and applying the same convention to T4a/T4b. (This sits alongside the previous finding that NAT-card is not defined anywhere in the ASN.)

VERDICT: OBSERVE

## Result

Regional review converged after 2 cycles.

*Elapsed: 2007s*
