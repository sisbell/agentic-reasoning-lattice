# Review of ASN-0126

I read this as a genuinely careful note. The forgetful-projection bridge (`π`), the effect-identity argument, the three-move R-Scope transfer for the Binary retraction wrapper, and the "born nullified" worked example are all rigorous — I checked the tumbler arithmetic in the ghost-root counterexample (`a = 1.1.0.1.0.1.0.2`, `zeros = 3`, `#E = 1`, so `a ∉ dom(Σ.L)` and `a ≠ a_emit`, P-tgt fails on both disjuncts, coverage is the whole link subspace) and the Step-1/Step-2 born-nullified trace (`a_R = …2.3 ∉ coverage(G_rng)`, `g = …2.4 ∈ coverage(G_rng)`), and both hold. The wp derivation correctly isolates C3 as the conjunct *newly* live under `→_sh`. The note honestly discloses that single-tuple-scope is an app obligation rather than a `→_sh` guarantee — that is a disclosed design boundary, not a defect.

One real inconsistency remains.

## REVISE

### Issue 1: "stays inert until an app registers a type" contradicts the immutable-registry thesis (P1)

**ASN-0126, Worked illustration ("Two Multi types coexist (C0)")**: "At the opposite extreme C0 permits the *empty* registry `Σ_init.registry = ∅` … so `→_sh` never extends `dom(Σ.L)` — the substrate stays inert until an app registers a type."

**Problem**: P1 (RegistryInvariance) proves `Σ.registry = Σ_init.registry` at *every* `→_sh*`-reachable state — the registry never drifts. The framework also defines no registration operation: the operation set is the inherited `{Emit_K, Observe_K, Nullify}` plus the refined `K.λ_sh`, none of which touches the registry (every step frames it, per Registry permanence). Consequently a substrate whose `Σ_init.registry` is empty stays inert *forever*, not "until" some later registration event — registration cannot occur at runtime. The word "until" describes a temporal progression the note's own central theorem forecloses. The deeper gap behind the slip: the note repeatedly speaks of an app "declaring"/"registering" a type ("for each type an app declares," "until an app registers a type," and OQ4's "app-declared entries") but never states plainly that registration is confined to the construction of `Σ_init` and that no runtime registration primitive exists. A precise reader hits the contradiction directly: how can an app register a type at run time when `Σ.registry` is provably constant?

**Required**: Align the prose with P1. State explicitly that the registry is populated only when `Σ_init` is constructed and that the framework provides no runtime registration operation (the registry is fixed input to the dynamics, not a mutable component). Then rephrase the empty-registry sentence to drop the temporal "until" — e.g. "an empty `Σ_init.registry` yields a permanently inert substrate: with no type registered at construction and no runtime registration, `→_sh` can never extend `dom(Σ.L)`."

## OUT_OF_SCOPE

### Topic 1: Dynamic (runtime) type registration
**Why out of scope**: This framework's deliberate commitment is an *immutable* registry (P1), and that is a legitimate design. A framework that lets `Σ.registry` grow during a run — with a `Register` primitive, its own freshness/conflict discipline, and a re-proof of the conformance invariants under a non-constant registry — is a different framework, not an error here. (Note: this is distinct from Issue 1, which is about making the *current* static design internally consistent.)

### Topic 2: Validation of app-supplied shape declarations
**Why out of scope**: C0 *assumes* `Σ_init.registry` is well-formed (shape values in `{Unary, Binary, Multi}`, coverage-class keys unique). How a construction-time API checks an app's declaration against C0 before admitting it — and what happens to a malformed declaration — is a registration-protocol concern for the operational-semantics layer the note's Open Questions already point at, not a state/operation/invariant of this ASN.

The note's own Open Questions 1–6 (idem semantics, behavior catalog, default predicates, standard registrations, predicate composition, extension beyond `F=1`/`N=3`) are correctly scoped as successor work; no objection there.

VERDICT: REVISE
