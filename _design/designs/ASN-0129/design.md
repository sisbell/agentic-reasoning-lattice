## What this is

ASN-0129 defines the substrate's **predicate language (PL)** — the closed algebra (Boolean composition, finite quantification, value-composition, aggregation) that turns ASN-0128's per-type atomic read predicates into the substrate's complete query/condition language, together with its type discipline, its purity/termination guarantees, and a dynamics theory describing how a predicate's truth moves as the substrate changes. PL is the substrate's *extension language*: every protocol-level trigger, termination condition, and gate is written in it.

## Design commitments

(forced unless marked conventional)

- **Composition is the only extension mechanism.** Builders extend the substrate by registering types and composing predicates in a fixed, closed algebra — never by injecting read-path code. The substrate evaluates terms of this algebra and runs no foreign code. This is the keystone: it is *why* purity, termination, and the structural-read boundary hold for every predicate anyone will ever write. Architecturally, the closed algebra **is** the sandbox — safety comes from inexpressibility, not a runtime guard.
- **The atomic vocabulary is generated from the registry, not authored.** Available atoms are a pure function of the registration records (shape, idempotency, attached behaviors). Registering a type mechanically yields its template family; there is no hand-written per-type predicate code.
- **The vocabulary is static at runtime** (V-STAT). It changes only at construction-time registration, never via a transition. Consequence: typing, expansion, and stability analysis run once at construction and stay valid for every reachable state.
- **Predicates are pure, total functions of state** (PC4). A term reads only the link store, the arrangement-store *domain*, the registry, plus its arguments and one view — no content bytes, no side effects, no emission-order or memo dependence. Same inputs → same result, always.
- **Every predicate terminates at every state** (PC5), and the grammar ships no fixpoint/recursion operator (PC6a). All iteration is either a finite fold over a finite domain or an atom's internal iteration behind a proven bound.
- **Reads are structural only.** No predicate touches the content store (value *or* domain) or dereferences an arrangement binding. PL asks "what does the link store assert," never "what bytes are here."
- **The expressive ceiling is fixed and registry-pinned** (PC6). PL is *exactly* what feedback-free, syntax-directed evaluation over the read base computes. Transitive closure, self-emit, and mutually-recursive definitions are deliberately *outside* — computed at agent time by unrolling, never handed to the substrate. The ceiling moves only when the registry does.
- **Well-typing is decidable and construction-time** (WT) — a bottom-up pass over the finite syntax tree decides it, reading no state.
- **One view per term** (PC3), fixed at the top level — audit / active / default — not a per-atom parameter. The three views are three different questions (ever-held / currently-holds / currently-holds-as-presented).
- **Partiality is explicit** (PC2). ⊥ is a verdict with meaning, eliminated only through an explicit binder guard behind a definedness test — never a silent undefined evaluation.
- **Counting is set-semantics** (PC2a): count counts distinct elements of the view-selected domain, never occurrences; cross-type totals are sums of per-type counts.
- **Conventional, not forced:** the specific aggregates that ship (count, T1-extrema, union-fold); the exact default-view rewrite (UV drops filtered elements from collections only); and — importantly — *which compositions ship as named atoms*. AM's directional keying and BH3's reverse-lookup opt-in are naming/exposure conventions, not capability fences: the algebra expresses forward *and* reverse lookup for every type whether or not the named atom is exposed. "What BH3 withholds is the atom, never the question."

## What must be built

