# Review of ASN-0042

I read the note in full and checked each proof against its preconditions, cases, and invariant conjuncts, with particular attention to the anti-bloat / forward-reference patterns flagged for this cycle.

## Correctness

The core proofs hold up under scrutiny:

- **O2** (exclusivity) discharges all four steps — non-emptiness (O4), chain comparability (covering-chain lemma), finiteness (`|C(a)| ≤ #a` via length-determined prefixes), unique maximum (O1b).
- **O3 / O8 / OwnershipDomainPermanence** correctly rest on the persistence triple (O12 principal-persistence, O13 prefix-immutability, B0 address-permanence) and rule out the equal-length displacer via O1b — no reversal or shortening case is skipped.
- **O10**'s non-coverage analysis is exhaustive: the Form A / Form B split on the component at position `#pfx(π)+1` covers every sub-delegate, both `zeros(pfx(π)) ∈ {0,1}` branches are handled, and the `hwm_0+1` selection is shown structurally outside every sub-delegate via PrefixBaptismCoupling + B1. The worked example exercises both the sibling-advance (`hwm_0=5`) and field-opening (`hwm_0=0`) branches, plus the node-level (`zeros=0`, Form A live) case.
- **O6 / O9** handle the `zeros ∈ {0,1}` field-structure cases with equality vs. proper-prefix distinctions made explicit, and the `owns` precondition discharges `T4(a)` via O17.
- Boundary cases are present: empty principal set (O14.1), node-vs-node disjointness (O9 via T10), self-ownership at the prefix boundary (`a₆ = pfx(π_A)`), reflexive cover (`covers_Σ*` Step 4).

Foundation usage is consistent — references are confined to ASN-0034 and ASN-0040 (both foundation), with no reinvented notation and no non-foundation cross-references.

## Anti-bloat check

The patterns flagged for this cycle are largely absent: no "Scope/Rationale/Why-the-axiom-is-needed" sub-paragraphs around axioms, no document-ordering justifications, no downstream-consumer enumerations in definitions, no duplicate paragraphs. The Nelson/Gregory design-justification sentences after each axiom are the spec's standard evidentiary convention, not accretion. The repeated persistence-triple invocation across O3/O4/O8/O10/OwnershipDomainPermanence is load-bearing per-proof citation, and the statement/proof/contract triplication is the spec's house structure. I did not have to skip meta-prose to follow any claim.

## OUT_OF_SCOPE

None to flag — the note stays within ownership state, predicates, and invariants, and correctly defers content effects (O10(b)), transfer (O3 closing remark), and federation (O9 / Open Questions) rather than specifying them.

VERDICT: CONVERGED
