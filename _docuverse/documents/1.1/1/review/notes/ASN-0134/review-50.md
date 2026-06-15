# Review of ASN-0134

This is a strong, careful note. The conflict theory (H0–H3), the confluence result (G1), the surface-emit divergence (G2), and the multi-read soundness chain (V2) are rigorous, and the boundary cases that usually get skipped are actually handled — the first-emission boundary in H2, the cross-document cross-subspace pair in H1, the both-miss interleaving in §4, the banking argument and its two strictness witnesses in V2. I found no hand-waved proof and no missed allocation boundary. My findings are concentrated where the note's `review-mode.anti-bloat` classifier points — restated conditionals, duplicated exposition, essay in structural slots — plus one precision gap in the minimality argument.

## REVISE

### Issue 1: The K.σ realization conditional is restated repeatedly after declaring it stated "once"

**ASN-0134, §4**: "The account-tier *collision* is the conditional part, and we state the realization conditional **here, once**."

**Problem**: The shared-frontier-vs-collision-free conditional (and its consequence: the account-tier obligation binds the shared-frontier family, is vacuous on the collision-free family) is then restated in at least five further places: the long "It arises exactly under realizations that compute a document address from a shared per-account frontier…" paragraph that immediately follows the "once" claim; the H3 statement and its proof; the G1-extension paragraph ("register-before-allocate always, and, *on a shared-frontier realization*, *per-account serialization*"); MIC clause 2 ("under the shared-frontier conditional (§4/H3); on a collision-free realization it is vacuous"); the "Registration adds no eighth clause" sentence; and SAFE(c). This is the "two paragraphs say the same thing in different words" pattern, made conspicuous by the literal claim to state it once.

**Required**: State the conditional once (in §4 or H3) and let the downstream slots cite it by label without re-deriving "shared-frontier ⟹ obligation; collision-free ⟹ vacuous." The MIC/SAFE pointers can be a clause reference, not a re-explanation.

### Issue 2: Clause 4 re-imports clause 1's content, and the minimality argument does not distinguish their counterexamples

**ASN-0134, §9 MIC clause 4 and the minimality paragraph**: clause 4 reads "…is evaluated against a single committed state `Σ_k` and never witnesses a partial step"; the minimality one-liners read "drop 1 and reads tear … drop 4 and a single bounded-access read … reads across a commit."

**Problem**: Clause 4's "never witnesses a partial step" *is* clause 1's "no observer reads a state strictly between `Σ_i` and `Σ_{i+1}`" (i.e. A4, itself a consequence of A0/clause 1). Clause 4's genuinely independent content is the *other* half — that a *compound* single read (an `age` frontier descent, or `Observe_K`'s internal `A_K = L_K ∖ nullified` computation) does not span two *complete committed* states, a failure clause 1 does **not** preclude. But the minimality counterexample "reads across a commit" reads as a restatement of clause 1's "reads tear," so the argument as written does not exhibit a scenario where clause 1 holds and clause 4 fails — which is exactly what "independently load-bearing" requires. The minimality claim is therefore asserted but not demonstrated for clause 4.

**Required**: Drop the redundant "never witnesses a partial step" from clause 4 (it is clause 1's), and phrase clause 4's drop-counterexample so it is plainly distinct — a compound single read whose internal accesses straddle a commit *despite* atomic transitions. This sharpens (does not lengthen) the argument.

### Issue 3: G0's serializability/SC/linearizability exposition is duplicated and longer than the result needs

**ASN-0134, §3 (G0 in-text) and the Claims Introduced table (G0 row)**: the in-text claim spends a paragraph on "the standard theorem that linearizability entails SC for *sequential* clients … pipelining severs program order from real-time order," and the table row re-states the same distinction ("coexists with §3's linearizability (real-time order only), a sequential client recovering SC by its own acknowledgment discipline plus A7").

**Problem**: The same SC-vs-linearizability reconciliation is given twice (in-text and table), and the in-text version restates textbook material (the standard implication and why it fails under pipelining). The result the note actually needs — serializable, not SC under pipelined clients, logical-not-temporal order — is short; the surrounding three-way terminology disambiguation is the bulk. This is "two paragraphs say the same thing" plus essay content. (Several other table rows — G1, SAFE — are also paragraph-length re-expositions rather than summaries.)

**Required**: Reduce the table entry to a one-line summary and trim the in-text textbook restatement to the load-bearing sentence (program order ⊄ real-time order under pipelining ⟹ linearizable but not SC).

### Issue 4: Motivational design-intent restatements occupy structural slots after technical claims

**ASN-0134, §4**: "This is not our invention; it is Nelson's 'owned numbers' made operational." and "This is exactly Nelson's distributed intent (each server 'at all times unified and operational,' progress never gated on a global agreement) rescued from the implementation's incidental global lock."

**Problem**: These advance no reasoning — they re-assert that the formal result matches design intent. They are essay in a structural slot. (The line is worth drawing: the *concrete* Gregory evidence — response-before-check, the counter-style allocator that loses contiguity, the granfilade fusion breaking text runs — is appropriate grounding and should stay. The pure "made operational"/"rescued from the incidental global lock"/"not our invention" asides are the noise.)

**Required**: Cut the motivational restatements; keep the concrete implementation evidence.

### Issue 5: Numbering gap in the W-series claims

**ASN-0134, §5–§6 and Claims Introduced**: the W-series runs W0, W3, W4, W5, W6 — no W1, W2.

**Problem**: A reader cannot tell whether W1/W2 were removed in revision (a churn artifact, relevant to the anti-bloat pass) or are referenced silently elsewhere. Every other claim family (A0–A7, H0–H3, V0–V2) is gapless.

**Required**: Renumber the W-series contiguously, or note the reservation.

## OUT_OF_SCOPE

### Topic 1: Read-isolation for content retrieval

A5 and §8 fix the read surface as link-store reads (`Observe_K`, link-subspace frontier descents) "with no read over content population," so a content run is "non-atomic only *structurally* … its prefix is witnessed by no read the note models."

**Why out of scope**: This is a correct scoping of the *current* operation surface (the foundations expose no content-retrieval operation). When a future ASN introduces one, a content run's partial visibility becomes read-witnessed and the §8 verdict analysis (which constituents exist, what is `Q`-affecting) must be re-run over content-reads — new territory, not a defect here. Worth a one-line forward note in the corpus, not a revision to this ASN.

VERDICT: REVISE
