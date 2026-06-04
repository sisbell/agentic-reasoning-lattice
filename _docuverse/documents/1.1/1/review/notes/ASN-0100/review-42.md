# Review of ASN-0100

## REVISE

### Issue 1: Circular citation between INS.M-exhaustive and §Atomicity
**ASN-0100, Effect — Arrangement (INS.M-exhaustive) and §Atomicity (uniqueness)**: "The exhaustiveness clause is a property of the post-state `V_{s_C}(d')`, established by direct step-tracking of the canonical decomposition; since Σ' is the unique post-state (§Atomicity), it is a property of Σ'."
**Problem**: INS.M-exhaustive justifies that it is "a property of Σ'" by appeal to uniqueness from §Atomicity, but §Atomicity's uniqueness argument for the arrangement ("`V_{s_C}(d')` equals Left ∪ Insertion ∪ Shifted-right by INS.M-left, INS.M-insert, INS.M-shift, and INS.M-exhaustive") in turn cites INS.M-exhaustive. The step-tracking that follows in INS.M-exhaustive ("no other elementary step can introduce an `s_C` position, since K.α and K.ρ frame `M`…and K.μ⁻ only removes") already establishes exhaustiveness of the decomposition's output without needing uniqueness.
**Required**: Drop the "since Σ' is the unique post-state (§Atomicity), it is a property of Σ'" clause; let INS.M-exhaustive rest on its step-tracking, which §Atomicity may then cite without circularity.

### Issue 2: Defensive non-citation parenthetical (Effect One)
**ASN-0100, Discovering the Three Effects → Effect One**: "(This conclusion is consistent with L14, StoreDisjointness; ASN-0093, and with DisjointSubAllocatorChains; ASN-0093 — both follow from the same subspace separation — but neither directly entails the clause for `a_k` since `a_k ∉ dom(Σ_k.C)` already, so L14's per-state disjointness at `Σ_k` carries no constraint between `a_k` and `dom(Σ_k.L)`.)"
**Problem**: Meta-prose explaining why two lemmas are *not* cited. The `a_k ∉ dom(Σ_k.L)` clause is already discharged by the preceding DisjointSubAllocatorChains + L0 + SC-NEQ argument; this parenthetical adds nothing to the reasoning and forces the reader past a citation-bookkeeping aside.
**Required**: Delete the parenthetical.

### Issue 3: I3 scope-note use-site sentence
**ASN-0100, Effect Three (Scope of ASN-0082's I3)**: "Downstream verification cites this single scope note rather than re-deriving it."
**Problem**: Enumerates how downstream sections consume the note rather than advancing the scope claim itself — the residual accretion the "tighten I3 scope note" revision did not remove.
**Required**: Delete the sentence; the scope note stands on its two-clause statement (I3-C and I3-S7 fail here).

### Issue 4: Use-site inventory in the Notational convention
**ASN-0100, The Operation's Inputs (Notational convention)**: "The convention is used throughout the per-region clauses (Insertion at `k = 0` resolves to `M'(d)(p) = a_0`) and in the S8a, OrdAddHom, and ord-extraction analyses that follow."
**Problem**: A definition's introduction enumerating its downstream consumers — the flagged pattern. The convention's meaning (`shift(t,0):=t`) is fully stated; the consumer list does not advance it.
**Required**: Cut the sentence; consumers invoke the convention at their own sites.

### Issue 5: Duplicate S8a verification with subsumption announcement
**ASN-0100, §Post-state V-position well-formedness (S8a bullet)**: "This subsumes the empty-case S8a verification above, factoring out the Insertion-region argument as a general property of `shift(p, k)` independent of whether the Left and Shifted-right regions are non-empty."
**Problem**: A paragraph that announces it duplicates an earlier passage (the S8a check inside §Sequential text-subspace structure, empty case) is a signal the earlier copy should be removed, not back-referenced. The same `shift(p,k)` S8a argument is also restated in §Atomicity step 3. The author has noticed the redundancy without resolving it.
**Required**: Consolidate the `shift(p,k)` S8a argument to one site and have the others cite it, deleting the verbatim re-derivation rather than annotating it as subsumed.

### Issue 6: "Non-tight alternative" reconstructs foundation internals
**ASN-0100, A Worked Example (Non-tight alternative)**: "*Failure mode (a) — non-canonical span:*…LP-Fin…gives `|F ∩ [s, s ⊕ ℓ_w)| = ℵ₀`…*Failure mode (b) — F-candidate gap:*…"
**Problem**: This passage re-derives ASN-0098's tightness definition (its two failure regimes and LP-Fin's cardinality argument) rather than citing it. It is essay content about ASN-0098 internals occupying a worked-example slot; the INSERT-relevant point (INS.proj's general form admits non-empty `N_I`) is made in one sentence and does not need the failure-mode taxonomy reconstructed.
**Required**: Reduce to the operative statement — when `tight(e_1, Σ_{e_1})` fails, LP19a is inapplicable and `N_I` may be non-empty per INS.proj — citing ASN-0098 for the conditions rather than restating them.

## OUT_OF_SCOPE

### Topic 1: Recovery of canonical order after partial composite failure
**Why out of scope**: The first Open Question (minimum substrate machinery / failure recovery) is correctly deferred; it concerns substrate transactional mechanics, not INSERT's per-state contract.

### Topic 2: Link-subspace insertion (K.μ⁺_L)
**Why out of scope**: Already bounded by §Bounding the Scope; link-subspace insertion is a distinct operation.

VERDICT: REVISE
