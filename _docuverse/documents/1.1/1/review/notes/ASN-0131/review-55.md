# Review of ASN-0131

This is a careful, substantively sound note. I verified the core arithmetic: the worked example computes correctly (`a₂ ⊕ δ(2,#a₂) = shift(a₂,2) = a₄`, so the width-2 span's coverage contains `{a₂, a₃}` and the touch test fires on `a₂`); the `coverage(e₃) ∩ dom(Σ.C) = ∅` argument via separator-zero alignment is valid; RE-UDIST's `Avail`-factoring is legitimate (`touch_W(e)` is genuinely independent of `a`, so it pulls out of the existential); the RE-UDIST-∩ counterexample is a real refutation of `⊇` under non-injective `Σ.M(d)`; and RE-CWP is the correct weakest precondition with a sound `R = ∅` boundary. RE-ADDR's antichain argument is arity-independent as claimed, since nullification is driven only by arity-3 `L_R` tuples. The findings below are narrower.

## REVISE

### Issue 1: The standing assumption is mislabeled and hides the restriction RE-RET actually depends on

**ASN-0131, "The unit of the answer"**: "We adopt throughout, as a **standing assumption**, ASN-0086's *unit-depth retraction discipline*: retraction-typed links enter the store only through `Nullify`, so every retraction to-set is a unit-depth span `{(t, δ(1, #t))}` at a single prior target."

**Problem**: In ASN-0086 these are two distinct things. "Unit-depth retraction discipline" *is* the to-set property (every `L_R` tuple has to-endset `{(b, δ(1,#b))}`). "Retraction-typed links enter only through Nullify" is the *relational-layer discipline commitment* (every `L_R`-growing `→`-step is a `Nullify`), from which the discipline is *derived*. The note equates the name with the mechanism. This is not merely cosmetic: the mechanism is strictly stronger than the discipline, because `Nullify` hardcodes an **empty from-set**, whereas ASN-0086's unit-depth discipline constrains only the to-set and its Convention RetractionDirectionality explicitly permits attribution-bearing (non-empty) from-sets. RE-RET then relies on the extra strength silently — "the empty from-set `∅`... The first two are content-disjoint *unconditionally*" holds only because the from-set is `∅`. A reader who looks up "unit-depth retraction discipline" in ASN-0086 finds the to-set property alone and will not see that RE-RET's net-removal result also assumes away attributed retractions.

**Required**: Name the standing assumption as ASN-0086's relational-layer discipline commitment (all retractions enter via `Nullify`), note that ASN-0086's unit-depth retraction discipline is its to-set consequence, and state explicitly that RE-RET additionally rests on `Nullify`'s empty from-set — so attributed retractions (non-empty from-set, permitted by ASN-0086) are excluded by this assumption, and RE-RET's "content-disjoint unconditionally" is conditional on that exclusion.

### Issue 2: The Σ.L-evolution bridge is established once, then re-litigated at its use sites

**ASN-0131, opening + RE-ADDR**: the bridge paragraph carries "This carries even the lemmas whose hypotheses additionally name `dom(Σ.M)` — R-Scope's `d_retr ∈ dom(Σ.M)`, **the one we rely on below**, among them — because `dom(Σ.M)` is the *same* ASN-0093 document substrate..."; then RE-ADDR re-closes with "The argument rests only on R0a and the discipline — both `Σ.L`-constraints — so **the bridge carries it verbatim, with no hypothesis over `dom(Σ.M)`**, and it holds for every `K.λ` output regardless of arity."

**Problem**: The bridge's load-bearing claim — `Σ.L` evolves only through `K.λ`, so ASN-0086's `Σ.L`/`nullified` lemmas hold at ASN-0047-reachable states — is sound and is stated once. It is then re-justified anticipatorily: the nested em-dash aside about `dom(Σ.M)`-naming lemmas plus the "the one we rely on below" use-site preview interrupt the bridge claim, and RE-ADDR re-asserts the bridge transfer ("carries it verbatim, with no hypothesis over `dom(Σ.M)`") rather than just invoking it. Arity-independence is also stated twice inside RE-ADDR ("settles this for an output of *any* arity" / "regardless of arity"). The reader must parse past anticipated objections to follow each claim.

**Required**: State the bridge once, cleanly. Drop the use-site preview ("the one we rely on below") and the RE-ADDR re-justification of the bridge; if R-Scope's `dom(Σ.M)`-hypothesis transfer needs a word, attach it at R-Scope's actual use site (the retraction proof), not preemptively. State arity-independence once.

### Issue 3: Claims-table entries re-argue their sections instead of stating the claim

**ASN-0131, Claims Introduced table, RE-EDIT**: the entry runs ~160 words — "Over ASN-0047's atomic movers, only the content-subspace movers... `K.λ` emission/retraction... Extension to ASN-0082's shift-based insert/delete is M-only at every content depth: their `(C, M)` primitives write only `Σ.M(d)`, so the unique full-state lift *unconditionally* frames `L`, `E`, `R`... What the foundation scopes is the *displacement's existence* — delete to text depth `#p = 2`, insert to every `#p ≥ 2`... `RE` is evaluated at the post-insert reachable state..."

**Problem**: This table cell reproduces the entire editing-stability section's argument (the M-only lift, the depth asymmetry, the bare-shift gap vs. backfill) rather than stating the RE-EDIT guarantee. The same compression appears in RE-ADDR (which re-runs the antichain argument) and RE-RET (which re-states the hypothesis structure). The claims table should hold the statement of each guarantee with its conditions; the derivation belongs in the prose, and duplicating it in the table is the "essay content in a structural slot" pattern that compounds across cycles.

**Required**: Reduce RE-EDIT to its statement (present-tense, non-monotone stability tracking `d`'s content-subspace arrangement; spans fixed by RE-IDENT; the population-movers being content-subspace `K.μ` on `d` and `K.λ` emission/retraction), and similarly trim RE-ADDR and RE-RET to their statements plus the conditions they depend on, leaving the arguments to the body.

## OUT_OF_SCOPE

### Topic 1: Rendered answers, non-co-resident stores, link-subspace regions
**Why out of scope**: Open Questions 3, 5, and 7 defer, respectively, rendering a surfaced endset into the querying document's V-order (RETRIEVEV territory), completeness against a link store not co-resident with the queried document (BEBE/replication), and region queries over link-subspace V-positions. The note correctly leaves these as Open Questions rather than defining claims for them; no action — this is appropriate scoping, recorded here only to confirm the deferrals are not gaps in this ASN.

VERDICT: REVISE
