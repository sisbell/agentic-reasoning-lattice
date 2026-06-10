# Channel Assignment — ASN-0114 review-24

**Date:** 2026-06-10 00:45

## Issue 1: Forward-reference use-site inventory and mischaracterization of LP-Fin in the substrate setup
Reason: Both faults are derivable from the ASN's own content. Fault (a) is editorial — drop the `(F4)`/`(F5)` forward-inventory clause while keeping "FOLLOWLINK consults only `Σ.L`." Fault (b) needs no external evidence: the ASN already characterizes LP13 correctly in F5's derivation ("UnconditionalLinkPersistence ... for every reachable state sequence `Σ →* Σ'`") and already uses LP-Fin correctly in the worked instance ("the interval contributes only `{a₃, a₄}` (LP-Fin Corollary)"), so the corrected description of each at its true site can be read straight off the note's existing use-sites.
