# Review of ASN-0036

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Maximal decomposition uniqueness
S8 proves existence of a finite correspondence-run decomposition via singleton construction. Whether the maximal decomposition (fewest runs, obtained by greedily merging compatible singletons) is unique — and whether it is the canonical representation for implementation — is a question for a future span algebra or enfilade representation ASN.
**Why out of scope**: S8's existential claim is fully proved; canonicality is a separate concern.

### Topic 2: Sharing inverse computability
S5 establishes that the sharing set `{(d, v) : M(d)(v) = a}` is determined by the state. The open question about cost bounds for this reverse lookup (given an I-address, which documents reference it?) matters for link traversal and attribution queries but requires index-level analysis beyond the two-stream model.
**Why out of scope**: The state model supports the query; the efficiency of its extraction is an implementation and indexing concern.

### Topic 3: D-CTG preservation by editing operations
The ASN correctly identifies that "whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG and D-MIN is a verification obligation for each operation's ASN." This is the right separation — the invariant is defined here, its maintenance is verified per-operation.
**Why out of scope**: New territory for operation ASNs, not an error in this one.

## Assessment

The proofs are thorough. Every theorem has a complete argument; no case is elided by "similarly" or checkmark. Key observations:

**S0–S1**: S1's derivation from S0 is clean and correctly distinguishes the domain-persistence corollary from the full immutability axiom.

**S4**: The derivation from GlobalUniqueness correctly traces the value-independence of address distinctness — none of the foundation properties (T9, T10, T10a, TA5) reference Val.

**S5**: Both constructions (cross-document and within-document) are verified against all four invariants S0–S3, including the non-obvious confirmation that non-injective M(d) satisfies S2 (functionality requires unique image per domain element, not injectivity).

**S7**: The well-definedness chain S7b → T4 → fields(a) → origin(a) is complete. The permanence argument correctly observes that origin(a) is a pure function of a's components, so it is state-independent.

**S8 partition proof**: The within-subspace uniqueness argument (case analysis on first divergence at j < m and j = m) is the load-bearing step and is fully worked. The cross-subspace argument handles m = 1 and m ≥ 2 separately; the m = 1 case requires its own proof (not subsumed by the T5/T10 argument used for m ≥ 2) and is correctly provided — showing every tumbler in [[S₁], [S₁+1]) has first component S₁ by exhaustive case analysis on T1.

**D-CTG-depth**: The infinity-by-construction argument (varying a single intermediate component to produce unboundedly many intermediates, contradicting S8-fin) correctly establishes the shared-prefix reduction. The concrete depth-3 illustration ([S, 1, 5] and [S, 2, 1] forcing infinitely many intermediates) grounds the abstract argument.

**D-SEQ**: The four-step derivation (shared prefix → minimum k → contiguity → finiteness) is clean. The m ≥ 2 precondition is necessary and the ASN correctly explains why m = 1 fails (subspace/ordinal conflation under shift).

**Worked example**: All nine invariants (S0, S3, S5, S6, S7, S8, S9, D-CTG, D-SEQ) are verified against three concrete state transitions (creation, transclusion+append, deletion). The correspondence-run decompositions are explicitly verified per-element.

VERDICT: CONVERGED
