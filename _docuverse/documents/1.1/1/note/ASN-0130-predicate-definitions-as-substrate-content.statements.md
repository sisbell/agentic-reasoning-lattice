# ASN-0130 Claim Statements

*Source: ASN-0130-predicate-definitions-as-substrate-content.md (revised unknown) — Extracted: 2026-06-12*

## PR-ENC — EncodingDiscipline (AXIOM, axiom)

An *encoding* is an injective map from *signed syntactic terms* — a pair of an ordered, sorted parameter context `Γ_D = ⟨x₁ : C₁, …, x_k : C_k⟩` (each `Cᵢ ∈ Codom`; `k = 0` for closed terms) and a body in ASN-0129's grammar extended with *applied definitional references* (PR-SIG), and no view component — to finite content-value sequences, with a decidable parse and **prefix-freeness**: no parse-valid sequence is a proper prefix of another; equivalently, the parse is *self-delimiting*, determining its own extent from its start.

The domain is *syntax only* — grammatical well-formedness, no typing requirement.

The discipline reserves a countable supply of *expansion names* `ν₁, ν₂, …`, which no recorded parameter name and no body binder may inhabit.

A *definition artifact* is a contiguous run `A_def = {shift(a, k) : 0 ≤ k < n}` (`n ≥ 1`) of content addresses holding a parse-valid encoding, identified by its start `a` — *the definition's address*. The run is one segment of `a`'s origin K.α chain, because on T4-valid content addresses `shift(x, 1) = inc(x, 0)`.

---

## PR-ENC-uniq — EncodingUniqueness (LEMMA, lemma)

At most one parse-valid run starts at any address.

**Proof sketch:** Were `{shift(a, k) : 0 ≤ k < n}` and `{shift(a, k) : 0 ≤ k < n'}` both parse-valid with `n < n'`, the shorter's value sequence would be a proper prefix of the longer's — both parse-valid encodings — contradicting prefix-freeness.

**Corollary:** Runs may overlap (a suffix of a run may itself decode), but identity and resolution are start-anchored, so a definition starting mid-run is a different definition at a different start, never confused with the containing one.

---

## Definition — Sig

`sig(a) = (Γ_D, C_D)`: the parse layer's recorded context, paired with the result sort the WT + WT-ref pass derives for `a`'s body *at `a`'s first registration*.

`sig` is defined exactly on the *ever-registered* addresses, by induction on first-registration order. At `a`'s first registration, PR0 (iv) has every referenced address `r` carrying an active tuple at the pre-state — so `sig(r)` is already defined by the induction: every signature WT-ref consults is grounded, the pass is a terminating syntax-directed walk, and `C_D` is determined — unique, WT being syntax-directed.

Once defined, `sig(a)` never changes, and it re-derives identically at every later deposit event for `a`: the body is content-fixed (S0), each consulted `sig(r)` was fixed at its own earlier first registration, and the pass is deterministic.

---

## PR-SIG — SignaturesAndReferences (SPEC, spec)

The *parse layer* is content-intrinsic: wherever a parse-valid run starts, the self-delimiting parse returns the recorded parameter context `Γ_D` and the body — functions of the immutable values (S0, PR-ENC), defined at every state alike.

The syntax PL gains is the *applied reference*: for an address `r` and terms `e₁, …, e_k`, the form `r(e₁, …, e_k)`, bare `r` when `k = 0` — a grammatical form, parsed with no store consulted.

The *type layer* cannot be content-intrinsic: typing a reference needs the referent's parameter sorts and result sort, so a reference-bearing body's well-typing is not a property of its own run's values. Registration order grounds the type layer (see `sig` definition above).

---

## WT-ref — WTRef (RULE, rule)

For a context `Γ`, an address `r` with `sig(r)` *defined* and `sig(r) = (⟨x₁ : C₁, …, x_k : C_k⟩, C_r)`, and `Γ ⊢ eᵢ : Cᵢ` for each `1 ≤ i ≤ k`:

`Γ ⊢ r(e₁, …, e_k) : C_r`

Definedness of `sig(r)` is the rule's domain condition — a reference to a never-registered address has no typing judgment.

---

## PR0 — DefinitionRegistration (SPEC, spec)

