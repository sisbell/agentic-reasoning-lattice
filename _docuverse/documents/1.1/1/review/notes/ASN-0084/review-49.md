# Review of ASN-0084

## REVISE

### Issue 1: Foundation property S8 renamed "SpanDecomposition"

**ASN-0084, throughout (R-SP, R-NS, R-BLK, Invariant preservation)**: "S8 (SpanDecomposition) with its clauses S8(a) ... and S8(b)"

**Problem**: The foundation (ASN-0036) names this property **S8 — CorrespondenceRunPartition**, and the ASN under review consistently calls it "SpanDecomposition." Worse, the foundation S8 has postconditions (a) lockstep-displacement, (b) well-defined label, (c) unique decomposition; ASN-0084 silently rebinds "S8(a)" to mean *uniqueness of containing run* (foundation's (c)) and "S8(b)" to mean *consistency* (foundation's (a)). A reader cross-referencing the foundation will read the wrong clause. Standard 7: an ASN must use the foundation's notation, not reinvent it.

**Required**: Use the name CorrespondenceRunPartition, and either adopt the foundation's clause lettering or introduce locally-disambiguated labels (e.g., S8-uniq, S8-cons) that do not collide with the foundation's own (a)/(b)/(c).

### Issue 2: Citations to ASN-0036 properties not present in the foundation

**ASN-0084, R-NS(NS-inv) and R-SP**: "ShiftPreservation (ASN-0036) gives ... subspace_I(shift(a_j, k)) = subspace_I(a_j)"; "the S8 corollary (preservation of subspace_I, zeros, and #E ...)"; and "per OrdinalExtraction, ASN-0036."

**Problem**: The foundation ASN-0036 exposes **OrdShiftHom (OrdinalShiftPreservation)** — `subspace(shift(v,n)) = subspace(v)` on V-positions — but no "ShiftPreservation" giving field-level preservation (subspace_I, zeros, #E) on **I-addresses**, no "S8 corollary" about field preservation across runs, and no "OrdinalExtraction." These citations cannot be verified against the foundation; the field-preservation step in S8(b)-corollary discharge therefore rests on an unestablished claim. (Separately, the "singleton-tumbler identification" is *defined in this ASN* yet attributed "of ASN-0036.")

**Required**: Either cite the actual foundation property names, or — if these results do not exist in ASN-0036 — establish the I-address field-preservation step within this ASN rather than deferring to a non-existent export. Fix the singleton-identification attribution.

### Issue 3: Meta-prose justifying proof ordering and reading conventions

**ASN-0084, R-NS "Dependencies and direction" and "Citation convention"**: "R-NS is therefore upstream of the bijection lemmas: R-PPERM and R-SPERM cite R-NS(NS-π) ... and R-NS does *not* depend on the bijectivity ..."; "Throughout the remainder of this ASN, when an invariant proof ... splits into 'subspace-S' and 'non-S' cases, the non-S case is dispatched by citing R-NS ..."

**Problem**: These paragraphs do not advance any claim — they argue document ordering (non-circularity) and instruct the reader how to read later sections. This is exactly the forward-reference accretion the note's classifier targets ("prose justifies document ordering," meta-prose in structural slots).

**Required**: Delete. The lemma's actual dependencies are already recorded in its *Depends on*-style clause; cite R-NS at each consumer without a global narration of the citation policy.

### Issue 4: The same invariant-transport argument is repeated three times

**ASN-0084, "Invariant preservation" paragraph, R-NS(NS-inv), R-SP ("S0, S1, S4, S7 ...")**

**Problem**: The argument "C' = C plus two-stream separation transports every Σ.C invariant by identity" is stated nearly verbatim in three sections, and the "multiset-of-I-addresses preserved by bijectivity of π ⇒ S5 preserved" argument appears in both the Invariant-preservation paragraph and R-SP. Two paragraphs saying the same thing in different words is noise the precise reader must reconcile.

**Required**: State the C'=C transport and the S5/multiplicity argument once, and have R-SP cite that single location rather than re-deriving.

### Issue 5: Use-site inventories and "we do not repeat" forward-management prose

**ASN-0084, "OrdinalShift consumers under the identity extension" and "Reduction of compound shifts"**: "Every appearance of 'by associativity' ... below this point cites the Extended Associativity reductions of the present paragraph; we do not repeat the case analysis at each consumer."

**Problem**: The bulleted enumeration of which downstream consumers (TS2, TS5, OrdShiftHom, Extended Associativity) extend to n=0, followed by an explicit "we do not repeat" management statement, is a use-site inventory rather than content advancing the definitions. The n=0 identity extension is a one-line fact; the surrounding inventory is accreted meta-prose.

**Required**: Keep the single substantive fact (identity convention extends shift to n=0) and drop the consumer roster and the repetition-management sentence; let each later use stand on the convention directly.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The Open Questions correctly defer generalization beyond the 3-/4-cut forms; characterizing the permutation class for k>4 is new territory, not a defect here.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Whether a composition of rearrangements is itself a single rearrangement is a future-ASN concern; this ASN's contract is a single REARRANGE_K and need not close composition.

### Topic 3: Conditions under which canonical-run count increases
**Why out of scope**: R-BLK honestly notes it does not characterize which pre-state pairs produce post-state mergeability; quantifying run-count growth is legitimately a separate analysis.

VERDICT: REVISE
