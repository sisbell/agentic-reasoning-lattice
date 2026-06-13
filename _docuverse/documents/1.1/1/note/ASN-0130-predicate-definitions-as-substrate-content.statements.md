# ASN-0130 Claim Statements

*Source: ASN-0130-predicate-definitions-as-substrate-content.md (revised unknown) — Extracted: 2026-06-13*

## PR-ENC — EncodingDiscipline (DEF, definition)

An *encoding* is an injective map from *signed syntactic terms* — a pair of an ordered, sorted parameter context `Γ_D = ⟨x₁ : C₁, …, x_k : C_k⟩` (each `Cᵢ ∈ Codom`, COD of ASN-0129; `k = 0` for closed terms) and a body in ASN-0129's grammar extended with *applied definitional references* (PR-SIG), and no view component (PR-VIEW) — to finite content-value sequences, with a decidable parse and **prefix-freeness**: no parse-valid sequence is a proper prefix of another; equivalently, the parse is *self-delimiting*, determining its own extent from its start.

The domain is *syntax only*: grammatical well-formedness, no typing requirement.

The discipline also reserves a countable supply of *expansion names* `ν₁, ν₂, …`, which no recorded parameter name and no body binder may inhabit.

A *definition artifact* is a contiguous run `A_def = {shift(a, k) : 0 ≤ k < n}` (`n ≥ 1`) of content addresses holding a parse-valid encoding, identified by its start `a` — *the definition's address*.

---

## PR-ENC-uniq — EncodingUniqueness (LEMMA, uniqueness)

At most one parse-valid run starts at any address: were `{shift(a, k) : 0 ≤ k < n}` and `{shift(a, k) : 0 ≤ k < n'}` both parse-valid with `n < n'`, the shorter's value sequence would be a proper prefix of the longer's — both parse-valid encodings — contradicting prefix-freeness.

---

## PR-DISC — RegistrationDiscipline (DEF, scoping hypothesis)

A derivation is *registration-disciplined* iff every `L_pdef`-growing step along it is the deposit branch of a `register_pred` call (PR0) and every `L_pd_stable`-growing step the deposit branch of a `certify_pd_stable` call (PR5a).

On such a derivation every active `pdef` tuple is the trace of a validated registration, and every active `pd_stable` tuple the trace of a validated certification.

---

## Definition — Sig

`sig(a) = (Γ_D, C_D)`: the parse layer's recorded context, paired with the result sort the WT + WT-ref pass derives for `a`'s body *at `a`'s first registration*.

`sig` is defined exactly on the *ever-registered* addresses, by induction on first-registration order — well-founded, registration events being totally ordered along the derivation (PR2). At `a`'s first registration, PR0 (iv) has every referenced address `r` carrying an active tuple at the pre-state; so `r`'s first registration is strictly earlier (PR2(a)) and `sig(r)` is already defined by the induction: every signature WT-ref consults is grounded, the pass is a terminating syntax-directed walk, and `C_D` is determined — unique, WT being syntax-directed.

Once defined, `sig(a)` never changes, and it re-derives identically at every later deposit event for `a`: the body is content-fixed (S0), each consulted `sig(r)` was fixed at its own earlier first registration, and the pass is deterministic.

---

## Definition — WTRef

For a context `Γ`, an address `r` with `sig(r)` *defined* and `sig(r) = (⟨x₁ : C₁, …, x_k : C_k⟩, C_r)`, and `Γ ⊢ eᵢ : Cᵢ` for each `1 ≤ i ≤ k`: `Γ ⊢ r(e₁, …, e_k) : C_r`.

Definedness of `sig(r)` is the rule's domain condition — a reference to a never-registered address has no typing judgment, not a false one.

---

## PR0 — DefinitionRegistration (DEF, operation contract)

The operation surface exposes `register_pred(d, A_def)`: *validate, then emit through the `pdef`-class emit it wraps*, returning the classifier tuple's address.

*Validation* runs in full on every call at the call state Σ:

- (0) `A_def` is a non-empty finite address set (`A_def ≠ ∅`, `|A_def| < ∞`)
- Writing `a := min(A_def)` (T1) and `n := |A_def|`:
  - (i) the run is resident and chain-contiguous — `A_def ⊆ dom(Σ.C)` and `A_def = {shift(a, k) : 0 ≤ k < n}`
  - (ii) the run's values are exactly one parse-valid encoding — the self-delimiting parse from `a` succeeds and consumes precisely the presented extent
  - (iii) the decoded term well-types, `Γ_D ⊢ body : C_D`, under WT + WT-ref
  - (iv) every definitional reference names an *actively*-registered definition: for each referenced address `r`, some `(b, F, G) ∈ A_pdef^Σ` with `r ∈ addrs(F)`