The operation surface exposes `register_pred(d, A_def)`: *validate, then emit through the `pdef`-class emit it wraps*, returning the classifier tuple's address.

*Validation* runs in full on every call at the call state Σ, writing `a := min(A_def)` (T1) and `n := |A_def|`:

**(i)** the run is resident and chain-contiguous: `A_def ⊆ dom(Σ.C)` and `A_def = {shift(a, k) : 0 ≤ k < n}`, one segment of one origin's K.α chain (PR-ENC);

**(ii)** the run's values are exactly one parse-valid encoding — the self-delimiting parse from `a` succeeds and consumes precisely the presented extent, and by PR-ENC-uniq no other extent could;

**(iii)** the decoded signed term well-types, `Γ_D ⊢ body : C_D`, under WT plus WT-ref (PR-SIG);

**(iv)** every definitional reference names an *already-registered* definition: for each referenced address `r`, some `(b, F, G) ∈ A_pdef^Σ` with `r ∈ addrs(F)`.

On any validation failure the call is rejected — no step, no tuple, no address, *even when an I0-equal active tuple exists*.

On success:

`Emit_pdef(Σ, d, {a}, A_def)`

depositing `(enc({a}), enc(A_def), pdef)` on a miss, with `addrs(F) = {a}` and `addrs(G) = A_def`.

**POST-ref:**

`POST-ref ≡ (∃ (b, F', G') ∈ A_pdef^{Σ'} :: addrs(F') = {a})`

**wp (on registration-disciplined derivations):**

`wp(register_pred(d, A_def), POST-ref) ≡ VALID(Σ, A_def) ∧ (hit(Σ, a) ∨ (d ∈ dom(Σ.M) ∧ C3(Σ, d)))`

with `VALID` = conditions (i)–(iv) and `hit` = I1's branch condition at the `pdef` class.

**wp reduced (on surface-disciplined derivations, where DR empties C3):**

`wp(register_pred(d, A_def), POST-ref) ≡ VALID(Σ, A_def) ∧ (hit(Σ, a) ∨ d ∈ dom(Σ.M))`

*Discipline and uniqueness:* A derivation is *registration-disciplined* iff every `L_pdef`-growing step along it is the deposit branch of a `register_pred` call and every `L_pd_stable`-growing step the deposit branch of a `certify_pd_stable` call. On such derivations: at most one active `pdef` tuple per I0 class at every state reached; all validated tuples at one start are I0-equal (PR-ENC-uniq) — *at most one active registration per definition address*.

---

## PR1 — ValidationPermanence (LEMMA, lemma)

At any state Σ reached by a registration-disciplined derivation, if `(b, F, G) ∈ L_pdef^Σ`, then the run `addrs(G)`, with start `addrs(F) = {a}`, passed PR0's validation at its deposit's pre-state — parse-valid (ii), well-typed (iii), every reference registered (iv) — and holds the same values at Σ and at every `→_sh*`-successor.

**Proof structure:** Each step of the substrate relation either frames the content store — K.σ and K.λ_sh carry `Σ'.C = Σ.C` in their frames — or is a K.α step with `C' = C ∪ {a' ↦ v}` at a key fresh against `dom(Σ.C)`, leaving every existing binding intact. By induction along the derivation, every already-stored content address remains resident with value fixed. The tuple persists via L12 as a transition invariant (B2 with RP-b), inducted along the derivation.

---

## PR2 — AcyclicReference (LEMMA, lemma)

Under PR0's discipline, deposits into the `pdef` class are `→_sh` steps, totally ordered along any derivation. For an ever-registered definition D, write `e₁(D)` for its *earliest* deposit event.

**(a)** *Every deposit event sees each referent registered strictly earlier.*

A deposit is the miss branch of a `register_pred` whose validation (iv) had just passed at the pre-state: each referenced address `r` carries an active tuple there, which entered `L_pdef` at some strictly earlier deposit event. Hence `e₁(r) <` the current event; instantiating at D's earliest event, `e₁(r) < e₁(D)`.

**(b)** *Self-reference fails at every deposit event.*

