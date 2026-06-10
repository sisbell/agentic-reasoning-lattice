# Review of ASN-0126

This is a technically strong note. I checked the core arguments — the wp refinement (both the `K ≁ R` self-nullification branch and the newly-live C3 conjunct), the ProjectionBridge construction, the retraction re-derivation's "frame the two post-states together" step, the RegisteredAdmissible chain, and the Born-Nullified worked scenario (addresses, `a_emit` chain, half-open coverage of `G_rng`, and `nullified` membership) — and they hold up. The findings below are concentrated in the area the `review-mode.anti-bloat` classifier flags: forward-reference accretion driven by inverted lemma ordering, plus two boundary-coverage gaps.

## REVISE

### Issue 1: P5 (and RegisteredAdmissible) are defined after the sections that consume them

**ASN-0126, "Retraction as an attributed Binary" / "The projection bridge" / "Weakest precondition of the shape-gated emit"**: the retraction re-derivation states "the conforming gated emit therefore exists by P5 (GateRealizability, **proved below**)", and the projection bridge's B2 says R0 "is therefore obtained not through B2 but by **lifting (P5)**" — yet P5 and the Lemma (RegisteredAdmissible) it depends on are both first stated several sections later, inside "Weakest precondition of the shape-gated emit."

**Problem**: Two different sections defer to the same downstream lemma — exactly the "multiple paragraphs in different sections defer to the same downstream location" pattern. The note even writes "proved below," acknowledging the inversion in text. P5 does not depend on the wp analysis at all: its proof rests only on the gate, effect-identity, the projection bridge, and RegisteredAdmissible — all established before the projection bridge ends. Its placement in the wp section is thematic ("the liveness dual of P3"), and that thematic pairing is what forces the forward references.

**Required**: Relocate P5 and RegisteredAdmissible to immediately after the projection bridge (their last dependency), so "Retraction as an attributed Binary" and the B2 discussion cite an already-established result rather than pointing forward. The "liveness dual of P3" framing can remain as a one-line remark at the wp section.

### Issue 2: The "Existence-of-successor results are excluded" paragraph is method meta-prose plus a use-site inventory

**ASN-0126, "The projection bridge"**: "*Existence-of-successor results are excluded.* An ASN-0086 result whose conclusion has the form `∃ Σ' : Σ → Σ' ∧ …` does not transfer via B2 … The one such result this note needs, R0 (TupleAddressFreshness), is therefore obtained not through B2 but by lifting (P5)…"

**Problem**: B2's own statement already scopes transfer to "a predicate over the C/M/L components — either of a single `→*`-reachable state, or of a transition between two states each separately exhibited as `→_sh`-reachable." That phrasing structurally excludes `∃Σ'` conclusions; the separate paragraph re-derives that exclusion as commentary about the transfer *method*, then appends a use-site inventory ("The one such result this note needs, R0…"). This is the defensive-justification / use-site-inventory pattern the anti-bloat pass targets.

**Required**: Drop the standalone caveat. If a pointer is wanted, keep at most a one-clause note that B2 yields no `→_sh`-successors; place the R0-versus-lifting remark at P5, where the lifting is actually performed (and, once Issue 1 is fixed, where R0's value-shape consequence is used).

### Issue 3: The wp "absorption" narration restates inherited conditions to justify their absence

**ASN-0126, "Weakest precondition of the shape-gated emit"**: "The gate's other inherited component, L3, is likewise absent from the wp, for the parallel reason: its three clauses — arity ≥ 3, both content slots in `Endset`, and a non-empty type slot — are discharged respectively by precondition (0) …, the input typing `F, G ∈ Endset`, and Lemma (RegisteredAdmissible) …; so L3 is absorbed by guards already accounted for and contributes no conjunct of its own."

**Problem**: L3's three clauses are foundation content (ASN-0043); re-enumerating them and discharging each to explain why L3 does not appear as a wp conjunct is exhaustiveness bookkeeping justifying an absence, not reasoning that advances the weakest precondition. The parallel `K ∈ T_admissible` "absorbs it" passage is the same move. RegisteredAdmissible is needed; the surrounding "likewise absent / for the parallel reason / contributes no conjunct of its own" narration is not.

**Required**: Collapse to a single clause — e.g., "L3 and `K ∈ T_admissible` are discharged by precondition (0), the input typing, and RegisteredAdmissible, so neither contributes a wp conjunct" — without re-listing L3's clauses.

### Issue 4: The worked illustration omits the "possibly zero targets" Multi case it advertises

**ASN-0126, "Three shapes by G span count" / "Worked illustration"**: the shape table defines Multi as "A single source connected to finitely many — **possibly zero** — target spans," and the conformance definition makes `Sh-conf(Multi, F, ∅)` hold. But every Multi example in the illustration uses `|G| = 2` ("`G = [c₂] ∪ [c₃]` … `|G| = 2 < ∞`"); the `G = ∅` boundary under Multi is never exercised, nor is the minimal/empty registry.

**Problem**: The zero-target Multi case is the boundary where a Multi tuple becomes shape-indistinguishable from a Unary tuple, separated only by type registration — precisely the "shapes classify *registrations*, not tuples" claim the note makes. Leaving it unillustrated skips the boundary (`zero`) the rubric requires and the case the table explicitly advertises. The empty registry (`Σ_init.registry = ∅`, permitted by C0's `|registry| < ∞`) is a second unexercised boundary, under which `→_sh` can never extend `dom(Σ.L)`.

**Required**: Add a one-line Multi emit with `G = ∅` (showing it conforms yet is typed Multi, not Unary). Optionally note the empty-registry degenerate case in passing.

## OUT_OF_SCOPE

### Topic 1: Operational semantics over the shapes (idem, behavior catalog, default predicates, composition)
**Why out of scope**: Open Questions 1–3 and 5 ask what guarantees/behaviors each shape unlocks. The note correctly fixes only well-formedness (the static gate) and registry permanence; behavioral semantics belong to the successor note it names.

### Topic 2: Dynamic registration and richer arity/multi-span sources
**Why out of scope**: How `Σ_init.registry` is populated (OQ4) and any path past `F=1`/`N=3` (OQ6) are deliberately deferred. The immutable-registry design is internally complete as specified; loosening it is a different framework.

### Topic 3: Read-side treatment of `Observe_K` under shapes
**Why out of scope**: `Observe_K` is read-only and needs no gate; P6 already guarantees the slices it reads contain only conforming tuples. Shape-aware read filters fall under OQ2's behavior catalog.

META: not applicable — the note specifies abstract state (the registry), an abstract precondition-refinement of the transition relation (`→_sh`), and state-independent invariants (P1–P6), all of which an alternative implementation would have to satisfy.

VERDICT: REVISE
