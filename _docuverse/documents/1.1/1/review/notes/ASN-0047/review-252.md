# Review of ASN-0047

I checked the load-bearing proofs against their stated preconditions, traced the tumbler arithmetic in the worked examples, and looked for skipped cases and unsubstantiated "follows from" claims. Detail below, then the verdict.

## Areas verified (no defect found)

- **K.δ structural identities and zero-count progression.** The four K.δ-ID identities discharge `parent(e) ∈ E` and the level constraints correctly across k ∈ {0,1,2}; the worked-example arithmetic (`inc([1,2],2)=[1,2,0,1]`, `inc([1,2,0,1,0,1],0)=[1,2,0,1,0,2]`, `inc(d_src,1)` preserving `zeros=2`) is consistent with TA5(c)/(d) and T4b's parent projection.
- **FrontierEquivalence.** Both directions are genuinely proved; the reverse leans on T10a.6 to pin the producing event to A's `(t,0)` advance, and `inc(t,0) ∈ dom(A)` holds as a chain element. Sound.
- **D-SEQ★ derivation.** The m=2 and m≥3 cases are each self-contained; the `u_M` infinite-family construction against S8-fin correctly forces inner positions to 1. No hand-wave.
- **K.μ⁻ admissible-shape equivalence.** The reverse direction correctly treats value-preservation as making the candidate a restriction, then uses D-SEQ★ + the trailing-component bijection to force the suffix-prefix form. No circularity with K.μ~-FIX.
- **K.μ~ link-subspace fixity and necessity/sufficiency.** Sub-steps (1)–(4) are non-circular (K.μ~-FIX proved first, fixity then uses it + pre-state CL-UNIQ); clause (iv) is correctly identified as independent of (i)–(iii); the transposition witness discharges sufficiency. The "net-effect ≠ identity-map" distinction under transclusion (S5) is handled.
- **S8★ split.** The content projection's application of ASN-0036 S8 is correctly gated on OrdShiftHom(a) shift-closure; the link projection's omission of condition (c) via the trivial length-1 decomposition is internally consistent (it claims a partition + (a),(b), not maximality).
- **P7a / J0 temporal discharge.** The V-position witness is correctly placed at the composite endpoint Σ', not the post-K.α intermediate; the cross-document (transcluding) containing document is admissible for the existential.
- **Cross-references.** All ASN-number references are to foundation ASNs (0034/0036/0043/0045/0093); ASN-0040 appears only inside inherited ASN-0093 lemmas, not as a direct 0047 citation.

## REVISE

None. I was unable to identify a correctness gap, an uncovered boundary case (empty document, full clearance, first/subsequent emission, k=0 vs k=1 fork, interior replacement, orphan link), an unsubstantiated derivation, or a missing invariant conjunct that is not already discharged in the body or already addressed by the declined sprawl/matrix findings.

## OUT_OF_SCOPE

The eleven open questions correctly defer genuinely new territory (fork-arrangement subset constraints, transitive-transclusion provenance, link-subspace withdrawal/tombstoning, concurrency and address-exhaustion, node-baptism protocol mechanism, type-only links). None of these is an error in this ASN.

VERDICT: CONVERGED
