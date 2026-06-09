# Review of ASN-0126

## REVISE

### Issue 1: Span-count-vs-coverage coalescing burden analyzed for F but skipped for Binary's G

**ASN-0126, Shape-conformance**: "One edge follows from counting spans rather than coverage... a source presenting one contiguous extent as two abutting spans `(a, ℓ₁)`, `(a ⊕ ℓ₁, ℓ₂)` has `|F| = 2` and fails every shape... coalescing abutting spans to that canonical one-span form is the app's responsibility before emit."

**Problem**: This edge is resolved exclusively for F ("single-source means a single span as emitted"). But Binary's G slot is *also* a single-span slot (`|G| = 1`) subject to the identical span-count-vs-coverage divergence: an app emitting `succession` whose target is one contiguous predecessor presented as two abutting spans has `|G| = 2` and fails Binary's `Sh-conf`, even though its coverage equals the conformant one-span form. The note exhaustively treats the F case and is silent on the structurally identical G case. Under the Dijkstra standard, this is a skipped case in the conformance analysis — the one slot besides F where span-count matters (Multi's G never rejects, Unary's G is empty) is exactly Binary's G, and it is the one left unaddressed.

**Required**: State explicitly that the app-side coalescing responsibility extends to Binary's to-span — any single-span shape slot (`|F| = 1` for all shapes; `|G| = 1` for Binary) carries the same normalization burden — or argue why G is exempt. The Worked illustration's Binary case (`G = [c₁]`, already a single span) does not exercise this; an abutting-G witness would.

### Issue 2: Projection base case does not anchor to ASN-0086's Σ_init

**ASN-0126, The shape-gated emit**: "By induction on derivation length, π maps every →_sh*-reachable state to a →*-reachable state: the base π(Σ_init) is →*-reachable from itself... ASN-0086's structural lemmas — R0..., a_emit totality, L-ContiguousPrefix, PrefixSpanCoverage — are quantified over →*-reachable three-component states, so they hold at π(Σ)."

**Problem**: ASN-0086's R0, `a_emit`-totality, and L-ContiguousPrefix are quantified over states →*-reachable *from ASN-0086's Σ_init*. The induction establishes only that `π(Σ)` is →*-reachable from `π(Σ_init)`. "Reachable from itself" gives reachability from `π(Σ_init)`, not from ASN-0086's initial state. For the imported lemmas to fire at `π(Σ)`, the argument needs `π(Σ_init^{sh}) = Σ_init^{0086}` (or →*-reachable from it) — i.e., the framework's initial three components must coincide with ASN-0086's initial state. This equality is assumed but never stated, leaving the licensing step ("their conclusions transfer to Σ directly") resting on an unasserted premise.

**Required**: One sentence asserting `π(Σ_init) = Σ_init^{0086}` (the framework adds the registry to ASN-0086's initial state without altering C/M/L), closing the base case so the inherited lemmas are genuinely applicable at every `π(Σ)`.

## OUT_OF_SCOPE

### Topic 1: Empty-registry degenerate substrate
A substrate with `Σ_init.registry = ∅` is C0-conforming (finite) but admits no link emit under `→_sh` (precondition (i) always fails). The behavior is well-defined (only C/M grow); whether to forbid the empty registry is a construction-policy question, not a defect in the structural commitments here.

### Topic 2: Idem semantics and standard registrations
The operational meaning of the idem flag and whether R/`supersedes`/`retired` ship pre-registered are correctly deferred (Open questions #1, #4). P3 commits only to structural presence and state-independence, which is fully discharged.

VERDICT: REVISE
