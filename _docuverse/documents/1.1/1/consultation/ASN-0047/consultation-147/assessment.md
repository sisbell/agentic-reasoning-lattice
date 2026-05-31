# Channel Assignment — ASN-0047 review-147

**Date:** 2026-05-31 15:17

## Issue 1: Internal contradiction over which step of the K.μ~ chain consumes CL-UNIQ
Reason: Purely internal — the ASN already states elsewhere (the "Dual consequence" paragraph and the chain preamble) that Steps 1–3 / Step (C) do not invoke CL-UNIQ; the necessity argument's attribution is simply inconsistent with the ASN's own established structure. Fix is to align the citation.

## Issue 2: S9 "follows from P0 unconditionally" — derived guarantee without derivation
Reason: Internal — the one-line derivation (every M-mutating transition frames C, so no arrangement op touches the append-only/immutable content store) is fully available from the frames already stated for K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~ in this ASN.

## Issue 3: LinkVPositionDepthAxiom asymmetry — content first-insertion depth left underdetermined with no stated reason
Reason: The foundation-mechanism half (whether ASN-0036 pins content first-insertion depth) is checkable internally, but justifying the asymmetry as genuine — that the link subspace depth is intentionally variable while content is fixed-width positional — turns on design intent, so Nelson is needed to confirm the design distinction.
Nelson question: Was the link subspace deliberately designed to permit a freely-chosen positional depth (subdividable "by further digits", LM 4/31) while the byte/content subspace has a fixed positional depth per document, or were both intended to share a common positional discipline?

## Issue 4: Redundant A2-dispatch induction retained despite an admitted one-line alternative
Reason: Internal editorial fix — the ASN itself supplies the direct T10a.6 discharge as sufficient; replacing the inductive construction with it requires no external input.

## Issue 5: Forward-reference duplication in the K.μ~ proof — summary plus "full proof below" for the same case analysis
Reason: Internal editorial fix — collapsing the duplicated `s_C → s_L` / `s_L → s_C` case analysis into a single presentation needs no design or implementation evidence.

## Issue 6: Use-site inventories and downstream-consumer enumerations (anti-bloat)
Reason: Internal editorial fix — removing the consumer inventory and folding/deleting the matrix-preamble justifications is a structural cleanup derivable from the ASN alone.