Deposits occur only on a dedup miss, and all validated tuples at one start are I0-equal (PR-ENC-uniq), so at a deposit event for D every existing tuple denoting D's start is inactive — and the depositing tuple does not yet exist during its own validation. Condition (iv) therefore has no witness for a reference to D's own start: a self-referencing term is rejected at every would-be deposit event.

**Consequence:** The reference relation on ever-registered definitions embeds in the strict order `e₁(r) < e₁(D)` — irreflexive, acyclic, a DAG with no cycle check ever run. Definitional expansion terminates: expansion descends reference edges, `e₁` strictly decreasing among the finitely many deposit events.

---

## Definition — Expand

`expand(a)`: in `body`, replace each applied reference by the referent's expansion with the expanded arguments substituted for its parameters.

Processing order: references bottom-up, siblings left to right (arguments fully expanded before the node they feed).

At a node `r(·)` with expanded arguments `E₁, …, E_k`:

1. Take `expand(r)` — recursion well-founded because descent strictly decreases first-registration rank (PR2).
2. Rename `expand(r)`'s parameters *and* every binding site in it to expansion names from PR-ENC's reserved supply: the least-indexed names occurring nowhere in the term under construction, the `Eⱼ`, or `expand(r)` itself, assigned in a fixed order (parameters first in signature order, then binding sites depth-first, left to right).
3. Substitute `Eⱼ` simultaneously for the renamed `j`-th parameter.

The renaming is total — a referent's free variables are among its parameters (PR-SIG), and all parameters are renamed — and capture-free by construction: every introduced name is fresh for everything in scope, and no author-written name inhabits the expansion-name supply (PR-ENC).

`expand` is a *function* of content — two evaluators expanding the same address at any two states obtain the same concrete term, not merely α-equivalent ones.

---

## Definition — Evaluate

`evaluate(a, args, view, Σ)`:

**Precondition:** `a` is *ever-registered* at Σ — spelled as the audit-slice fact: some `(b, F, G) ∈ L_pdef^Σ` with `addrs(F) = {a}` (in PL: `(∃ x ∈ L_pdef :: a ∈ addrs_F(x))`; equivalently `a ∈ M_pdef` at view `audit`, V-AUD). Active registration is *not* required of `a` or any referent.

`args` is a `Γ_D`-*environment*: one value of sort `Cᵢ` per parameter `xᵢ`, per `sig(a) = (Γ_D, C_D)`.

**Result:** the ASN-0129 denotation of `expand(a)` at `(args, view, Σ)` — a denotation that exists at the signature's result sort because `expand(a)` is a PL term with `Γ_D ⊢ expand(a) : C_D` (PR3a), the view fixed at the top level per PC3.

Purity (PC4), termination (PC5), decidability, and the ceiling (PC6) hold verbatim — the expansion is a pure PL term fixed by immutable content before evaluation begins.

---

## PR3 — EvaluationByReference (SPEC, spec)

Three layers:

**Resolution** — address to signed term: read content values from `a` along its origin chain — successive addresses `shift(a, k)`, the chain's `inc(·, 0)` siblings (PR-ENC) — feeding the self-delimiting parse, which determines the run's extent from content alone and yields `(Γ_D, body)`. Resolution consults no slice and no tuple.

**Expansion** — `expand(a)` as defined above. `expand` is a *function* of immutable content — two evaluators expanding the same address at any two states obtain the same concrete term, not merely α-equivalent ones.

**Evaluation** — `evaluate(a, args, view, Σ)` as defined above. References are *view-transparent*: a referent contributes spelling, never scope — the artifact fixes the term, the reader fixes which state the term's parameterized reads see.

**PR-VIEW applies:** the view binding every view-parameterized constituent in every inlined referent is the evaluating *caller's*, not anything the referent's author chose.

---

## PR3a — ExpansionWellTyping (LEMMA, lemma)

On registration-disciplined derivations: for every ever-registered `a` with `sig(a) = (Γ_D, C_D)`,

`expand(a)` is a pure PL term with `Γ_D ⊢ expand(a) : C_D`.

**Sub-lemma WT-α (renaming):** If `Γ ⊢ u : C` and `ρ` renames variables sort-preservingly and injectively — acting on `dom(Γ)` and on `u`'s binding sites, its image names pairwise distinct and occurring nowhere in `u` — then `ρΓ ⊢ ρu : C`.

