# Channel Assignment — ASN-0108 review-27

**Date:** 2026-06-13 01:45

## Issue 1: W5 states the resurrection/inflow aside twice and over-explains clause 1's already-excluded cases
Reason: Pure redundancy removal — the both-states scoping, the W6 blind-spot routing, and the W9b inflow routing are all already stated in the ASN; consolidating them and dropping the duplicate parenthetical requires no design intent or implementation evidence.

## Issue 2: The "ladder of key conditions" carries use-site inventory and pre-states W8's conclusion
Reason: Editorial cut of use-site inventory and a premature statement of a conclusion W8 already establishes from the ASN's own value-totality definition; the load-bearing definitions and converse-failure example stay, so nothing external is consulted.

## Issue 3: W9 restates the computability-vs-clause-1 distinction three times within W9/W9b
Reason: Deduplication of a distinction already fully introduced at the W9 opening (with the W5 walk as witness); dropping the closing recap and trimming the W9b(i) parenthetical to a cross-reference is internal to the ASN.

## Issue 4: The `m=0` walk says "zero windows" but the reader receives one (empty) window
Reason: Internal consistency fix — W4 already names the delivered batch `W_0` a window and W9 already treats the empty window as the terminal signal, so the rewording aligns the walk with the ASN's own usage without external input.
