# Review of ASN-0134

This is a careful, largely sound note. The step/operation seam (A1–A2 vs A5), the per-home conflict theory (H0–H2), the step-level confluence vs operation-level non-confluence distinction (G1 vs the §4 families), and the quiescence snapshot analysis (V0/V2/V1) are all rigorously argued, with boundary cases (first-emission H2, empty home, m=0/m=1 batches, empty-slice `stale`) explicitly handled and two concrete traces (§7, §8) that check out address-by-address. The findings below are predominantly the accreted meta-prose the `review-mode.anti-bloat` classifier asks for, plus one precision slip against the note's own headline distinction.

## REVISE

### Issue 1: Reviser-drift and defensive meta-prose around K.σ
**ASN-0134, §4 (the K.σ scoping paragraph and the freshness paragraph)**: "It is tempting to call K.σ *conflict-free* and scope it out; that would be an error." … "This corrects the standing of K.σ's two preconditions, which an earlier reading mistook for free hypotheses."
**Problem**: Both sentences are meta-commentary on the note's own revision, not reasoning that advances the claim. "an earlier reading mistook" narrates the edit history; "It is tempting to … that would be an error" argues against a scoping decision no longer on the table. Worse, the wrapping obscures a real reconciliation burden: the §4 opening asserts "H0/H1/H2 carry over to K.σ *by the same argument* … the **account as home** and `A_doc` its sub-allocator" as a direct consequence, but the freshness paragraph then concedes that ASN-0093's `K.σ` is "freshness-by-*test*" and that the A_doc frontier discipline is "not assumed but *obtained*." The carry-over holds only under the imposed A_doc realization (the content/link H2 is a *forced* collision; the bare-`K.σ` analog is a *contingent* same-target collision), and the meta-prose hides rather than states this.
**Required**: Collapse to one derivation — K.σ is realized as an account-tier `A_doc` emission (per ASN-0047 + the cited Gregory evidence), so H0/H1/H2 apply with the account as home; ASN-0093's `d ∉ dom(M)` freshness-test is the *rejection path* for a losing same-account racer. Drop the "tempting to scope out" and "an earlier reading mistook" framing.

### Issue 2: "global, not per-home" restated ~5× in the V2 region
**ASN-0134, §8 (V2 and the two paragraphs following it)**: "This exclusion — and even V2's weaker middle condition — is *global* in scope, not per-home (§8)…"; "V2 is the reader-side counterpart of §4–§6, global in scope where those are per-home."; "…so neither the minimal condition nor the one-index construction clause 6 adopts is per-home."; "…why the 'per-home' promise of this note is a *writer-side* promise that does not carry over to the reader's multi-read verdict."
**Problem**: The conclusion ("the verdict exclusion is global, not per-home") is asserted four or five times in adjacent paragraphs. The genuine supporting work — the dual-to-W4 scope contrast and the constituent-kind analysis showing the nullifier sits at an arbitrary `d_retr` — is real and should stay; the bare restatements of the conclusion around it are noise.
**Required**: State the conclusion once, retain the Q-affecting/constituent-kind argument that establishes *why* it is global, and cut the remaining restatements.

### Issue 3: Meta-framing clause introducing the subspace-fusion caveat
**ASN-0134, §6 (W4 implementation caveat)**: "One implementation caveat earns a mention because it is a real divergence between the abstract model and Gregory's code, and an implementer must know which they are honouring."
**Problem**: The caveat's content (abstract disjoint `s_C`/`s_L` frontiers vs Gregory's fused granfilade, and the coarser exclusion the fusion inherits) is substantive and belongs. The framing sentence — "earns a mention because … an implementer must know" — is pure justification for including the paragraph and advances nothing.
**Required**: Open with the divergence itself; delete the "earns a mention because" framing.

### Issue 4: §9 wp postcondition bundles model-intrinsic gaplessness into the serialization wp
**ASN-0134, §9 (allocation wp)**: "For an emission into `(d, S)` with the postcondition `R ≡` 'the deposited address is fresh and unique *and the S-prefix of d remains a gapless interval*,' `wp(emit into (d,S), R) ≡` (no other emission into `(d,S)` is realized between this emission's frontier-read and its deposit)."
**Problem**: §5's W3 is emphatic that "dense chain contiguity … is *model-intrinsic*" and that "What per-home serialization buys is thus *not* contiguity but same-home *uniqueness* (H2)." The §9 wp — explicitly offered as "the most honest summary of clause 2" — folds the gapless-interval (contiguity) conjunct into a postcondition whose weakest precondition is exactly the serialization condition. The equivalence is technically true only because the gapless conjunct is invariantly satisfied (it rides along while `fresh ∧ unique` drives the wp), but bundling it directly muddies the note's own centerpiece distinction: a reader who internalized W3 will read this as "serialization is needed for contiguity," which W3 denies.
**Required**: Set `R ≡` "the deposited address is fresh and unique" (the property clause 2 actually buys), or state explicitly that the gapless conjunct is the model-intrinsic rider not driving the wp.

## OUT_OF_SCOPE

### Topic 1: Multi-step batch atomicity to a reader, and cross-server composition of per-home orders
**Why out of scope**: A5/§2 correctly isolate that the substrate's all-or-nothing guarantee stops at the single step and that a mid-batch snapshot is canonical-but-not-settled; closing that to reader-visible batch atomicity (a completion marker or batch critical section) is genuinely new contract territory, and the note already routes it to Open Question 4. Likewise the across-servers survival of G1 (Open Question 6). These are future-ASN material, not gaps in this one.

META: none — the note specifies system guarantees (a contract MIC that any realization must meet, explicitly "no lock, no transaction, no scheduler"), not implementation mechanics, so it sits squarely in the specification.

VERDICT: REVISE
