# ASN-0030 Proof Index

*Source: ASN-0030-address-permanence.md (revised 2026-03-11) — Index generated: 2026-03-12*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| reachable(a, d) | Reachable | INV | predicate(Addr, DocId, State) | definition |
| reachable(a) | GloballyReachable | INV | predicate(Addr, State) | definition |
| A0 | IdentityPermanence | LEMMA | lemma | derived from P0, P1 (ASN-0026); transition |
| A1 | ReachabilityNonMonotone | LEMMA | lemma | witness: DELETE |
| A2 | AccessibilityPartition | LEMMA | lemma | derived from P2 (ASN-0026) |
| A3 | AccessibilityTransitions | LEMMA | lemma | derived from P1, operation definitions |
| A4 pre | DeletePre | PRE | requires | |
| A4(a) | ISpaceUnchanged | FRAME | ensures | DELETE; +\_ext, fresh = ∅ |
| A4(b) | DeleteContentPersists | LEMMA | lemma | derived from A4(a) |
| A4(c) | DeleteVLength | POST | ensures | |
| A4(d) | LeftUnchanged | FRAME | ensures | DELETE |
| A4(e) | DeleteRightShift | POST | ensures | symmetric to P9-right (reversed) |
| A4(f) | OtherDocsUnchanged | FRAME | ensures | DELETE; instance of P7 |
| A4(g) | DocSetUnchanged | FRAME | ensures | DELETE |
| A4a pre | RearrangePre | PRE | requires | |
| A4a(a) | ISpaceUnchanged | FRAME | ensures | REARRANGE |
| A4a(b) | RearrangeVLength | FRAME | ensures | length preserved |
| A4a(c) | RearrangePermutation | POST | ensures | |
| A4a(d) | OtherDocsUnchanged | FRAME | ensures | REARRANGE; instance of P7 |
| A4a(e) | DocSetUnchanged | FRAME | ensures | REARRANGE |
| A5 pre | CopyPre | PRE | requires | |
| A5(a) | CopyAddressSharing | POST | ensures | transclusion — key property |
| A5(b) | ISpaceUnchanged | FRAME | ensures | COPY; +\_ext, fresh = ∅ |
| A5(c) | CopyTargetLength | POST | ensures | |
| A5(d) | LeftUnchanged | FRAME | ensures | COPY target |
| A5(e) | CopyRightShift | POST | ensures | |
| A5(f) | CopySourceUnchanged | FRAME | ensures | conditional: d\_s ≠ d\_t |
| A5(g) | OtherDocsUnchanged | FRAME | ensures | COPY; instance of P7 |
| A5(h) | DocSetUnchanged | FRAME | ensures | COPY |
| A6 | VersionCorrespondence | LEMMA | lemma | derived from D12 (ASN-0029) |
| endset(L) | Endset | INV | function(Link): set\<Addr\> | definition |
| A7 | LinkTargetStability | LEMMA | lemma | derived from A0 |
| A7a | EndsetPermanence | LEMMA | lemma | derived from P1 (ASN-0026) |
| resolvable(L, d) | Resolvable | INV | predicate(Link, DocId, State) | definition |
| A7b | EndsetResolvability | LEMMA | lemma | non-monotone; witness: DELETE |
| ghost(a) | Ghost | INV | predicate(Addr, State) | definition |
| A8 | GhostLinkValidity | INV | predicate(Link, State) | |
| A9 | CoordinateIndependence | — | — | remark |
| A10 | AuthenticityCaveat | — | — | remark |
