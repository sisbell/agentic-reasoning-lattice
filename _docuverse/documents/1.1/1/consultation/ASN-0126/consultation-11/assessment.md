# Channel Assignment — ASN-0126 review-11

**Date:** 2026-06-08 23:23

## Issue 1: "No fourth shape" completeness claim ignores lower-bound G-disciplines
Reason: Deciding between fix (a) and (b) turns on whether a zero-target citation/fan-out is a legitimate structural form or whether a "must-cite-something" floor is genuinely required; this is a design-intent question (does the floor live at the structural level or the operational/front-end layer?) plus implementation evidence on whether the link store actually admits empty to-sets.
Nelson question: Was a citation/link designed so it must carry at least one target, or is a zero-target (empty-G) typed relation a legitimate (if degenerate) form whose "must cite something" rule belongs to the operational/front-end layer rather than the structural shape?
Gregory question: Does udanax-green permit creating a link with an empty to-set (G = ∅) — i.e., does MAKELINK / the link-store path enforce a non-empty target endset, or does it store a link with no targets without complaint?
