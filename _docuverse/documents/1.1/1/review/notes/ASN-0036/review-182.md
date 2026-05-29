# Review of ASN-0036

I checked every proof (S0, S1, S4, S5, S7, S8, D-CTG-depth, D-SEQ) for case completeness, boundary handling, and hand-waves. The mathematics is sound. Specifics below, then OUT_OF_SCOPE notes.

## Proof verification (no REVISE items found)

- **S8 partition.** Coverage and uniqueness are both established. The within-subspace incompatibility lemma correctly splits `j < m` and `j = m`, and explicitly collapses to `j = m` at `m = 2` (no excluded case is imagined). Cross-subspace uniqueness via T5 + T10 is complete — every point of `[v, shift(v,1))` is shown to extend `[v₁]`, and non-nesting prefixes discharge disjointness. The half-open upper bound is handled. Empty arrangement is treated (vacuous). ✓
- **D-CTG-depth.** The infinitely-many-intermediates contradiction with S8-fin is valid; `w` is verified to satisfy S8a before invoking D-CTG, and the `j = m−1` empty-range subcase is consistent. ✓
- **D-SEQ.** Steps 1–4 cover `m = 2` (vacuous shared prefix) and `m ≥ 3` (via D-CTG-depth + D-MIN) separately; the `k`-value contiguity uses D-CTG legitimately at the common depth. ✓
- **S5.** Both cross-document and within-document constructions succeed for arbitrary `N`; S2/S3 are verified per construction, S0/S1 vacuously under identity transition. Witness documents have `zeros = 2`, consistent with S7d. ✓
- **S7.** Well-definedness, identification, cross-document uniqueness (S7d + T3), and permanence (S0 + deterministic field decomposition) are each shown. `zeros(origin) = 2` follows from the non-empty field segments. ✓
- **Worked example.** Σ₁–Σ₃ exercise S0/S3/S5/S7/S8/D-SEQ at depth 2; the depth-3 example and both contiguity-violation cases are concrete. Satisfies the concrete-example requirement. ✓

**Cross-references:** Only ASN-0034 (foundation) is cited by number — permitted. No improper cross-ASN references.

**Anti-bloat scan:** The S0 necessity argument, the Nelson/Gregory grounding quotes, and the S7 "subtlety" paragraph all advance the "what must hold" derivation or state what `origin` does/does not do — none is flaggable meta-prose under the ASN's stated grounding methodology. No "Why the axiom is needed" sub-paragraphs, no document-ordering justifications, no consumer-inventory definitions, no duplicated forward-deferral remain. The domain-restriction axiom / S8a pairing is a legitimate axiom-plus-derived-per-component-form (S8a carries its own `By T0` derivation and is the citable handle used throughout the proofs), not accretion. Recent trimming appears complete.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN/S2
Whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants — including insertion at an occupied V-position — is operation-specific frame/postcondition territory, correctly deferred (and already listed in Open Questions).

### Topic 2: Subspace alignment (`subspace(v) = v₁` matching the I-address element field)
Treated as an operations-layer obligation rather than a state invariant; correctly out of scope and noted in Open Questions.

### Topic 3: Canonical choice of V-position depth `m`
The strand fixes only `m ≥ 2`; the canonical value is an operation-layer allocation convention. Out of scope.

VERDICT: CONVERGED
