# Channel Assignment — ASN-0086 review-35

**Date:** 2026-05-17 06:58

## Issue 1: Terminology overlap with T4 foundation
Reason: The fix is purely terminological — rename the generic "element-field" usage to align with T4's existing "field segment" vocabulary (already cited in the ASN). The ASN itself acknowledges the divergence; resolving it requires only consistent renaming within the document.

## Issue 2: Asymmetric L-invariant verification in Worked Sketch
Reason: The verification pattern is already established in Steps 1-2 and is mechanical to apply to b₂, a₃, b₃ — each L-invariant discharge follows the same structure against the existing foundation ASNs. The cross-document case (b₂) is structurally distinct only in which depth-1 allocator (A_{d'}) is invoked, but the L1a/L14/L14a checks proceed identically once home(b₂) = d' is fixed by construction. No design or implementation input required.

## Issue 3: R0 Step 4's home() description and element-field count under SharedDepthOneAllocator
Reason: The fix is structural reorganization of the proof presentation — either folding empty Step 3 into Step 2, or making Step 3 do substantive work (e.g., explicitly mapping the constructed chain to each L1c clause). The home() and element-field arithmetic is already internally consistent (a = d.0.s_L.1 yields home(a) = d, #E(a) = 2); only the Step 3/4 flow needs tightening.

## Issue 4: Repetition obscures the substantive content
Reason: Editorial consolidation — the Hypothesis dependency view table already captures the conditionality structure; the fix is to trim redundant inline restatements to single citations of that table. No external information needed.
