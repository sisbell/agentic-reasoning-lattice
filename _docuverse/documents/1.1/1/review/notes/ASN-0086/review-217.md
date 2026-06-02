# Review of ASN-0086

## REVISE

### Issue 1: FreshLinkKeyDisjointness is unused machinery
**ASN-0086, "Sub-lemma — FreshLinkKeyDisjointness"**: "L14 (DualPrimitive) and L14a (NonTranscludability) of ASN-0043 are *not* published by ASN-0093's K.λ contract, so this note carries them across each K.λ-step itself, via this sub-lemma."

**Problem**: No argument anywhere in this note consumes L14 or L14a. The disjointness the note actually invokes — at *Definition — Partition*, *Definition — AddressUniverse*, and R4 — is SD (StoreDisjointness, ASN-0093), not L14. L14a (no V-position maps to a link) concerns arrangements `Σ.M(d)(v)`, which the note never reads — indeed it declares "Arrangement modification is out of scope." Moreover L14/L14a are not freestanding obligations this note must re-discharge: ASN-0043 derives L14 from L1d(b) and L14a from S3 + L1d(b), and those premises hold at every reachable state of any ASN-0093-conforming system, so L14/L14a hold as standing theorems without per-K.λ-step re-proof. The sub-lemma, its opening provenance sentence, and the L14/L14a mentions in R0's "L-invariant preservation" and Step 1's invariant inventory are all machinery with no downstream reader in this note. The foundation itself warns against exactly this ("Anything more would be unused machinery and unverified obligation," TA-assoc note).

**Required**: Either cite the specific place in this note where L14 or L14a is load-bearing (there is none), or delete the sub-lemma and drop L14/L14a from the R0 preservation clause and the Step 1 inventory, relying on ASN-0093's SD where disjointness is actually used.

### Issue 2: Convention RetractionDirectionality is re-explained at its consumption site
**ASN-0086, "Definition — Nullified"**: "The existential checks `coverage(G')` only — the to-set's coverage — and does not inspect `coverage(F')`, per Convention RetractionDirectionality; an `Emit_R` call whose to-span coverage misses `a` does not nullify `a`, regardless of what its from-set covers."

**Problem**: Convention — RetractionDirectionality already fixes that the to-set carries targets and the from-set is attribution. The quoted sentence restates that convention as a worked-out consequence inside the definition rather than letting the formula `a ∈ coverage(G')` speak for itself with a bare citation. The "regardless of what its from-set covers" clause adds nothing the definition's `coverage(G')`-only quantifier does not already say.

**Required**: Replace the explanatory restatement with a one-clause citation, or move the directionality reading entirely into the Convention and out of the definition body.

### Issue 3: WP Case 1 is presented as part of a "Weakest-Precondition Analysis" but is, by its own statement, not a wp
**ASN-0086, "Weakest-Precondition Analysis," Case 1**: "This conjunction is **not** the weakest precondition: `→*`-reachability holds *globally* over the whole store, while the postcondition is *local* to `a`'s prefix-subtree, so it is strictly stronger than the postcondition requires."

**Problem**: The section header and its framing paragraph ("Case 1 ... is a sufficient-precondition and load-bearingness analysis, while Case 2 ... is a genuine weakest precondition") spend prose distinguishing what Case 1 *is not*. A sufficient-condition-plus-load-bearingness argument is fine content, but the meta-prose announcing in advance that the first case fails to be a wp, then re-explaining mid-case why, is justification about the analysis rather than the analysis. The substance is the load-bearingness counterexamples; the "this is not the weakest, because global vs. local" commentary is removable.

**Required**: State Case 1 as a sufficiency + load-bearingness result for `P0 ∧ P1` and drop the framing prose contrasting it against a wp it never claimed to be.

## OUT_OF_SCOPE

### Topic 1: Elevating the unit-depth retraction discipline to a substrate guarantee
The note correctly localizes this as a layer convention and flags it in Open Questions. Whether a dedicated retraction K-operation with a unit-depth shape constraint should exist is genuinely new substrate territory, not a defect here.

### Topic 2: Concurrency/atomicity of Emit vs. Observe and ordering of Observe results
These (also in the author's Open Questions) require a concurrency model the substrate does not yet specify; correctly deferred.

VERDICT: REVISE
