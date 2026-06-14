Reviewing the digest against the note, its formal claims, and the Q11–Q20 evidence.

This is a strong digest — accurate on every forced/corollary classification (F1, F4, F7 forced; F2/F3/F5/F6/F8 as corollaries), faithful to the de-bundling boundary, and grounded in evidence throughout with no fabricated source claims. I found no material problem. Two sharpenings below, then strengths.

## Revision list

**1. [SHARPENING] Design commitments, resolution-de-bundling bullet — tighten the "orphaned or ghost → drops to empty (Q15, Q19)" attribution.** The drop-to-empty behavior is the content-deleted (*ghost*) case, grounded in Q15/EC-GHOST-LINK. Q19's *headline* finding is the opposite — the reference **succeeds** reading the recorded end with no document handle/BERT (the very no-lock/no-handle and F8 evidence the digest rightly uses in the Link-lookup approach) — and Q19's code reading uses "orphaned" for a *spanfilade-index-missing* link whose content is still live, for which the reference returns the **resolved endpoints, not empty**. Do: scope "drops to empty" to the ghost/content-deleted case and cite Q15 (+EC-GHOST-LINK); reserve Q19 for the succeeds-without-handle point; drop or disambiguate "orphaned" (you mean *content-undiscoverable*). The companion clause — "resolves the same recorded end differently against different queried documents (Q11)" — is correct and is the orphan-relevant divergence; keep it. (Note the digest already correctly separates this from "the F7 empty-*recorded*-endset bug," which is the right distinction.)

**2. [SHARPENING] How it fits, RETRIEVEENDSETS sentence — disambiguate "shares with FOLLOWLINK only the endset→span-set conversion."** Here "endset→span-set conversion" denotes the reference's I→V *resolution* step (`linksporglset2specset`), which collides with the digest's own term "endset→span-set **emitter**" for the in-scope verbatim operation — and which the Emitter section explicitly says to **skip**. Do: name the shared step the reference's I→V conversion/resolution (`linksporglset2specset`) and note it is the resolution step abstract FOLLOWLINK omits — so a builder does not read "shared" as "reusable for the recorded-end emitter."

## Genuinely solid sections

- **The Q13 split is sharper than the note.** Correctly treating the raw-I-span path as the in-scope F3 representation example and the V-spec path as out-of-scope **resolution** (different coordinate space, can drop per Q15, hence not an F1-satisfying span-set over `T`) is right — and it quietly corrects the note's looser "Representation is free" passage, which uses the V-spec path as an F3 example. Good skepticism.
- **The domain-guard / F7 section** (lower-bound + address syntax boundary-checkable, upper bound necessarily post-lookup once arity is unfrozen; derive emptiness in the core against the endset; copy RETRIEVEENDSETS's empty-handling, not the followlink path's) is exactly the load-bearing engineering and is correctly grounded in Q12/Q17.
- **The monotonicity-≠-lock-free-safety caveat** (needs atomic publication, a representation choice belonging to ASN-0093, not a logical consequence of monotonicity) is a correct, well-placed concurrency point at the right altitude.
- The digest **does not inherit the note's loosest synthesis claim** — it never asserts the reference's bundled followlink satisfies F1/F5; it shows the opposite (resolution shrinks and is document-dependent), which is the more accurate reading.

Neither sharpening is load-bearing: the build instructions (verbatim recorded-end emit, post-lookup bounds, variant-typed result with explicit wire discriminant, no resolution/handle/lock) are sound and correct as written.

VERDICT: CONVERGED
