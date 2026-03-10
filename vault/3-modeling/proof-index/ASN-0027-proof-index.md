# ASN-0027 Proof Index

*Source: ASN-0027-address-permanence.md (revised 2026-03-10) — Index generated: 2026-03-10*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| Σ.reachable | Reachable | INV | predicate(Addr, State) | definition |
| A0 | ReachabilityNonPermanent | LEMMA | lemma | derived from A2 |
| A1 | ISpaceFrame | INV | predicate(State, State) | transition; all operations |
| A2.pre | DeletePre | PRE | requires | |
| A2.length | DeleteLength | POST | ensures | |
| A2.left | DeleteLeftFrame | FRAME | ensures | |
| A2.compact | DeleteCompaction | POST | ensures | |
| A2.frame-I | DeleteISpacePreserved | FRAME | ensures | instance of A1 |
| A2.frame-doc | DeleteCrossDocFrame | FRAME | ensures | |
| A3.pre | RearrangePre | PRE | requires | |
| A3.length | RearrangeLength | POST | ensures | |
| A3.perm | RearrangePermutation | POST | ensures | |
| A3.range | RearrangeRangePreservation | LEMMA | lemma | derived from A3.perm |
| A3.frame-I | RearrangeISpacePreserved | FRAME | ensures | instance of A1 |
| A3.frame-doc | RearrangeCrossDocFrame | FRAME | ensures | |
| A4.pre | CopyPre | PRE | requires | |
| A4.identity | CopyIdentitySharing | POST | ensures | |
| A4.length | CopyLength | POST | ensures | |
| A4.left | CopyLeftFrame | FRAME | ensures | |
| A4.right | CopyRightShift | POST | ensures | |
| A4.frame-I | CopyISpacePreserved | FRAME | ensures | instance of A1 |
| A4.frame-doc | CopyCrossDocFrame | FRAME | ensures | |
| A5.new | VersionNewDoc | POST | ensures | |
| A5.identity | VersionIdentitySharing | POST | ensures | |
| A5.frame-doc | VersionCrossDocFrame | FRAME | ensures | |
| A5.frame-I | VersionISpacePreserved | FRAME | ensures | instance of A1 |
| A6 | NonInvertibility | LEMMA | lemma | derived from A2, ASN-0026 |
| A7 | IdentityRestoringCopy | LEMMA | lemma | derived from A2, A4 |
| A7.corollary | FullRestoration | LEMMA | lemma | derived from A7, A2, A4 |
| A8 | ReferencePermanence | LEMMA | lemma | derived from A1 |
| A9 | ReachabilityDecay | LEMMA | lemma | derived from A2 |
| A10 | PublicationObligation | INV | predicate(Addr, State) | contractual, not architectural |
