# Review of ASN-0115

This is a careful, well-structured specification. I checked the load-bearing derivations — the Confinement lemma (T5 application), R6's terminal-overrun argument (D-SEQ★ frontier + canonical-start derivation), R7's repeatability proof (and its correct insistence on comparability under the sequential order, not mere co-reachability), R8's link-vacuity argument (CL-OWN + CL-UNIQ), and R11's wp decomposition — and they hold. Boundary cases are covered (empty spec-set `p = 0`; empty arrangement / `V_S(d) = ∅`; span entirely past the frontier; span partially past the frontier; transclusion; multi-origin; cross-subspace; orphaned-but-referenced content). Foundation citations are in-bounds, and the worked instances verify the key postconditions concretely. The scope boundary against READLINK/FOLLOWLINK is respected — link positions deliver a *reference* (`⟨ref, a⟩`), never the endset structure.

One anti-bloat finding remains.

## REVISE

### Issue 1: V-spec definition pre-empts R6's gap analysis
**ASN-0115, "What a spec-set is, and what delivery is" (V-spec definition)**: "When `V_S(d) = ∅` the constraint is vacuous — any well-formed start of depth ≥ 2 is admissible — but then `act = ∅` and **the gap analysis is trivial** (every named position is unbound)."

**Problem**: The clause "and the gap analysis is trivial" forward-references R6 (it names "the gap analysis" before R6 introduces it) and pre-states R6's `V_S(d) = ∅` trivial case inside a *definition* slot. R6 then owns this exact case in full: "If `V_S(d) = ∅` the sharpening is trivial: `act = ∅`, every named position is an unbound terminal overrun of the empty active range, and there is no interior range for a hole to fall in." This is the forward-reference accretion pattern the review mode targets — a definition deferring to and duplicating a downstream section. The definitional fact (`act = ∅` when `V_S(d) = ∅`) is legitimate here; the pre-emption of R6's analysis is not.

**Required**: In the V-spec definition, keep only the definitional consequence (e.g., "then `act = ∅`, since `⟦σ⟧` lies in subspace `S` (Confinement) and `dom(Σ.M(d)) ∩ {subspace-S} = V_S(d) = ∅`"), and drop "and the gap analysis is trivial (every named position is unbound)" — R6 already discharges the `V_S(d) = ∅` case where it belongs.

## OUT_OF_SCOPE

The Open Questions section correctly defers inline content provenance (OQ1), partial-vs-fail delivery (OQ2), references to addresses with no bound entity (OQ3), channel faithfulness (OQ4 — properly distinguished from R2's denotation-level faithfulness via the explicit frame limit), and subspace-straddling spans (OQ5, excluded by the ordinal-level confinement discipline). No additional out-of-scope coverage is owed, and the ASN defines no claims belonging to the listed sibling operations.

META: not applicable — the ASN specifies a query operation's abstract delivery semantics (R0) and the state-relative invariants any faithful realization must satisfy (R1–R11), stated independently of mechanism.

VERDICT: REVISE
