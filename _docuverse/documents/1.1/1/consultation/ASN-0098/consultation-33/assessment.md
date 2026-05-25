# Channel Assignment — ASN-0051 review-33

**Date:** 2026-05-16 00:32

## Issue 1: Notation inconsistency in worked example
Reason: This is a purely notational fix selecting one convention (⊕ vs + vs shift) already defined in ASN-0034 (TumblerAdd) and ASN-0058 (OrdinalShiftBase). The choice is derivable from the ASN's own citation framework and requires no design intent or implementation evidence.

## Issue 2: CrossDocumentDecoupling witness omits referential-integrity discharge
Reason: The fix requires making the construction sequence explicit (K.δ → K.α → K.μ⁺) to discharge S3/S3★. All necessary machinery (ASN-0036 referential integrity, ASN-0047 elementary transitions, K.α amendment) is already cited within the ASN and the witness body — this is internal proof completion.

## Issue 3: SV11 strictness analysis omits the empty-term mechanism
Reason: Both mechanisms (empty decomposition terms and intra-block coalescence) follow from the set-theoretic decomposition already developed in the proof body. The fix is a precision amendment to a clause whose underlying content is fully present in the ASN.

## Issue 4: SV11 cites M11/M12 for a restriction; correct foundation lemma is C1a
Reason: This is a citation correction internal to the ASN-0058 reference frame. The proof body already invokes C1a's conditions correctly; the statement-level citation simply needs to match. No external channel input required.
