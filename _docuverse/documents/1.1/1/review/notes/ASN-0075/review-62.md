# Review of ASN-0075

## REVISE

### Issue 1: Rationale/essay accretion in the granularity discussion
**ASN-0075, "The Three States of Content," second paragraph after "Classification is at I-address-set granularity"**: "We adopt this set granularity deliberately, because SHOWDELETIONS is a cross-document content comparison. Nelson's design attaches survivability and correspondence to bytes (I-addresses) ... (LM 4/42) ... The verified comparison operations work at I-address / shared-origin granularity — SHOWRELATIONOF2VERSIONS and FINDDOCSCONTAINING (LM 4/70) compute correspondence from shared I-addresses, not from V-position counts."

**Problem**: The preceding paragraph already states the granularity choice and gives its concrete, object-level consequence (a per-occurrence removal is invisible while any occurrence survives). This second paragraph is defensive rationale: it explains *why* the choice is justified by appealing to Nelson's design philosophy and to two other operations, rather than advancing what the predicates assert. The carrier note flags `review-mode.anti-bloat`; this is exactly the "new prose explains why X is needed rather than what it says" pattern. The only spec-bearing sentence is the scope-out ("Per-occurrence removal ... is a V-position concern ... we scope it out of this operation").

**Required**: Cut the Nelson-philosophy and cross-operation justification sentences. Retain the one-sentence scope-out statement. The granularity choice does not need to be argued from external authority — it needs to be stated.

### Issue 2: Forward-referencing restatement of the witness condition
**ASN-0075, same paragraph**: "The cross-document witness condition (a still-current copy of `a` in the partner document, "The SHOWDELETIONS Operation" below) is likewise an I-address-set fact: it asks whether `a ∈ ran(M(d_B))`, not how many times `a` occurs in `d_B`."

**Problem**: This sentence pre-explains the witness condition that "The SHOWDELETIONS Operation" section defines and characterizes properly. It is a forward reference whose content is redundant with the later definition, inserted only to extend the granularity discussion. The granularity point (set, not count) is already made by the surviving scope-out sentence.

**Required**: Remove the sentence. The witness condition belongs at its definition site, where its I-address-set character is already evident from `a ∈ ran(M(d_B))`.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (V-position) removal detection
**Why out of scope**: Distinguishing which of several V-positions holding the same I-address was removed is a Vstream concern. The note correctly scopes this out; it belongs to a future V-position-granularity operation, not here.

### Topic 2: Multi-document generalization and third-document witnesses
**Why out of scope**: The Open Questions raise reporting deletions across families of >2 documents and third-document witness structure. These are genuine future-ASN territory, not defects in the binary operation specified here.

VERDICT: REVISE
