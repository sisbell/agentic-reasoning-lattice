# Review of ASN-0058

## REVISE

### Issue 1: OrdShiftHom citation for depth preservation in M12b

**ASN-0058, proof of M12b (No right-extension)**: "For depth of `v + (n − 1)`: if `n = 1`, then `v + (n − 1) = v + 0 = v` by OrdinalShiftBase, which has depth `m`; if `n ≥ 2`, then `n − 1 ≥ 1` and OrdShiftHom gives `v + (n − 1)` depth `m`."

**Problem**: OrdShiftHom (ASN-0036) establishes only ord, subspace, and S8a preservation — not depth preservation. Its three conclusions are: (a) `ord(shift(v, n)) = shift(ord(v), n)`, (b) `subspace(shift(v, n)) = subspace(v)`, (c) S8a preservation when `v` satisfies S8a. Depth preservation `#shift(v, n) = #v` is from OrdinalShift's postcondition (ASN-0034), not OrdShiftHom. The conclusion (depth `m`) is correct, but a reader who looks up OrdShiftHom will not find depth preservation in its postconditions.

**Required**: Replace the OrdShiftHom citation with OrdinalShift's postcondition `#shift(v, n) = #v` in the depth-derivation step (both for `v + (n − 1)` and for `v' + (j − 1)`).

### Issue 2: M16a prose conflates document prefix with broader preserved segment

**ASN-0058, proof of M16a**: "The document prefix is identified structurally as the segment up to and including the third separator zero; since this segment lies entirely at indices < #a..."

**Problem**: The document prefix `origin(a) = N(a).0.U(a).0.D(a)` is a tumbler with `zeros = 2`, occupying positions `[1, z_3 − 1]` where `z_3` is the position of the third zero (which separates `D` from `E`). "The segment up to and including the third separator zero" instead describes the wider segment `[1, z_3]` containing the document prefix plus the third separator (`zeros = 3`). Both segments lie at indices `< #a`, so the argument's conclusion (`origin(a+k) = origin(a)`) is sound — but the prose identifies the wider segment as the prefix, then applies T3 to "`N(a+k).0.U(a+k).0.D(a+k) = N(a).0.U(a).0.D(a)`", which is the narrower prefix tumbler. The two are conflated mid-proof.

**Required**: Either describe the document prefix as the segment from position 1 up to (but not including) the third separator zero, or state explicitly that the wider segment up to and including `z_3` is preserved by TumblerAdd, and hence the document-prefix sub-segment `[1, z_3 − 1]` is preserved.

## OUT_OF_SCOPE

No items.

VERDICT: REVISE
