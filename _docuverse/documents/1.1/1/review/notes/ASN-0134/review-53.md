# Review of ASN-0134

The substantive backbone is sound. I checked the load-bearing proofs — H0–H2's frontier/commutation case analysis (including the first-emission boundary), G1's validity-then-reachability ordering and adjacent-transposition confluence, H3's two distinct commutation arguments, G2's literal-vs-operative `K`-surface-emittedness split, V2's strict-implication chain with both converse witnesses, the §7/§8 worked traces — and they hold up, with boundary cases handled and the step/operation seam kept honestly distinct from raw-step confluence. The note also correctly scopes itself to a *contract* (no mechanism), so no META.

The findings below are predominantly the forward-reference/meta-prose accretion the `anti-bloat` classifier asks me to surface at source, plus one logical imprecision.

## REVISE

### Issue 1: Use-site forward-pointers pre-announcing where a claim gets consumed
**ASN-0134, A6 / G1 / A1 / §1**:
- A6: "so a gapless initial segment stays a gapless initial segment step by step … **§5's W0 and W1 cite this preservation rather than re-deriving it.**"
- G1 (proof): "… same-home uniqueness serialization-borne (H2) — is the one A6 established **and §5's W1 classifies.**"
- A1: "**§4 leans on this** — an operation's very presence in the realized step set can be order-dependent."
- §1: "… via the prefix `Σ₀ → ⋯ → Σ_k`; **A6 will lean on this as its base case.**"

**Problem**: These are the "definition enumerates its downstream consumers rather than advancing its own meaning" pattern. A6's content is the canonicity of every `Σ_k`; whether W0/W1 later cite it is bookkeeping a reader must skip to follow A6. The citation direction belongs downstream (W1 may say "by A6"); the upstream pre-announcement ("W1 will classify this") carries no reasoning. These compound across cycles — the note has at least four.

**Required**: Drop the upstream pre-announcements. Let the consuming claim cite its premise; the premise should not catalogue its consumers.

### Issue 2: V2's "global, not per-home / writer-side vs reader-side" point is stated twice before it is used
**ASN-0134, §8 (V2 statement and the paragraph following it)**:
- V2: "This exclusion — and even V2's weaker middle condition — **is global in scope, not per-home** (§8): the per-home liberation of §4–§6 is a **writer-side result that does not extend to reader-side** multi-read isolation."
- Next paragraph: "This is a **reader-side** obligation, dual to W2's **writer-side** run contiguity in role but not in scope … **that is global, because any writer step at any home advances the index** … The roles are dual (writer-side vs reader-side); **the scopes are not (local vs global).**"

**Problem**: The second paragraph opens by re-deriving, in different words, exactly the scope/duality assertion V2 already made, before it reaches its genuinely new content (which homes a `Q`-affecting step lives at, and the retraction-undercounting correction). The reader works through a paraphrase to reach the new material. Clause 6 then echoes it a third time ("This exclusion is global, not per-home (V2)") — defensible there as a contract summary, but the V2-statement/next-paragraph pair is redundant.

**Required**: State the scope/duality once. Since the new content (Q-affecting-step homes, the nullification undercounting) lives in the following paragraph, let that paragraph carry the scope claim and trim the duplicate sentence from V2's body — or vice versa, but not both.

### Issue 3: H3(b)'s commutation attributes a case hypothesis to the wrong premise
**ASN-0134, H3 (proof, case (b))**: "a membership-test-and-insert of `d_new` and one of `d'_new` do not interfere precisely because the targets are distinct **(by §4's conditional)**, so each step's `dom(M)`-read verdict and inserted element are unchanged by the other's insertion."

**Problem**: Case (b)'s hypothesis is `d'_new ≠ d_new` — the targets are distinct *by assumption of the case*, not as a consequence of §4's shared-frontier conditional. §4's conditional governs the *other* branch: it tells you that two *same-account* `K.σ` against a common pre-state compute the *same* target (the non-commuting account-tier H2 pair). As written, "(by §4's conditional)" reads as "the conditional implies the targets are distinct," which is backwards — the conditional is what produces the *colliding* case, not the distinct one.

**Required**: Either drop the parenthetical (distinctness is the case hypothesis) or restate it correctly: §4's conditional is what *separates out* the same-target collision into H3's `≺`-comparable account-tier pair, leaving case (b) as the residual distinct-target regime.

## OUT_OF_SCOPE

No additional out-of-scope topics to raise. The note's deferred territory (scheduler/fairness, rule bodies, BEBE replication, lock mechanism, predicate cost) is correctly held out via "What this note does not cover" and the Open Questions, and no claim drifts into it. One observation, not a finding: instance (ii) (an `idem=⊤` coverage-equal emit racing a nullify of the *incumbent*) is documented inline as an irreducible order-dependence that neither clause 7 nor emit-before-retract tames — correctly treated as inherent assert/retract semantics rather than an open problem, and consistent with SAFE(b) (it yields 0-or-1, never a duplicate). It does not need elevation to an Open Question the way the target-residence race (OQ8) does.

VERDICT: REVISE
