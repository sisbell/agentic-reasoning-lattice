# Review of ASN-0036

This is a mature, largely sound note — I checked the derivations for S1, S4, S5, S7, ShiftPreservation, OrdAddHom/OrdAddS8a/OrdShiftHom, the S8 partition proof (within- and across-subspace uniqueness), and D-CTG-depth/D-SEQ, and found no mathematical errors. The worked example correctly exhibits a length-5 run consistent with the singleton existence theorem. The findings below are the accretion patterns the `review-mode.anti-bloat` classifier calls for, plus one lemma with no consumer.

## REVISE

### Issue 1: ShiftPreservation is fully proved but has no proof-level consumer in this ASN
**ASN-0036, "Structural attribution" / Properties table**: ShiftPreservation establishes conclusions (i)–(iv) via a multi-paragraph proof, listed as a lemma "from S7b, S7c, T0, T4, T4b, T10a.4, OrdinalShift, TumblerAdd, NAT-…".
**Problem**: No claim in this ASN depends on it. S7's proof does not use it; the S8 contract's *Depends* does not list it; the correspondence-run existence proof uses singletons (`nⱼ = 1`) and therefore never invokes `shift(a, k)` on an I-address for `k ≥ 1`. Its only invocation is the worked-example annotation ("the field-structure preservation supplied by ShiftPreservation, conclusion (i)"). A heavy proved lemma justified solely by a worked-example check is exactly the accretion the anti-bloat pass targets.
**Required**: Either identify a claim in this ASN that is load-bearing on ShiftPreservation and cite it in that claim's *Depends*, or remove the lemma (the worked example can assert the field-structure preservation directly from TumblerAdd's prefix rule, which it already spells out inline).

### Issue 2: Abstract restatement duplicates the concrete "Violation" example
**ASN-0036, D-CTG section (closing paragraph) and "Concrete example" (Violation note)**: The closing paragraph states "removing a single interior V-position … leaves the positions on either side no longer contiguous. D-CTG is therefore preserved only by those modifications that constitute well-formed editing operations … (e.g., by shifting subsequent positions)." The Violation note then says the same: "removing a single interior V-position is not a well-formed editing operation on its own; a well-formed deletion must also shift subsequent positions to restore contiguity."
**Problem**: Two paragraphs in the same document say the same thing in different words. Concrete examples are legitimate even in the wrong slot; the abstract restatement is the redundant copy. The Open Question "Does each well-formed editing operation preserve D-CTG and D-MIN?" covers the same idea a third time.
**Required**: Cut the abstract closing paragraph; the concrete example carries the point and the Open Question records the deferral.

### Issue 3: Motivational meta-prose in a structural slot (OrdAddHom lead-in)
**ASN-0036, lead-in to OrdAddHom**: "We now establish that the decomposition is structure-preserving … This is the property that makes the definitions more than naming conventions — it connects V-position arithmetic to TA7a's closure guarantees on S."
**Problem**: This is essay/justification for why the lemma matters rather than content that advances the argument — the precise reader must skip it to reach the claim. The lemma statement and proof already establish the homomorphism; the "makes the definitions more than naming conventions" framing adds nothing checkable.
**Required**: Reduce to the lemma statement, or a single clause naming what is proved ("ord and ⊕ commute").

### Issue 4: Derivation prose and contracts state the same postconditions twice (self-flagged)
**ASN-0036, ValidInsertionPosition section**: The paragraph beginning "By D-MIN, min(V_1(d)) = …" derives depth preservation, subspace identity, S8a consistency, and distinctness of the `N+1` positions, then closes: "These facts are restated in the contracts below."
**Problem**: The phrase is an explicit admission that the prose and the formal contract (postconditions (a)–(d)) carry identical content. The distinctness argument (last components `1+j` differ ⇒ T3) is the one step worth keeping in prose; the rest is verbatim with the contract.
**Required**: Keep the distinctness derivation in prose; let the contract carry (a), (b), (d) without the prose pre-statement, and drop the "restated in the contracts below" tell.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN/S2 and subspace alignment
**Why out of scope**: Whether INSERT/DELETE/REARRANGE preserve the contiguity invariants and `subspace(v) = subspace_I(M(d)(v))` is operation-specific frame/postcondition territory, correctly deferred to the Open Questions and the operations layer rather than resolved here.

### Topic 2: Subtraction homomorphism and round-trip for ord
**Why out of scope**: `ord(v ⊖ w) = ord(v) ⊖ w_ord` and the round-trip conditions depend on TA7a's conditional S-membership for subtraction; deferring them to a future note is appropriate.

VERDICT: REVISE
