# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable proof is an over-defensive mega-paragraph
**ASN-0086, Lemma — CoverageEqualityDecidable**: "The membership *test* therefore never enumerates a gap's interior; but the *soundness* of reading set-equality off the gap-indicators does rest on each gap being non-empty as a set of tumblers — were some gap empty…" … "that indicator constrains endpoints, not membership of a vacuous interval, and so could spuriously disagree on equal-coverage endsets (precisely the soundness hazard named above)."

**Problem**: The proof is a single ~600-word paragraph that names one empty-gap soundness hazard and then restates it three times ("were some gap empty…", "precisely the soundness hazard named above", "that indicator constrains endpoints, not membership of a vacuous interval"). The actual mathematical content — finite endpoint set, partition into point/gap cells, decide each cell's membership, test gap-emptiness via the immediate-successor witness `c_k.0` — is brief; the surrounding self-referential hand-wringing about *why* empty gaps must be excluded is exactly the essay-in-a-proof-slot pattern the anti-bloat classifier flags. A precise reader must work past the repeated meta-commentary to extract the algorithm.

**Required**: State the gap-emptiness handling once, mechanically: cells are points `{c_k}` and gaps `(c_k, c_{k+1})`; a gap is empty iff `c_{k+1} = c_k.0`; test indicators only on non-empty cells. Drop the repeated soundness-hazard restatements.

### Issue 2: Emit_K partiality characterization asserts an "exactly" via a pointer, not a derivation
**ASN-0086, Definition — Emit_K**: "`Emit_K` is total over substrate-conforming Σ (R0) and partial over the broader state-local-conforming sub-space: it is undefined *exactly* where the chain frontier is ill-formed (Remark — NestedLinkWitness)."

**Problem**: "undefined exactly where X" is a biconditional. The only support is a parenthetical pointer to Remark — NestedLinkWitness, which constructs *one* ill-formed-frontier state and proves the strict containment of conformance classes. It does not show (a) that `Emit_K` is undefined at that state, nor (b) that `Emit_K` is defined at *every* well-formed-frontier state — both needed for "exactly." The mechanism is also obscured: `a_emit(Σ, d)` is stated to be *total* (Definition — `a_emit`), so the partiality must arise from K.λ's "produced by `A_L(d)`" gate rejecting `a_emit`'s output when the homed-set is non-contiguous, but this is never said. "Undefined follows from the Remark" is a claim, not a proof.

**Required**: Either spell out both directions — K.λ's on-chain gate fails iff the homed-set is not a contiguous chain prefix (the P0f condition) — or soften "exactly" to the one direction actually supported.

### Issue 3: K.σ/K.α "out of scope" restated across sections
**ASN-0086, intro**: "(Document allocation (K.σ) and content emission (K.α), the other two primitive transitions in `→`, are inherited from ASN-0093; the reduction below concerns only the link store `Σ.L`.)"
**ASN-0086, Three Operations**: "(Document allocation K.σ and content emission K.α are also visible substrate changes, but lie outside this note's `Σ.L` scope and outside the three operations.)"

**Problem**: The same scope-exclusion of K.σ/K.α is asserted in the introduction and again at Three Operations (and gestured at a third time in the "Arrangement modification is out of scope" paragraph). This is the "two paragraphs say the same thing in different words" pattern — meta-prose justifying what the note does not cover, accreted across sections.

**Required**: State the K.σ/K.α scope exclusion once (the Three Operations placement is the natural home) and remove the duplicate.

## OUT_OF_SCOPE

### Topic 1: Concurrency and atomicity of Emit vs. Observe
The Open Questions already route observe-ordering, Emit/Observe atomicity, and the consistency model under which `A_K` transitions are observed to future work. These are genuinely new territory (a concurrency model), not defects in this note's single-writer `→`-sequential treatment.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The restriction to standard triples (`|Σ.L(a)| = 3`) is explicit, and the n-ary generalization is correctly deferred to an Open Question rather than half-built here.

VERDICT: REVISE
