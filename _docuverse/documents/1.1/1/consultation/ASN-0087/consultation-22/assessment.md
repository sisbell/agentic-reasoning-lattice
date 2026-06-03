# Channel Assignment — ASN-0087 review-22

**Date:** 2026-06-03 16:16

## Issue 1: M-DepthConv's universal claim is derived from a scope-limited premise
Reason: Resolving via option (b) — the system-wide universal "always 2" — requires both design intent (was the link subspace depth meant to be canonically 2 for *all* links, or only a typical placement?) and implementation evidence (does any code path other than the MAKELINK/findnextlinkvsa route ever seed a first link V-position at depth ≠ 2?). Option (a)'s pure weakening is internal, but choosing between (a) and (b) needs both channels to know whether the universal is actually supportable.
Nelson question: Does the design fix every link's V-position at the canonical depth-2 link subspace (`version.0.2.serial`) as a system-wide invariant, or is depth 2 only the intended placement for the standard link-creation path, leaving other depths admissible for links seeded by other means?
Gregory question: In udanax-green, is there any operation other than the standard link-creation path (`findnextlinkvsa`) that seeds a document's first link-subspace V-position, and if so can it place that first link at a depth other than 2?
