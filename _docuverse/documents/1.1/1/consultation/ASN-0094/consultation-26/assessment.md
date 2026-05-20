# Channel Assignment — ASN-0094 review-26

**Date:** 2026-05-20 05:20

## Issue 1: FDD contract's ordering with Sh-conf gates is implicit
Reason: Pure structural fix — Sh4's existing "Ordering with Sh-conf" paragraph supplies the template; replicating it for FDD is mechanical and derivable from the ASN.

## Issue 2: AllocatedAddressAntichain Step 3.1 contradiction is elliptical
Reason: Expository sharpening; the reviewer even supplies the spelled-out contradiction. All facts (`Z_x`, `zeros(x) = 3`, pairwise distinctness) are already present in the proof.

## Issue 3: Audit table mixes acceptance and rejection awkwardly
Reason: Presentation/organization choice between two equivalent ways of exhibiting the discipline's two-sided gate. No design intent or implementation evidence needed.

## Issue 4: Notational inconsistency across worked examples
Reason: Pure notational cleanup — choosing a uniform state-naming scheme across the walkthroughs. Mechanical edit.

## Issue 5: Open Questions conflates fundamental limitations with refinement questions
Reason: Each open question's category (scope decision vs refinement candidate) is already determined by the framework's existing commitments in the ASN — the *Sh4 idempotency contract*'s explicit single-process scope, etc.

## Issue 6: Length and density obscure the substantive content
Reason: Editorial restructuring — moving repeated worked examples and audit detail to supporting material. No external information required.

## Issue 7: "Framework" used throughout without definition
Reason: The framework's components (Sh-conf, Sh0–Sh4, Sh5, four layer-discipline contracts, scaffolding interface) are all already named and defined throughout the ASN; the fix is to consolidate them in one definitional paragraph.

## Issue 8: Resolution row's mechanical-generation claim needs verification at a non-Comment consumer
Reason: The structural claim (Sh5(b) mechanically generates the base family from shape components) is already established in the ASN; any plausible synthetic standalone Resolution-shape K suffices as the worked example, and the reviewer's "ApprovedBy" sketch is adequate.
