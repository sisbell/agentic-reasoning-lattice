# Review of ASN-0126

## REVISE

### Issue 1: "Cardinality" of F and G is never defined on endsets
**ASN-0126, Three shapes / Shape-conformance**: "Unary: `G = ∅`; Binary: `|F| = 1` and `|G| = 1`; Multi: `|F| = 1` and `G` is a finite set of addresses."
**Problem**: F and G are *endsets* — `Endset = 𝒫_fin(Span)` (ASN-0043) — and an endset's `coverage` is a set of *tumblers* obtained by unioning half-open intervals. The framework's entire shape vocabulary rests on `|F|`, `|G|`, and `G = ∅`, but never says whether these count (a) spans in the endset, or (b) addresses in `coverage`. The two diverge sharply: a single unit-depth span `(a, δ(1,#a))` has `coverage = {t : a ≼ t}`, generally infinite (PrefixSpanCoverage, ASN-0043). So "single source" (`|F| = 1`) is ambiguous, and "exactly one F" could mean one span covering an entire subtree.
**Required**: Define the cardinality measure precisely — almost certainly `|coverage(F)| = 1` and `|coverage(G)| = 1` — and reconcile it with the fact that ordinary spans cover ranges, not single addresses. State which spans yield singleton coverage.

### Issue 2: Multi's "finite set of addresses" can be an infinite coverage
**ASN-0126, Shape-conformance**: "Multi: `|F| = 1` and `G` is a finite set of addresses."
**Problem**: An endset is a finite set of *spans*, but its `coverage` need not be finite — a single span covering a subtree is an infinite tumbler set. "G is a finite set of addresses" is therefore not guaranteed by `G ∈ Endset`. Either the predicate means "finite *span* set" (trivially true for every endset, making the conjunct vacuous) or it means "finite coverage" (a real, currently-unstated restriction).
**Required**: Pin down whether Multi constrains span count (vacuous) or coverage cardinality (substantive), and if the latter, give the well-formedness condition that forces finite coverage.

### Issue 3: t_F / t_G domain checks contradict P5 (Sh-confStateIndependence)
**ASN-0126, Registration entries / P5**: "a **t_F** domain — `A_doc`, `A_rel`, or `A`" and "P5 ... `Sh-conf(K, F, G)` evaluated against Σ equals ... against Σ'."
**Problem**: `A_doc^Σ = dom(Σ.C)`, `A_rel^Σ = dom(Σ.L)`, and `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` are all explicitly *state-indexed* in ASN-0086, and grow monotonically across `→`. The Sh-conf clause "the F element lies in K's declared `t_F` domain" therefore depends on Σ: an F address that is a ghost at Σ (not yet in `dom(Σ.C)`) but stored at Σ' would make `Sh-conf` evaluate to `⊥` at Σ and `⊤` at Σ'. This directly contradicts P5, which asserts state-independence. The note even says "No other component of Σ is consulted," which is false if `t_F = A_doc = dom(Σ.C)`.
**Required**: Either (a) drop the residence-domain check from Sh-conf so the predicate depends only on `(F, G, K)` and the registry (making P5 true), or (b) keep the domain check and retract P5. You cannot have both.

### Issue 4: Domain restriction to A_doc/A_rel/A contradicts L4 and L9
**ASN-0126, Target domains / Shape-conformance**: "`F` ranges over `A = A_doc ∪ A_rel`... every G element lies in `t_G`."
**Problem**: L4 (EndsetGenerality, ASN-0043) states endset spans "may reference any addresses in the tumbler space... no constraint confining spans to... addresses at which content currently exists," and L9 (TypeGhostPermission) permits references outside `dom(Σ.C) ∪ dom(Σ.L)`. Restricting F/G to stored addresses (`A_doc/A_rel/A`) narrows what the foundation explicitly permits. If this narrowing is intentional it must be stated as a deliberate restriction of L4/L9 with justification — not slipped in as a default.
**Required**: State explicitly that Sh-conf restricts beyond L4/L9, justify it, and resolve the consequence for ghost-typed references the lattice already uses.