**Sub-lemma WT-W (weakening):** If `Γ ⊢ u : C`, `y ∉ dom(Γ)`, and `y` occurs nowhere in `u` as a binder, then `Γ, y : C′ ⊢ u : C` for any sort `C′`.

**Proof structure (by induction on first-registration rank, nested structural induction on body):** For a reference node `r(e₁, …, e_k)` typed at context `Γ` by WT-ref with premises `Γ ⊢ eᵢ : Cᵢ` and `sig(r) = (⟨x₁ : C₁, …, x_k : C_k⟩, C_r)`:

- *Arguments:* structural induction gives `Γ ⊢ Eᵢ : Cᵢ` for each `i`.
- *Referent:* rank induction gives `expand(r) ∈ PL` with `⟨x₁ : C₁, …, x_k : C_k⟩ ⊢ expand(r) : C_r`.
- *Rename (WT-α):* yields `⟨y₁ : C₁, …, y_k : C_k⟩ ⊢ u : C_r` where `u` is the renamed term with fresh `yⱼ` outside `dom(Γ)`.
- *Weaken (WT-W iterated):* yields `Γ, y₁ : C₁, …, y_k : C_k ⊢ u : C_r`.
- *Substitute (PC2 iterated, last parameter first):* Write `Γⱼ := Γ ∪ {y₁ : C₁, …, yⱼ : Cⱼ}`; at step `j = k, …, 1`, lift `Γ ⊢ Eⱼ : Cⱼ` to `Γ_{j−1} ⊢ Eⱼ : Cⱼ` by WT-W, apply PC2 to lower the judgment one context at a time. After step `1`: `Γ ⊢ u[y₁ ↦ E₁, …, y_k ↦ E_k] : C_r`. ∎

---

## PR-VIEW — ViewTransparency (DEF, definition)

