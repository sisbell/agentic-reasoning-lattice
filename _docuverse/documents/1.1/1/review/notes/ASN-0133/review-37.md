# Review of ASN-0133

I worked the rigor checklist first: Q0's view-merge (the four PC3 view-parameterized atoms, the six UV-rewritten collections, the verdict/Boolean/Map view-stable atoms, the `chain`-via-`elems`/`is_in_chain` case), the Marker-pattern dedup-hit and born-nullified arguments in Q3, the SF + extinction composition in Q-EXT, Q5's index-injection, Q5a's bound and its SF-alone counterexample, and Q6's regime/obstruction analysis with the H-SFAIR regime form. The mathematics holds — the proofs show their cases, boundaries (empty registry, empty domain, no-real-fire `N`, finite σ) are covered, foundation citations are used correctly, and the note stays at the level of abstract guarantees (no META). The findings below are all the flagged class — residual meta-prose around forward references — not correctness.

## REVISE

### Issue 1: Document-structure narration around forward references
**ASN-0133, intro / RG / Q1 / Q4**:
- Intro: "This note closes the arc: it defines what it is for such a system to be *done* … and proves what can and cannot be guaranteed about reaching it. The shape of the answer is fixed by a fact about forward-chaining systems generally…"
- RG: "It is this *open* reading the termination hypotheses below are built for…"
- Q1: "They say nothing about whether quiescence is reachable; that is the rest of the note."
- Q4: "(H-W is doing real work)."

**Problem**: These narrate the note's own layout and forward-justify hypotheses not yet stated, rather than advancing a claim. "that is the rest of the note" and "(H-W is doing real work)" are pure structure/forward-pointing commentary; "the termination hypotheses below are built for" is framing wrapped around the one substantive clause ("they bound external input, not the registry's own fire-reachable states"); the intro's "closes the arc" / "a fact about forward-chaining systems generally" is essay framing. This is exactly the accretion the `review-mode.anti-bloat` classifier targets — a reader skips it to reach the argument.

**Required**: Trim to the content. Keep RG's "the hypotheses bound external input" and drop "It is this open reading … built for"; delete Q1's "that is the rest of the note" and Q4's parenthetical (Q4's own sentence already makes the locality-insufficiency point); reduce the intro framing to the usable preview (the extinction/work/fairness hypothesis families) without the "closes the arc" / general-CS-fact essay.

### Issue 2: Reassurance meta-prose in Q0's view-rebuild
**ASN-0133, Q0**: "recovering their *audit* and *active* values, the rebuild equations being PC3's (ASN-0129), **cited here rather than re-derived**." and "the filter being precisely UV's own default-view rewrite (ASN-0129) recast as a PL term, **not a fresh construction**."

**Problem**: "cited here rather than re-derived" and "not a fresh construction" tell the reader about the author's choices, not about the rewrite. The bare citations ("PC3's (ASN-0129)", "UV's own default-view rewrite (ASN-0129)") already carry the load; the reassurance clauses add nothing a precise reader uses.

**Required**: Strike both clauses; the parenthetical citations stand on their own.

### Issue 3: Q-EXT previews Open Question 1
**ASN-0133, Q-EXT**: "The check is registration-time and spelling-level — **exactly the SF certificate Open Question 1 calls for; with it, 'every rule in this registry is at-most-once' becomes a structural lint for Marker-pattern registries.**"

**Problem**: The substantive claim — SF membership is a registration-time, spelling-level check — is sound and belongs here. The tail forward-references OQ1 and previews its "structural lint" framing, which OQ1 then states in full ("make SF membership the load-bearing *uncertified* registration check … closing the loop where 'this registry terminates on bounded input' is a structural lint"). The current-capability claim (spelling-checkable) and the future-work question (ship a `pd_extinct` class) are distinct; conflating them in a forward pointer duplicates OQ1.

**Required**: End Q-EXT at the capability claim ("The check is registration-time and spelling-level"). Let OQ1 raise the certificate-class question and the lint payoff once.

## OUT_OF_SCOPE

None beyond what the note already defers. "What this note doesn't cover" (scheduler construction, multi-step-fire serialization, stochastic bodies, activation binding, environment model) and the five Open Questions correctly route the future territory — including the SF-certificate class, the PL surrogate for H-W, and per-scope vs. global termination.

VERDICT: REVISE
