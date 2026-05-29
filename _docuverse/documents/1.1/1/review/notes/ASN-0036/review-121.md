# Review of ASN-0036

## REVISE

### Issue 1: Dangling forward reference to "#runs(d) below"
**ASN-0036, S8 *Non-canonicality* remark**: "their occurrence and preservation are determined by operations-layer behavior... The architectural discussion of `#runs(d)` below addresses typical operational regimes; the invariant itself does not commit to a canonical run count."
**Problem**: There is no "architectural discussion of `#runs(d)`" below. The only post-proof sentence reads: "The number of distinct Istream allocation events underlying a document's history is monotonically non-decreasing (by S1), but the current arrangement's run count fluctuates with editing." It neither uses the notation `#runs(d)` nor discusses operational regimes. The forward pointer points at nothing — classic forward-reference accretion.
**Required**: Delete the forward pointer (and the `#runs(d)` notation), or replace it with the actual one-sentence statement it gestures at.

### Issue 2: S8 corollary is conditioned on a run the theorem does not construct
**ASN-0036, S8 Postconditions, "Corollary ... conditional on a hypothesized non-trivial run"**: "*Hypothesize* a non-trivial run `(vⱼ, aⱼ, nⱼ)` with `nⱼ > 1` ... — a structure this theorem does not construct ... For any such hypothesized run, every image `shift(aⱼ, k)` ... preserves the structural properties of `aⱼ`."
**Problem**: The existence proof establishes only the singleton decomposition (`nⱼ = 1`), for which the corollary is self-admittedly "vacuous beyond `k = 0`." A whole postcondition paragraph then reasons about a case the proven claim explicitly excludes. This is reviser drift — imagining a case the carrier does not deliver. The underlying fact (shifts preserve subspace/zero-count/depth) is real, but it is a pointwise consequence of `ShiftPreservation` on `dom(Σ.C)` and does not depend on any run existing.
**Required**: State the structural-preservation fact unconditionally as a consequence of `ShiftPreservation` applied to each `aⱼ ∈ ran(M(d)) ⊆ dom(Σ.C)`, dropping the "hypothesize a run this theorem does not construct" framing. If non-trivial runs are genuinely operations-layer territory, move the corollary there entirely.

### Issue 3: Repeated deferral to the same operations-layer location
**ASN-0036, S8**: the *Non-canonicality* remark defers run coarsening to "operations-layer behavior"; the Postconditions corollary defers again with "(its occurrence is operations-layer-determined; see the Non-canonicality remark)"; the Open Questions section defers a third time ("must sequential content creation produce a single run...").
**Problem**: Three sites in the same theorem point at the same downstream concern. The cross-reference "see the Non-canonicality remark" inside the formal contract is meta-prose the precise reader must navigate around.
**Required**: Consolidate to a single statement that run cardinality is operations-layer-determined; remove the intra-contract cross-reference.

### Issue 4: Verbatim-duplicated actionPoint-bound parenthetical
**ASN-0036, OrdAddHom Preconditions and OrdAddS8a Preconditions**: both contain, word-for-word, "(The bound `actionPoint(w) ≤ m` is not stated separately: ActionPoint's contract in ASN-0034 already gives `1 ≤ actionPoint(w) ≤ #w`, and `#w = m` then forces `actionPoint(w) ≤ m`.)"
**Problem**: The identical justification appears twice in adjacent contracts — duplicated prose that compounds across cycles.
**Required**: State it once (e.g., at OrdAddHom, the first consumer) and let OrdAddS8a inherit the precondition silently.

### Issue 5: S7c Consequence (a) "Derivation" is trivial filler
**ASN-0036, S7c Consequence (a)**: "*Derivation:* By S7b, `zeros(a) = 3`, so ... `E(a)` is well-defined ... `E(a)₁` and `E(a)₂` are therefore distinct positions. The content ordinal ... begins at position 2 ... and so does not overlap `E(a)₁` at position 1."
**Problem**: The "derivation" establishes only that position 1 differs from position 2 when a sequence has ≥2 components — a restatement of the axiom `#E(a) ≥ 2`, advancing no reasoning. A definition's introduction padded with a vacuous derivation.
**Required**: Drop the Consequence/Derivation block; the axiom `#E(a) ≥ 2` already says it.

### Issue 6: ValidInsertionPosition structural postconditions asserted, not derived
**ASN-0036, Valid insertion position**: "The structural postconditions of both predicates — distinctness of the valid positions, depth preservation, subspace identity, and S8a consistency — follow from this explicit form and are stated in the contracts below."
**Problem**: Postcondition (c) ("exactly `N + 1` values of `v` satisfy the predicate") depends on `shift(min, j)` being distinct across `j ∈ {0,…,N}`. "Follow from this explicit form" is a claim, not a derivation — the distinctness of `[1,…,1+j]` across `j` (by T3 on distinct last components, plus strict monotonicity of `shift`) is never shown. For a depth-mandatory review this is a one-line gap left open.
**Required**: Either show the one-line distinctness step (`1+j` distinct ⇒ tumblers distinct by T3) or cite it explicitly rather than hand-waving with "follow from."

## OUT_OF_SCOPE

### Topic 1: Link-subspace (S = 2) well-formedness claim
**ASN-0036, Arrangement contiguity *Remark***: "Link-subspace V-positions satisfy the same `zeros(v) = 0`, `#v ≥ 2` ... constraints ... S8a holds uniformly across both subspaces."
**Why out of scope**: Links and the link subspace are explicitly out of scope per the Scope section ("links and endsets"). The remark asserts a substantive claim about link-subspace V-positions. Defer the link-subspace structural claim to the future link ASN; here it is unverified scope creep. (Scoping D-CTG/D-MIN/D-SEQ to `S = 1` is correct and should stay; only the affirmative claim about `S = 2` belongs elsewhere.)

### Topic 2: Operation-level preservation of D-CTG/D-MIN and subspace alignment
**Why out of scope**: The Open Questions correctly route "does each editing operation preserve D-CTG/D-MIN" and "which operations establish subspace alignment" to the operations layer. These are operation frame/postcondition concerns (explicitly out of scope) and are appropriately deferred, not flagged as gaps here.

VERDICT: REVISE
