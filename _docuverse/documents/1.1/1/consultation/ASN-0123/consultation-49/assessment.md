# Channel Assignment — ASN-0123 review-49

**Date:** 2026-06-13 22:10

## Issue 1: Contract-slot commentary restates V-WF's realization proof and PS's ω-totality
Reason: Pure prose-pruning internal to the ASN. The single-allocation fact lives in V-WF and V0, the ω-totality conclusion lives in PS, and the k=2/k=0 mechanics and well-definedness are already proved at V-WF and the nextd definition — the fix only removes duplication and replaces it with cites to material already present. No design-intent or implementation question is at stake.

## Issue 2: V0 defers the node-tier exclusion to a rationale that is never stated
Reason: Derivable from the ASN's own apparatus. The reason is tumbler arithmetic already available in the note: a node-tier forker (zeros(pfx(π)) = 0) applied to nextd yields inc(node, 2) = [node, 0, 1] with zeros = 1 — an Account, not a Document — so the single-K.δ realization V-WF relies on cannot deliver v ∈ E_doc. Stating this requires only nextd's definition and the tier/zeros structure, no Nelson or Gregory input.
