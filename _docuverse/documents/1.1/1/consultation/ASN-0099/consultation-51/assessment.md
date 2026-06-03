# Channel Assignment — ASN-0099 review-51

**Date:** 2026-06-03 09:07

## Issue 1: Operation vocabulary V conflates two incompatible state models
Reason: The fix is internal — the ASN already commits to ASN-0047's extended state (C, L, M, E, R) and invokes M1, P8, E_doc, and ValidComposite★ throughout, so the operative vocabulary is ASN-0047's extended-state set (K.δ performing document registration), not ASN-0093's substrate K.σ. The reviewer's option (a) is derivable from the ASN's own state-model commitment and its already-cited ValidComposite★ list; no design-intent or implementation evidence is required to resolve which published vocabulary governs.