- **A vocabulary generator** — walks the registry and emits the available atoms: the core family for every type, behavior families per attached behavior, the cross-type join (`targets_keyed`) when any type attaches reverse-lookup, plus the fixed primitive/projection/residence vocabulary. Each entry carries the signature the type checker needs and binds to the base read the evaluator dispatches to.
- **A representation for composed terms and domain expressions** — the (mutually recursive) syntactic structures of the algebra: atoms, connectives, quantifiers, value-composition with its guard, aggregates, filters, reflected domains, and the one view tag.
- **A type checker** — a syntax-directed, state-free pass deciding well-typing, assigning codomains/sorts, handling binder-guard narrowing, the tuple sort, and the Reg instance-wise rule.
- **A Reg-expander** (V-IDX) — statically expands class-quantified terms into a finite conjunction/disjunction over registered classes, rejecting instances that apply an absent behavior atom.
- **An evaluator** — syntax-directed, single-pass, pure, terminating; dispatches atom leaves to base reads, combinators to Boolean/value ops, domains to filter-select or reflected-enumeration, and folds to short-circuiting quantifier/aggregate passes, against a pinned state and a fixed view.
- **A read-base adapter** — exposes the substrate's read surface at *atom granularity*: pattern queries and slice enumeration over typed link tuples, link-store domain enumeration, document-store membership (only), registry lookup, per-tuple value reads, and the address/set/ℕ primitives — keeping span arithmetic *inside* each call.
- **The view machinery** — the three lenses, with active computed as audit-minus-nullified and the default-view presentation rewrite applied elementwise to collection-valued results.
- **A dynamics certifier** (PD0–PD2) — a second static pass computing each term's read footprint and stability class (⊤-stable / ⊥-stable / neither), so the protocol layer can validate triggers and termination conditions and skip re-evaluation safely.

## Implementation approaches

**Term representation & evaluation — interpret first, compile if hot.**
The algebra is tiny and its control tree is fixed by syntax independent of state (PC6a), so two approaches both work and the spec makes the choice low-risk:
- *Tree-walking interpreter.* Walk the AST, dispatch per node against the pinned state and view. This is PC6 made literal — the control tree *is* the syntax tree — and is trivially correct. Start here.
- *Compile-once to a pure evaluation closure.* Because typing and structure are state-independent (WT / V-STAT / PC6a), do all structural work once at construction and emit a specialized evaluator over `(state, view)`. This is the make-the-common-case-fast option when triggers fire after every step. It gives up nothing — you are caching a *recomputable* structure (a hint), and purity makes the closure freely shareable across threads.

Skip bytecode/VM — the combinator set is bounded and small; it buys nothing.

**Vocabulary generation — eager, built once.**
The registry is static (V-STAT), so build the full vocabulary table at construction by walking the registry: per-type template families, the conditional global join, the fixed primitives. There is no reason to resolve atoms lazily; this mirrors the spec's own treatment of `V_atom` as a fixed set.

**The read base — append-only journal plus indexes-as-hints.**
The link store is grow-only (PD0 leans on "no step removes an address or rewrites a stored value"), which is exactly the shape of this repo's own substrate (an append-only `links.jsonl` journal with a small registry, recovered by replay) and of udanax-green's append-only granfilade. Commit to it:
- *Authoritative store:* an append-only journal of link writes, recovered by replay on load; the registry is the small authoritative side-table. Stored values are immutable, so journal entries are never rewritten.
- *Indexes as hints (recomputable on a miss).* Slice enumeration, pattern matching, and the active/audit distinction are all served by secondary structures derivable from the journal — never authoritative duplicate state. Two carry the load:
  - a *per-type slice index* (type → its tuples) for `M_K`/`A_K`/`L_K` enumeration and every PC1/PC2a fold;
  - a *symmetric span-intersection index* over **both** endsets of all links, answering coverage-keyed forward *and* reverse pattern queries. This is the spanfilade approach, and the udanax-green evidence is decisive: Green matches endsets by span *intersection* (not exact value) and answers to-keyed (reverse) queries for every link from one symmetrically-built index *with no per-type opt-in*. That is precisely the note's "reverse lookup is the atom, never the question" — build the symmetric index once and let BH3's opt-in govern only whether the *named* `sources_to`/`target_of` atom is exposed, never whether the index supports the query.
- *Recovery:* rebuild indexes by replaying the journal; optionally snapshot for fast startup, but the journal is the source of truth. Green's discipline is the model here: content existence is *never* checked on the read path because the append-only store makes "address exists ⇒ content exists" a construction invariant — rely on the invariant, not a runtime check. (My inference, from that verified behavior: this is exactly why `is_doc` is membership-only and `dom(Σ.C)` has no read. Green's granfilade is likewise a pure point-lookup store — no read enumerates document keys — matching the note's no-document-census / membership-only residence.)

