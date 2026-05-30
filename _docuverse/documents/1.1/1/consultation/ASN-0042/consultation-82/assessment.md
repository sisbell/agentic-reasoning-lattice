# Channel Assignment — ASN-0042 review-82

**Date:** 2026-05-29 23:52

## Issue 1: Duplicated "owns is pair-decidable / ω needs the registry" framing
Reason: Pure deduplication of existing prose; the fix is choosing the load-bearing site and deleting restatements, fully derivable from the ASN's own content.

## Issue 2: Premature forward reference to ω inside O1
Reason: Editorial relocation of an explanation to where ω is defined; no design intent or implementation evidence is at stake.

## Issue 3: Defensive use-site inventory of the reachability premise
Reason: Compressing a per-step accounting into one clause; the proof structure is already in the ASN, nothing external needed.

## Issue 4: Repeated deferral and ordering prose around the delegation predicate
Reason: Consolidating cross-references to the single `delegated` definition; purely internal restructuring of existing conditions.

## Issue 5: Protocol-rationale prose around axioms (O13, O17)
Reason: Removing "why the axiom is needed" commentary while keeping the statements; the retained Nelson/Gregory grounding clause already exists in-text, so no fresh consultation is required.

## Issue 6: Over-elaboration of the node-level O10 case the design excludes
Reason: The ASN already asserts Nelson confines the node operator to account allocation, so the collapse is justified by content already present; deciding how far to trim leans on that stated design intent, which is worth confirming with Nelson rather than re-deriving.
Nelson question: Is a node-level operator ever intended to place or modify content directly, or is its role strictly confined to allocating accounts (so the node-level fork-to-content branch is genuinely out of scope)?
