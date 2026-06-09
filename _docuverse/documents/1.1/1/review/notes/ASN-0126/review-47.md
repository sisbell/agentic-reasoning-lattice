# Review of ASN-0126

## REVISE

### Issue 1: Gate-vs-landing separation elaborated in two places
**ASN-0126, The shape-gated emit + Worked illustration**: "This weakest precondition is *strictly stronger* than `K.λ_sh`'s own precondition — and the gap is exactly the two inherited ASN-0086 landing conjuncts… the born-nullified case (demonstrated in Worked illustration)."
**Problem**: The wp formula already exhibits the gap directly — `g_sh` has two conjuncts, the full wp has five. The paragraph that re-narrates "these two are not enablement conditions but *landing* conditions" restates what the formula shows, and then defers to the Worked illustration, which demonstrates the *same* separation a third time. This is the "multiple paragraphs defer to the same downstream location" pattern: the reader must skip meta-prose to reach the formula and then read the same point twice more.
**Required**: Keep the wp formula and one pointer to the Worked illustration. Delete the enablement-vs-landing re-narration paragraph; the formula and the worked witness carry it.

### Issue 2: P6 recapitulates its own derivation verbatim
**ASN-0126, Properties established (P6)**: "the stored value `(F, G, K)` persists unchanged by L12… K's registration status persists by P1… and the conformance verdict persists by P4… Value by L12, registration by P1, verdict by P4 — the three together preserve the hypothesis."
**Problem**: The final sentence ("Value by L12, registration by P1, verdict by P4") is a compressed restatement of the three clauses immediately preceding it — two sentences saying the same thing.
**Required**: Drop the trailing recap sentence.

### Issue 3: C0 finiteness justified by analogy rather than stated
**ASN-0126, Registration entries**: "The finiteness conjunct `|Σ_init.registry| < ∞` parallels L-fin (LinkStoreFiniteness, ASN-0043): like the link store, the catalog of registered types is a finite object."
**Problem**: This sentence advances no reasoning — it is "why C0 looks like a prior invariant" meta-prose. The substantive content (finiteness ⟹ gate-check terminates) is in the following sentence and stands on its own.
**Required**: Delete the L-fin parallel sentence; keep the decidability/termination argument that actually uses finiteness.

### Issue 4: Registration entries states the `~`-respecting fact twice
**ASN-0126, Registration entries**: "Two coverage-equal endsets therefore cannot carry different shapes." … then later: "Because lookup is by coverage class, `shape` and `Sh-conf` respect `~`: for `K ~ K'`, `shape(K) = shape(K')`…"
**Problem**: Both sentences assert that coverage-equal endsets receive the same shape — the second is the first restated with the predicate spelled out. Two paragraphs in one section saying the same thing.
**Required**: Merge into a single statement (the second, fuller form), removing the earlier sentence.

### Issue 5: Single-source carries repeated scope-disclaimer prose
**ASN-0126, Single-source**: "This is a commitment about what the framework admits, not about the link store underneath… The substrate narrows away only the multi-span, discontiguous from-set that the full link store (ASN-0043) would permit; it does not narrow what one span may reach…"
**Problem**: The "commitment-about-framework-not-link-store" framing is asserted, then immediately re-asserted in the next sentence, and echoed again at the section's close ("An app needing multi-source relations drops to a *different* substrate"). The single load-bearing claim — `|F| = 1` for `→_sh`-gated emits, multi-span F lives in ungated `→` — survives one statement.
**Required**: State `|F| = 1` and the ungated-`→` escape once; remove the duplicated scope disclaimers.

## OUT_OF_SCOPE

### Topic 1: Idem semantics, behavior catalog, default predicates, standard registrations
**Why out of scope**: The Open questions section correctly defers operational semantics, predicate composition, and pre-registered types to a successor note. These are new territory, not gaps in this framework's structural commitments.

### Topic 2: Richer arity / multi-source path
**Why out of scope**: Extension beyond F=1 and N=3 (Open question 6) is a separate framework; this note's job is to define the narrowed shape, not the loosening.

VERDICT: REVISE
