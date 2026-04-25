# Regional Review — ASN-0034/T5 (cycle 1)

*2026-04-24 13:47*

### T1 trichotomy proof contains meta-prose explaining proof structure
**Class**: OBSERVE
**Foundation**: n/a (foundation ASN, internal review)
**ASN**: T1 (LexicographicOrder), proof of part (b) trichotomy
**Issue**: Two passages function as prose about the proof rather than steps within it. (1) "The proof splits first on whether any divergence position exists; when at least one does, NAT-wellorder applied to the nonempty set of such positions delivers a least element — the first divergence position `k` — after which a sub-split on which clause `k` satisfies completes the analysis. The three branches below are exhaustive." — this previews structure and asserts exhaustiveness; the cases themselves carry the burden. (2) "These three cases partition `T × T`, and in each case exactly one of the three relations holds." — restates the postcondition as a closing summary. A reader following the case body does not need either.

---

### T1 transitivity ends with summary sentence restating goal
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T1 (LexicographicOrder), proof of part (c) transitivity, final line
**Issue**: "In every realizable combination, a witness for `a < c` under T1 is produced. ∎" — a recap rather than a derivation. The last genuine step in each sub-case already names the witness; the closing sentence is meta-prose in a structural slot.

---

### T5 precondition `#p ≥ 1` is redundant with T0
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T5 (ContiguousSubtrees), statement and *Preconditions* bullet: "`p` is a tumbler prefix with `#p ≥ 1`"
**Issue**: T0 already guarantees `1 ≤ #a` for every `a ∈ T`, so if `p ∈ T` the bound `#p ≥ 1` is automatic. Stating it as a separate precondition is defensive and suggests the callee expects callers that do not satisfy T0.

---

### T5 "tumbler prefix p" is a non-term
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T5 statement: "For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` forms a contiguous interval under T1"; and *Preconditions*: "`p` is a tumbler prefix"
**Issue**: "Prefix" is defined as a relation (`p ≼ q`), not as a unary predicate on tumblers. Calling `p` a "tumbler prefix" in isolation is informal — the only well-typed statement is `p ∈ T`. A reader chasing the definition finds no "tumbler prefix" entry.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 624s*
