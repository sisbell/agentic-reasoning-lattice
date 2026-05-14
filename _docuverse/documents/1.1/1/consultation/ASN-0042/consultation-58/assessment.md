# Channel Assignment — ASN-0042 review-58

**Date:** 2026-05-14 11:49

## Issue 1: O5 used in O4's proof before its formal introduction
Reason: Pure structural/ordering fix within the ASN — moving O5's formal statement to the State Axioms section alongside the other transition axioms. No design intent or implementation evidence needed.

## Issue 2: `delegated` relation referenced by name before its formal definition
Reason: Pure structural/ordering fix — either promote the definition into O15 (whose conditions already enumerate it) or reorder sections so Delegation precedes its dependents. Derivable from the ASN's own content.

## Issue 3: "Five axioms" count is inconsistent with section contents
Reason: Pure textual fix — recount the axioms and restate the intro accurately. No external input needed.

## Issue 4: Bootstrap allocation regime versus transition allocation regime is not explicitly distinguished
Reason: Fix is to add a clarifying sentence noting that O5/O16 govern transitions while bootstrap is governed by O14 + ASN-0040 B₀ conf. All ingredients are already present in the ASN and the lattice; no new evidence needed.

## Issue 5: O10's fork construction at node level produces a user-level address but the cited implementation evidence is account-level
Reason: To choose between tracing a multi-baptism trajectory versus restating O10's postcondition, we need design intent on whether the fork was meant to produce content-bearing addresses at every principal level, and implementation evidence on whether udanax-green supports a node-level fork path.
Nelson question: Was the fork mechanism (denial-as-fork at an ownership boundary) intended to produce content-bearing addresses for node-level principals, or is the node operator's role limited to account allocation with content creation occurring only at account level and below?
Gregory question: Does udanax-green provide an allocation path by which a node-level principal (a session whose account tumbler has `zeros = 0`) creates a content-bearing address in a single allocation call, analogous to `docreatenewversion`'s `makehint(ACCOUNT, DOCUMENT, ...)` for account-level principals?

## Issue 6: O0's structural-decidability postcondition is asserted but not derived from the O1 definition
Reason: Pure internal logical restatement — update Properties Introduced table to mark O0 derived from O1 + Prefix + T3, or recast O0 as a verification target met by O1. All needed reasoning is already in the ASN.
