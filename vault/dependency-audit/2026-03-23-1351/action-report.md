## Dependencies to Add

**ASN-0061** — add dependency on **ASN-0043**
Transitive dependency detected: ASN-0061 uses labels (L0, L1, L12, L14, L1a, L3) that originate in ASN-0043 but ASN-0043 is not declared as a dependency.

**ASN-0067** — add dependency on **ASN-0043**
Same as above. ASN-0067 uses the same set of labels (L0, L1, L12, L14, L1a, L3) from ASN-0043 without declaring it.

---

## Label Collisions (consider rename)

**B1 (Coverage), B2 (Disjointness), B3 (Consistency)**

Both ASN-0040 and ASN-0058 define properties under the labels B1, B2, and B3. ASN-0058's versions are the block decomposition predicates (Coverage, Disjointness, Consistency on mapping blocks). ASN-0040's versions are structurally distinct properties about a different object.

The following ASNs use B1/B2/B3 from ASN-0058 (a declared dependency in each case) but the shared label causes scanner ambiguity:

| ASN | Labels affected |
|-----|----------------|
| ASN-0051 | B1 |
| ASN-0059 | B1, B2, B3 |
| ASN-0061 | B1, B2, B3 |
| ASN-0065 | B1, B2, B3 |
| ASN-0067 | B1, B2, B3 |
| ASN-0079 | B3 |

No missing dependencies — all affected ASNs already declare ASN-0058. The collision is a naming conflict between ASN-0040 and ASN-0058 that should be resolved by renaming one set of labels.

---

## Label Overlaps (informational)

**S0, S1** — ASN-0040 introduces S0 and S1 as local properties of its sibling stream. These labels also appear in ASN-0036's exports. The properties are independent; ASN-0040 does not consume ASN-0036's versions.

**S0–S9** — ASN-0053 introduces all ten labels locally (Convexity through NormalizationUniqueness). These labels also appear in ASN-0036, where ASN-0036 is the consumer of ASN-0053's definitions, not the other way around. No action needed.

**B1, B2, B3** — ASN-0058 introduces B1, B2, B3 locally as block decomposition predicates. These labels also exist in ASN-0040. This is the same naming conflict described in the Collisions section above, viewed from ASN-0058's side as a local definition.

---

## Clean

ASN-0034, ASN-0036, ASN-0042, ASN-0043, ASN-0045, ASN-0047