**Active slice & nullification — compute from two authoritative slices, cache as a hint.**
Active = audit minus nullified, and nullified is a prefix/subtree cover read off the retraction slice (FP: active footprint is `L_K ∪ L_R`). Rather than maintain active as authoritative derived state, test active-membership by "in the audit slice AND not covered by any retraction," answering the cover test through the *same* span-intersection index (a `≼`-prefix query). Cache the active set as a hint, recomputable from the two slices on demand. One index does both jobs.

**Views — active by subtraction, default by elementwise rewrite.**
Read audit straight from the journal segment; derive active by the nullification subtraction; derive default by applying the UV presentation rewrite — drop elements whose `filtered` predicate holds — to collection-valued results *only*, leaving verdicts, Booleans, traversal, and stored values untouched. Eager (rewrite during enumeration) is simplest; the cost is the BH1 footprint increment (FP) every default-view collection term carries.

**Keep span arithmetic inside the leaf — this preserves the ceiling.**
Coverage tests are add-then-compare (form the span upper bound, then compare under the tumbler order). The udanax-green read path does exactly this — `tumbleradd` to form the reach, then `tumblercmp` — and notably it *reads* a link's home document out of the stored record rather than recomputing it from the address (`movetumbler`, never address arithmetic). Mirror both: the combinator layer sees only Booleans and finished values; arithmetic lives inside the base call. Exposing span-add as a composable operator would breach PC6's granularity restriction and lift the language above its proven ceiling. (It is also why self-emit and home-grouping are agent-time questions, not PL atoms — keep them out of the base.)

**Type checker & dynamics certifier — two bottom-up passes sharing a traversal.**
- *Typing:* a single synthesis pass, one rule per former, run at construction and cached; reject ill-typed terms at registration. The interesting cases (binder-guard narrowing, tuple sort, Reg instance-wise expansion) are local.
- *Dynamics:* a second pass computing, per subterm, its footprint (union over atoms, per FP) and its stability class (the ST/SF inductive rules, polarity-checked). Ship it **sound-but-incomplete** — the certified spellings are the quantified forms; extensionally-equal but unrecognized spellings are conservatively rejected. The minimum worth building is footprint analysis plus the ST/SF polarity check; that alone lets a protocol checker validate a termination condition mechanically.

**Reg-expansion — at construction.**
Expand class-quantified terms into their per-class instances when the term is built, checking each instance; the term then becomes an ordinary Boolean over closed instances with no runtime class-variable machinery. The registry is static, so this is a one-time substitution — and it matches Green's stance, where no read operation aggregates or enumerates over link types at all (types enter only as caller-supplied selectors).

