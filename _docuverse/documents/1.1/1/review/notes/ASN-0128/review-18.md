# Review of ASN-0128

## REVISE

### Issue 1: SD's definiens has an unbound state variable and an unstated relation to I1a's notion
**ASN-0128, Idem operational semantics, SD**: "Call a substrate *surface-disciplined* when every tuple in `L_R^Σ` was deposited through this note's operation surface (DR)."
**Problem**: The predicate is declared of a *substrate*, but the defining formula reads one state's `L_R^Σ` with `Σ` free — nothing binds it. The intended reading matters: DR's derivation instantiates the discipline at arbitrary later states ("at a later emit's pre-state Θ — any state where the retraction tuple already sits in `L_R^Θ`"), so DR needs the all-reachable-states reading, which the definition never states. The neighboring I1a definition gets this right ("Call a *state's* K-history surface-emitted…"), which makes SD's looseness conspicuous; moreover SD is, modulo the wrapper being the only surface route into `L_R` (I6's `K ≁ R` exclusion), exactly "surface-emitted R-history at every reachable state" — a relation the note uses implicitly (the wrapper's hit branch invokes I1a via "R's history being wrapper-routed hence surface-emitted") but never records. Finally, the definiens cites its own consumer — "(DR)" — a forward pointer inside a definition.
**Required**: Bind the quantifier ("a substrate is surface-disciplined iff at every reachable state Σ, every tuple in `L_R^Σ` was deposited through the operation surface"), state SD's relation to I1a's surface-emitted notion at [R] in one sentence, and drop the consumer pointer.

### Issue 2: The view-selection mechanism for the enumeration surfaces is unspecified
**ASN-0128, Denotation and views (Views), BH1 Rewrite scope, D1–D3**: "the escape hatches differ accordingly: filtering is undone by asking the active view" and "the default view of `members(K')` is `{x ∈ members(K') : …}`" — against signatures `members(K) → set of addrs`, `targets_of(x) → set of addrs` with no view argument.
**Problem**: The note commits two distinct readings of each rewritten enumeration surface — the active-view value (D1/D3's definitions) and the default-view value (BH1's rewrite) — and the escape-hatch sentence presupposes a caller can *ask* for either. But no predicate signature carries a view selector, and `Observe_K`'s selector spans only `{hist, oper}`; the default view is reachable through no stated call form. This is not a corner case: `retired` ships with BH1 (S1), so `Φ ≠ ∅` on every conforming substrate and the two views differ at every retired-marked address. The example exercises both readings in consecutive sentences ("the default view of `members(marker)` excludes `a_x` … and the active view returns it") without ever showing how a caller designates one. An alternative implementation could conformantly expose only the default view, only the active view, or both under unspecified names — which is exactly what an operation surface must not leave open.
**Required**: Fix the surface: either extend the enumeration predicates with a view parameter (`default | active`, mirroring `Observe_K`'s `View`), or declare the unmarked call default-view and name the active-view escape explicitly. State the rule once in Denotation and views; this is independent of Open question 1's dominance choice, which concerns *which* surfaces the rewrite reaches, not how a caller selects a view on the surfaces it does reach.

### Issue 3: Forward-deferral and duplicated content in the Denotation block (anti-bloat)
**ASN-0128, Denotation and views (AD, AM) and D3**:
- AD's closing sentence: "AD types results and encodes the surface; it does not decide de-duplication — the idem section fixes sameness as coverage equality (I0), on surface emits strictly coarser than denoted-set equality (I0a)." This is a scope disclaimer plus a downstream deferral; I0 states its own criterion and its own coarseness claim (with I0a's separating pair). The sentence advances nothing AD owns.
- AM's closing sentence: "What denotation-keying refuses on the F-slot it does not lose: the assertion-level forward reading is recoverable by one composition over the D2 bridge — stated as `targets_under` at D3 — exactly as `is_K` recovers the subtree reading from `members`." D3 then carries the same content in full — the `targets_under` definition, the coverage-keyed equivalence, and "`targets_under` answers D2's question with D3's data." Two passages in different sections saying the same thing, one of them a preview of the other.
- The section intro: "These notions need pinning first, because the stored data is spans and the store forgets nothing" — prose justifying document ordering, the flagged pattern verbatim.
- RP-c's tail enumerates downstream consumers ("P5 … is the canonical instance; the same lift admits the wrapper's miss-branch deposit at extended-record states (Standard registrations)") — the second clause is a use-site inventory, not part of what RP-c asserts.
**Problem**: These are the accretion patterns this note is flagged for: deferrals to a downstream owner, the same argument stated in two places, and ordering justification. Each forces the reader to hold a pointer instead of a claim.
**Required**: Delete AD's closing sentence and the section intro's ordering justification; keep the recoverability argument in exactly one place (D3), reducing AM's closing to nothing or a bare cross-reference; trim RP-c to its assertion plus at most the canonical instance.

## OUT_OF_SCOPE

### Topic 1: Formal serialization and atomicity of the operation surface
I4 posits "a serializing authority orders the two calls before either becomes a step," and I1a's step case treats the dedup consultation and the `K.λ_sh` step as one event (the miss is evaluated at the step's own pre-state). Formalizing that atomicity — what the authority is, whether check-plus-step is interruptible, what happens under genuine interleaving — is a concurrency model the substrate relation deliberately lacks.
**Why out of scope**: The note correctly confines itself to the sequential interleaved model it inherits from ASN-0086; a concurrency semantics is new machinery, not an error here.

### Topic 2: Audit-view enumeration layer
Open question 6 covers audit-view chain walking only; audit-view variants of `members`/`targets_of`/`sources_to` (historical enumeration, reconstruction of pre-retraction states) are likewise unshipped, reachable today only through raw `Observe_K(…, hist)`.
**Why out of scope**: The active-view commitments are complete on their own terms; a committed audit-enumeration surface is a successor's territory.

### Topic 3: Rejection-reason taxonomy
The surface fixes rejection uniformly as "no step, no address" across gate failure, `K ~ R` exclusion, invalid home, and P-tgt failure. Whether callers can distinguish the reasons — an error model for the exposed partial operations — is an implementation-surface question.
**Why out of scope**: The note's obligation is the state semantics of rejection, which it discharges; error signaling adds no state, operation, or invariant.

VERDICT: REVISE
