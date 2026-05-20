# Channel Assignment — ASN-0094 review-18

**Date:** 2026-05-20 02:06

## Issue 1: Cross-ASN references to ASN-0093 by number
Reason: Pure citation hygiene — either redirect through already-named scaffolding clauses or formally adopt ASN-0093/ASN-0036 as foundation. The decision is internal to the ASN's editorial policy and the existing scaffolding interface.

## Issue 2: EffectiveWpSimplification's Step 1 underjustifies the past-to-present bridge
Reason: Fix replaces an implicit R2+monotonicity step with explicit citations to Sh1 and Sh3, both named preservation theorems already proved in this ASN. All required content is present.

## Issue 3: Implicit Resolution-shape constraint on K_res is undocumented in the template signature
Reason: The Resolution shape `(1, 1, A_doc, A_rel, ⊤)` is already in this ASN's catalog and the parametric column already mentions "Resolution-shaped K_res"; the fix is to lift that into the formal signature. Internal editorial work.

## Issue 4: Sh-conf "Effective wp" preview duplicates the Corollary and creates forward-reference fog
Reason: Editorial decision about whether to delete or condense a preview paragraph in favor of the downstream named Corollary. No external evidence needed.

## Issue 5: AllocatedAddressAntichain Step 3.1's fourth-zero argument has a hidden case
Reason: Reorganization of an existing proof — the componentwise-agreement step is already in the proof; the fix is to surface it explicitly before the fourth-zero contradiction rather than entangling both halves. Internal.

## Issue 6: Sh4 Case D's "leaving" set lacks an explicit cardinality / antichain bound
Reason: Fix adds a one-sentence bound using R0a (ASN-0086 foundation) and Sh-conf at Retraction (this ASN's own axiom applied to the catalog's Retraction row). All cited machinery is internal.
