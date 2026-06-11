# Review of ASN-0129

## REVISE

### Issue 1: The conservativity accounting omits the store-domain enumeration bases, and `C_dom` is admitted without a ground

**ASN-0129, The atomic vocabulary (V) / Quantification domains (QD) / PC6**: "This note's own additions are exactly four, each conservative and each fenced where introduced... Only the first two of the four extend what the vocabulary *reads*."

**Problem**: The audit is scoped to `V_atom`, but the note's genuinely novel read capabilities are not all in `V_atom`. PC6 itself concedes that `dom(Σ.C)` and `dom(Σ.M)`, "with no reading atom, stand as irreducible base reads" — i.e., QD's `C_dom` and `M_dom` bases grant enumeration reads that no upstream surface exposes (ASN-0086's `Observe_K` reads `Σ.L` only; ASN-0128 ships no domain-enumeration atom). Of the note's four counted additions, V-AUD is derivable from `Observe_K`'s hist selector and V-TUP reads values `Observe_K` already returns — the *most* novel reads in the note are exactly the two that escape the accounting. Moreover, `M_dom` receives a deliberate-admission sentence in QD (the gating-clause ground via I1/I5), but `C_dom` receives none at its introduction; its only rationale is a dynamics-cost remark in PD2 ("`C_dom` buys content-existence tests at the price of K.α-sensitivity"), which prices the read but does not license it. A symptom of the under-integration: PC4's mechanism sentence ("atoms evaluate through `Observe_K` and the active-subset machinery") is false of the store-domain enumerations and of BH4's chain arithmetic.

**Required**: Extend the conservativity audit to cover QD's base admissions (count the store-domain enumerations among the note's additions, or state explicitly at QD why domain-expression bases sit outside the vocabulary audit and give them their own audit line); give `C_dom` an admission ground parallel to `M_dom`'s, or drop it; correct PC4's mechanism sentence to name all three read routes (Observe_K/active-subset machinery, store-domain enumeration, home-chain arithmetic).

### Issue 2: COD omits bare `T` while the note types terms at `T`

**ASN-0129, COD (Codomains)**: "`Codom = {Bool, ℘_fin(T), T ∪ {⊥}, Seq_fin(T), Map_fin, ℕ, ℕ ∪ {⊥}}`... Atom and composite codomains are drawn from Codom... PC0–PC2a compose within `Codom` and introduce no codomain beyond it."

**Problem**: V-TUP types `addr(x) : T`; PC2's binder guard explicitly produces a binder "at the *narrowed* base type — `T` from `T ∪ {⊥}`" to which `is_K`, address equality, and `≼` apply; and V-PRIM admits address literals as constants. So bare `T` is a working type of the system — atoms have it as codomain, binders carry it, literals inhabit it — yet it is absent from the enumerated codomain set, falsifying "atom and composite codomains are drawn from Codom." The asymmetry is conspicuous: ℕ appears in both bare and ⊥-adjoined form, `T` only ⊥-adjoined.

**Required**: Add `T` to `Codom` (and, if intended, state the evident coercion `T ⊆ T ∪ {⊥}` so the binder-guard narrowing is an operation between two listed codomains), or state explicitly that `T`-typed forms are the defined fragment of `T ∪ {⊥}` and adjust `addr`'s and the literals' stated types to match.

### Issue 3: UV — the note's settlement of ASN-0128 Open Question 1 — is never exercised against a concrete state

**ASN-0129, UV / Worked composition**: "UV closes the question by extending the committed rule per codomain rather than inventing a second one..."

**Problem**: The note's trace is exemplary for the active/audit split: three named states, every gate and landing checked, `quiescent` and `ever_res` evaluated per state. The default view gets nothing comparable. UV is one of the note's two open-question settlements and its most consequential definitional commitment (collections rewritten; verdicts, Booleans, traversal, arguments never), yet no worked evaluation verifies the split — `head_live` mentions retirement but is never evaluated at a state, and the trace never deposits a `retired` tuple. The verification is cheap and the scenario is constructible from the trace's own endpoint: `Emit_retired(Σ₃, d, {c₁}, ∅)` passes the Unary gate, misses dedup (`A_retired^{Σ₃} = ∅`), and lands active at `chain_d(3)` (C3: the lone retraction's coverage is `subtree(a₂)`, which the fresh slot avoids by R0a); at Σ₄ under `default`, `members(cmt, default) = ∅` while `is_cmt(c₁) = ⊤` — one atom rewritten, one preserved, and `quiescent(t)` reading ⊤ at default versus ⊥ at active exhibits FP's default-view footprint increment in the same stroke.

