# Channel Assignment — ASN-0071 review-1

**Date:** 2026-05-25 05:32

## Issue 1: S3 cited but state model is ASN-0047 (which supersedes S3 with S3★)
Reason: The citation fix (S3→S3★) is internal, but the scope choice between option (a) content-subspace only and option (b) generalize to `dom(C) ∪ dom(L)` requires Nelson's design intent on what FINDDOCSCONTAINING is meant to discover.
Nelson question: Was FINDDOCSCONTAINING intended to discover documents by their content-subspace references only, or to range over any V-position references including link-subspace ones?

## Issue 2: vspec admits link-subspace positions silently; F-iaddrs codomain inconsistent
Reason: The choice of whether to constrain vspec to `subspace(u) = s_C` or to specify link-subspace semantics is a design-intent question about the operation's domain. Nelson resolves whether "containing this content" was meant to exclude link references.
Nelson question: Does Nelson's notion of "containing" in FINDDOCSCONTAINING admit queries naming link-subspace positions, or is it restricted to content-subspace material?

## Issue 3: Reinvents ASN-0058's ContentReference
Reason: ContentReference and resolve are already defined in a known foundation (ASN-0058); the relaxation rationale (charitable reading on partial resolvability) is already argued internally in the ASN. The fix is to use ContentReference and document which preconditions are dropped — derivable from the ASN's own justification.

## Issue 4: No concrete example verifying the operation
Reason: Standards require verification against a scenario from implementation evidence. Gregory holds the udanax-green code and can provide a concrete state with transclusion that exercises F-SHARE, F-PART, and F-DIST.
Gregory question: What is a minimal udanax-green scenario showing two documents sharing a single content I-address through transclusion, suitable for verifying that find returns both documents exactly once?

## Issue 5: Eleven claims, no derivations
Reason: Marking each claim as definitional vs. derived and showing derivation chains for F-CUR, F-LOC, F-FIN is purely internal — all needed material is in the ASN's own definitions and the cited foundation.

## Issue 6: Finiteness argument incomplete
Reason: The three steps (initial-state document count, K.δ growth bound, reachability finiteness) are facts about ASN-0047's foundation that the author can verify by reading ASN-0047 directly. No design intent or implementation evidence required.

## Issue 7: Empty-query behavior unspecified
Reason: For `Q = ∅`, the union semantics in F-iaddrs immediately yield `iaddrs(∅) = ∅` and `find(∅) = ∅`. The boundary statement is derivable from the ASN's own definitions; whether to require Q non-empty is a stipulation the author can make.

## Issue 8: vspec-set notation inconsistent with operation
Reason: Pure notation/type-signature fix; resolved by choosing set notation `{q₁,...,q_k}` or stating sequence-with-set-semantics. Internal.

## Issue 9: Existential body malformed
Reason: Eindhoven syntax correction — move the body from after `:` to after `::`. Mechanical fix, internal.

## Issue 10: F-COMP and F-SOUND framing muddled
Reason: Reframing F-COMP and F-SOUND as the two directions of the defining biconditional (vs. the separate concern of implementation conformance) is a clarification derivable from the ASN's own structure. Internal.
