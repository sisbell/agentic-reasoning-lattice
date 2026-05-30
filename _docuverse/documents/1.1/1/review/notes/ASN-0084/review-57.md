# Review of ASN-0084

## REVISE

### Issue 1: R-SP re-discharges invariants already established generically
**ASN-0084, R-SP proof**: "We discharge Q clause-by-clause, leaning on the prior derivations." followed by per-clause re-proofs of S0, S1, S2, S3, S4, S5, S7, S7a, S7b, S7d, D-CTG, D-CTG-depth, D-MIN, D-SEQ, S8a, S8-fin, S8-depth.
**Problem**: The end of R-PPERM and R-SPERM already states "it therefore constitutes an arrangement rearrangement, and the invariant preservation established above applies" — meaning the generic "Invariant preservation" paragraph already discharged every one of these clauses. R-SP then re-walks the identical list (C-transport for S0/S1/S4/S7*, bijectivity for S2, R-RI for S3, multiset preservation for S5, dom-equality for D-*). The only genuinely new content is the wp framing and the B' = R-BLK(B) run-level documentation for S8. The clause-by-clause re-derivation is the accretion: a reader must read the same discharge twice.
**Required**: Collapse the S0–S7d and D-CTG/D-SEQ/S8a/S8-fin/S8-depth clauses to a single citation of the generic result ("these are discharged generically above, since REARRANGE_K is an arrangement rearrangement") and retain only the S8 run-level verification and the wp statement.

### Issue 2: "Σ.C is unchanged" is triple-justified
**ASN-0084, "C-transport"**: "C' = C (the rearrangement definition), and the two-stream separation of the ASN-0036 state model — Σ.C and Σ.M(d) are distinct components, so no mutation of Σ.M(d) can alter Σ.C — together with S0 (content immutability) make 'Σ.C is unchanged' immediate".
**Problem**: Three independent grounds (the rearrangement definition's `C' = C`, the two-stream separation, and S0) are stacked to establish a fact the first ground already gives outright. The middle clause is defensive meta-prose explaining *why* the state model keeps streams separate rather than advancing the argument.
**Required**: State once: "C' = C by the rearrangement definition, so every Σ.C-only invariant transports by identity." Drop the two-stream and S0 over-justification.

### Issue 3: Tiling "verification" restates commutativity as filler
**ASN-0084, after REARRANGE_K (compound-shift tiling)**: "The total width is w_β + w_μ + w_α. We need this to equal |[c₀, c₃)| = w_α + w_μ + w_β. Trivially: w_β + w_μ + w_α = w_α + w_μ + w_β."
**Problem**: A sentence that "needs to show" an equation and then discharges it with "Trivially: A = A under reordering" carries no content. The same tiling fact is then re-established rigorously two sentences later ("the three ranges tile [c₀, c₃) exactly"), so the trivial-commutativity sentence is pure padding.
**Required**: Delete the "We need this to equal… Trivially…" sentences; keep only the ordinal-range tiling argument that actually does the work.

### Issue 4: "Reduction of compound shifts" duplicates the associativity steps inside R-PIV/R-SWP
**ASN-0084, "Reduction of compound shifts (R-P2, R-S2, R-S3)"** vs **R-PIV / R-SWP**: the standalone section derives `c₀ + w_β + j = (c₀ + w_β) + j` and `c₀ + w_β + w_μ + j = ((c₀ + w_β) + w_μ) + j` via Extended Associativity; R-PIV then re-derives "By associativity of ordinal addition, c₀ + (w_β + j) = (c₀ + w_β) + j, so these are well-defined" and R-SWP repeats "By associativity, c₀ + (w_β + j) = (c₀ + w_β) + j, so these are well-defined."
**Problem**: The well-definedness-by-associativity argument is stated in three places. Either the standalone section is the canonical home (and R-PIV/R-SWP should cite it) or it is redundant; as written, all three carry the full derivation.
**Required**: Keep the reduction once and have R-PIV/R-SWP cite it by name rather than re-derive.

### Issue 5: Extended Associativity carries an unused use-site inventory
**ASN-0084, "Extended Associativity"**: "The same identity convention extends TS2 (ShiftInjectivity) and OrdShiftHom (a) … to n = 0, since shift(v, 0) = v; TS5 (ShiftAmountMonotonicity) extends to a zero amount via TS4 (StrictIncrease), since shift(v, 0) = v differs from shift(v, n) > v for n ≥ 1. TS4 itself requires n ≥ 1: shift(v, n) > v fails at n = 0 under T1 irreflexivity."
**Problem**: This is an enumeration of which foundation lemmas the n = 0 convention "also extends," several of which (the TS5/TS4 zero-amount remarks) are never consumed by any subsequent proof step — the displacement remark reports directions read off the explicit formulas, not via TS5-at-zero. Enumerating downstream extensibility rather than using it is accretion.
**Required**: Retain only the extensions actually invoked (the `(c+j)+k = c+(j+k)` identity and the OrdShiftHom (a) n = 0 case used in Subspace confinement / R-COMM); delete the TS5/TS4 zero-amount commentary unless a proof step consumes it.

### Issue 6: R-SPERM's uniqueness-scope paragraph restates R-PPERM's
**ASN-0084, R-SPERM**: "As in R-PPERM, π is the unique such bijection when M(d) is injective on V_S(d); otherwise (under S5 sharing) it is the canonical representative whose action depends only on the cut sequence and region widths, not on the I-address fibre structure."
**Problem**: This reproduces, in different words, the entire "Uniqueness scope" discussion already given in R-PPERM (injective ⇒ unique; S5 ⇒ canonical representative up to fibre-permutation). Two lemmas in the same document say the same thing.
**Required**: State the uniqueness/S5-fibre discussion once (e.g., factor it into the ArrangementRearrangement definition or R-PPERM) and have R-SPERM cite it without restatement.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The ASN deliberately fixes n ∈ {3, 4} (CS1) and the Open Questions section flags generalization as future work; it is new territory, not a defect.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Whether two rearrangements compose to a single rearrangement is a property of sequences of operations, outside this single-operation contract; correctly deferred to a future ASN.

### Topic 3: Operational recovery of the maximal (canonical) partition from B'
**Why out of scope**: R-BLK exhibits a valid non-maximal B' and relies on foundation S8 for existence/uniqueness of the maximal partition; the merge-confluence algorithm is genuinely separate work, as the table and Open Questions both acknowledge.

VERDICT: REVISE