On success: `Emit_pdef(Σ, d, {a}, A_def)` with deposited endsets `F = enc({a})` and `G = enc(A_def)`.

*Weakest precondition* — on registration-disciplined derivations (PR-DISC), for `POST-ref ≡ (E (b, F', G') ∈ A_pdef^{Σ'} :: addrs(F') = {a})`:

```
wp(register_pred(d, A_def), POST-ref)
  ≡ (E (b, F', G') ∈ A_pdef^Σ :: addrs(F') = {a})
  ∨ (VALID(Σ, A_def) ∧ d ∈ dom(Σ.M) ∧ C3(Σ, d))
```

with `VALID` conditions (0)–(iv). On surface-disciplined derivations (DR), C3 vanishes:

```
wp(register_pred(d, A_def), POST-ref)
  ≡ (E (b, F', G') ∈ A_pdef^Σ :: addrs(F') = {a})
  ∨ (VALID(Σ, A_def) ∧ d ∈ dom(Σ.M))
```

---

## PR1 — ValidationPermanence (LEMMA, permanence)

At any state Σ reached by a registration-disciplined derivation (PR-DISC), if `(b, F, G) ∈ L_pdef^Σ`, then the run `addrs(G)`, with start `addrs(F) = {a}`, passed PR0's validation at its deposit's pre-state — parse-valid (ii), well-typed (iii), every reference registered (iv) — and holds the same values at Σ and at every `→_sh*`-successor.

Permanence divides across conjuncts:
- Conjuncts (ii) and (iii) are *content/signature-intrinsic*: parse-validity reads only the immutable run; well-typedness reads the run plus each consulted `sig(r)`, fixed at `r`'s first registration (PR-SIG). These are validation forever.
- Conjunct (iv) is a *deposit-time reference-endorsement* — permanent as a fact about the deposit's pre-state, not as a standing fact at Σ.

---

## PR2 — AcyclicReference (LEMMA, DAG)

Under the registration discipline (PR-DISC), deposits into the `pdef` class are `→_sh` steps, totally ordered along any derivation.

For an ever-registered definition D, write `e₁(D)` for its *earliest* deposit event.

- (a) *Every deposit event sees each referent registered strictly earlier.* A deposit is the miss branch of a `register_pred` whose validation (iv) had just passed at the pre-state: each referenced address `r` carries an active tuple there, which entered `L_pdef` at some strictly earlier deposit event. Hence `e₁(r) < e₁(D)`.

- (b) *Self-reference fails at every deposit event.* At a deposit event for D every existing tuple denoting D's start is inactive — and the depositing tuple does not yet exist during its own validation. Condition (iv) therefore has no witness for a reference to D's own start.

The reference relation on ever-registered definitions thus embeds in the strict order `e₁(r) < e₁(D)` — irreflexive, acyclic, a DAG with no cycle check ever run.

*Consequently definitional expansion terminates*: expansion (PR3) descends reference edges, `e₁` strictly decreasing among the finitely many deposit events, each term finite; the expanded result is a pure PL term (no references).

---

## PR3 — EvaluationByReference (DEF, three-layer operation)

**Resolution** — address to signed term: read content values from `a` along its origin chain — successive addresses `shift(a, k)` — feeding the self-delimiting parse, which determines the run's extent from content alone and yields `(Γ_D, body)`. Resolution consults no slice and no tuple.

**Expansion** — `expand(a)`: in `body`, replace each applied reference by the referent's expansion with the expanded arguments substituted for its parameters. References are processed bottom-up, siblings left to right. At a node `r(·)` with expanded arguments `E₁, …, E_k`: take `expand(r)` — the recursion is well-founded because descent strictly decreases first-registration rank (PR2) — rename its parameters *and* every binding site in it to expansion names from PR-ENC's reserved supply, the least-indexed names occurring nowhere in the term under construction, the `Eⱼ`, or `expand(r)` itself, assigned in a fixed order (parameters first in signature order, then binding sites depth-first, left to right); then substitute `Eⱼ` simultaneously for the renamed j-th parameter.

`expand` is *determinate*: the parses are content (S0), the reference DAG is fixed by the parses, and every processing order and name choice above is fixed, so `expand` is a function of immutable content.

