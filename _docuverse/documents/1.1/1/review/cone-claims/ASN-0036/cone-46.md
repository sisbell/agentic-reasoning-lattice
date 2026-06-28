The axiom and derivation chain is sound. S1 follows from S0's first conjunct in one line. S3's induction is correctly structured: AX-1 gives the vacuous base, and the inherited / new-or-redirected case split is exhaustive (complement of the inherited condition) and correctly dispatched — inherited via J0 + S1, new-or-redirected via AX-2. AX-2's range predicate is well-formed under the partial-function reading because the domain guard on the second disjunct discharges before the equality comparison. S5's two constructions (cross-document, within-document) each satisfy S2 and S3 directly on the witness state, and satisfy S0 and S1 vacuously over the empty transition relation; T3 is correctly invoked for distinctness of documents and V-positions from distinct last components. No proof step depends on a claim not in scope.

Three observations follow.

---

### S5 body claims "possibly infinite" multiplicity; finite witnesses do not establish this

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S5 (UnrestrictedSharing), body — "the sharing multiplicity of each address is a specific (possibly infinite) count"
**Issue**: The proof provides, for each N ∈ ℕ, a finite model with exactly N+1 referencing pairs. The formal postcondition is correctly bounded to "no finite uniform bound." The parenthetical "(possibly infinite)" in the body is a stronger claim — consistency of S0–S3 with a model having infinitely many referencing pairs — which would require either an explicit infinite witness or a separate argument that S0–S3 impose no cardinality axiom on dom(M(d)). Neither is supplied. The formal postcondition is not affected, but the body asserts more than the proof reaches.
**What needs resolving**: Either supply the missing argument (noting that S0–S3 contain no cardinality-bounding axiom on dom(M(d))), or remove "(possibly infinite)" from the body and restrict the informal summary to what the constructions establish: multiplicity unbounded over ℕ.

---

### AX-2: meta-prose explains why the domain guard is written rather than what the axiom asserts

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: AX-2 (GroundedExtension), body — "Classically the guard adds nothing, since the first disjunct already accounts for every v ∉ dom(Σ.M(d)); we write it out only so the application Σ.M(d)(v) is never reached outside dom(Σ.M(d))."
**Issue**: This sentence explains the author's motive for a stylistic choice in writing the axiom, not what the axiom says. The axiom's content — the write-side discipline requiring every new or redirected mapping to target dom(Σ'.C) — is fully stated in the formal quantifier. The meta-commentary on classical vs. tool-enforced reading is prose around an axiom explaining why it is formulated as it is, which degrades the reader's ability to extract the claim's content directly.
**What needs resolving**: N/A — formal content is unaffected. Remove or trim to the precision-relevant observation (the domain guard is carried to keep Σ.M(d)(v) well-defined under strict partial-function evaluation), without narrating the authoring rationale.

---

### S3 post-proof paragraph invokes "the earlier reading" — reviser drift

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S3 (ReferentialIntegrity), closing paragraph — "The earlier reading, that S1 alone forces a ∈ dom(Σ'.C) for any mapping established by a transition, conflated these: it assumed precisely the new-reference half that AX-2, not S1, supplies."
**Issue**: The paragraph references a past incorrect reading of the proof and explains why it was wrong. A reader of the current spec has no "earlier reading" to compare against; this is a history artifact. The structural point — that S3 requires both S1 (to retain valid references) and AX-2 (to ground new ones) — is already implicit in the case split and the Depends section. The sentence naming the earlier mistake is defensive prose that relocates prior-finding content into the proof body rather than removing it.
**What needs resolving**: N/A — the proof is sound. Remove the sentence beginning "The earlier reading" and its antecedent framing. The preceding sentences in the paragraph make the S1-versus-AX-2 distinction adequately without the historical reference.

---

VERDICT: OBSERVE