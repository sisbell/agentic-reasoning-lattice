## What this is

The reactive coordination layer: a forward‑chaining rule engine that watches the substrate, fires rules through the operation surface, and — the note's real subject — defines *quiescence* (the engine's terminal "done" state) as a predicate‑language fact and proves termination as a *conditional* theorem, every hypothesis (extinction discipline, bounded input, fair scheduling) named. A rule is a watcher (a Boolean trigger over a finite domain) plus an output contract; the registry is a finite set of them running as one actor on a shared substrate.

## Design commitments

**Forced — downstream design cannot violate these:**

- **Quiescence is recognizable from inside.** `quiescent_R(Σ)` is a *pure, decidable, terminating* PL term over (state, registry), and every observer computes the same verdict (observer‑uniform by purity). Consequence: done‑ness is never authoritative stored state — you journal neither "quiescent" nor the agenda that approximates it; both are recomputed.
- **A quiescent state is a fixed point of firing**, unconditionally — independent of discipline, fairness, or convergence. The engine may halt its own firing on first detection; only fresh *environment* input can re‑arm it.
- **Rules contract on outputs, not bodies.** Extinction discipline is decided by trigger evaluations at pre/post states (public PL facts); the body choosing emissions is outside the model. The engine treats bodies as black boxes, and nondeterministic bodies are admissible exactly when *all* their permitted outputs honor the contract.
- **The registry is one actor on an open, shared substrate.** Environment steps (other agents, registries, raw input) interleave with fires; between two fires a domain may grow *or* shrink. The termination hypotheses bound *external input*, never the registry's own reachable states. There is no closed‑world assumption anywhere — and "the registry is done firing" is a strictly weaker claim than "the system is quiescent."
- **Fires are atomic against environment interleaving (H‑ATOM) and finite (H‑FIN).** Environment steps fall *between* fires, never within one. This forces a concurrency boundary around each fire and makes any contract admitting an infinite emission set illegal.
- **State changes only through the fixed surface `{Emit_K, Nullify_Binary}`; reads (`Observe_K`) are not emissions** — and that surface is append‑only/monotone. (Verified for Green: the granfilade is strictly append‑only, ISAs are never removed or reused, the spanfilade is write‑only, and content deposits grow the content domain *alone*.) The only way the engine moves state is monotone deposition.
- **Termination is conditional, with hypotheses named.** Recognizability and absorption are unconditional; *reaching* quiescence needs (extinction) + (bounded growth / bounded input) + (fairness), and the note pins exactly which combination buys "registry inert," "reached and held," or nothing.
- **SF‑spelling + extinction discipline = at‑most‑once firing per argument (Q‑EXT), and this is registration‑checkable.** This is the reward path: certify both and you get a monotone‑work‑queue engine and a clean termination bound.

**Conventional (chosen, not forced):**

- Triggers may be inline PL terms *or* `pdef` addresses (registry‑as‑substrate‑content). The note allows both; the choice carries consequences (below).
- The canonical scope tiers (per‑target, per‑collection, system‑wide) are *application vocabulary*. The substrate commits to no particular scopes — any PL predicate is a scope.

## What must be built

- A **rule registry with registration** that accepts (domain expression, Boolean trigger, emission contract) and, at registration, *classifies* the rule: is the trigger an SF spelling? is it extinction‑disciplined (Marker pattern)? is its domain grow‑only? — rejecting or flagging what it cannot verify.
- A **trigger evaluator**: given a state, enumerate each rule's finite domain and evaluate its trigger, resolving views to one common view.
- A **quiescence recognizer**: the pure, decidable "no domain element has a true trigger" conjunction — the engine's done‑oracle and recovery confirmation pass.
- A **firing engine**: invoke a black‑box body, take its emission set, and apply it through the surface *atomically* (against environment steps) and *finitely*.
- A **scheduler**: select fireable `(ρ, x)` and satisfy fairness (every trigger‑true occurrence eventually fired, removed, or falsified).
- A **scope restrictor**: filter domains by a scope predicate through the canonical bodies, preserving S‑monotonicity.
- A **status monitor** distinguishing "registry inert (done firing)" from "system quiescent" — genuinely different in the open model.

## Implementation approaches

### Trigger evaluation + quiescence recognition

Build three tiers; pick per registry:

