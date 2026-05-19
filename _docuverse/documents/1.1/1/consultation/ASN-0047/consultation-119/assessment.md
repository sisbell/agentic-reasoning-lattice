# Channel Assignment — ASN-0047 review-119

**Date:** 2026-05-19 15:50

## Issue 1: K.δ case (ii) k = 2 sub-case A "induction" framing is incoherent
Reason: Fix is internal — the substantive content (NodeUniqueAllocation, NodeRegistryBootstrap, P1 preservation) is already established in the ASN; only the proof framing needs restructuring as either direct preservation or explicit well-founded induction on entity-tree depth.

## Issue 2: K.μ⁻ derived precondition `dom(M(d)) ≠ ∅` is not stated explicitly
Reason: Fix is internal — making an implicit precondition derivable from effect-clause unsatisfiability into an explicit precondition is a presentation change requiring no design intent or implementation evidence.

## Issue 3: K.μ~ dependency chain misroutes S3★(Σ') through admissibility (ii)
Reason: Fix is internal — the body text already supplies the correct derivation (K.μ⁻ + K.μ⁺ decomposition as independent route), and the verification matrix entry confirms it; only the chain header needs rewording to match.

## Issue 4: Inconsistent P4 vs P4★ in worked examples
Reason: Fix is internal — pure naming consistency, replacing superseded labels (P4, Contains) with extended-state labels (P4★, Contains_C) throughout the interior content replacement example.

## Issue 5: Worked example fork verification omits S3★ link clause and L-invariants
Reason: Fix is internal — the vacuous satisfaction of link-related invariants at states with `dom(L) = ∅` follows from definitions already in the ASN; the fix adds catch-all verification lines acknowledging this.
