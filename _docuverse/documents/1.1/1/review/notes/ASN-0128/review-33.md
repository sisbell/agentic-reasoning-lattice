# Review of ASN-0128

The technical core held up under scrutiny: I probed the I0 single-span-identity argument (T1-least start, endpoint comparison, TA-LC), the I0a minimal-elements proof both directions, I1a's induction including the K ~ R wrapper instantiation, the I6 wp's sufficiency and necessity per branch, the DR proof (monotonicity + freshness + R0a antichain, with the RP-c reachability step), the wrapper hit branch's Residence/Nullification/Scope bullets, the off-discipline bypass witness, BH2's termination bound and self-loop verdict, BH4's batch admission argument, and the D2/D3 bridge equalities — all sound, with transfer chains (B2/B3, RP-a/b/c) cited at the right granularity. The example section exercises the load-bearing postconditions concretely, including the separating-pair suppression and the born-nullified case. The remaining findings are all in the anti-bloat category this note carries.

## REVISE

### Issue 1: BH1's Effect and S1 state the same doctrine twice
**ASN-0128, BH1 (read-filter), Effect / S1 (Retired)**: BH1's Effect ends "routing default presentation away from the marked entity's internal parts while destroying none of them"; S1 then says "Retiring a document-level address thus retires its entire subtree from default presentation: the container-level mark scopes over the contained parts, which persist and remain reachable under the `active` selector — exactly Nelson's lifecycle semantics, a mark routing readers away from the whole marked entity, internal passages included, while destroying nothing."
**Problem**: Two paragraphs say the same thing in different words. The subtree-scope claim ("the marked address *and every extension of it*" appears verbatim in both), the document-level-mark-filters-the-whole-subtree reading, the Nelson container-level-metalink grounding, and the near-identical "routing … away … while destroying none/nothing" closing clause are each stated once in BH1's Effect and again in S1. S1's only registration-specific content is the record itself, the active-subsets-untouched clause, and `active`-selector reachability.
**Required**: Keep the doctrine once, in BH1's Effect, where the coverage-scoped exclusion is defined and the LM 4/23 evidence sits. Reduce S1 to the registration-specific content — record, "active subsets are untouched — nothing is nullified," and reachability under the `active` selector — with a bare citation to BH1's Effect for scope.

### Issue 2: DR's roadmap sentence pre-announces what the next page states in place
**ASN-0128, DR (DisciplineRestoration — proof and wrapper wp)**: "Necessity holds at every reachable state, disciplined or not; sufficiency holds only on the disciplined domain, and only its hit branch needs it — the miss branch's contract is ASN-0126's, discipline-independent, while the hit branch consumes the discipline at its Residence bullet, and off the discipline the unqualified equivalence is false outright, by the unit-depth bypass at this section's close."
**Problem**: Every clause of this sentence is restated where the work is actually done: the labeled *Necessity, at every reachable state* and *Sufficiency, on the disciplined domain* passages immediately follow; the hit-branch-consumes-discipline point recurs in the closing wrap-up ("the one branch that consumes the discipline (its Residence bullet)"); the off-discipline falsity recurs at the section close ("the silent no-op is the witness that the display's SD qualifier cannot be dropped"). The domain split is thereby stated three times within one claim. The preceding sentence ("its two halves hold on different domains — the qualifier scopes sufficiency alone") already fixes how the display's qualifier reads, which is the only interpretive content needed before the labeled passages.
**Required**: Delete the roadmap sentence. Retain the one interpretive sentence on the qualifier's scope; let the labeled Necessity/Sufficiency passages and the section's closing bypass carry the split.

### Issue 3: R-VAL and R-C1 trade bookkeeping citations instead of content
**ASN-0128, R-VAL (ConstructionValidation) / R-C1 (DesignationNonCollision)**: R-VAL: "— `O(|registry|²)` decidable tests, each on the representative endsets directly (R-C1)". R-C1: "This is not a check beyond R-VAL's: the shipped representatives are registry entries, so C0's pairwise key-uniqueness sweep — already counted in R-VAL's `O(|registry|²)` tests — includes the three shipped pairs, and R-C1 names that instance."
**Problem**: Mutual accounting that advances neither claim. R-VAL's parenthetical forward-cites a claim defined two sections downstream and adds nothing to R-VAL's procedure; R-C1's middle sentence explains which claim's test "already counts" the check — accounting about the document's own structure, reading as residue of a prior fold rather than specification content. R-C1's load-bearing content is two facts: the three designated classes are pairwise non-`~`-equivalent, and a colliding parameterization fails construction exactly as a colliding app declaration does.
**Required**: Drop the "(R-C1)" parenthetical from R-VAL and the "not a check beyond / already counted / names that instance" sentence from R-C1. R-C1 states the constraint and its failure semantics, with a bare citation to C0/R-VAL for enforcement.

## OUT_OF_SCOPE

### Topic 1: Caller-side discrimination of rejection causes
The surface fixes rejection uniformly as "no step, no address" (I1, I5, I6, S3), so a caller cannot distinguish a gate failure from an invalid home from a P-tgt failure.
**Why out of scope**: The note deliberately makes the operation partial rather than total-with-error-values; a diagnostic or error-signaling surface is API territory for a successor, not an error in this contract.

### Topic 2: Concurrency semantics beyond serialization
I4 reads races through a serializing authority ahead of the sequential `→_sh`, which is correct for what the substrate commits.
**Why out of scope**: A genuine concurrency model — commit protocols, visibility, multi-writer interleaving guarantees — is new machinery the inherited sequential relation does not carry; I4 correctly declines to invent it inline.

META: not warranted — the note defines operations on state, invariants, and weakest preconditions throughout, squarely within specification territory.

VERDICT: REVISE
