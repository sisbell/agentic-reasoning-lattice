# Review of ASN-0084

## REVISE

### Issue 1: Duplicated "arrangement-parametric" meta-commentary and downstream-consumer enumeration in Split/Merge
**ASN-0084, "Correspondence-Run Decomposition Transformation" (Split, Merge)**: Split closes with "The proof is arrangement-parametric: it uses only S8-cons of the original run and Extended Associativity, with no property specific to a particular arrangement." Merge repeats "As with Split, this proof is arrangement-parametric: it depends only on S8-cons of the two constituents and Extended Associativity," and then adds "In particular, when R-BLK applies Merge to the post-rearrangement arrangement M'(d), the verification holds because the reassembled runs already satisfy S8-cons for M'(d) (established in Phase 3)."
**Problem**: Two paragraphs state the same meta-point ("arrangement-parametric") in different words, and Merge's closing sentence enumerates a downstream consumer (R-BLK Phase 3) rather than advancing the Merge definition — exactly the "definition enumerates downstream consumers" / "deferral to the same downstream location" anti-pattern flagged for this note. The Split/Merge proofs already quantify over an arbitrary arrangement A; the generality is visible from the proof itself.
**Required**: Drop the duplicated "arrangement-parametric" remarks and Merge's Phase-3 consumer note. If the A-parametricity must be stated, state it once.

### Issue 2: Forward use-site inventories that the reader must skip
**ASN-0084, Remark (uniqueness scope) after R-PPERM**: "This scope depends only on the fibre structure of M(d), not on the cut count, so it applies verbatim to the 4-cut swap (R-SPERM)."
**ASN-0084, Region Partition**: "Their identification with cut-ordinal differences and their positivity are established in the *Width positivity* consequence of R-PRE below."
**Problem**: Both are forward use-site pointers ("applies verbatim to R-SPERM"; "established … below") that defer rather than advance the local claim — the forward-reference accretion pattern. The uniqueness remark's last sentence is a cross-lemma applicability note; the width sentence forward-defers a property to a later section instead of stating it where the widths are introduced.
**Required**: Remove the "applies verbatim to R-SPERM" sentence (place the remark once where it covers both, or let R-SPERM inherit silently). Either define width positivity where w_α, w_β, w_μ are introduced, or introduce them where positivity is proved — not split across a forward pointer.

### Issue 3: Section heading "Sufficient Precondition" contradicts its content
**ASN-0084, "Sufficient Precondition" section / R-CS3**: The section opens "This section records a complementary necessity result" and R-CS3 is a *necessity* lemma (CS3 cannot be dropped).
**Problem**: The heading names a sufficiency claim; the body is a necessity argument. A precise reader must reconcile the mismatch before reading R-CS3.
**Required**: Rename the heading to reflect the necessity content (e.g., "Necessity of CS3").

## OUT_OF_SCOPE

### Topic 1: Composition of multiple rearrangements / k>4 cuts
**Why out of scope**: Already captured in Open Questions; the closure of REARRANGE under composition and the k-cut generalization are new territory, not gaps in the present pivot/swap treatment.

### Topic 2: Operational recovery of the canonical (maximal) partition
**Why out of scope**: R-BLK establishes a *valid* B' and defers maximal-partition recovery to foundation S8 plus a future ASN; the merge-order confluence question is correctly deferred, not an error here.

VERDICT: REVISE
