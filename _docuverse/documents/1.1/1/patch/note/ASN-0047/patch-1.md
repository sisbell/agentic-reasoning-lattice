# N-Endset Generalization — ASN-0047

Nelson (LM 4/79) lists "4-sets, 5-sets ... n-sets supported in link
storage and search" as a desired feature. ASN-0093 (post-patch)
admits `N ≥ 3` per its NEndsetStructure; ASN-0043 has admitted it
all along.

L3 currently narrows to fixed-three-arity as "this ASN's local
strengthening" on top of ASN-0093's K.λ. The narrowing is not
load-bearing — CL-OWN/CL-UNIQ and the K.μ-family proofs reference
`origin(ℓ)` and V-position uniqueness, both arity-agnostic; the
worked example uses arity-3 only as exhibition. Revert L3 to
ASN-0093's `NEndsetStructure` form and make K.λ's inheritance from
ASN-0093 complete (signature, precondition, effect all from ASN-0093
verbatim).

The three-endset convention (slot 1 = from, slot 2 = to, slot 3 = type)
should be preserved as the default in worked examples but not
enforced structurally.
