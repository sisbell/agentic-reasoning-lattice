# Review of ASN-0040

## REVISE

### Issue 1: "Why the axiom is needed" prose preceding B-Seq
**ASN-0040, State space and transitions**: "Because →* branches, a uniqueness argument that presumed a single execution path would not hold across divergent branches: two acts proceeding from a common state could compute the same address independently. We therefore make the execution discipline an explicit axiom."
**Problem**: This (with the preceding "This framework leaves →* branching in general…forms a tree rather than a chain") is two paragraphs motivating *why* B-Seq exists, not stating *what* it says. It is the flagged anti-bloat pattern — meta-prose around an axiom explaining its necessity. The branching fact is used nowhere except to justify B-Seq, and B-Seq's role is already exercised concretely at B8 Case 1.
**Required**: Cut to a single sentence introducing B-Seq, or move the "needed for cross-branch uniqueness" remark to B8 where it is actually consumed.

### Issue 2: B-Seq Justification mixes grounding with restated scope
**ASN-0040, B-Seq, Justification + Scope**: "Gregory's udanax-green commits baptisms through a single fully serialized path — a single-process, single-threaded event loop dispatches each operation run-to-completion, and there is exactly one persistent-store writer…" then *Scope:* "single baptismal authority (one serialized commit path); cross-replica concurrency is out of scope."
**Problem**: The "single baptismal authority / cross-replica out of scope" qualification is stated three times (axiom *Scope*, justification, and again in the final Open Question on coexisting replicas). The implementation-mechanics detail (event loop, single writer) is heavier than needed to ground an abstract total-order axiom.
**Required**: State the grounding in one clause; drop the duplicated scope qualifications, keeping the single authoritative one on the axiom.

### Issue 3: B8 Case 1 explains an excluded case rather than dispatching it
**ASN-0040, B8 proof, Case 1**: "since β₁ and β₂ play symmetric roles, this relabeling is without loss of generality and excludes the case s₂ →* s₁ in which a ∉ s₂.B."
**Problem**: The trailing "in which a ∉ s₂.B" describes the branch the relabeling has already removed — a paragraph gesturing at a case the WLOG step excludes. This is reviser drift; the relabeling either holds by symmetry (state that) or it does not. The aside about `a ∉ s₂.B` adds no step.
**Required**: End the relabeling sentence at "without loss of generality." The symmetric roles of β₁, β₂ are the whole justification.

### Issue 4: B6 necessity does not address (iii) at d = 1
**ASN-0040, B6 proof, (⟹) Necessity**: "*Condition (iii) is necessary at d = 2.*"
**Problem**: The theorem claims (ii) and (iii) are jointly necessary, but necessity of (iii) is shown only for d = 2. At d = 1, (iii) reduces to `zeros(p) ≤ 3`, which is implied by T4 and is therefore *not* an independent constraint. The proof leaves this unstated, so a reader cannot tell whether the d = 1 omission is an oversight or a vacuity.
**Required**: One sentence noting that at d = 1, (iii) is discharged by T4-validity of p and so imposes no additional condition — making the d = 2 argument the only binding necessity claim for (iii).

## OUT_OF_SCOPE

None — the ASN keeps to the registry, the baptize operation, and their invariants; ownership/content/concurrency questions are correctly parked in Open Questions.

VERDICT: REVISE
