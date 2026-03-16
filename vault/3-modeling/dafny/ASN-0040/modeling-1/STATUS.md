# Verification Status — modeling-1

Updated: 2026-03-16 10:12
Verified: 18/18

| Property | Status | Divergences |
|----------|--------|-------------|
| StreamStrictlyOrdered | verified |  |
| StreamExtendsParent | verified |  |
| Irrevocability | verified |  |
| BaptismalClosure | verified |  |
| SeedConformance | verified |  |
| ContiguousPrefix | verified |  |
| HighWaterMarkSufficiency | verified |  |
| GhostValidity | verified | The ASN's baptismal state Σ contains only Σ.B. "Occupied" is a downstream concep... |
| NamespaceSerialized | verified | The ASN uses temporal precedence (≺) over concurrent events. The sequential func... |
| FieldAdvancement | verified |  |
| SiblingZerosPreserved | verified |  |
| ValidDepth | verified |  |
| NamespaceDisjointness | verified |  |
| GlobalUniqueness | verified | The ASN derives B8 from B1 (ContiguousPrefix), B4 (NamespaceSerialized), and B7 ... |
| UnboundedExtent | verified | The ASN states UnboundedExtent over the full operational model (registries reach... |
| RegistryT4Validity | verified | The ASN states B10 as a universal over all reachable registry states. The Dafny ... |
| RegistryGrowth | verified | The ASN defines next(B, p, d) as: if children = ∅ then inc(p, d) else inc(max(ch... |
| OnlyRegistryModified | verified | The BaptismState used in RegistryGrowth has only field B, making the frame trivi... |
