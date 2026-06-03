# Review of ASN-0102

## REVISE

### Issue 1: The grounding sentence for P4★ at COPY's pre-state cites the wrong composite endpoint

**ASN-0102, "Definition of COPY" (Amendment to ValidComposite★)**: "Σ is a composite boundary because COPY's own application is a valid composite ending there, so P4★ is available as a hypothesis at Σ, not merely assumed."

**Problem**: COPY's application is the transition `Σ → Σ'`; as a length-1 composite it *ends* at `Σ'`, not at `Σ`. It *begins* at `Σ`. So the stated reason — "a valid composite ending there [at Σ]" — does not establish that `Σ` is a boundary. The fact that actually makes `Σ` a composite boundary is independent of COPY's forward application: `Σ` is the terminus of the preceding valid composite in the trace (or `Σ = Σ₀`), and is therefore a recognized boundary at which the composite-boundary properties of ASN-0047 hold. Using COPY's own forward step to certify a property of COPY's own *pre*-state inverts the dependency. This is load-bearing: the entire X14 Old-branch (`a ∈ Old ⟹ (a,d) ∈ Contains_C(Σ) ⊆ R` by P4★) rests on P4★ being available at `Σ`. The X14 section itself states the clean version correctly ("its pre- and post-states Σ, Σ' are composite boundaries… P4★ holds at Σ"), so the Definition-section justification is internally inconsistent with the very argument it is meant to support.

**Required**: Reground `Σ`'s boundary status on the trace history — `Σ` is a composite boundary because it is the initial state of COPY's length-1 composite (equivalently, the terminus of the preceding valid composite, or `Σ₀`), and the *initial* state of any valid composite in a trace is a boundary — rather than on COPY's application "ending there." Replace "ending there" with the correct endpoint characterization so the P4★-at-`Σ` hypothesis is justified by where `Σ` sits in the trace, not by COPY's forward effect.

## OUT_OF_SCOPE

(none — the four Open Questions correctly route later-displacement, downstream-source containment, time-varying views, and unreachable-allocator identity to future ASNs rather than asserting claims about them.)

Notes on coverage checked and found adequate: zero-width copy excluded by P1 (`W ≥ 1`); self-transclusion handled by pre-state resolution (X10b) under atomicity (X15) with a dedicated worked example; empty-subspace first insertion and append both worked; cross-origin non-merge (X11), boundary absorption independence (X12), no-gap density (X16), and the `wp(COPY, S3★)` reduction are all derived in full rather than by "similarly"/checkmark.

VERDICT: REVISE
