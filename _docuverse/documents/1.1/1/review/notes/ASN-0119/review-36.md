# Review of ASN-0119

I checked the imported results against ASN-0084 (REARRANGE_K, R-PIV/R-SWP, R-PPERM/R-SPERM, R-COMM, R-RI, R-BLK, R-CANON, R-NS) and verified the two worked examples numerically — the pivot's π-table, the swap's middle displacement `w_β − w_α`, the four illustrative footprint cases, and the two-move atomicity decomposition all check out. The invariant discharge is, for the hard conjuncts, genuinely rigorous: S3★ via the inverse-permutation route (correctly noting `M'(d)(v) ≠ M(d)(v)` inside the interval), the key-set inheritance of D-CTG★/D-SEQ★/D-MIN★/S8a/S8-depth/S8-fin (because `V_{s_C}(d)` is unchanged *as a set* under RA2), S8★ via R-BLK + R-CANON, and the P4a trace-witnessing split. RA7c's run-structure claim follows soundly from R-COMM's region-constant displacement. One traceability gap remains.

## REVISE

### Issue 1: Four conjuncts of the discharged invariant package are not individually traceable
**ASN-0119, "What is preserved: I-address correspondence"** (transition-invariant paragraph): "The genuinely per-state ExtendedReachableStateInvariants conjuncts that remain (P6, P7, P8, the E-family NodeLineage/ActivatedEmission, the L-family, the C-family) are preserved by the C/E/R/L frame." The section then concludes "the invariant package REARRANGE joins is fully accounted for."

**Problem**: ASN-0047's `ExtendedReachableStateInvariants` is an explicit conjunction. Cross-checking it against this ASN's discharge, every conjunct is traceable to a named discharge — S2, S3★, S3★-aux, S8★, S8a, S8-fin, S8-depth, D-CTG★/D-MIN★/D-SEQ★ handled in the body; C1b, C1c, C-fin, L0–L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ, P6, P7, P8, NodeLineage, ActivatedEmission named in the catch-all — *except* **S4, S7a, S7b, and S7d**. These four are S-prefixed and are silently assigned to "the C-family" / "the E-family," whose membership the ASN never defines. The parenthetical even reads "the E-family NodeLineage/ActivatedEmission" as if E-family *is* those two, which would exclude S7d. The substance is not in doubt — S4/S7a/S7b are `dom(C)` properties frozen verbatim by RA0, and S7d is a document-tumbler property frozen by the inert E — but the "fully accounted for" claim requires each conjunct be checkable against a discharge, and these four are not. This is the same standard the ASN itself meets meticulously when it names CL-OWN, CL-UNIQ, P6, P7, P8 explicitly; the omission is an internal inconsistency in its own enumeration practice, not a substantive error.

**Required**: Either name S4, S7a, S7b, S7d in the catch-all, or state the closure rule that subsumes them once — e.g., "every conjunct keyed solely on a frame-frozen component (`dom(C)` by RA0, `E`/`R` inert, `dom(L)` by RA6) is preserved by that component's frame; this covers S4, S7a, S7b, S7d together with the C-, E-, L-families." One clause closes the gap.

## OUT_OF_SCOPE

None. The Open Questions already defer the genuinely future-territory items (cross-document boundary-hood, concurrency/serialization, discovery-index invariants, prior-arrangement recoverability, displacement-arithmetic boundary guards) as questions rather than claims, and the discussions of transclusion-isolation, existing-link survival, and discoverability are REARRANGE's own frame/preservation guarantees, not encroachments on COPY / MAKELINK / FINDLINKS.

VERDICT: REVISE
