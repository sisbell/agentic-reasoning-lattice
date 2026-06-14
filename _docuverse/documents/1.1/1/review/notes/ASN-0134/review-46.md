# Review of ASN-0134

This is a rigorous note. The core frontier lemmas (H0–H2) carry full case analysis including the first-emission boundary (H2); the worked scenario (§7) is concrete and the addresses check out; the V2 strictness demonstration (§8) supplies explicit witnesses for each non-implication. The proofs I checked are sound. The note is also a legitimate consistency/isolation model — MIC is a guarantee-level contract, not a mechanism — so it belongs in the spec; no META.

Given the `review-mode.anti-bloat` classifier, most of what follows is accretion/placement. One item is a genuine correctness/consistency gap.

## REVISE

### Issue 1: Content-run prefixes are claimed "readable," but the formalized read surface exposes no content read

**ASN-0134, §1 (A5 and the atomicity-vs-contiguity paragraph)**: A5 — "an `Observe` at an interior index `k` ... witnesses a strict, non-empty *prefix* of the batch's own effects" — with a content run ("one `K.α` per atom") given as an example batch; and §1: "even a perfectly contiguous content run leaves every interior index `Σ_{i₁+1}, …, Σ_{i₁+m−1}` readable as a strict prefix (A5)."

**Problem**: §8 formalizes the read surface as *bounded-access constituents* — active-view reads (`Observe_K`, over typed relations `L_K` in the link store) and *frontier descents*, and V0 pins the latter to "the home `d`'s **link-subspace** frontier `f_d^Σ`" (the `age`/`stale` reads, BH4, link-tuple-only). Nothing in that surface reads content population `φ_{s_C}(d)` or `dom(C)` membership. So a content run's effects are *not* witnessable by any read the note models: `Observe_K` reads the link store, and the only frontier descents named are link-frontier. The §1 readability claim therefore asserts a capability the §8 surface does not provide — and §1's own conclusion that "contiguity does **not** construct atomicity" (because interior content states are "readable") rests on it. The `retract_stale` example (a link-store batch) *is* `Observe_K`-witnessable and carries A5's partial-visibility claim cleanly; the content run does not.

**Required**: Reconcile §1 with §8's read vocabulary. Either (a) qualify A5/§1 so the read-witnessed partial-visibility is exhibited by link-store batches, with content runs non-atomic only structurally (the mid-batch state exists and is canonical, A6) and their prefix exposed by no modeled read; or (b) if content population is meant to be readable, name a content-frontier descent in §8 parallel to the link-frontier one and extend V0/clause 4 to cover it. As written the note over-claims content-run readability against its own surface.

### Issue 2: The `K.σ` shared-frontier conditional is over-introduced and over-repeated

**ASN-0134, §4 (the four paragraphs before H0), H3, MIC clause 2, SAFE(c), claims table**: the qualifier "on a shared-frontier realization ... vacuous on a collision-free scheme" (and its expansion via `A_doc`/`max_child+1`) recurs at every site that mentions `K.σ`.

**Problem**: This is the accretion pattern the anti-bloat mode targets. (a) *Placement*: §4 opens with ~4 dense paragraphs of registration scoping rationale ("bare freshness-by-test," "Nor is the deficit closed by importing `A_doc` directly," "What attaches ... unconditionally," "The rejection path sharpens the conditional") *before* H0 — the section's actual lever. The core conflict lemmas H0–H2 are buried behind a digression about a secondary case (`K.σ`), and the reader must skip past it to reach the frontier theory the section is named for. (b) *Repetition*: the same conditional is then restated in the H3 statement, the H3 proof, clause 2 ("binding on a shared-frontier realization, vacuous on a collision-free one"), SAFE(c), and both the H3 and G1 table rows. The conditional is genuine and worth stating once; stating it six times is noise.

**Required**: State the realization conditional once (introducing H3), and reference it elsewhere rather than re-hedging. Move the registration treatment to *after* H0–H2 (it is an application of the per-home discipline at the account tier, so it reads naturally as a corollary of H1/H2 + H3, not as a precondition for stating them). The pre-H0 preamble should shrink to the one load-bearing fact — the committed stack carries no document-allocator-conformance invariant, so the account-tier obligation is conditional — and defer the rest to H3.

### Issue 3: G1(i) re-derives the §5 contiguity-vs-uniqueness partition inline

**ASN-0134, §4 G1(i), §5 W3, §5 collecting paragraph**: the claim "serialization buys same-home uniqueness, not contiguity" appears three times — G1(i) ("Contiguity rides the step-local route for free; only collision-freedom is bought by serialization"), W3 ("What per-home serialization buys is thus not contiguity but same-home uniqueness (H2)"), and the §5 collecting paragraph ("Cross-home ... uniqueness is model-intrinsic ... Same-home `(d,S)` uniqueness is serialization-borne").

**Problem**: Two paragraphs (here three) saying the same thing in different words. §5 is the dedicated partition section and W3 is the contiguity claim; G1(i)'s inline re-derivation of the partition ("What the per-home frontier argument *separately* secures ... Contiguity rides the step-local route for free ...") duplicates it. Since G1 forward-references W3 already, the re-derivation adds nothing.

**Required**: In G1(i), once reachability is in hand, cite A6 for the per-state package and W3/§5 for the "contiguity free, uniqueness bought" split rather than re-arguing it. Keep the derivation in §5.

### Issue 4: Smaller repetitions to collapse

**ASN-0134, several sites**:
- **A6's "representative members" list** — A6 says "We do not enumerate the package, because the argument does not turn on the roster," then enumerates five representative members with parentheticals. The disclaimer-then-list is self-undercutting; if the reachability argument is what carries A6, the list is a use-site inventory that can be cut to one example or dropped (the conjuncts §2 actually invokes — `SD`/`L0`, `P6`, contiguity, registry-fixity — are cited again at their use sites in §2 anyway).
- **"states that never coexisted"** recurs as a set phrase across §8 (V0 reasoning, the V2 trace conclusion, the second-converse witness) and SAFE(d). Once is vivid; four times is a tic.
- **§9 wp closing** — "The reader who wants the one-sentence form of this entire note can take it from the `wp`: **the only thing a concurrent writer must wait for is another writer reaching into the very same sub-allocator; everything else is free.**" — this restates H1 + clause 2 rhetorically. The `wp` itself already says it; the gloss plus the "Nelson's owned-numbers tree and Gregory's run-to-completion loop, reconciled" flourish is essay content in a structural slot.

**Required**: Cut the A6 list to a single illustrative member or none; reduce the "states that never coexisted" repetitions to the one at the V2 trace where it is earned; trim the §9 wp gloss to the `wp` statement and at most one sentence.

## OUT_OF_SCOPE

Nothing to add. The note's own scope hygiene is sound — the scheduler, rule bodies, BEBE/replication, concrete mechanism, and predicate-evaluation cost are correctly deferred (Open Questions + "What this note does not cover"), and the per-home thesis's residual gaps (operation-level families in §4, durability in V1, multi-step reader-atomicity in OQ4) are honestly surfaced rather than papered over.

VERDICT: REVISE