**Required**: Extend the worked trace (or add a short fourth step) depositing a BH1-type tuple and evaluating at least one collection-valued atom and one Boolean- or verdict-valued atom under `v = default`, confirming UV's rewrite/preservation split at a concrete state.

### Issue 4: Duplicated fences and deferrals across sections (anti-bloat)

**ASN-0129, multiple sites**: the same scope statements recur in different slots:

- The protocol-constructions fence is stated three times: intro ("what protocols are built, and under what scheduler, is application-layer territory fenced at the end"), the close of Predicate dynamics ("The termination arguments themselves... are protocol-layer constructions over these classes, outside this note's scope"), and "What this note doesn't cover" bullet 1.
- The bounded-LFP successor is stated twice: C-reach's close ("the first candidate for a successor that consciously raises the ceiling is a bounded least-fixed-point operator (Open Question 4)") and Open Question 4 itself, in nearly the same words.
- Ceiling-pinned-to-registry is stated three times: intro ("Composition extends expressiveness within a ceiling fixed by the registry's shapes and behaviors"), V-STAT ("The expressive ceiling is thereby pinned to `Σ_init`'s registry"), and PC6's close ("The ceiling moves only when the registry does").
- The extension-language commitment appears near-verbatim in the intro and inside PC6 ("the substrate never executing foreign read-path code, only evaluating terms of a closed algebra" / "evaluates terms of a closed algebra and never executes foreign read-path code").
- Consumer-enumeration pointers sit in definition slots: QD-refl's "the worked `quiescent(t) ≡ OPEN(t) = ∅` is its use case," QD filtering's "(the worked `OPEN(t)` below)," and V-PRIM's literal inventory "(the `n` of `under_cap`, the `h` of `stale`... the `t` of `OPEN(t)`)."

**Problem**: Each instance is small, but this is exactly the compounding pattern the anti-bloat classifier targets: multiple sections deferring to the same downstream location, and the same sentence said in two or three slots. The load-bearing instances are PC6's (the commitment grounds the evaluation-class choice) and the structural slots (What-this-note-doesn't-cover; OQ4); the others are framing echoes a precise reader must re-read to confirm they add nothing.

**Required**: One canonical site per fence — keep the protocol fence in "What this note doesn't cover," the LFP successor in Open Question 4, the ceiling/commitment statements in PC6 — and trim the echoes (the intro keeps at most one clause each, the C-reach close keeps the pointer to OQ4 without restating its content; drop the use-case pointers from the definition slots or reduce to bare claim-label cross-references).

## OUT_OF_SCOPE

### Topic 1: Completing the PD0 stability classes
**Why out of scope**: PD0 deliberately scopes to enumerated forms ("we keep the class to the enumerated forms") and several semantically stable forms fall outside it — `targets_of(x, audit)` as a grow-only set-valued domain, the guarded T1-extremum bound the note itself proves stable in passing, sums of counts over grow-only domains against literals. A sound-and-more-complete classification, and its mechanical decidability, is exactly Open Question 5's territory — a successor's work, not an error in this note's conservative classes.

### Topic 2: I0-class selection as a PL predicate
**Why out of scope**: PC2a's illustrative counting bounds speak of per-I0-class counts semantically, but whether "x is I0-equal to a given `(F₀, G₀)`" is *expressible* in PL is unaddressed: V-TUP supplies coverage *membership* tests only, and coverage *equality* against query data is not obviously reconstructible (I0a gives a route for address-denoting endsets via `addrs` and ≼-minimality; the general case is open). Nothing in this note's claims depends on the answer; it is a natural successor question for the algebra, alongside the note's own acknowledged value-position omissions (e.g., binary set union), which are closable by V-PRIM-style admission if a consumer forces them.

VERDICT: REVISE