### Issue 5: P4 asserts a constraint on → with no enforcement mechanism
**ASN-0126, Shape-conformance / P4**: "no `→`-step extends `dom(Σ.L)` with such a tuple, in any reachable state."
**Problem**: The transition relation `→ ≡ K.σ ∪ K.α ∪ K.λ` is fixed by ASN-0086, and K.λ's precondition is L3 (arity ≥ 3, non-empty type) — it does *not* check `|F| = 1` or any G cardinality. As written, ASN-0086's `→` admits non-conforming tuples. P4 is stated as an established property ("No `→`-step extends..."), but it is actually a *redefinition* of the transition relation, presented as a derived fact. No mechanism is shown by which Sh-conf gates K.λ.
**Required**: Either redefine the emit step (a Sh-conf-gated `→` or a refinement of K.λ) and prove P4 against that definition, or label P4 a definitional restriction rather than a property "established."

### Issue 6: P1 (RegistryInvariance) is asserted, not derived; Σ is silently extended
**ASN-0126, Registry permanence / P1**: "The registry is a component of Σ_init. It is invariant across every `→`-step."
**Problem**: ASN-0043/0086 define `Σ = (Σ.C, Σ.M, Σ.L)`. This note adds a fourth component `Σ.registry` without reconciling it with the foundation state definition or with StateExtension (ASN-0043), which quantifies only over C/M/L. P1's "proof" is a single assertion. The actual argument — that `→ ≡ K.σ ∪ K.α ∪ K.λ` touches only C, M, L respectively, so registry sits in the frame of every step — is available but never written. P2 and P3 are corollaries of P1 and inherit the gap.
**Required**: Define the extended state tuple, state the frame condition (each of K.σ/K.α/K.λ leaves `registry` unchanged), and derive P1 from those frame conditions explicitly. Then P2/P3 follow.

### Issue 7: The three shapes do not partition tuples
**ASN-0126, Three shapes / Shape-conformance**: Unary (`G = ∅`), Binary (`|G| = 1`), Multi (`G` finite).
**Problem**: Multi's conformance condition subsumes both Unary (`G = ∅`) and Binary (`|G| = 1`) — a Multi-registered tuple with empty or singleton G also conforms. The "rules out a fourth" / clean-catalog framing implies disjoint shapes, but the predicates overlap. This is tolerable because shape is fixed per-K at registration, but the note should say so rather than imply a partition of expressible tuples.
**Required**: State that shapes classify *registrations*, not tuples, and that the conformance conditions are nested (Unary ⊂ Binary-cardinality ⊂ Multi); adjust the "rules out a fourth" prose accordingly.

### Issue 8: No concrete worked example
**ASN-0126, Worked illustration**: four named entries, abstract `(F, G, K)`.
**Problem**: The illustration never instantiates a single concrete tumbler. Per the review standard, the ASN should check its key claims (P4, P5) against at least one concrete scenario — e.g., a citation tuple with explicit F = one document address, G = two target addresses, showing Sh-conf evaluates identically at two distinct reachable states. Without addresses, Issues 1–3 (the cardinality/state-dependence ambiguities) hide.
**Required**: Add a worked example with concrete tumblers exercising Unary, Binary, and Multi, verifying Sh-conf and its state-independence claim explicitly.

## OUT_OF_SCOPE

### Topic 1: Idem operational semantics
**Why out of scope**: The note commits only to the flag's structural presence and state-independence; emit/nullify/re-emit semantics are explicitly deferred to a successor (Open question 1). Appropriate deferral.

### Topic 2: Behavior catalog, default predicates, predicate composition, standard registrations
**Why out of scope**: Open questions 2–5 layer operational semantics on top of the structural framework; they are genuinely new territory, not gaps in this note's commitments.

### Topic 3: Multi-source / higher-arity extension
**Why out of scope**: Open question 6 — the substrate deliberately delegates higher arity to direct link-store interaction (ASN-0043 permits it). Future supplemental note, not an error here.

VERDICT: REVISE
