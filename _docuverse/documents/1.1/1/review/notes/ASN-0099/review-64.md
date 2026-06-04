# Review of ASN-0099

This note carries the `review-mode.anti-bloat` classifier, and the dominant findings are accreted meta-prose around the forward-reference and lemma-citation machinery. The underlying claims (F1–F20a, A1, the two meta-lemmas) are largely sound; the worked example exercises the load-bearing cases (F6, F9 multi-step, F9-λ growth, F11 across K.λ). The issues below are placement and accretion, not arithmetic.

## REVISE

### Issue 1: Meta-lemma introductions enumerate downstream consumers
**ASN-0099, "Determinism and Comprehension Invariance"**: "We name it once so downstream claims (F11, F15, F17, F19, F19-filt, and related variants) can cite it as a discrete step."
**Problem**: This is a use-site inventory — a list of who will cite the meta-lemma — not content that advances the lemma's meaning. The same pattern recurs for `PerLinkInvarianceUnderValuePreservation` ("Several downstream claims (F11, F19-filt) reason from a per-link hypothesis…"). A lemma's worth is its statement and proof; the citation roster rots as downstream claims are renumbered.
**Required**: State each meta-lemma and its proof. Drop the enumerations of downstream consumers; let the downstream claims cite the lemma at their own site.

### Issue 2: A1 carries scope-inventory and downstream-restatement meta-prose
**ASN-0099, A1 (LinkStoreInertOfNonAllocatingOperations)**: "Vocabulary scope: V = {K.α, K.λ, …} … Downstream ASNs consuming A1 against an evolved vocabulary must restate the claim."
**Problem**: The labeled "Vocabulary scope:" sub-paragraph and the closing sentence about downstream ASNs are prose about how A1 should be reused, not about what A1 says. The K.μ~ exclusion paragraph similarly explains *why* A1a is structured to route through the decomposition rather than stating the fact ("Its ASN-0047 frame clause `L' = L` is labelled '(derived)' precisely because…"). This is rationale accretion.
**Required**: Collapse A1/A1a to the claim (K.λ is the unique L-modifying operation of V; every other op publishes `L' = L`; K.μ~ inherits via its two atomic steps). Remove the scope-reuse sentence and the "(derived)"-label exegesis.

### Issue 3: F4 defensive "essential" notes on witness constructions
**ASN-0099, F4 realizability witnesses**: "Populating all three slots is essential…", "Placing the witness at slot 3 is essential…", "Placing the witness at slot 3 with slots 1 and 2 empty is essential…".
**Problem**: Each witness is followed by a paragraph defending the construction choice against a hypothetical mis-construction (vacuous-empty-slot masking, etc.). These defend the proof's bookkeeping rather than advancing the refutation. They are exactly the "defensive justification" the anti-bloat lens names.
**Required**: Keep each witness's construction and the one-line consequence (predicate P excludes the witness, F1 admits it). Drop the "X is essential" defenses.

### Issue 4: Redundant universal-realizability paragraph layered over five worked witnesses
**ASN-0099, F4 "Realizability discharge"**: "We close the realizability gap universally. … Therefore every F1-admitted (endset configuration, I) pair is realizable by a K.λ allocation under any document." followed by: "The illustrative refutations below — three strengthenings and two weakenings — are concrete instances of this universal realization."
**Problem**: If the universal K.λ argument closes realizability for all pairs, the five fully-worked witnesses are illustrative surplus; if the five witnesses carry the load, the universal paragraph is framing overhead. The note keeps both at full length, doing the same work twice.
**Required**: Choose one. State the universal realizability argument once, then cite at most one concrete witness as illustration — or keep the witnesses and reduce the universal paragraph to its conclusion.

### Issue 5: The "meta-lemma not applicable here" caveat is repeated four times
**ASN-0099, F11 / F9-λ / F19-filt / Query 6**: e.g. F11 "(The comprehension-level meta-lemma ComprehensionInvariantUnderΣL is not available here, since K.λ steps … may grow dom(L); per-link reasoning is the appropriate tool.)"; F9-λ "ComprehensionInvariantUnderΣL is *not* applicable here (dom(Σ'.L) ⊋ dom(Σ.L))…"; F19-filt "(The comprehension-level meta-lemma is not available across the reachable sequence…)"; Query 6 "The comprehension-level ComprehensionInvariantUnderΣL is *not* applicable (dom(Σ_6.L) ⊋ dom(Σ_5.L))…".
**Problem**: The same explanation — "domain grows under K.λ, so use the per-link primitive" — is restated in four sections. This is the "multiple paragraphs say the same thing" pattern.
**Required**: State the dom-growth/per-link distinction once (at PerLinkInvarianceUnderValuePreservation, where the primitive is introduced) and let the citing claims simply invoke the per-link primitive without re-explaining why the comprehension form fails.

### Issue 6: Silent-projection counterexample apparatus is defensive design-justification
**ASN-0099, "A Two-Phase Factoring"**: the `g(R,d,Σ)` treatment, conditions (i)/(ii), and "The constant-`ran` treatment … violates the strengthened (i) whenever R fails to cover dom(Σ.M(d)): with dom(Σ.M(d)) = {v¹,v²,v³}… it emits α₂, α₃…".
**Problem**: `image` is defined by a one-line comprehension; the surrounding paragraph constructs an alternative treatment and a counterexample purely to argue *why* silent projection rather than constant-`ran` was chosen. That is justification of a definitional choice, not specification content.
**Required**: Keep the `image` definition and the one-sentence statement that V-positions absent from the arrangement contribute nothing. Move or cut the `g`/constant-`ran` uniqueness argument; if the uniqueness result is wanted, state it as a named lemma rather than embedding the counterexample in the definition's prose.

## OUT_OF_SCOPE

### Topic 1: Inverse direction (FOLLOWLINK / endset→V-position resolution)
**Why out of scope**: Correctly deferred by the note itself; resolving result endsets back to V-positions is a separate operation, not a gap in FINDLINKS.

### Topic 2: Partition/replication consistency and timing bounds
**Why out of scope**: Multi-instance link stores, BEBE propagation, and any latency bound beyond "next query after K.λ" are future-ASN territory; the note properly lists them under "What We Have Not Specified" and "Open Questions."

VERDICT: REVISE
