# Review of ASN-0126

This note is, on its proof content, in good shape. I checked the gate (P3), the weakest-precondition refinement of ASN-0086's Case 2 (C1/C2/C3, with the (0)-omission and the L3 / `K ∈ T_admissible` absorptions), the projection-bridge simulation, P5's constructive lifting, P6's induction, and the worked "born-nullified" trace — the boundary cases (empty `G`, empty `F` re-routing, first vs. subsequent `a_emit`, Binary range-G, self-nullifying C2, pre-existing-retraction C3, arity restriction to 3) are all handled, and the address arithmetic in the worked illustration checks out. The substantive problem is structural, and it is exactly the kind of forward-reference accretion the note is flagged to surface.

## REVISE

### Issue 1: "Single-source" forward-references the note's entire core machinery; the projection bridge serves four sites but is stated after two of them

**ASN-0126, "Single-source" (and "The shape-gated emit")**: The first substantive section makes claims that can only be discharged by constructs introduced in *later* sections:

- *"To obtain a gated retraction an app registers R as **Binary**"* — `Binary` is defined later ("Three shapes" / "Shape-conformance").
- *"`Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` ... has **no** `→_sh` image"* — `→_sh` / `K.λ_sh` are defined later ("The shape-gated emit").
- The R-Scope transfer: *"The projection bridge (established below, The shape-gated emit) sends Σ to a `→*`-reachable `π(Σ)` ..."*

And "The shape-gated emit" itself forward-references its own bridge from the wp: *"applies to this note's `→_sh*`-reachable Σ through the projection bridge (established below in this section)."*

**Problem**: The projection bridge is load-bearing for **four** sites — the Single-source R-Scope transfer, the wp Case-2 domain transfer, P5, and P6 — yet it is stated inside "The shape-gated emit," *after* the first two of those uses. This is precisely the anti-bloat pattern "multiple paragraphs in different sections defer to the same downstream location," here at structural scale. Worse, the R-Scope transfer in Single-source is not a preview but a full frame-argument derivation, planted before any of the machinery it rests on exists; a reader cannot verify the section's central retraction argument until the end of the note. The note is not *circular* (the dependencies all flow forward and everything closes once read whole), but the ordering forces the reader to skip ahead repeatedly, and each of the four sites re-derives the bridge's two consequences (`a_emit(π(Σ),d)=a_emit(Σ,d)`, `dom(π(Σ).L)=dom(Σ.L)`, lemma transfer) in slightly different words rather than citing a single lemma.

**Required**: Hoist the projection bridge to a named lemma in its own section, placed before its first use, and have all four sites cite it instead of re-deriving its consequences. Because the bridge needs `→_sh` (hence the shapes), the cleanest fix also reorders so that the shape catalog + `→_sh`/`K.λ_sh` + the bridge precede Single-source; alternatively, split Single-source — keep the `|F| = 1` thesis and the "Nullify has no `→_sh` image" observation up front as motivation, and move the Binary re-routing and the R-Scope transfer to after `→_sh` and the bridge are established.

## OUT_OF_SCOPE

### Topic 1: Dynamic (post-`Σ_init`) type registration
**Why out of scope**: P1 freezes the registry at `Σ_init`, so an app cannot register a type after substrate initialization, and apps sharing a substrate must declare all types at init. The note treats immutability as a deliberate design choice with real payoffs (P2, P4), and does not claim otherwise — so this is not an error. But it is a genuine usability constraint that the Open Questions do not name (Q4 asks *who* supplies entries, not *when* registration may occur). Adding "is dynamic registration ever needed, and what would it cost P2/P4?" to Open Questions would close the gap; it belongs in a successor note, not a revision here.

VERDICT: REVISE
