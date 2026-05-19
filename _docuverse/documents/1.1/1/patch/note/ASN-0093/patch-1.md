# N-Endset Generalization — ASN-0093

Nelson (LM 4/79) lists "4-sets, 5-sets ... n-sets supported in link
storage and search" as a desired feature. ASN-0043 already admits
`N ≥ 3` per its NEndsetStructure.

L3 currently narrows to fixed-three-arity, inheriting the narrowing
from ASN-0047. The substrate's job is minimal commitment — narrowing
belongs at higher-layer consumers, not at the substrate. Revert L3
to ASN-0043's general `N ≥ 3` form.

The three-endset convention (slot 1 = from, slot 2 = to, slot 3 = type)
should be preserved as the default but not enforced structurally.
