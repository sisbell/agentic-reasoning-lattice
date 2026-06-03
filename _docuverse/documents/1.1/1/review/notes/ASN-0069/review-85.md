# Review of ASN-0069

This note carries `review-mode.anti-bloat`. The mathematical spine (V0–V12, the two inductions, the composite verification) is sound on the cases I checked — the sibling/chain distinction is consistent, the state-stamping in V8a/V11 is careful, and the empty-source branch is verified separately and correctly. The findings below are concentrated where prior cycles have accreted duplicated discharge prose and defensive meta-prose, plus one scope drift.

## REVISE

### Issue 1: Verbatim duplication of shared K.δ precondition discharges across sub-cases A and B
**ASN-0069, §"The Fork Composite", K.δ sub-case A and sub-case B**: 

Sub-case A: "Outer-precondition `T4-valid(d_new)` is discharged by T10a.4 ... Outer-precondition `¬Element(d_new)` follows from `Document(d_new)` ... Uniform-precondition `parent(d_new) ∈ E` is discharged in two steps. V1 gives `parent(d_new) = parent(d_src)` ... P8 ... yields `parent(d_src) ∈ E`. Composing ..."

Sub-case B: "Outer-precondition `T4-valid(d_new)` is discharged by T10a.4 ... Outer-precondition `¬Element(d_new)` follows from `Document(d_new)` ... Uniform-precondition `parent(d_new) ∈ E` is discharged in two steps. V1 gives `parent(d_new) = parent(d_src)` ... P8 ... yields `parent(d_src) ∈ E`. Composing ..."

**Problem**: Three of the five discharges — T4-validity (via T10a.4), `¬Element` (via `Document(d_new)`), and `parent(d_new) ∈ E` (via V1 + P8) — are stated near-verbatim in both sub-cases. They are genuinely sub-case-independent: the T10a.4 argument is "every output of `A_v(d_src)` is T4-valid," the `¬Element` argument is `zeros = 2 ≠ 3`, and the parent argument uses only V1's identity postcondition (which holds in both sub-cases) plus P8 on `d_src`. This is the "same statement in different words" (here, the same words) the anti-bloat pass targets.

**Required**: State the three shared discharges once before the sub-case split; retain under sub-case A only ChildSpawnFreshness for `e ∉ E`, and under sub-case B only the per-sub-case `d_prev ∈ E` / `¬Node(d_prev)` and FrontierEquivalence for `inc(d_prev, 0) ∉ E`.

### Issue 2: Defensive justifications and document-convention meta-prose in structural slots
**ASN-0069, §"Identity by Sub-Allocation"** (after V2): "We name this consequence so that downstream users of the operation can rely on it as a structural property of the operation itself, not as a metadata field that could fall out of sync."

**ASN-0069, §"What Must Be Constructed"**: "Most of this ASN's narrative and the worked example treat the first fork, where `d_op = d_src`; the content-inheritance claims below are stated against `d_op` so that they remain correct for subsequent forks, and reduce to the `d_src` reading when `d_op = d_src`."

**ASN-0069, §"The Empty-Source Case"**: "The behavior of each property over the empty case is discharged concretely on `d_src°` in the worked example's 'Empty source (V7)' paragraph below; we do not restate that case-by-case here."

**Problem**: The first is a defensive justification of *why a property is named* rather than what it states. The second is essay content about the document's own notational convention. The third is a forward deferral to a downstream location that does not advance the reasoning at its site. None advances the argument; each is prose the reader must skip past.

**Required**: Delete the naming rationale (V2's statement stands on its own). Replace the convention paragraph with a single clause at first use of `d_op` ("`d_op = d_src` on a first fork, the prior version otherwise"). Drop the empty-case deferral sentence; the "organising principle is quantifier domain" sentence that follows is the substantive content and suffices.

## OUT_OF_SCOPE

### Topic 1: Link-discoverability apparatus in V6a (coverage, project, discoverable_from)
**ASN-0069, §"Subspace Selectivity"**: V6a introduces three local definitions — `coverage(e)`, `project(a, i, d, Σ)`, `discoverable_from(a, d, Σ)` — built on link endset structure, spans (T12), and slot indexing (L3), then proves the fork preserves projection.

**Why out of scope**: "Link semantics" is explicitly out of scope for this ASN. The fork-relevant guarantee is the consequence that shared I-addresses (V4, V5) keep links attached identically — that belongs here. But the projection/coverage/discoverability *apparatus* is link-semantics primitive machinery, defined by no foundation and not specific to forking; it belongs in a future link-semantics ASN that this ASN would then reference. V6a(i) (`L' = L`, a one-line frame consequence) can remain; V6a(ii)–(iii) and their three supporting definitions are the drift.

VERDICT: REVISE
