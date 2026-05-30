# Channel Assignment — ASN-0042 review-120

**Date:** 2026-05-30 05:07

## Issue 1: O17b closes with document-history meta-prose
Reason: Purely editorial — deleting a sentence that narrates the note's consolidation history. No design intent or implementation evidence bears on whether the prose stays; the fix is internal.

## Issue 2: O7(c) proof and Formal Contract carry the same self-referential classification note
Reason: Internal cleanup — stating which conditions bind (iii and v, already established in the proof body) and dropping cross-referential bookkeeping. The substantive classification is already present in the ASN; no channel needed.

## Issue 3: RegistryReachability ends with a use-site inventory
Reason: Editorial — collapsing a use-site inventory into a one-line corollary. The mathematical consequence (next/hwm well-defined, B1/B6 available) is already stated; only the framing changes. Internal.

## Issue 4: Freshness-(v) forward-tags O17b that is itself a later axiom
Reason: Internal reorganization — choosing one home (O18) for the freshness conjunct and citing it without forward tags. The derivation structure is entirely within the ASN; no design or implementation question arises.
