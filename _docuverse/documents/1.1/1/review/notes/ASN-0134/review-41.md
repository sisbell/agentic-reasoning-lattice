# Review of ASN-0134

## REVISE

### Issue 1: The target-residence race is developed in three places with mutual deferrals
**ASN-0134, §4 (second family) / §5 W5 / Open Question 9**: §4's "second family" paragraph fully develops the race (the `A;B` vs `B;A` Nullify/Emit scenario, the rejection-to-zero outcome, the emit-before-retract remedy). W5 then re-states it: *"This order-sensitivity is precisely §4's target-residence race (the second family of operation-level non-confluence), removed only by the coordination layer's emit-before-retract discipline (Open Question 9)."* OQ9 restates it a third time.
**Problem**: W5's load-bearing content is slice coherence (`A_K = L_K ∖ nullified` at every state, P-tgt checked at the nullify's `lin`). The order-sensitivity paragraph inside W5 re-derives §4's race and adds a deferral to OQ9 — the "multiple paragraphs in different sections defer to the same downstream location" / "prior finding's content relocated" pattern.
**Required**: Develop the race once (§4). In W5, replace the re-derivation with a one-clause cite ("the order under which a nullify and its target's emission interleave is §4's target-residence race"). Let OQ9 stand alone.

### Issue 2: "Design intent" asides explain why a claim matters rather than advance it
**ASN-0134, A6 / W0 / V0**: e.g. *"Design intent: A6 makes formal Nelson's 'canonical order is an internal mandate of the system'…"*; *"Design intent: this is Nelson's permanence guarantee made operational…"*; *"Design intent: this is Nelson's requirement made precise — the verdict 'taken against one version of the store at one instant…'"*
**Problem**: These are labeled sub-paragraphs re-quoting Nelson to restate a claim's significance — the "new prose explains why … rather than what it says" pattern. The Nelson reconciliation is already the note's stated thesis (epigraph + intro), and these asides repeat the same three quotes ("canonical order," "one instant," "states that never coexisted") to the same effect across sections.
**Required**: Establish the design-intent framing once in the intro; drop the per-claim "Design intent" asides. (Gregory *implementation evidence* — response-before-check, `findpreviousisagr`, the granfilade-fusion caveat — is concrete and should stay; it is the Nelson *motivation* asides that have accreted.)

### Issue 3: Defensive justifications for roads not taken
**ASN-0134, §1 parenthetical / §4 opening**: §1 carries *"(We commit 𝔼 to this one substrate stack — ASN-0093's allocation model carried up through ASN-0086/0126/0128 — rather than mixing in a second foundation's arrangement-and-entity steps; …)"*; §4 opens with a paragraph explaining why `K.σ` is scoped out and that its two preconditions "are assumed preconditions, supplied by the entity-allocation layer this note excludes, exactly as G-PO below starts from…".
**Problem**: Both explain *why a scope choice was made* (not mixing a second foundation; deferring document-freshness) rather than advancing the argument. The scope *commitments* are load-bearing (G1/H3 need them); the justifications for the alternative are not.
**Required**: State the commitments tersely — "𝔼 is the ASN-0093→0128 stack; `K.σ` freshness and register-before-allocate are assumed from the entity layer" — and drop the defense of the excluded alternative.

### Issue 4: Clause 6 is a self-admitted redundant contract clause defended by surrounding prose
**ASN-0134, §9 MIC clause 6 + minimality note**: *"This is a derived directive, not an independent obligation — it follows from W6, which already establishes that no runtime step writes the registry — kept as an explicit clause only for implementer guidance (see the minimality note below)."* The minimality note then carries *"The contract is minimal modulo W6-derivable directives: seven of its eight clauses are independently load-bearing … Clause 6 is the lone derived directive…"*
**Problem**: A numbered contract clause the note itself flags as derivable (admittedly not load-bearing), plus a "minimal modulo" hedge whose sole job is to defend keeping it. This is accretion: the contract carries an item only to then argue for its presence.
**Required**: Demote registry-write confinement to a remark under W6 (or a footnote on MIC). Then "minimal" needs no "modulo W6-derivable directives" qualifier and the minimality note simplifies to the seven counterexamples.

### Issue 5: A6 enumerates its downstream consumers
**ASN-0134, A6**: *"this last conjunct is the single-state content of ASN-0126's P1 … W0 is exactly this clause read as a concurrency guarantee"* and *"which §5's W3 reads as a model-intrinsic invariant, kept by the allocator shape rather than bought by per-home serialization."*
**Problem**: A6's prose points forward to which later claims (W0, W3) consume its conjuncts — the "definition's introduction enumerates downstream consumers" pattern. W0 and W3 already cite A6 where they are stated; the back-pointer adds nothing to A6's meaning. (Minor, same family: OQ4 and OQ5 both ask for the batch-atomicity-to-a-reader contract — A5's gap — and could be merged.)
**Required**: Drop A6's forward pointers to W0/W3; consolidate OQ4/OQ5.

## OUT_OF_SCOPE

### Topic 1: Read-access-count of BH2 navigation walks (`chain`/`tip`/`succs`) under interleaving
**Why out of scope**: §8 is scoped to quiescence *verdicts* and works `Observe_K`, `age`, cross-type joins, and `stale`. A determinate walk's successive `succs`-reads could, under drift, compose a list corresponding to no single state's `chain` — the same "states that never coexisted" hazard, for a navigation result. The V0/V2 single-vs-multi-access dichotomy already subsumes it conceptually, so this is a natural extension to a later note, not a defect here.

META: not applicable — the note specifies implementation-independent guarantees (the MIC obligations, the model-intrinsic/serialization-borne partition, the snapshot/verdict semantics) and deliberately holds the mechanism (lock, scheduler, CAS) out of scope, so it remains in specification territory.

VERDICT: REVISE
