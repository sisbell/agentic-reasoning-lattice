# Review of ASN-0111

## REVISE

### Issue 1: RL-REP is downstream-interpretation essay, not a READLINK guarantee
**ASN-0111, RL-REP / "Invariants governing the returned structure"**: "This is guidance for the *reader* of the result, not a relaxation of what the read returns: by RL1 the read delivers the exact recorded span decomposition, verbatim... What RL-REP adds is how to *interpret* that decomposition. Every downstream coverage-based use of an endset — projection, type-matching — depends only on its `coverage`..."
**Problem**: This carries the anti-bloat patterns the note's classifier targets. (a) The opening sentence is defensive meta-prose — it exists to pre-empt a misreading ("not a relaxation of what the read returns") rather than advance a claim; RL1 already fixes the verbatim return, so the defense is against a case RL1 excludes. (b) The body enumerates downstream consumers (projection, type-matching) and restates LP21 of ASN-0098, which govern operations explicitly out of scope here (FOLLOWLINK / search). RL-REP places no constraint on READLINK's output that RL1 does not already impose. The table entry concedes this: "does not weaken RL1's verbatim return." This reads as prior-finding content relocated and reframed rather than removed.
**Required**: Drop RL-REP as a READLINK claim, or reduce it to a single one-line pointer noting that downstream coverage-based uses (specified elsewhere) consume the returned spans only via coverage. Remove the defensive opening sentence and the downstream-consumer enumeration.

### Issue 2: RL1's formal predicate is weaker than the claim and than the definition
**ASN-0111, RL1 (Completeness)**: "`(A i, (s, ℓ) : 1 ≤ i ≤ |Σ.L(a)| ∧ (s, ℓ) ∈ Σ.L(a).eᵢ : (s, ℓ) ∈ readlink(a, Σ).eᵢ)`, and conversely the read introduces no span not recorded."
**Problem**: The displayed predicate gives only one inclusion (the read omits nothing), while the claim is "Completeness" — both directions. The converse is asserted in prose but not formalized. Worse, since the operation is *defined* as `readlink(a, Σ) = Σ.L(a)`, the one-directional display is strictly weaker than the definition it is meant to characterize, so as stated it adds nothing and understates the guarantee.
**Required**: State RL1 as the componentwise equality `readlink(a, Σ).eᵢ = Σ.L(a).eᵢ` for each slot (capturing both "omits nothing" and "introduces nothing"), or drop the redundant display and let the definition carry it.

### Issue 3: RL0 weakest-precondition postcondition references the partial function off its domain
**ASN-0111, RL0 (Definedness)**: "`wp(readlink request at a, result = Σ.L(a)) ≡ a ∈ dom(Σ.L)`."
**Problem**: The postcondition `result = Σ.L(a)` mentions `Σ.L(a)`, which is undefined exactly when the wp evaluates to false (`a ∉ dom(Σ.L)`). The predicate is thus ill-formed precisely on the states the wp is meant to discriminate, making the "analysis" circular rather than a derivation.
**Required**: Phrase the postcondition without dereferencing off-domain — e.g. "the result is the recorded relationship at `a`" — so the equivalence `wp ≡ a ∈ dom(Σ.L)` is well-formed.

## OUT_OF_SCOPE

### Topic 1: RL-REP's downstream coverage-based interpretation
**Why out of scope**: Projection and type-matching are FOLLOWLINK / search territory per the scope list. Even if some pointer to representation-independence is wanted, the substantive content belongs in those ASNs, not as a READLINK claim (see Issue 1).

VERDICT: REVISE
