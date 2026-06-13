# Channel Assignment — ASN-0108 review-20

**Date:** 2026-06-12 23:19

## Issue 1: W9b's charge-exhaustiveness omits a tail-entry route
Reason: Internal. W9b already defines a tail-inflow event generally ("any single transition that places a link into the reachable tail ahead of the then-current cursor"); the repair rests exhaustiveness on that definition (or broadens kind 3 via the already-cited LP18/`K.μ⁺` mechanism). The reviewer has already exhibited the born-ghost route and grounded it in cited foundations (L4/L9 of ASN-0043, LP17/LP18 of ASN-0098), so no new design intent or implementation evidence is required.

## Issue 2: W4 derives and recaps W9a's count formula
Reason: Internal. The closed-form count, its derivation, and its placement are all the ASN's own material; the fix is to delete the duplicated derivation from W4's proof, defer the count to W9a, and compress the variable-schedule observation. No external evidence is involved.

## Issue 3: W5's "same hazard" parenthetical overgeneralizes
Reason: Internal. The relationship between clause 1 and clause 2 follows from their own quantification already stated in W5 (clause 2 ranges over every tail pair, clause-1-at-cursors only over cursor-involving ones), and W9d already treats clause 2 as separately dispensable — both present in the ASN. The fix is to restrict or drop the parenthetical using content already on the page.

## Issue 4: W6 and W6a carry removable defensive meta-prose
Reason: Internal. Purely editorial deletion — the converse disclaimer in W6 and the argument-inventory sentence in W6a are removable without touching the load-bearing claims (W6's forward direction, W6a's `K.λ`-frame justification), which stand on their own. No external channel.