- **Authoritative full scan.** Enumerate every rule's finite domain, evaluate every trigger; quiescent iff none true. Stateless (no index to keep consistent with Σ), obviously correct, and Q0 guarantees it terminates. Use it as the *ground‑truth* quiescence check and the *recovery* path. This is the simplest thing that honors Q0 — start here.
- **Monotone work queue (the SF fast path).** When registration certifies all‑SF + extinction (a Marker‑pattern registry), each `(ρ, x)` fires at most once and a falsified SF trigger never re‑arms. So: enqueue trigger‑true arguments, fire each once, and *never re‑examine a fired one*. New arguments enter only by domain growth (own emissions or environment). No retraction logic, no re‑arming — far simpler than a general rule engine. Empty queue is your quiescence *hint*; confirm with the full scan when it matters. Pick this whenever SF + extinction is certified — which the note actively steers you toward ("triggers in SF, termination conditions in ST").
- **Change‑propagation network (the non‑SF remainder).** Where triggers aren't SF, re‑arming is real, so maintain a dependency index — the discrimination‑network idea from RETE/TREAT, *minus* the multi‑condition join machinery, since triggers are single‑element guards, not joins. Index "emission of type K → triggers it can move" directly from Q‑FLIP's falsifier inventory (retraction of a read slice, a default‑view move, a footprint change, a bare active‑slice deposit flipping an `∃`‑trigger), and re‑evaluate only affected triggers per emission. More machinery and a derived index to keep consistent, but it's the proven forward‑chaining architecture and the note hands you the exact dependency analysis.

In either incremental tier the agenda is a **hint** in the precise sense — recomputable from (Σ, R) by the full scan on a miss — so never journal it; rebuild on load.

**Indexing the Marker trigger.** The Marker trigger is a coverage‑membership query: "is address `a` covered by any audit‑slice K‑tuple?" Coverage is the infinite downward closure — verified *membership‑testable by tumbler‑prefix truncation, not enumerable* (the finite denoted endset is the separate, enumerable set). So index audit slices by coverage region: a prefix/trie index on tumbler addresses answers the test directly, and Green's **spanfilade** is the proven enfilade for exactly this "which tuples' endsets cover this region" query. Use a prefix index for the common case; reach for a full spanfilade‑style enfilade only when you also need its richer span queries.

### View normalization

Compile each trigger to one canonical view *at registration* (the fixed‑view‑base rebuild + UV filter — "a change of spelling, not of value"), and keep evaluation single‑view. The alternative — resolving views lazily on every read — skips the compile step but re‑pays resolution on every evaluation. Put the function where it belongs: view resolution is a property of the trigger, so fix it when the trigger is registered. Single‑view registries pay nothing.

### Firing / emission application

