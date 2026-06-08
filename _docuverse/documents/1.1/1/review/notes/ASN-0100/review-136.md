# Review of ASN-0100

This is a heavily-iterated, mathematically sound specification. I checked the substrate decomposition, the three-region effect, every invariant discharge (S0/P0, S2, S3★, D-CTG★/D-MIN★/D-SEQ★, S8a/S8-depth/S8-fin, S8★, the S7/L0/P6/P7 family), the provenance couplings (J0, J1★, J1'★, P4★, P4a, P7a), the wp analysis, and the boundary cases (prepend `j=0` full-clearance, append `j=N` no-K.μ⁻, empty document, residual-content subsequent-emission, deep `m_C=3` off-prefix D-CTG★). I found no correctness gap. The forced-ordering, uniqueness, and projection-shift derivations hold.

The findings below are accretion/exposition, per the `review-mode.anti-bloat` directive — not math errors.

## REVISE

### Issue 1: Duplicated worked-example skeleton (empty-document vs. re-insertion)
**ASN-0100, §A Worked Example** (the "Empty-document first insertion" and "Re-insertion into a cleared content subspace" examples)
**Problem**: Both examples instantiate the identical composite skeleton (a K.α batch + one K.μ⁺ + a K.ρ batch, no K.μ⁻, because `V_{s_C}(d)=∅`), and both re-run the same three-region verification and the same D-MIN★/D-SEQ★ checks on `{[s_C,1,...,1,k]}`. The only genuinely new content in the second example is the K.α *branch selection* (subsequent vs. first emission) and the V-index/I-chain decoupling point. The full second trace restates structure already established by the first — matching "two paragraphs say the same thing in different words."
**Required**: Collapse the re-insertion example to its delta — the residual-content branch firing and the observation that D-MIN★/D-SEQ★ are blind to the chain frontier index — without re-deriving the region partition and sequential invariants the empty-document example already exhibits.

### Issue 2: Overlapping well-definedness derivations in §Atomicity
**ASN-0100, §Atomicity and Canonical Order** (the post-state-uniqueness-by-component paragraph, the three-plus-one forced-ordering enumeration, and the "two representative comparisons" paragraph)
**Problem**: Three consecutive blocks all argue that the decomposition is well-behaved relative to the unique Σ': (a) a component-by-component uniqueness derivation, (b) a catalog of forced orderings each re-deriving a precondition-failure at length (K.α→K.α, K.α→K.μ⁺, K.α→K.ρ, K.μ⁻→K.μ⁺), and (c) a "full-shrinkage vs. canonical" comparison. The abstract guarantee is just "Σ' is unique and realizable as a valid composite, interleaving unobservable." The remaining detail is realization-mechanics scaffolding; the per-bullet precondition-failure re-derivations in (b) are the verbose essay-in-structural-slot pattern.
**Required**: Consolidate to the load-bearing claims (post-state uniqueness; the canonical decomposition is admissible; free interleavings reach the same Σ') and replace the per-ordering re-derivations with one-line citations to the relevant K-step preconditions.

### Issue 3: Forward deferral of a structural claim's own sub-case
**ASN-0100, §Cross-document independence**: "Cross-document independence extends to link projection; the `d' ≠ d` case is derived in INS.proj (§Coverage and link discoverability)."
**Problem**: A structural-invariant section forward-defers its own link-projection sub-case to a later section rather than stating it where the claim lives. This is the "defer forward to a downstream location" accretion pattern; the sentence advances no reasoning at its location.
**Required**: Either state the one-line `d' ≠ d` projection-invariance conclusion here, or drop the sentence (the cross-document frame already covers projection via LP4, cited downstream).

## OUT_OF_SCOPE

None. The §Bounding the Scope section and Open Questions correctly defer DELETE, COPY, REARRANGE, link-subspace insertion, version creation, and replication; these are not claims and need no flag.

VERDICT: REVISE