**Evaluation** — `evaluate(a, args, view, Σ)`. Precondition: `a` is *ever-registered* at Σ — spelled as: some `(b, F, G) ∈ L_pdef^Σ` with `addrs(F) = {a}` (equivalently `a ∈ M_pdef` at view `audit`, V-AUD). Active registration is *not* required.

`args` is a `Γ_D`-*environment*: one value of sort `Cᵢ` per parameter `xᵢ`, per `sig(a) = (Γ_D, C_D)` (PR-SIG).

`evaluate(a, args, view, Σ)` is the ASN-0129 denotation of `expand(a)` at `(args, view, Σ)`.

---

## PR3a — ExpansionWellTyping (LEMMA, well-typing)

On registration-disciplined derivations (PR-DISC): for every ever-registered `a` with `sig(a) = (Γ_D, C_D)`, `expand(a)` is a pure PL term with `Γ_D ⊢ expand(a) : C_D`.

Uses two auxiliary lemmas:

**WT-α (renaming).** If `Γ ⊢ u : C` and `ρ` renames variables sort-preservingly and injectively — acting on `dom(Γ)` and on `u`'s binding sites, its image names pairwise distinct and occurring nowhere in `u` — then `ρΓ ⊢ ρu : C`.

**WT-W (weakening).** If `Γ ⊢ u : C`, `y ∉ dom(Γ)`, and `y` occurs nowhere in `u` as a binder, then `Γ, y : C′ ⊢ u : C` for any sort `C′`.

*Proof structure* — induction on first-registration rank (well-founded by PR2) with nested structural induction on the body. At a reference node `r(e₁, …, e_k)` typed by WT-ref as `Γ ⊢ r(e₁, …, e_k) : C_r` with `sig(r) = (⟨x₁ : C₁, …, x_k : C_k⟩, C_r)`:

- *Arguments*: structural induction gives `Γ ⊢ Eᵢ : Cᵢ` for each `i`
- *Referent*: rank induction gives `expand(r) ∈ PL` with `⟨x₁ : C₁, …, x_k : C_k⟩ ⊢ expand(r) : C_r`; WT-α at the parameter-and-binder renaming yields `⟨y₁ : C₁, …, y_k : C_k⟩ ⊢ u : C_r`
- *Weaken*: iterated WT-W adjoins `dom(Γ)`, giving `Γ, y₁ : C₁, …, y_k : C_k ⊢ u : C_r`
- *Substitute*: `k` applications of WT's PC2 plain-composition rule, last parameter first, discharge to `Γ ⊢ u[y₁ ↦ E₁, …, y_k ↦ E_k] : C_r`

Result: `Γ_D ⊢ expand(a) : C_D`, with `expand(a) ∈ PL`.

---

## Definition — WTAlpha

If `Γ ⊢ u : C` and `ρ` renames variables sort-preservingly and injectively — acting on `dom(Γ)` and on `u`'s binding sites, its image names pairwise distinct and occurring nowhere in `u` — then `ρΓ ⊢ ρu : C`.

---

## Definition — WTWeaken

If `Γ ⊢ u : C`, `y ∉ dom(Γ)`, and `y` occurs nowhere in `u` as a binder, then `Γ, y : C′ ⊢ u : C` for any sort `C′`.

---

## PR-VIEW — ViewTransparency (DEF, view discipline)

A signed term records no view (PR-ENC) and `evaluate` takes one (PR3). PC3 (ASN-0129) gives every PL term exactly one view, fixed at the top level; expansion yields one pure term; so the view binding every view-parameterized constituent in every inlined referent is the evaluating *caller's*.

Call a term *view-independent* iff it contains no view-parameterized constituent and no collection-valued behavior atom on UV's rewrite list (`succs`, `sources_to`, `chain`, `stale`): a syntactic condition, decided by the same finite scan that decides well-typing. A view-independent term's denotation is invariant in the view argument.

---

## PR4 — VersioningBySupersession (DEF, versioning)

Definitions are never edited; they are *succeeded*. To update a predicate: register the successor (PR0), then emit `supersedes` (the shipped S2 class, ASN-0128) from the old definition's address to the new.

`tip(a)` resolves the current version of the lineage rooted at `a`; competing successors make a branch and `tip` returns ⊥.

---

## PR5 — DynamicsCertification (DEF, certification)

`certify_pd_stable` certifies a definition's expansion `ST⁺`.

**ST⁺** is a *sound superset* of PD0's literal closed-term **ST**: every literal-ST closed term is ST⁺, ST⁺ additionally admits parametrized terms, and the two coincide exactly at `k = 0`.

Three qualifications:

- *Purity*: the certified object is the definition's expansion `expand(a)` (PR3, well-typed by PR3a), not the artifact's literal reference-bearing spelling.
- *View*: the surface certifies only *view-independent* expansions (PR-VIEW's syntactic class). A view-independent term's denotation is invariant in the view argument, and the certificate binds at every `evaluate` call whatever view the caller passes.
- *Parameters*: ST⁺'s parameter reading is per-instantiation — the checker runs PD0's rules with each parameter treated as a bound constant of its declared sort. The certificate asserts that *every* `Γ_D`-instantiation of `expand(a)` is ⊤-stable: once true at a reachable Σ for given `args`, true at every `→_sh*`-successor for the same `args`.

The aggregate rule extension: the threshold position is extended from "ℕ literal" to *an ℕ literal or an environment-bound parameter*.

The universal lint form — "every registered definition carries `pd_stable`" — is the one-quantifier PL term:

`(A t ∈ M_pdef :: is_pd_stable(t))` — one term, view `active`

where `is_pd_stable(t)` is true iff some active certificate's F covers `t`, and the coverage test is exact at starts: `t ∈ subtree(t')` between starts forces `t' = t`.

---

## PR5a — CertificationSurface (DEF, operation contract)

The surface exposes `certify_pd_stable(d, a)`: *validate, then emit through the `pd_stable`-class emit it wraps*, returning the certificate tuple's address.

*Validation* at call state Σ, in order:

- (0) *Predicate sort*: `sig(a)` is defined with Boolean result sort — `sig(a) = (Γ_D, Bool)`
- (i) *Target status*: `a` is *actively* registered — some `(b, F, G) ∈ A_pdef^Σ` with `addrs(F) = {a}`
- (ii) *Well-posedness*: `expand(a)` is view-independent: PR-VIEW's syntactic scan, no view-parameterized constituent and no UV-rewritten collection atom
- (iii) *Class membership*: the checker's verdict `expand(a) ∈ ST⁺`, by PD0's rules under PR5's *Parameters* reading

On success: `Emit_pd_stable(Σ, d, {a}, ∅)` with deposit `(enc({a}), ∅, pd_stable)`.

*Weakest precondition* — for `POST-cert ≡ (E (b, F', G') ∈ A_pd_stable^{Σ'} :: addrs(F') = {a})`, on registration-disciplined derivations (PR-DISC):

```
wp(certify_pd_stable(d, a), POST-cert)
  ≡ (E (b, F', G') ∈ A_pd_stable^Σ :: addrs(F') = {a})
  ∨ (CVALID(Σ, a) ∧ d ∈ dom(Σ.M) ∧ C3(Σ, d))
```

with `CVALID` the conjunction (0)–(iii). C3 vanishes on surface-disciplined derivations (DR).

*Permanence for the slice*: At any state Σ reached by a registration-disciplined derivation, if `(b, F, G) ∈ L_pd_stable^Σ` with `addrs(F) = {a}`, then at the deposit's pre-state: `a` was actively registered with `sig(a)` Boolean, `expand(a)` was view-independent, and `expand(a) ∈ ST⁺` held. These facts are permanent: `expand(a)` is the same concrete term at every state (PR3's determinacy), view-independence is a syntactic property of that fixed term, the ST⁺ verdict is PD0's classification of that fixed spelling, and the Boolean sort is fixed at `a`'s first registration.

---

## PS1 — PredicateDefinition (DEF, class specification)

`pdef` — Multi, idem=⊤, behaviors=∅.

Slot convention: `F = enc({a})` denotes the definition's address — identity by start — and `G = enc(A_def)` denotes its run. `|F| = 1`, `|G| = n < ∞` (Multi shape conformance).

Marks a content run as a validated predicate definition. Dedup is by I0 coverage identity on both slots — same start, same run. No read-filter.

Emitted only through `register_pred` (entry-point seal: the exposed `Emit_K` rejects every `pdef`-class call by the uniform class-exclusion mechanism).

---

## PS2 — StabilityCertificate (DEF, class specification)

`pd_stable` — Unary, idem=⊤, behaviors=∅.

Slot convention: `F = enc({a})`, the certified definition's address; `G = ∅` (Unary).

Asserts **ST⁺** certification (PR5) of the view-independent expansion of the definition at `a`. Identity is by slot-F coverage `subtree(a)` alone — the Unary `G = ∅` collapsing the slot-2 coverage test.

Emitted only by `certify_pd_stable` (PR5a) (entry-point seal: same uniform class-exclusion mechanism extends to `K ≁ R ∧ K ≁ pdef ∧ K ≁ pd_stable`).
