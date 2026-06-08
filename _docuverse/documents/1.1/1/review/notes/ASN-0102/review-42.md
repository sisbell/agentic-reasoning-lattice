# Review of ASN-0102

I checked the operation definition, every X-claim's derivation, all six worked examples (arithmetic and class-tiling), the `wp(COPY, S3★)` reduction, and the full invariant-discharge in X14 (J0/J1★/J1'★, P3/P4★/P7/P7a, the Class-(a) vacuity argument). The mathematics is sound: the three-class V-position tiling in X16 is disjoint and gap-free, the New/Old split in X14 discharges the provenance couplings correctly, the snapshot-resolution argument (X10b/X15) is load-bearing and correctly justified, and every worked-example table is arithmetically correct, including the coalescing case where the X8 and X12 merge predicates actually fire. The findings below are confined to accreted meta-prose, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Trailing summary prose after the proof obligation is already discharged
**ASN-0102, X14 (final paragraph)**: "Origin-traceability (X6) and containment-recording (X14) are independent facts: the former says where the content was born, the latter says which documents now hold it — COPY establishes both."
**Problem**: By the time this sentence is reached, X6 and X14 have both been fully proven. The sentence restates their conclusions in apposition without advancing any reasoning — essay content in a proof slot. It is the kind of meta-prose a precise reader must skip to find the next obligation.
**Required**: Delete. If a one-line pointer is genuinely wanted, fold it into the claim table, not the proof body.

### Issue 2: Well-typedness of the *effect's* `Σ.R`-write proved inside a *precondition* bullet
**ASN-0102, PC2**: "The pair `(a_j + i, d)` that COPY's effect writes into `Σ.R ⊆ T_elem × E_doc` ... is well-typed on both factors: the `E_doc` side by `d ∈ E_doc` here, and the `T_elem` side because `Element(a_j + i)` holds — by C1 ... and by S7b ..."
**Problem**: PC2 is a precondition slot; it should state what `COPY` requires of its inputs. The quoted material instead discharges a downstream obligation about the effect's provenance write (`Σ.R` well-typedness), using C1/S7b. That reasoning is already carried by X14 (which establishes the same `Element(a_j+i)` fact for P7/P4★). Placing it in the precondition is structural-slot drift and duplicates X14.
**Required**: Reduce PC2 to its actual precondition (`d ∈ E_doc`). Move (or drop, since X14 covers it) the `T_elem`/`Element` justification into the X14 discharge where the `Σ.R` write is argued.

### Issue 3: Editorial gloss restating a foundation distinction without advancing the effect
**ASN-0102, Provenance effect clause**: "This is a state component distinct from the *derived* containment relation `Contains_C` (which reads off `Σ'.M` automatically): the provenance relation `Σ.R` records the fact persistently."
**Problem**: The stored-vs-derived distinction between `Σ.R` and `Contains_C` is fixed by ASN-0047's definitions and is not specific to COPY. The sentence explains a foundation fact rather than the COPY effect, and the "persistence" point is then re-asserted in X14's tail ("By content-containment permanence this record persists across subsequent states"). The persistence claim is made in two places.
**Required**: State the effect (`Σ'.R = Σ.R ∪ {(a_j+i, d)}`) plainly; let X14 carry the single permanence statement. Remove the duplicated gloss.

## OUT_OF_SCOPE

The four Open Questions (re-displacement of copied content, transitive containment when a referencing document is itself a source, time-varying views, identity under an unreachable allocator) are correctly deferred — they concern operations and reachability guarantees beyond a single COPY transition. No action.

VERDICT: REVISE