**Concurrency & state representation — pin an immutable snapshot.**
Purity (PC4) makes concurrent evaluation safe with no read-side locking; "coordination is entirely an emit-side concern." Represent state as an immutable value with structural sharing between versions (`im`'s persistent maps/sets): a writer produces a new version, readers cheaply pin old ones — MVCC by construction. Version the hint-indexes *alongside* the state so a pinned snapshot carries internally-consistent indexes. This sidesteps the whole class of read/write race the emit side must fight — the predicate evaluator is pure-read over a frozen snapshot.

**Make the common case fast — footprint-indexed re-evaluation.**
The dynamics theory is engineered for exactly this. After a step, PD2's frame analysis says which triggers *can* be perturbed: a trigger whose footprint is disjoint from the step's effect need not be re-evaluated at all. Index live triggers by footprint and dispatch only the affected ones. PD0 sharpens it: an already-fired ⊤-stable (ST) trigger stays fired (stop watching it); an ⊥-stable termination condition won't un-fire. The read layer should expose the footprint and stability certificate so the protocol/scheduler layer can do this — the single biggest evaluation-cost win available, and it falls straight out of FP/PD0/PD2.

## Guarantees to uphold

*By construction (fall out of the design):*
- **Determinism/purity** (PC4) — a pure evaluator over the admitted vocabulary and a pinned snapshot.
- **Termination** (PC5) and **no fixpoint** (PC6a) — only the bounded forms are admitted.
- **Decidable, state-free typing** (WT); **vocabulary staticity** (V-STAT) — registration is construction-only.
- **One view per term** (PC3) — enforced by the AST (view is a top-level tag).
- **Explicit partiality** (PC2) — enforced by the type system: ⊥-adjoined codomains are eliminable only through the guard.
- **Set-semantics counting** (PC2a) — count a set, not a multiset.

*By active enforcement (a boundary you must police):*
- **Structural-reads-only** — the base adapter must expose membership for the document store and *nothing* for the content store; no path may dereference content or arrangement bindings. Guard this layer boundary.
- **The expressive ceiling** (PC6) — do not expose span arithmetic as a composable operator, and do not add a feedback / repeat-until-stable evaluator. Either breach silently lifts the language above PL and forfeits the ceiling, termination, and the dynamics theory with it.
- **The grow-only / immutable-value assumption** the dynamics theory leans on is an *upstream* substrate guarantee (no address removed, no value rewritten); depend on it but assume no more — in particular, active membership is *not* monotone (resurrection re-deposits at a fresh address).

## How it fits

- **Leans on (below):** ASN-0128 for the atomic read surface (per-type predicates, the three views, the registration records) — PL's vocabulary is the generated closure of these; ASN-0086 for the pattern-query / slice-enumeration read primitive, the active-subset machinery, and address injectivity — this is the read base; ASN-0126 for the state model (stores, the gated transition relation and its frames, the home/chain frontier) and the reachable-state class; ASN-0034 for the address comparisons (total order, prefix, decidability) the primitives admit and the coverage tests use; ASN-0043 for the link/endset structure and coverage-vs-denotation.
- **Hands to (above):** the protocol/application layer — triggers, termination conditions, gating disciplines, schedulers — written *in* PL and typed *by* PD0–PD2. Explicitly *not* part of this note; the read layer supplies the language, its evaluation guarantees, and the dynamics certificates the protocol layer consumes.
- **Sibling boundary:** ASN-0127, the content-region (arrangement-reading) query layer over the arrangement store. PL deliberately excludes it; the two meet only at the substrate both read, and neither subsumes the other. Reachability and self-emit are likewise *handed out* to agent-time computation (unroll `succs`, recompute the frontier), not built into the substrate evaluator.

## Decisions for the builder

(distinct from the note's spec-level open questions)

- **Interpreter vs. compiled closures**, and the threshold to switch — driven by how often triggers are evaluated.
- **Index design for the read base:** the per-type slice index and the symmetric span-intersection index — keying, granularity, and incremental-maintenance vs. rebuild-on-load. (These are hints; the only hard constraint is that they stay recomputable from the journal.)
- **Active-slice strategy:** compute-on-read by retraction subtraction vs. a maintained active-set hint, and how to invalidate it.
- **Default-view rewrite:** eager (during enumeration) vs. lazy (post-filter), and where to charge the BH1 footprint increment.
- **How much dynamics certifier to ship:** footprint-only, footprint + ST/SF polarity, or a fuller (still sound-but-incomplete) classifier.
- **Snapshot/recovery:** journal-replay only vs. periodic index snapshots for startup latency.
- **State & index representation for concurrent reads:** persistent structures with snapshot-pinning (recommended) vs. copy-on-read; whether indexes are versioned with the state.
- **Result caching/memoization** across evaluations — permitted by purity but only as a hint keyed to a state-version; whether it pays depends on re-evaluation patterns (and is largely superseded by footprint-indexed dispatch).
- **Fold materialization:** stream vs. collect finite domains — a memory/latency tradeoff for large slices.
- **Where reachability lives:** since PL excludes closure by design, provide an agent-time iteration harness (iterate `succs`, unroll) rather than extending the evaluator — unless and until the bounded-fixpoint successor (the note's own future work) is adopted.