A signed term records no view (PR-ENC) and `evaluate` takes one (PR3). The view binding every view-parameterized constituent (`members`, `targets_of`, `is_K`, `M_K` — PC3's list) in every inlined referent is the evaluating *caller's*, not anything the referent's author chose.

Call a term *view-independent* iff it contains no view-parameterized constituent and no collection-valued behavior atom on UV's rewrite list (`succs`, `sources_to`, `chain`, `stale`; the verdict-valued behavior atoms UV never rewrites are admissible): a syntactic condition, decided by the same finite scan that decides well-typing.

A view-independent term's denotation is invariant in the view argument — by structural induction, PC3 and UV locate all view-sensitivity in exactly the excluded constituents — so for such a term the `view` argument is inert.

---

## PR4 — VersioningBySupersession (SPEC, spec)

Definitions are never edited; they are *succeeded*. To update a predicate: register the successor (PR0), then emit `supersedes` (the shipped S2 class, ASN-0128) from the old definition's address to the new.

`tip(a)` resolves the current version of the lineage rooted at `a`; competing successors make a branch and `tip` returns `⊥` — the multiplicity is *reported*, adjudicating among competing updates belongs to readers (BH2's stance).

---

## PR5 — DynamicsCertification (SPEC, spec)

A second validated surface — `certify_pd_stable` (operation contract PR5a) — classifies a registered definition's PD class (ASN-0129, PD0–PD2) by emitting a certification classifier, asserting membership in PD0's **ST** class.

Three qualifications:

**Purity:** The certified object is the definition's *expansion* (PR3, well-typed by PR3a) — the pure term `expand(a)`, not the artifact's literal reference-bearing spelling.

**View:** The surface certifies only *view-independent* expansions (PR-VIEW's syntactic class). Such a term denotes identically at every view, and the certificate binds at every `evaluate` call whatever view the caller passes.

**Parameters:** The checker runs PD0's rules with each parameter treated as a bound constant of its declared sort, and the certificate asserts that *every* `Γ_D`-instantiation of `expand(a)` is ⊤-stable: once true at a reachable Σ for given `args`, true at every `→_sh*`-successor for the same `args`. At `k = 0` the convention degenerates to PD0's statement itself.

**Lint term** ("every registered definition carries `pd_stable`", view `active`):

`(∀ t ∈ M_pdef :: is_pd_stable(t))`

where coverage is exact at starts: `t ∈ subtree(t')` between starts forces `t' = t`, because same-origin K.α chain addresses share their length (`inc(·, 0)` rewrites only the terminal sig position, TA5(c), TA5-SigValid, ASN-0034) and two prefixes of one tumbler are length-ordered.

**Permanence:** `expand(a)` is determined by immutable content alone — the certified object is one fixed pure spelling, frozen exactly as the artifact is.

---

## PR5a — CertificationSurface (SPEC, spec)

The surface exposes `certify_pd_stable(d, a)`: *validate, then emit through the `pd_stable`-class emit it wraps*, returning the certificate tuple's address.

*Validation* runs in full at call state Σ, in this order:

**(i)** *Target status:* `a` is *actively* registered — some `(b, F, G) ∈ A_pdef^Σ` with `addrs(F) = {a}`.

**(ii)** *Well-posedness:* `expand(a)` is view-independent (PR-VIEW's syntactic scan — no view-parameterized constituent and no UV-rewritten collection atom).

**(iii)** *Class membership:* the checker's verdict `expand(a) ∈ ST` by PD0's rules — parameters read as bound constants of their declared sorts.

Checks run in the stated order; the first failure rejects — no step, no tuple, no address — and rejection asserts nothing about the definition or any standing certificate.

On success:

`Emit_pd_stable(Σ, d, {a}, ∅)`

Unary shape conformant (`|F| = 1`, `G = ∅`), under I1's idem-⊤ contract.

**POST-cert:**

`POST-cert ≡ (∃ (b, F', G') ∈ A_pd_stable^{Σ'} :: addrs(F') = {a})`

**wp (on registration-disciplined derivations):**

`wp(certify_pd_stable(d, a), POST-cert) ≡ CVALID(Σ, a) ∧ (hit(Σ, a) ∨ (d ∈ dom(Σ.M) ∧ C3(Σ, d)))`

with `CVALID` = conjunction of (i)–(iii); on surface-disciplined derivations, C3 vanishes (DR).

**Permanence for the slice:** At any state Σ reached by a registration-disciplined derivation, if `(b, F, G) ∈ L_pd_stable^Σ` with `addrs(F) = {a}`, then at the deposit's pre-state: `a` was actively registered, `expand(a)` was view-independent, and `expand(a) ∈ ST` held — and all three facts are permanent, because `expand(a)` is the same concrete term at every state (PR3's determinacy), view-independence is a syntactic property of that fixed term, and the ST verdict is PD0's classification of that fixed spelling.

---

## PS1 — PredicateDefinition (DEF, registration)

`pdef` — Multi, idem=⊤, behaviors=∅.

Slot convention: F = `enc({a})` denotes the definition's address — identity by start — and G = `enc(A_def)` denotes its run. `addrs(F) = {a}` and `addrs(G) = A_def`.

Marks a content run as a validated predicate definition.

`M_pdef` enumerates the registered definitions (D1): under PR0's discipline, exactly the registered definition addresses at view `active`.

Idempotent: re-registering the same run while its tuple is active and the presentation still validates dedups to the existing tuple (I0's coverage identity on both slots — same start, same run); a re-presentation whose referents have since been de-registered fails (iv) and is *rejected*, the incumbent untouched.

The exposed `Emit_K` rejects every `pdef`-class call — so `register_pred` is the one surface route into the `pdef` slice.

---

## PS2 — StabilityCertificate (DEF, registration)

`pd_stable` — Unary, idem=⊤, behaviors=∅.

Slot convention: F = `enc({a})`, the certified definition's address; G = ∅ (Unary).

Asserts ST-class certification (PD0, ASN-0129) of the *expansion* — view-independent, per PR5 — of the definition at `a`.

`is_pd_stable(t)` is true iff some active certificate's F covers `t` (D2). Coverage is exact at starts: a certificate's F-coverage is `subtree(t')` (PrefixSpanCoverage), and distinct content-run starts are prefix-incomparable, so `t ∈ subtree(t')` between starts forces `t' = t`.

Emitted only by `certify_pd_stable` (PR5a). The exposed `Emit_K` rejects every `pd_stable`-class call — so `certify_pd_stable` is the one surface route into the `pd_stable` slice.
