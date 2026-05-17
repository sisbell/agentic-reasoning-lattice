# Channel Assignment — ASN-0086 review-17

**Date:** 2026-05-16 22:32

## Issue 1: Introduction undercounts R-properties
Reason: Purely internal counting/labeling inconsistency. The R-labels are all defined within the ASN itself; reconciling the headline count against the body's labels (R0, R0a, R1–R7) requires only reading the document.

## Issue 2: Substrate emission primitive's allocator-state semantics left implicit
Reason: The fix is to choose between (a) implicit Act(s)/n_s extension by the class-(iii) step or (b) structural reinterpretation of T2 admissibility. Both are internally consistent with the ASN, but the choice should be informed by what udanax-green's link-emission path actually does at the allocator-state level — does it maintain and extend allocator activation/realization state during link emission, or does it deposit at any conforming address without such state tracking? Nelson's ghost-element design is already cited and supports both readings.
Gregory question: In udanax-green's link-emission code path (`docreatelink`, granfilade orgl tree extension, POOM update), does the substrate maintain an explicit per-allocator activation/realization state that is extended atomically when a link is emitted at an address whose enumeration index hasn't been reached yet, or does the implementation treat allocator addresses as purely logical (depositing at any address whose tumbler-algebra structure is admissible, without tracking activation state)?
