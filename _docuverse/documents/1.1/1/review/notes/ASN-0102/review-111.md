# Review of ASN-0102

## REVISE

### Issue 1: Claim numbering skips X2 with no explanation

**ASN-0102, "Claims Introduced" table and body**: The introduced claims run X1, X3, X4, …, X17. There is no X2 anywhere in the note, and no claim references X2.

**Problem**: A gap in a contiguous label sequence reads as a renumbering artifact — a claim that was removed (or relocated) in a prior revision cycle without closing the gap. A precise reader cannot tell whether X2 is missing by accident, deleted deliberately, or referenced somewhere they have not yet reached. This is exactly the "prior finding's content relocated rather than removed" pattern.

**Required**: Either renumber the introduced claims contiguously (X1, X2, X3, …) or, if the gap is intentional, this is unlikely to be worth a note — contiguous renumbering is the clean fix.

### Issue 2: X17 P4a discharge states the same disclaimer twice

**ASN-0102, X17, P4a bullet**: opens with "We discharge P4a parametrically … *not by claiming anything about all traces to the state value Σ'*" and closes with "We do *not* assert that every trace reaching the state value Σ' passes through this Σ; the universal-over-traces form of P4a follows from the reachability induction over all valid traces …".

**Problem**: The opening clause and the closing sentence make the identical disclaimer in different words — the "two paragraphs say the same thing" pattern, here within one bullet. The disclaimer is correct and worth stating once; stating it twice forces the reader to confirm the second sentence adds nothing.

**Required**: Keep one statement of the parametric/inductive framing and delete the redundant restatement.

### Issue 3: X15's "modeling choice" exploration is rationale, not a guarantee

**ASN-0102, X15**: "In the displacing case this atomicity is forced; in the non-displacing cases it is a modeling choice," followed by the full non-displacing paragraph demonstrating how COPY "is expressible as a valid composite … fill the new positions one at a time."

**Problem**: COPY's contract is that it is a single elementary transition with no observable intermediate state. The proof that atomicity is *forced* in the displacing case (the D-CTG★/D-SEQ★ gap and the X7 destruction arguments) is load-bearing and justifies the model. But the demonstration that COPY is *not forced* to be elementary in the append/empty cases — that it "coincides with a valid composite extension" — establishes no system guarantee. An alternative implementation must satisfy COPY's postconditions; it need not know whether COPY could alternatively be decomposed. This is modeling commentary occupying a claim slot.

**Required**: Trim X15 to the atomicity guarantee and the forced-ness argument (both orderings) that justifies it. Drop the non-displacing "choice not forced" exploration, or relocate it to an explicit design-note aside rather than a claim.

## OUT_OF_SCOPE

### Topic 1: Re-displacement, transitive containment-as-source, and unreachable-origin behavior
**Why out of scope**: These are the note's own Open Questions and concern interactions with future operations (subsequent displacement, a copied-then-re-sourced document, deallocation/reachability of the origin document). They are correctly deferred, not errors here.

VERDICT: REVISE
