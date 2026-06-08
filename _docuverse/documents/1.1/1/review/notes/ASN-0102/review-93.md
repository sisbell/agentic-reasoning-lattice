# Review of ASN-0102

I checked the arithmetic of all five worked examples, the X16 tiling/disjointness argument, the `wp(COPY, S3★)` partition, the X8 within-/cross-reference merge split, and the X14 provenance discharge. The formal content is sound — the tilings close, the three position-classes are domain-disjoint, pre-state resolution is handled consistently, and the invariant discharge is complete. My findings are confined to the anti-bloat patterns this cycle is tagged for.

## REVISE

### Issue 1: X14 restates its own Σ₀-residency split
**ASN-0102, X14 (ContainmentRecording)**: the two bullets ("`a ∉ ran_{s_C}(M_{Σ_0}(d))`…" / "`a ∈ ran_{s_C}(M_{Σ_0}(d))`…") already establish the J1★/J1'★ case split fully, including which case invokes P4★. The following paragraph — "In neither case does an R-new pair (relative to Σ_0) lack a range-new address. The split turns on Σ_0-residency alone: P4★ is invoked only where it applies… while pre-state residency that reflects a mid-composite write… is routed to the first bullet…" — re-derives the same conclusion in different words.
**Problem**: Two paragraphs in the same claim say the same thing; the reader must reconcile the restatement against the bullets to confirm it adds nothing. This is the "two paragraphs say the same thing" accretion pattern.
**Required**: Delete the closing summary paragraph; the bullets are self-contained.

### Issue 2: Motivational source quotes embedded inside formal derivations
**ASN-0102, X1 / X4 / X7**: the *Derivation*/justification slots of these claims carry multi-line Nelson quotes that do not advance the formal step — e.g. X1's "No copying operations are required among the documents… especially the problem of updating documents which depend on other documents" [LM 2/36] sits between the one-line proof (`Σ'.C = Σ.C`) and the Gregory trace; X4's [LM 4/11] native-bytes block and X7's [LM 2/45] quote are likewise inside derivations whose formal work is already complete.
**Problem**: Essay/motivation content occupying a structural (derivation) slot — the precise reader must skip past it to follow the proof. The claims `X1`/`X4`/`X7` are discharged by the surrounding one-line arguments alone.
**Required**: Move source-grounding quotes to the motivational prose (the chapter framing already cites Nelson), or reduce to a bracketed citation, leaving derivation slots to carry only steps.

### Issue 3: X2 framing leans on relationship-to-X1 meta-prose
**ASN-0102, X2 (NoFreshAllocation)**: "Beyond X1's invariance of `dom(Σ.C)`, X2 fixes the concrete allocation handle that K.α (ASN-0093) consults." The substance that follows (the frontier is unchanged because `D_d` is identical across `Σ'/Σ`) is correct, but the opening sentence and the parenthetical "this is the regime of a cross-origin copy into a natively-empty document" justify X2's existence relative to X1 rather than advancing the frontier claim.
**Problem**: Definition introduced via its relation to a sibling claim plus a defensive regime aside — mild meta-prose around an otherwise tight result.
**Required**: State the frontier-unchanged result directly from X1 (`dom` unchanged) + X6 (origin unchanged); drop the "Beyond X1…" framing and the regime aside.

## OUT_OF_SCOPE

The four Open Questions (re-displacement discoverability, transitive containment recording, time-varying resolution, allocator unreachability) are correctly forward-looking and not obligations of this ASN.

VERDICT: REVISE
