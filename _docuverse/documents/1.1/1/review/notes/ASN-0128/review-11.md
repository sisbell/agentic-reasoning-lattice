# Review of ASN-0128

The technical core of this note holds up well under checking: I0a's two-direction proof is sound, I1a's induction covers the K ~ R case honestly, DR's antichain derivation is complete (distinctness via freshness, then R0a at the post-state), the hit-branch re-establishment of single-tuple scope at the unchanged state is correctly argued, and the batch P0 entry-evaluation analysis in BH4 correctly identifies the front-truncation hazard under interleaving. The findings below are one precision slip in a formal claim and several instances of the accretion patterns this note's classifier asks to be surfaced.

## REVISE

### Issue 1: I6's necessity claim attaches to the wrong syntactic unit
**ASN-0128, Idem operational semantics, I6 (The wp, assembled)**: "Each disjunct is necessary as well as sufficient: a rejected call returns no address (gate failure, or miss with invalid `d`), and an admitted miss failing C2 or C3 deposits born nullified with no I0-equal active tuple anywhere at the post-state…"
**Problem**: As stated, this is false. Neither disjunct of `hit(Σ, F, G) ∨ (d ∈ dom(Σ.M) ∧ C2 ∧ C3)` is individually necessary: at a state where both disjuncts hold, either may be dropped and POST is still attained. Necessity belongs to the *disjunction* (equivalently, to the whole displayed formula). Per-conjunct necessity is the right notion for DR's conjunctive wp — and DR states it correctly ("necessity holds per precondition") — but it does not transfer to I6's disjunctive shape. The case analysis that follows the sentence actually proves the right thing (every state falsifying the formula falsifies POST); only the framing sentence misstates what is being proved.
**Required**: Restate as necessity-and-sufficiency of the displayed equivalence — e.g., "The formula is necessary as well as sufficient: …" — keeping the existing case analysis unchanged.

### Issue 2: S3 and DR carry duplicated organizational pointers, one justifying placement
**ASN-0128, Standard registrations, S3**: "The wrapper's full surface contract — uniform preconditions, the idem branch condition it inherits from I1, and per-branch postconditions — is stated in one place under DR below."
**ASN-0128, Standard registrations, DR**: "Since this note is the operational layer, the wrapper's full surface contract belongs here, in one place."
**Problem**: Two sentences in adjacent sections saying the same organizational thing; the second additionally justifies document placement ("belongs here") — a flagged pattern. Neither advances the contract's content; the inheritance of I1's branch condition is restated inside DR itself ("R ships `idem = ⊤` (S3) and `Nullify_Binary ≡ Emit_R`, so the wrapper inherits I1's de-duplication"), so the S3 pointer's one substantive clause is also duplicated.
**Required**: Delete both sentences. S3 may keep a bare "(DR)" citation where it relies on the contract; the contract's location needs no defense.

### Issue 3: S2 restates BH2's adjudication rationale in different words
**ASN-0128, Standard registrations, S2**: "The ⊥ cases are by design, not failure: supersession claims are owned assertions that accumulate — a rival's claim and the author's coexist — and the substrate records all of them, adjudication falling to the reader (BH2, Effect)."
**Problem**: This is BH2's Effect paragraph relocated: "Nelson's supersession is linear by *convention* only: supersession claims are owned links that accumulate, the mechanism admits branching, and adjudicating among competing claims belongs to readers, not the back end." Same content, same evidence, two sections — the "two paragraphs say the same thing in different words" pattern. S2's registration facts (Binary, idem=⊤, BH2; `tip()` resolution semantics) are what the section needs; the rationale already lives at its grounding site.
**Required**: Trim S2 to the registration facts and the `tip()`/⊥ behavior with a citation to BH2's Effect; drop the restated rationale.

### Issue 4: The BH1-interaction deferral is stated three times
**ASN-0128, BH1 (rewrite scope)**: "Whether the rewrite extends to behavior-unlocked surfaces — BH3's `sources_to`, BH2's walk through a filtered mid-chain element — is deliberately uncommitted (Open question 1)." **BH2**: "…whether it should is Open question 1." **Open question 1**: full restatement of both cases.
**Problem**: Multiple paragraphs in different sections deferring to the same downstream location — a flagged pattern. BH2's normative half ("BH1 filtering does not rewrite the walk") is a real commitment and must stay; the trailing deferral clause duplicates BH1's, and both duplicate OQ1, which is the elaboration's proper home.
**Required**: State the deferral once. Keep the normative commitments in BH1 and BH2 (rewrite scope; active-view walk), tag at most one of them "(Open question 1)", and cut the other deferral clause. OQ1 itself is fine as is.

### Issue 5: R-C0 closes with a grounding-site inventory
**ASN-0128, The registration record, R-C0**: "each clause is grounded where the behavior's machinery is defined — the shape clauses with BH1–BH3's predicates, the `idem = ⊥` clause and the absent shape clause in BH4's Compatibility paragraph."
**Problem**: This sentence enumerates where the justifications live rather than advancing the constraint — the downstream-consumer-inventory pattern. The reader who reaches BH1–BH4 finds the grounding in place; the map adds navigation, not meaning.
**Required**: Delete the sentence. R-C0's constraint table and the "enforced by failing construction (R-VAL)" clause are complete without it.

### Issue 6: The example section opens with a doubled disclaimer
**ASN-0128, An abstract registry example**: "These names are not standard registrations and not predictions of what specific apps will register; they exist only to exhibit the framework's mechanics."
**Problem**: Defensive justification, and a repeat — the preceding sentence already establishes the names are generic and illustrative ("uses generic type names … to illustrate behaviors against shapes the substrate-shipped registrations don't exhaust"). The disclaimer defends against a misreading the first sentence already forecloses.
**Required**: Delete the quoted sentence; the opening sentence carries the scoping.

## OUT_OF_SCOPE

### Topic 1: Rejection-reporting semantics at the operation surface
The note fixes that rejected calls take no step and return no address (I1, S3), but not how rejection is signaled — whether a caller can distinguish gate failure from invalid `d` from P-tgt failure, and what the surface returns in each case. retract_stale's "voided batch" similarly has no observable verdict.
**Why out of scope**: Error-surface design is new operational territory; the note's no-step/no-address commitment is sufficient for its containment and wp claims.

### Topic 2: The serializing authority presupposed by I4
I4 resolves concurrent emits by appeal to "a serializing authority [that] orders the two calls before either becomes a step," consistent with the relation's sequential model — but the authority itself (where it sits, what it guarantees beyond total ordering) is unspecified.
**Why out of scope**: Concurrency control is a runtime-topology concern outside the substrate relation; I4 correctly confines its claims to what holds after serialization.

VERDICT: REVISE
