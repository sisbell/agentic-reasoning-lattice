# Review of ASN-0069

## REVISE

### Issue 1: V8d trailing paragraphs are reviser-drift meta-prose
**ASN-0069, §"Structural Correspondence", the two paragraphs after the V8d blockquote**: 

> "V8d concerns the correspondence... The store-persistence of the shared content is a separate, unconditional matter, and we do not fold it into V8d. Writing `a = M''(d_op)(v)`... That store-persistence is exactly V12(b) below; we let V12(b)/P0 carry it rather than restate it under V8d's hypothesis, where it would falsely appear contingent on non-targeting."

> "The whole-document non-targeting hypothesis is the cleanest condition V5a supports. A finer claim — that an individual position `v` survives even when *other* positions... are edited — is available under K.μ⁻'s retention semantics... but it requires the per-position frame rather than the whole-document one, so we do not fold it into V8d."

**Problem**: Neither paragraph advances the V8d claim. Both explain what V8d *deliberately excludes* and why — store-persistence (deferred downstream to V12(b)) and a finer per-position claim (imagined, then declined). This is the reviser-drift pattern the anti-bloat classifier targets: prose justifying the document's organization (a recent split, per commit `revise(asn-69/V8d): split store-persistence out`) rather than stating object-level content, plus deferral to a downstream location ("V12(b) below"), plus an imagined finer case the claim's hypothesis already excludes. A reader following the derivation must skip both paragraphs to reach V9.

**Required**: Delete both paragraphs. V8d's blockquote already states the claim and its derivation completely; the exclusion of store-persistence is self-evident from V8d's text (it never mentions `dom(C)`), and V12(b) carries store-persistence on its own. If a one-clause cross-reference is wanted, a parenthetical "(store-persistence is V12(b))" suffices.

### Issue 2: V8d Properties-Introduced row states an exclusion, not the claim
**ASN-0069, §"Properties Introduced", V8d row**: "Perpetuity of correspondence: while neither `d_op` nor `d_new` is M-targeted, V8's equality... persists (V5a) — store-persistence of the shared content is V12(b)/P0, not part of V8d"

**Problem**: The summary table should record what each property *claims*. The trailing clause "store-persistence... not part of V8d" reproduces Issue 1's exclusion prose inside a structural slot — the same statement in different words appearing both in V8d's body and in the index row.

**Required**: Trim the row to the positive claim: "Perpetuity of correspondence: while neither `d_op` nor `d_new` is M-targeted, V8's equality `M''(d_op)(v) = M''(d_new)(v)` persists (V5a)." Drop the exclusion clause.

## OUT_OF_SCOPE

### Topic 1: Operand semantics on subsequent forks (inheriting from a prior version, not d_src's current state)
On a subsequent fork, J4 fixes `d_op = d_prev`, so "fork of `d_src`" inherits the prior version's content rather than `d_src`'s current arrangement — and may be empty even when `d_src` is non-empty (§"The Empty-Source Case"). Whether that is the intended CREATENEWVERSION semantics is a question about J4 itself.
**Why out of scope**: J4's operand-tracking rule is fixed in foundation ASN-0047; ASN-0069 consumes it faithfully. Any concern belongs against the foundation, not this ASN.

VERDICT: REVISE
