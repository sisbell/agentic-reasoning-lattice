# Review of ASN-0121

The mathematics of this ASN holds up under pressure — I verified the forcing argument, all three weakest preconditions including the ghost-pre-coverage and self-retraction hazards, the tumbler arithmetic in the boundary-straddling home-span example, and Traces 1–3 and 5–7 by direct computation. One worked trace, however, posits a state its own locality lemma proves impossible, and the anti-bloat pass surfaces three duplication patterns. Verdict: REVISE.

## REVISE

### Issue 1: Trace 4 asserts a nullification with no witness in the store, and its conclusion depends on the missing witness

**ASN-0121, "A worked instance," Trace 4**: "If instead `a₁ ∈ nullified(Σ)`, then `addressable(Σ) = {a₂, a₃}`, and Trace 1's `q = (∗, X, Y, ∗)` now yields `findlinks(q, Σ) = ∅`"

**Problem**: `nullified(Σ)` is not a free parameter — FL-LOC, this ASN's own claim, makes it a function of `Σ.L`, determined through `L_R^Σ` by stored values. Over the enumerated store `{a₁, a₂, a₃}` with types `τ, τ, σ` and to-coverages in the content subspace, `nullified(Σ) = ∅` necessarily: no stored link has retraction-class type, and even if `τ` or `σ` were the retraction class, no to-coverage contains a link address. So "`a₁ ∈ nullified(Σ)`" is unsatisfiable without adding a retraction tuple to `dom(Σ.L)`. Once added, both stated consequences break:

1. `addressable(Σ) = {a₂, a₃}` is false — the retractor itself is in `dom(Σ.L)` and (unless self-covered, which the trace does not construct) is addressable, so `addressable(Σ)` has at least three members.
2. `findlinks(q, Σ) = ∅` is witness-dependent, not forced. This ASN works over the full vocabulary with no RetractionDirectionality discipline (FL-WP case (a) says so explicitly), so an attribution-bearing retractor is admissible: `r` with `e₁ = {(x, δ(1,#x))}`, `e₂ = {(a₁, δ(1,#a₁)), (y, δ(1,#y))}`, retraction-class `e₃` is L3/L4-legal, lies in `L_R^Σ`, nullifies `a₁`, is not self-covered, and satisfies `(∗, X, Y, ∗)` — `lift(e₁, X)` holds via `x`, `lift(e₂, Y)` holds via `y`. With that witness the result is `{r}`, not `∅`.

**Required**: Construct the retractor explicitly — e.g. `r₄ = [1,0,1,0,1,0,2,4]` (the frontier after `a₃`) with value `(∅, {(a₁, δ(1,#a₁))}, Θ_ρ-class type)`. Then `nullified(Σ) = {a₁}` by computation, `addressable(Σ) = {a₂, a₃, r₄}`, and `findlinks((∗, X, Y, ∗), Σ) = ∅` follows because `a₂, a₃` fail the from-slot and `r₄` fails it by FL-EMP's link-side rule (`lift(∅, X) = false`). This repairs the trace and makes it exercise the determinacy of `nullified` rather than contradict it.

### Issue 2: The snapshot reading is stated twice, the second time as a relocated stub, with a meta-disclaimer

**ASN-0121, end of FL-CMP**: "The snapshot reading is FL-DEF as a membership test, FL-SND forward and FL-CMP backward; it carries no content beyond the pair." — and **"The result is a current snapshot," opening paragraph**: "The result's relationship to the link store *as it stands at the moment of inquiry* is fixed by FL-DEF's snapshot reading, recorded with FL-CMP above: the faithful, exhaustive satisfying subset of the currently addressable links."

**Problem**: The snapshot reading is delivered in full under FL-CMP, then restated as the opening of a section titled for it, whose actual content is something else (the two stability facts and FL-MON). The opening paragraph is relocated-content residue — it defers back to FL-CMP and re-says it. The sentence "it carries no content beyond the pair" is a disclaimer about the prose itself, not a specification statement: meta-prose defending against an objection rather than advancing a claim.

**Required**: State the snapshot reading once. Delete the disclaimer sentence; open the "current snapshot" section directly with the two stability facts (or fold them under FL-CMP and drop the section header).

### Issue 3: FL-LOC re-derives the nullified-locality argument given two paragraphs earlier

**ASN-0121, FL-LOC proof**: "nullified is a function of `Σ.L` (it is defined through the retraction relation `L_R^Σ`, itself determined by `Σ.L` — selected from `dom(Σ.L)` by the arity-3 and slot-3 coverage tests on stored values, as recorded above)"

**Problem**: This is a near-verbatim repetition of the structural argument in "The answer is forced" ("`nullified(Σ)` is a function of `Σ.L` *alone* — it is defined through the retraction relation `L_R^Σ`, which is itself determined by `Σ.L`: a projection of the arity-3 slice of the link store, selected from `dom(Σ.L)` by the arity-3 and slot-3 coverage tests on stored values"), and the duplication is self-acknowledged by "as recorded above." The FL-LOC claims-table row carries the same parenthetical derivation a third time.

**Required**: Derive once, at the first site; FL-LOC's proof should cite it ("nullified is a function of `Σ.L`, as established above") without re-running the parenthetical; trim the table row to the statement.

### Issue 4: FL-REACH opens and closes with the same assertion

**ASN-0121, "Cross-document reach," opening**: "The search is therefore intrinsically a global content-identity sieve over the link store, not a per-document enumeration." — and **closing paragraph**: "a complete discovery must — and FL-REACH does — range over the entire link store rather than the local arrangement."

**Problem**: The section's first and last paragraphs make the same assertion in different words, bracketing consequences (a)–(d) that already carry the substance (in-links covered by (a), transclusion by (b)). The closing's only novel material is the motivational enumeration ("in-links, its home, the transclusions of its endpoints, and the versions of its connected content"), which is rhetorical synthesis, not new specification content.

**Required**: Cut the closing paragraph, or reduce it to the one novel clause and fold that into consequence (a).

## OUT_OF_SCOPE

### Topic 1: Result presentation — ordering and enumeration of the answer set
Nelson's text says the operation "returns a list"; this ASN correctly specifies a set. Any ordering or incremental-enumeration contract belongs with the paginated retrieval operation (FINDNEXTNLINKSFROMTOTHREE), which the scope list already excludes.

**Why out of scope**: The set is the right abstraction for what the answer must contain; presentation order is a separate operation's contract, not an error here.

### Topic 2: Alignment with ASN-0086's Observe_K
ASN-0086's layer-level query matches by pattern containment (`F̂ ⊆ coverage(F)`) over the active subset, while findlinks matches by coverage overlap (`touch`) over `addressable(Σ)`. Whether one is expressible through the other, and which the relational layer should route through, is a valid alignment question.

**Why out of scope**: The two primitives serve different layers over the same store; reconciling them is new territory for a future ASN, not a defect in this operation's specification.

VERDICT: REVISE
