# Channel Assignment — ASN-0087 review-62

**Date:** 2026-06-04 02:22

## Issue 1: D-CTG★ proof asserts an unestablished reachable pre-state, contradicting M-DepthConv
Reason: The tension is whether an `m_L(d) ≥ 3` first-link pre-state can actually arise. Option (i) (generality hedge) is internally derivable, but choosing the cleaner reductive fix (ii) — strengthening M-DepthConv and collapsing the D-CTG★ branch — requires knowing whether any operation other than MAKELINK places a document's first link V-position, which is a fact about the operation set the ASN does not settle. Gregory can confirm this; Nelson is not needed since the question is about realized behavior, not design intent.
Gregory question: In udanax-green, does any link-placement path other than the MAKELINK-equivalent ever set a document's first link-subspace V-position at depth ≥ 3, or is the link-subspace depth always 2?

## Issue 2: Motivational essay prose in claim-bearing slots
Reason: The fix is a pure deletion of the motivational clause; the symmetry claim stands on the LP12 uniformity argument already present, so no design-intent or implementation evidence is required.
