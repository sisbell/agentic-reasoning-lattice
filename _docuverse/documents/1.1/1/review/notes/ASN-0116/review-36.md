# Review of ASN-0116

The mathematical content is sound. I verified the composite decomposition (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n), per-step precondition discharge for all three position cases (suffix-present, append, empty), the I-DOM interval argument, the I-NEW index-based withholding against I3-V/I3-CS, the J0/J1★/J1'★/P7a/P7 discharge, and the IP6 wp derivation. The single finding below is anti-bloat, not correctness.

## REVISE

### Issue 1: IP5's freshness-disjointness argument imagines a case F-DOC already excludes
**ASN-0116, "Isolation of documents sharing I-addresses" / IP5**: "And the fresh addresses `A_new` cannot already inhabit `ran(M(d'))`… so `A_new ∩ ran(M(d')) = ∅`. Therefore `d'` resolves every one of its V-positions to the same content…"

**Problem**: IP5's conclusion follows entirely from F-DOC (`M'(d') = M(d')` exactly) plus IP2 (values at `d'`'s referenced addresses preserved) plus F-LINK. Since `d'`'s arrangement is literally unchanged and every address it references pre-existed with its value fixed, `d'` is invariant regardless of `A_new`. The disjointness `A_new ∩ ran(M(d')) = ∅` plays no role in the formal IP5 statement — it guards against a collision that F-DOC has already rendered moot. This is the reviser-drift pattern: prose reasoning about a case the claim's carrier already excludes, which the reader must process and discard. The "Therefore" even mis-attributes the conclusion to the disjointness rather than to F-DOC/IP2.

**Required**: Drop the `A_new ∩ ran(M(d')) = ∅` derivation from IP5's proof (and the parallel sentence in the IP5 claim body), or relocate it to wherever fresh-address/other-document non-aliasing is actually load-bearing. Anchor IP5's "Therefore" on F-DOC + IP2 + F-LINK directly.

## OUT_OF_SCOPE

### Topic 1: Transclusion-shared insertion points, concurrent freshness, cross-origin provenance, post-edit fragmentation
**Why out of scope**: The four Open Questions correctly defer these to future operations (transclusion → ASN-0118, concurrency/replication → BEBE, fragmentation under later editing → DELETE/REARRANGE). They are new territory, not gaps in INSERT, and the note properly parks them rather than half-answering.

VERDICT: REVISE
