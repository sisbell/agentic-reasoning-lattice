# Review of ASN-0126

The note is largely rigorous: the projection bridge is constructed carefully, the wp derivation correctly isolates gate (enablement) from landing conjuncts, and the worked illustration supplies a genuine non-trivial witness (born-nullified) rather than a trivial check. My findings are modest but real.

## REVISE

### Issue 1: P3 (IdemStability) is a content-free property
**ASN-0126, Properties established / Registration entries**: "P3 (IdemStability). For every registered K, `idem(K) ∈ {⊤, ⊥}` is a structural property of K, equal at every reachable state. *Corollary of P2*."
**Problem**: Nothing in this ASN reads `idem`. No gate, predicate, invariant, or operation consults it — `Sh-conf` reads only span counts and `shape(K)`; `→_sh` ignores it; its entire semantics is deferred to Open Question 1. P3 therefore establishes stability of a field with no derivable consequence in this note. Per the depth standard ("postconditions established but consequences not explored"), an elevated numbered Property asserting invariance of an inert field is weight without load. The same applies to its appearance in the worked-illustration registry table, where the `idem` column does nothing.
**Required**: Either give `idem` a consuming role in this ASN (a predicate or gate clause that reads it), or demote `idem` to a reserved registry field mentioned once and drop P3 (fold its one-line argument into a remark under P2). Don't carry a Property whose only content is "a field nobody reads doesn't change."

### Issue 2: The gate-vs-landing separation is previewed in prose before it is demonstrated
**ASN-0126, The shape-gated emit / P4 / P6**: the claim "a gate-enabled emit may still fail the active-subset postcondition (born-nullified)" appears as prose in the wp paragraph ("may still fail to land active... the born-nullified case"), again in the next paragraph ("the born-nullified guard remains live"), again in P4 ("records the gate's enablement half only"), and again in P6 ("makes **no** claim about the active subset") — then is finally *demonstrated* in the Worked illustration.
**Problem**: This note carries the `review-mode.anti-bloat` classifier, and this is the flagged pattern: multiple paragraphs across sections previewing the same downstream conclusion. The worked illustration earns its place (it is the concrete witness); the repeated previews are meta-commentary a reader must skip past. The substantive, non-redundant content is exactly two things: the wp derivation (which conjunct is the landing condition) and the worked demonstration. The interstitial restatements add nothing.
**Required**: State the gate≠active-landing separation once — at its derivation in the wp — and let the worked illustration carry the demonstration. Strip the restatements in the post-wp paragraph, P4's tail clause, and P6's tail clause to bare pointers, or delete them.

### Issue 3: "well-defined without reference to state" overstates
**ASN-0126, P2 / P5**: "`shape(K)` is well-defined **without reference to state**" and "`Sh-conf` consults **no state-indexed set**... reading only the P1-invariant `shape(K)`."
**Problem**: `shape(K)` is a lookup into `Σ.registry`, which *is* state — the fourth component of `Σ`. It is invariant (P1), but it is not state-free. The honest statement is "depends only on the *invariant* component of state, hence is constant across reachable states." As written, P2/P5 conflate "invariant under `→_sh`" with "not a function of `Σ`," which is precisely the distinction the registry-as-parameter framing ("not state the substrate evolves through but a parameter") is trying to make. The prose undercuts it.
**Required**: Replace "without reference to state" with "depends only on the P1-invariant registry, hence is constant on `→_sh*`," and likewise tighten P5's "consults no state-indexed set" to "consults only the P1-invariant registry."

## OUT_OF_SCOPE

### Topic 1: Loss of R-Scope's single-tuple-scope under Binary-registered R
By registering R as Binary, `→_sh` admits non-unit contiguous-range retraction to-spans, so ASN-0086's R-Scope single-tuple result (`{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`) and UnitDepthRetractionDiscipline no longer hold at the framework level — they survive only when the app self-imposes the unit-depth wrapper.
**Why out of scope**: This is correctly acknowledged in Single-source as a deliberate weakening, and the framework operates at the ungated-substrate level, not the disciplined relational layer. Re-establishing a retraction discipline (and any invariant that depends on single-tuple scope) belongs to the layer note that defines operational semantics, not to this structural framework.

### Topic 2: idem/behavior semantics, predicate composition, standard registrations
Open Questions 1–5.
**Why out of scope**: Explicitly deferred; these are new territory for a successor note, not gaps in the structural commitments established here.

VERDICT: REVISE
