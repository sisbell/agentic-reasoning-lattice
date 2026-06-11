# Review of ASN-0128

I checked every proof obligation: I0's case analysis (the single-span-identity argument via T1-least element and TA-LC is complete), I0a's two inclusions, I1a's induction (all four step kinds, the K ~ R wrapper case, born-nullified deposits, no post-hoc class change), I6's wp in both directions including the rejection cases and the idem-⊥ corollary, DR's C3-emptiness derivation (distinctness via freshness, antichain via R0a at the post-state — the "step fires regardless of C3" move is what makes the antichain instantiation legitimate, and it is correctly justified by RP-c), DR's hit branch (the self-emit-cannot-hit argument via subtree-root uniqueness and L12a is sound), BH2's termination bound, BH4's totality of `age` via L-ContiguousPrefix uniqueness, the D2/D3 bridge at F-denoting states (the coverage-keyed/denotation-keyed equality holds — every denoted source is a `members` element, so the two unions coincide), and the retract_stale batch argument (P0 persistence, P-tgt via L12a, the dedup case split). The transfer apparatus (RP, RP-a/b/c) correctly mirrors ASN-0126's bridge structure, and every cross-system citation I traced uses the right clause (RP-a for single-state, RP-b for successor-quantified, RP-c for step existence — including the correct observation that RangeSterilization needs RP-b, not RP-a). The example section exercises hit suppression, born-nullified deposits, branch verdicts, and the batch contract against concrete scenarios. I found no technical fault.

The note carries the anti-bloat classifier, and one accretion pattern survives the last cycle's tightening.

## REVISE

### Issue 1: The hit-suppression consequence is narrated in three places, two of them forward deferrals to the third

**ASN-0128, I0 (closing), I0a (closing), I1 (hit clause)**:

- I0 ends: "We reject the finer criterion on that ground; the cost side of coverage-keying — what a hit suppresses — is priced in I1's hit clause."
- I0a ends: "…so what a hit can suppress is exactly the absorbed, non-minimal listings of a redundant presentation (I1)."
- I1's hit clause then delivers the account: "the suppressed call's decomposition is then never stored. Every enumeration predicate thereafter reflects the incumbent tuple's denoted sets… and the loss is avoidable at the source…"

**Problem**: This is the flagged pattern — multiple paragraphs in different sections deferring to the same downstream location. I0's deferral clause adds nothing to I0's own commitment (the criterion choice and its ground are complete without it). I0a's closing clause is worse: it states I1's content in different words ("what a hit can suppress is exactly the absorbed, non-minimal listings" is the irredundant-presentation point I1 makes in full), and nothing in I1 consumes that clause — I1's avoidability argument cites I0a's *lemma* (the minimal-elements identity), not its trailing consequence. The reader hits the suppression story as a promissory note twice before reaching the one place it is actually kept. The example's fourth telling is fine — it instantiates I1 concretely, which is what examples are for.

**Required**: Consolidate in I1's hit clause, which is the natural carrier (suppression is a hit-branch phenomenon). End I0 at "We reject the finer criterion on that ground." End I0a at "An address-denoting endset's coverage thus determines and is determined by its ≼-minimal denoted addresses." Delete both trailing deferral clauses; change nothing in I1.

## OUT_OF_SCOPE

### Topic 1: The serializing authority behind I4
**Why out of scope**: I4 correctly states that `→_sh` has no concurrency semantics and that some authority orders racing calls before either becomes a step, but the authority itself — its granularity (per-home? global?), its fairness, its failure modes — is transport/implementation territory. The note's first-to-commit analysis is complete *given* serialization; specifying the serializer is a future ASN, not a gap here.

### Topic 2: Name-to-representative binding for the operation surface
**Why out of scope**: Standard registrations notes that "the operation surface exposes the representatives under exactly these names," and app types presumably arrive with names too. How surface names resolve to stored representatives — namespace collisions between apps, name stability across the OQ8 merge protocol — is a distinct surface-layer concern. OQ8 covers key collision; name binding is adjacent new territory, not an error in this note.

VERDICT: REVISE