Treat a fire as a transaction: snapshot Σ, invoke the body, collect the emission set, optionally validate it against `Post_ρ`, then commit (apply through the surface) or discard. This buys H‑ATOM and lets a misbehaving body roll back. Persistent (structurally‑shared) state makes the snapshot effectively free — which is exactly the project's immutable‑Σ / pure‑operation modeling. The repo's own substrate is the proven pattern: workers buffer emissions to a per‑worker journal and the orchestrator flushes atomically — **buffer‑then‑flush is H‑ATOM**. For idem=⊤ types, dedup is content‑addressed collapse; but for Marker rules the audit‑slice reading makes a fire *necessarily a dedup miss* (this is the note's Q3 argument, not a Green source claim), so the engine needn't special‑case dedup or born‑nullified deposits for them — the spelling carries it. Runtime choice: validate emissions against `Post_ρ` (defensive) vs. trust registration‑certified bodies (fast); validate untrusted rules, trust certified ones on the hot path.

### Scheduler

Left open by the note, but the contract is sharp. For the SF + grow‑only common case a plain **FIFO agenda is weakly fair and sufficient to reach and hold** quiescence (regime ii) — no environment‑idle hypothesis. Round‑robin and priority‑with‑aging also discharge weak fairness (aging orders only *in‑domain* arguments). The rare case — non‑grow‑only domains under an environment that cycles arguments out of phase — needs *strong* fairness (H‑SFAIR) or environment‑idle even to *reach* quiescence, and H‑SFAIR is satisfiable only under a *turn‑fairness* the substrate cannot enforce (a joint scheduler+environment condition). So make the rare case *correct, not fast*: keep absorbing (Q1 always holds) and honestly report "work bounded, quiescence not reached" rather than claim termination. Note too that the engine's total work is bounded by total external input (Q5a): if a deployment *needs* termination, it must bound external input itself — admission control / backpressure — because the engine can't.

### Registration analysis (lints / certificates)

- **SF‑spelling**: syntax‑directed and decidable (the PD0 rules, same family as ASN‑0130's shipped `certify_pd_stable`). Run at registration; it gates the fast path.
- **Extinction via Marker**: a decidable syntactic match of the trigger's `∃`‑witness against the emission form. Run at registration.
- **General extinction**: a meta‑level, reachability‑quantified obligation the note does not show decidable — admit as *unverified* (failure‑to‑verify is not violation) or require the Marker shape for any rule that wants the termination guarantee.
- A reusable **design pattern to certify**: type‑isolate rule domains (no rule's emission enlarges another's domain) and spell triggers SF over audit slices — then, as in the worked cmt/res registry, the only divergence route is unbounded environment input; internal termination is structural.
- Open Q1 asks whether a `pd_extinct` certificate should ship as a designated class alongside `pd_stable`. Build stance: **yes** — it turns "this registry terminates on bounded input" into a registration‑time lint, the whole point of the discipline.

### Persistence / recovery

State Σ: **append‑only journal recovered by replay** — matching the repo's `links.jsonl` + `paths.json` and Green's permascroll/granfilade (verified strictly monotone; no content‑level retraction; the mutable POOM is a separate V‑space projection). Replay is pure append. The registry R is a real choice: as **pdef substrate content** it is itself journaled, auditable, versioned, and stays evaluable even after de‑registration (PR3 keys on *ever*‑registration) — at the cost of carrying PR‑DISC; as **inline configuration** it loads separately, carries no PR‑DISC premise, but isn't auditable substrate content. The agenda and quiescence verdict are hints — recomputed on load, never journaled.

## Guarantees to uphold

- **Recognizability** (quiescence decidable from Σ+R) — *by construction* (Q0), provided the evaluator stays faithful to PL and view‑normalization preserves value. Don't admit out‑of‑PL trigger forms.
- **Absorption** (quiescent ⟹ firing is a fixed point) — *by construction* (Q1), unconditional.
- **Observer‑uniformity** (all observers agree on the verdict) — *by construction*, from purity; requires evaluation be a pure function of (Σ, R), no hidden state.
- **At‑most‑once firing** (SF+extinction) — *actively enforced*: registration classification plus runtime honoring of the extinction contract (the body must emit the falsifier).
- **Atomicity of fires** (H‑ATOM) — *actively enforced* by the concurrency boundary / transactional flush.
- **Finiteness of fires** (H‑FIN) — *actively enforced*: reject contracts admitting infinite emission sets.
- **Reaching quiescence** — *conditional and partly outside the engine*: needs bounded external input and an environment hypothesis (idle, or turn‑fairness for H‑SFAIR) the substrate cannot enforce. The engine guarantees only the *registry‑side* half — finitely many real fires, inert past the last — under bounded input + fairness.

So recognizability, absorption, and observer‑uniformity are free; at‑most‑once, atomicity, and finiteness need enforcement; full termination is conditional and environmental.

## How it fits

- Leans on **ASN‑0129** for the trigger language — PL evaluation, finite QD‑domain enumeration, the view machinery, and the PD0–PD2 dynamics that classify a trigger SF/ST (and so decide the fast path). On **ASN‑0128** for the firing mechanism — the `Emit_K`/`Nullify_Binary` surface, idem/dedup semantics, the `→_sh` gated step. On **ASN‑0086** for the typed relations triggers read — the active/audit slices with `A_K ⊆ L_K`, which is what makes the audit‑slice SF discipline (and the Marker‑pattern dedup argument) go through. On **ASN‑0126** for the state model and the monotone gated relation. On **ASN‑0130** for `pdef`‑triggers and the certificate machinery (`register_pred`, `certify_pd_stable`, PR‑DISC) this note would extend with a `pd_extinct` class.
- Hands *up* to the protocol/operational layer everything runtime: the scheduler and its fairness proof, the serialization model for multi‑step fires (H‑ATOM, and the turn‑fairness H‑SFAIR needs), the environment/workload model (which inputs are bounded, whether the environment idles), rule activation and governance (who may register rules), concurrency reconciliation, and violation policy. This note is the *semantics* of the reactive layer; the runtime lives above it.

## Decisions for the builder

- **Scheduling discipline and its fairness proof** — FIFO agenda for the SF/grow‑only common case; something stronger (and a stated environment assumption) only for non‑grow‑only registries.
- **Concurrency control for H‑ATOM** — single‑writer serialization (orchestrator‑flush style) vs. transactional batching with rollback vs. locking. Buffer‑then‑flush is the proven default.
- **Where the registry lives** — `pdef` substrate content (auditable, versioned, carries PR‑DISC) vs. inline configuration (simpler, no PR‑DISC).
- **Evaluation tiering and coverage indexing** — how you split work across full‑scan / monotone‑queue / change‑propagation, and prefix/trie vs. full spanfilade for coverage triggers.
- **Emission validation policy** — check every emission set against `Post_ρ` vs. trust certified bodies.
- **Violation policy** when a body breaks its contract — log / halt / escalate.
- **Stochastic bodies** — retry / N‑consecutive‑clean stopping, if you admit bodies that flip the trigger with probability < 1 (the note pushes this to evaluator‑reliability engineering, not substrate).
- **Admission control** — whether to add backpressure to *make* the bounded‑input hypothesis true, since the engine can't enforce it.
- **What you report** — expose "registry inert" vs. "system quiescent" as distinct states so the open‑model honesty (work bounded but quiescence environment‑deferred) is visible to operators.
