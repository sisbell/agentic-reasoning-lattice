# Review of ASN-0133

## REVISE

### Issue 1: Q0's view rebuild omits the default-view UV filter for `members`/`targets_of`/`M_K`

**ASN-0133, Q0 (Recognizability)**: "through them PC3's cross-view derivations ... rebuild each of its *exactly four* view-parameterized constituents — `members`, `targets_of`, `is_K`, `M_K` — between audit and active at any chosen common view, value intact" and "a domain's `M_K` rebuilding as the set-valued term `⋃(A_K/L_K, addrs_F)`".

**Problem**: The rebuild for the four view-parameterized constituents is given only "between audit and active." But three of them — `members`, `targets_of`, `M_K` — are *collection-valued* and are therefore also UV-rewritten under the default view, which the note itself acknowledges ("UV ... rewrites *six* collection atoms under the default view: `members` and `targets_of`, already among the four, *and* the four ... behavior collections"). The note then supplies the UV-filter rebuild (`{y ∈ raw_active : ¬is_filtered_J(y)}`) explicitly and only for "*these four*" behavior collections, setting `members`/`targets_of` aside as "already among the four [view-parameterized]."

The consequence is concrete: `[M_K]_Σ = members(K, v)` (QD), so at `v = default` the domain denotes `members(K, default)` = active members **minus filtered** (ASN-0128 BH1 Rewrite scope). The stated rebuild `⋃(A_K, addrs_F)` equals `members(K, active)` — the *unfiltered* set. Applied to a default-view `M_K` domain (or a trigger reading `members(K, default)` / `targets_of(x, default)`), the note's explicit rebuild produces the wrong value. `is_K` is exempt (it is Boolean, never UV-rewritten, and `is_K` at default equals active per PC3), so the gap is exactly the three collection-valued constituents.

The conclusion `quiescent_R ∈ PL` remains *true* — the correct rebuild `{x ∈ ⋃(A_K, addrs_F) : ¬filtered(x)}` exists — but the exhaustiveness claim ("every view-sensitive part of every trigger *and* of every domain ... can be moved to one chosen term view") is not discharged by the construction as written. This is precisely the kind of case the heavily-emphasized view enumeration ("exactly four," "six") is meant to cover.

**Required**: State that `members`/`targets_of`/`M_K`, being *both* view-parameterized *and* UV-rewritten collections, take the UV filter at the default view exactly as the behavior collections do — compose the active reading with `{· : ¬filtered(·)}`. The `⋃(A_K/L_K, addrs_F)` rebuild covers only audit and active.

### Issue 2: PR-DISC framing in "Triggers: inline or by reference" states its conclusion twice around one technical sentence

**ASN-0133, "Triggers: inline or by reference"**: "that standing hypothesis (just named) is the premise of Q0's PL-membership, not a side condition on a "link": a pdef-trigger's verdict is a decidable PL evaluation only because `expand(a)` is a terminating, well-typed PL term ... PR-DISC is thus what makes there *be* a decidable PL verdict, the premise of Q0 rather than a condition on a link downstream of it."

**Problem**: The conclusion — *PR-DISC is the premise of Q0, not a "condition on a link"* — is asserted before the technical sentence and again after it; the middle sentence (`expand` needs PR2 acyclicity, itself proved under PR-DISC, else non-terminating) is the only content. The two bracketing assertions say the same thing in different words. The scare-quoted "link" is never explained — it reads as residue arguing against a prior characterization, consistent with the recent revisions touching "PR-DISC conditionality framing in Q0/Q1/Triggers." Separately, the unconditionality claim from Q1 ("Recognizability and absorption are *unconditional* relative to the dynamics hypotheses") is restated here ("Recognizability and absorption (Q0, Q1) are unconditional relative to the termination dynamics hypotheses (Q1) but *not* unconditional relative to PR-DISC").

**Required**: Keep one statement of the conclusion plus the one technical sentence; drop the unexplained "link"/"downstream" framing and the Q1 restatement (cite Q1 once).

### Issue 3: "fire sequence" denotes two distinct things

**ASN-0133, H-FIN vs H-FAIR**: H-FIN says "every admissible fire sequence terminates" (a single fire's internal `→_sh` steps) and then "the registry-level termination (Q5/Q6) of the fire *sequence*" (the interleaving). H-FAIR then *formally defines* "A *fire sequence* `σ`" as the interleaving.

**Problem**: The same term names a single fire's step run and the registry-level σ, and the formal definition is the latter — so the H-FIN usage collides with its own later definition. The note flags the two as "separate" but still spells them identically.

**Required**: Rename the fire-internal sense (e.g. "every admissible fire's step run terminates") so "fire sequence" is reserved for σ.

### Issue 4: H-RF, the operative hypothesis, is defined after the lemmas that conclude it

**ASN-0133, "Conditional termination"**: Q5 references "the same finite-real-fire conclusion (H-RF, below)"; Q5a "This supplies H-RF (below)"; H-W "the H-RF/H-W separation drawn at H-RF below." H-RF is then defined *after* Q5/Q5a.

**Problem**: The note's named operative hypothesis is pointed to "(below)" from three earlier sites before it exists, and the H-RF/H-W separation is deferred to from both H-W (forward) and Q6 (back) — the forward-reference accretion the review mode targets. The lemmas (Q5, Q5a) literally conclude H-RF, yet H-RF is stated downstream of them.

**Required**: Define H-RF (and the H-RF/H-W separation) before W/H-W and Q5, so Q5/Q5a reference it backward and the "(below)" pointers disappear.

## OUT_OF_SCOPE

### Topic 1: A turn-fair scheduler realizing H-SFAIR
**Why out of scope**: The note correctly observes that H-SFAIR's regime form is unsatisfiable against an arbitrary add-then-remove environment and "satisfiable only under a turn-fairness ... this note neither states nor derives." Constructing such a scheduler and proving it meets H-SFAIR belongs to the deferred scheduler note, not here.

### Topic 2: The `pd_extinct` (SF) certificate class
**Why out of scope**: Q-EXT/Q5a lean on SF membership as an uncertified (though decidable, syntax-directed) registration check; shipping a designated SF-certificate class is correctly raised as Open Question 1, paralleling ASN-0130's OQ4. SF-*checkability* is established in-note; only the certificate artifact is future.

META: not applicable — the note stays at the specification level (substrate-recognizable quiescence as a PL term, an absorption invariant, and conditional termination guarantees over contracts and state), and explicitly defers scheduler/environment/activation mechanics to layers above.

VERDICT: REVISE
