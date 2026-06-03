# Review of ASN-0077

I read the full ASN and checked each claim's proof, with particular attention to the operation specifications (SHOWORIGIN_I, SHOWORIGIN_V), the preservation claims under arrangement-modifying transitions, the boundary cases, and the discharge of foundation antecedents.

## Verification notes

I checked the points where prior cycles tend to fail, and found them discharged:

- **S3★ antecedent discharge.** Every application of S3★ (which requires `subspace(v) ∈ {s_C, s_L}`) is preceded by an explicit discharge via S3★-aux (or, in the link-subspace edge case, via C0a): O2, O7 step (3), O11 (⊆) step (3) and Case (i), O11' (⊆), and the SHOWORIGIN_V precondition all do this. No bare S3★ application remains.
- **Boundary cases.** Empty intersection (I-span), singleton I-span (with the full three-length-case argument, including the `#b > #a` zero-count/prefix-coincidence step), cross-subspace I-span, link-subspace V-span, empty document (precondition (iii) unsatisfiable), and empty-restriction-within-non-empty-document (`u ∈ dom(M(d))` forced by (vi)) are all handled.
- **Negative claims are load-bearing and witnessed.** O13 (K.μ⁻ admissibility loss) and O14 (K.μ~ non-preservation) correctly bound the preservation regime and each has a concrete witness in the worked example; the incomparability in O14 (`{d₁}` vs `{d₃}`) checks out, and the K.μ~ admissibility obligations (a)(b)(c) are individually discharged.
- **Multi-step lemmas.** O5★/O6★/O11★/O11'★/O11★★ are correct inductions; the exhaustiveness in O11★★ rests only on the binary modifies-`M(d)`/leaves-`M(d)`-fixed partition (given the hypothesis excludes K.μ⁻/K.μ~ on `d`), not on enumerating a complete transition vocabulary, which is the right move.
- **Foundation hygiene.** All cross-ASN references are to foundation ASNs (0034, 0036, 0047, 0053, 0058, 0098); ASN-0093 appears only inside the embedded foundation claim text of 0047/0098, not in 0077's own argument. No notation is reinvented.
- **wp analysis** is non-trivial (single-origin characterisation; document-membership characterisation) and concretely evaluated at both satisfying and falsifying states, including the `d_q = d₂` falsification that operationally confirms O4.

I could not find a skipped case, an unproven "by similar reasoning," a checkmark standing in for a proof, an unaddressed invariant conjunct, or a missing edge case. The cross-state depth identifications in O11 sub-case (a) and O11.1 are explicit about `m' = m` via S8-depth and the state-independence of `subspace(v)`/`#v`.

## OUT_OF_SCOPE

The ASN's own Open Questions correctly defer to future ASNs: link origins surfaced from an I-span (the I-span lift intersects only `dom(C)` by deliberate definitional choice), surfacing the intermediate transclusion chain, the native-vs-transcluded distinction, and historical containment from `Σ.R`. These are new territory, not defects here.

The ASN defines abstract state-derived sets (`origins_I`, `origins_V`), two operation arities with explicit pre/postconditions and a read-only frame, and invariants (permanence, monotonicity, preservation/non-preservation) stated so an alternative implementation must satisfy them. It has not drifted into implementation mechanics — the closing paragraph explicitly keeps the realization mechanisms (spanfilade, granfilade, homedoc records) outside the guarantees.

VERDICT: CONVERGED
