# Review of ASN-0108

I checked the proofs claim by claim. The technical content holds up well: the W2 weakest-precondition analysis (the `j' = j ∨ (j ≥ m' ∧ j' ≥ m')` formula and the strict membership-identity ⊋ frozen-prefix ⊋ wp nesting) is correct against the cases; W4's rank-block induction and W9a's `⌈m/N⌉ + [N divides m]` count check out against all four boundary walks (m=4, m=5, m=0, N>m); W6a's bridge from F-LAMBDA to the discoverability reading via a frozen image is sound; W9b's per-link multiplicity bound is intricate but the charge-injectivity argument survives scrutiny. The uses of T9, S0, L12/L12a/LP13, LP11, LP18, D-NONMONO, F-V/F-LAMBDA are all faithful to the foundations. The findings below are all anti-bloat / clarity, not correctness.

## REVISE

### Issue 1: W5's claim statement buries the claim and forward-references downstream material

**ASN-0108, W5 (OrderStability), statement**: "Resumption is *coherent* — *under the hypothesis that the pass terminates*, it skips no link that *remains* an undelivered tail matcher ... and — unconditionally — re-delivers no already-seen link that matches in both the cursor-setting state and the resume state — *if* the key satisfies **clause 1 (cut-point preservation)** at every cursor the reader actually holds ... for every `a` matching in both states, `κ_{Σ'}(c) <_K κ_{Σ'}(a) ⟺ κ_Σ(c) <_K κ_Σ(a)`."

**Problem**: This is the note's central guarantee, and it is one ~200-word sentence interleaving the claim, two differently-scoped halves, the governing condition, and clause 1's full definition — then continuing with "sufficient but not necessary," a clause-2 aside ("likewise *not* necessary for coherence; it belongs to the *sufficient* discipline below"), and a scope carve-out. The extractable requirement — *clause 1 at every visited cursor ⟹ (no re-delivery unconditionally) ∧ (no skip of a continuously-matching tail matcher, given termination)* — cannot be read off without disassembly. Two patterns compound it: the statement forward-references later material ("the sufficient discipline below", "the W9b scope"), coupling the claim to W9b inside its own statement slot; and the clause-2-non-necessity aside is redundant with the dedicated "Clause 2 governs only which order..." paragraph immediately following it and with W9d.

**Required**: State the claim crisply (condition ⟹ the two scoped guarantees), then put the sufficiency-not-necessity remark and the whole-pass scoping in separate sentences. Drop the clause-2 aside from the statement (delivered by the next paragraph and W9d). Replace the forward references with a local statement of what is assumed.

### Issue 2: The absolute-invariance / uniform-shift elaboration serves no claim

**ASN-0108, W5, state-stability paragraph**: "**Absolute key invariance** — `κ_{Σ'}(a) = κ_Σ(a)` for every surviving link — is the simplest state-stable discipline, trivially giving both clauses; it too is stronger than necessary, since a key that shifts every value uniformly (every key incremented by a fixed amount) violates absolute invariance yet preserves every comparison, so it stays state-stable and coherence holds."

**Problem**: "Absolute key invariance" and the hypothetical uniform-shift key appear nowhere else. Both adopted keys (address, least-covered-I-address) are *state-stable*, and every per-key argument in W5/W6/W8/W9 invokes state-stability (or computability/allocation-monotonicity), never absolute invariance. The sentence establishes a hierarchy gap (state-stable ⊋ absolutely-invariant) that no downstream claim consumes — a self-contained "stronger than necessary" digression of exactly the kind this pass targets.

**Required**: Drop the absolute-invariance/uniform-shift elaboration. The load-bearing point is already made by "Both identity keys are therefore state-stable."

## OUT_OF_SCOPE

(none) — The note correctly defines no claim for the excluded topics (count-only retrieval, full-set FINDLINKS, MAKELINK, FOLLOWLINK, BEBE). The cardinality query (W10) is named only to be deferred, and multi-document enumeration, non-monotone-key delivery, cross-call completeness, and delivery/sizing correspondence are properly routed to the Open Questions rather than half-specified here.

VERDICT: REVISE
