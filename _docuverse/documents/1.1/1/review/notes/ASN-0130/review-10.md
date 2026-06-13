# Review of ASN-0130

I checked the formal core hard and found no correctness defects. Specifically verified: PR-ENC-uniq (start-anchored identity from prefix-freeness); PR-SIG's registration-order induction grounding `sig` and WT-ref; PR0's two-direction wp, both scoped to the discipline at the flagged points; PR1's per-step content induction (K.σ/K.λ_sh frame `C`, K.α fresh-extends); PR2(a) and the (b) self-reference exclusion (miss ⇒ no active tuple denoting D's own start ⇒ (iv) unwitnessed, by induction never deposited); PR3a's substitution induction, including the WT-α/WT-W lifting and the `k`-fold PC2 discharge with the freshness provisos discharged; and PR5/PR5a's open-expansion certification — substituting `args` turns each bound-constant parameter into a state-independent literal, so the symbolic ST-derivation lifts to every instantiation and the soundness is exact. Boundary cases (`k=0`, reference-free bodies, de-registration leaving `sig`/`expand`/certificates standing, the frontier-ghost adversary at step 5, born-nullified vs. surface-discipline via DR) are all covered.

The note carries `review-mode.anti-bloat`. Every finding below is of that kind — prose that restates, previews, or justifies rather than advancing the argument. None challenges a result.

## REVISE

### Issue 1: PR-VIEW carries a historical essay and narrates itself
**ASN-0130, PR-VIEW**: "a deliberate pair, and a semantic commitment this paragraph states rather than leaves implicit" … "This is the published-artifact semantics Xanadu's read side already exhibits … in udanax-green every link query carries its own scope, each specset naming its own document or version per call, historical versions queryable on the same footing as current ones, with no backend-held 'current' substituted for the caller's choice — and link filtering is likewise front-end work, the reader's sieve."
**Problem**: PR-VIEW's formal content is the syntactic view-independence class and the result that such terms denote view-invariantly. The udanax-green passage is design justification by historical precedent and bears on none of the proof; a precise reader tracking the claim skips it. "a semantic commitment this paragraph states rather than leaves implicit" is the paragraph describing its own rhetorical posture.
**Required**: cut the self-referential framing outright. The udanax-green analogy is grounding, not meta-prose, so move it to a motivation slot rather than deleting it — but it should not sit inside the formal statement. Keep the operative pair (signed terms record no view; `evaluate` supplies it), the view-independence definition, and the invariance result.

### Issue 2: "What this note commits" re-derives instead of committing
**ASN-0130, What this note commits**: e.g. "**Validation permanence** (PR1): a pdef tuple's existence is a permanent proof that its run validated — the content store is framed or fresh-extended at every step of the substrate relation, so by induction along any derivation the run's values never drift and the validation can never go stale. No runtime re-validation path exists or is needed."
**Problem**: the commitment is the first clause; the rest is PR1's proof sketch, which PR1's body then gives in full. The same doubling runs through the PR0 bullet ("exactly the R-VAL/P-tgt pattern"), the PR1 bullet ("the strand model's S0/S1 guarantee, re-derived per step"), and the PR2/PR3/PR5 bullets — the section and the formal bodies say the same things twice.
**Required**: trim each bullet to the commitment it states, dropping the embedded derivation and the pattern-name citations. The bodies own the reasoning.

### Issue 3: PR-ENC previews PR-SIG's stratification argument
**ASN-0130, PR-ENC**: "The domain is deliberately syntax only … folding it into 'valid encoding' would make validity store-relative and circular (PR-SIG stratifies it onto registration order instead)."
**Problem**: PR-SIG then carries the full version of the same point — the type layer cannot be content-intrinsic, with the mutual-reference-loop example ("a loop with no ground, where a least-fixed-point reading calls both invalid, a greatest calls both valid"). Two sections argue the same circularity.
**Required**: PR-ENC should state that the domain is syntax-only and point forward (typing is stratified onto registration order, PR-SIG), without re-running the circularity argument. Let PR-SIG own it.

### Issue 4: scattered defensive and forward-deferring asides
**ASN-0130, PR5 / PR4 / PR0**:
- PR5: "(further certificate classes may ship as the checker matures; the conservative one is the protocol-critical one)" — duplicates Open Question 4 ("Certificate classes beyond ST"), which already owns this.
- PR4: "which for protocol definitions is precisely the right politics: the substrate records who claims to supersede what; choosing whose protocol update to follow is the consumer's act." — editorial gloss; the technical content (`tip` resolves, branch → ⊥, consumer chooses) stands without "the right politics."
- PR0, *Discipline and uniqueness*: "both uses are flagged where they occur" — bookkeeping that adds nothing once the inline "first use of the discipline" / "the second use" already label the two points.

**Problem**: each defers to, or restates, content that another location carries, or comments on the prose's own structure. This is the accretion the classifier names.
**Required**: cut all three.

## OUT_OF_SCOPE

### The deferred design forks are correctly left open
The "What this note doesn't cover" deferrals (concrete encoding bytes, activation/triggers, certifier algorithm) and Open Questions 1–4 are appropriately out of corpus. In particular, Open Question 3 (dangling *live* references — whether a `pdef` retraction should be blocked while live referents exist, checked transitively at evaluation, or only at registration) is a genuine policy fork; the note rightly records it as open rather than forcing a choice, since PR1/PR3 already make evaluation robust to it either way. No action needed.

VERDICT: REVISE
