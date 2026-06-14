# Channel Assignment — ASN-0134 review-11

**Date:** 2026-06-13 22:02

## Issue 1: The transition-invariant enumeration omits M1 (document permanence), but the text claims it is complete
Reason: Internal — the fix is to verify that ASN-0093 carries M1 (ArrangementMonotonicity, `dom(M) ⊆ dom(M')`) as a transition invariant, a dependency-ASN check within the project corpus, then add it to A6's transition clause and W0 and correct "two" to "three." The reviewer already supplies the independence argument (M1 doesn't follow from C2/L1a, which only forbid removing content-hosting, not childless, documents), and append-only document permanence is already a settled foundation of the note — no fresh design-intent or implementation question.

## Issue 2: G1's confluence is proven only for K.σ-free schedules, but the liberation result and contract govern full executions that contain K.σ
Reason: Internal — the cross-`d` K.σ commutation lemma (the H1-analog) follows from framing facts the note already cites (K.σ frames C/L per ASN-0093; K.α/K.λ_sh frame M, used in H0's proof) plus the document-address freshness §4 already assumes, so proving the lemma or scoping the result to registration-quiescent phases is a formal exercise over the operational semantics already in the stack. No design intent or implementation evidence is at stake.
