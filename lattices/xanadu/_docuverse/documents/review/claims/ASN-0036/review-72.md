# Cone Review — ASN-0036/D-CTG-depth (cycle 3)

*2026-04-14 21:01*

I've read the foundation statements and the ASN carefully. Here are the new cross-cutting findings.

---

### S8-depth, D-CTG, and S8-fin are peer constraints on dom(M(d)) with inconsistent formal classifications
**Foundation**: S8-fin labels itself `*Invariant:*` and provides an inductive proof framework: base case ("In the initial state Σ₀… dom(Σ₀.M(d)) = ∅… The empty set is finite"), inductive step (deferred to operations), and an explicit obligation statement ("every operation specification must individually discharge the obligation")
**ASN**: S8-depth labels itself `*Axiom:*` with no proof structure and no deferred obligation. D-CTG labels itself `*Invariant:*` with no proof structure and no deferred obligation.
**Issue**: All three properties constrain `dom(M(d))` across state transitions — S8-depth requires uniform depth within a subspace, D-CTG requires contiguous occupancy, S8-fin requires finiteness. Each must be preserved by every operation (INSERT, DELETE, etc.). But their formal classifications diverge in two ways. First, S8-depth is an axiom while D-CTG and S8-fin are invariants. An axiom constrains valid states but imposes no verification obligation on operation specifications; an invariant requires per-operation proof of preservation. If S8-depth is genuinely an axiom, operation authors have no formal obligation to prove that new V-positions maintain uniform depth — yet an INSERT that places a depth-3 position in a depth-2 subspace would violate it. Second, among the two invariants, S8-fin provides an explicit deferred-obligation framework while D-CTG provides none — an operation author reading the formal contracts would know to prove finiteness preservation (S8-fin says so) but would find no analogous statement for contiguity. For TLA+ formalization, all three need the same treatment: either state constraints (checked against the behavior spec) or inductive invariants (proved via Init ∧ □[Next]_vars), but the current ASN gives each a different status.
**What needs resolving**: Either classify all three as the same formal kind (axiom or invariant) or explicitly justify why they differ. If invariants, each needs at minimum a base-case argument and a statement that operations must individually discharge preservation — matching S8-fin's existing framework.

---

### S8-fin's base case and D-CTG's initial-state obligation both depend on Σ₀, which has no formal definition
**Foundation**: Σ.M(d) (Arrangement): defines `M(d) : T ⇀ T` but does not specify its initial value
**ASN**: S8-fin proof: "In the initial state Σ₀, no operations have been performed, so `dom(Σ₀.M(d)) = ∅` for every document `d`. The empty set is finite." D-CTG: no initial-state argument at all.
**Issue**: S8-fin's inductive proof rests on a base case — `dom(Σ₀.M(d)) = ∅` — that is asserted in prose but grounded in no formal contract. The arrangement definition (Σ.M(d)) characterizes the type of `M(d)` (partial function `T ⇀ T`) without specifying its value in any state, let alone the initial one. The claim `dom(Σ₀.M(d)) = ∅` is an implicit axiom about system initialization. D-CTG has the same dependency — contiguity holds vacuously when `V_S(d) = ∅`, so its truth in the initial state requires `dom(Σ₀.M(d)) = ∅` — but provides no base case at all. S8-depth as an axiom holds trivially for empty domains, but its truth in the initial state is also never stated. For TLA+ formalization, the initial state is defined by an `Init` predicate — a first-class construct that must appear somewhere. Currently, initialization is embedded in one property's proof text (S8-fin), invisible to the other two properties that depend on the same assumption, and absent from any formal contract.
**What needs resolving**: A definition or initialization property — either within Σ.M(d) or as a standalone property — that formally specifies `dom(Σ₀.M(d)) = ∅` for all `d`, giving S8-fin's base case a formal anchor and D-CTG a citable initial-state argument.
