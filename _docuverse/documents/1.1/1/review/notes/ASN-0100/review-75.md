# Review of ASN-0100

## REVISE

### Issue 1: INS.alloc claim row cites the wrong freshness lemma

**ASN-0100, Claims Introduced table, INS.alloc**: "each K.α firing satisfies its freshness precondition against its own intermediate state by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093)"

**Problem**: The body (Effect One, and the §Atomicity S4 bullet) correctly discharges K.α's freshness precondition `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)` via **SubsequentEmissionFreshness** (for `a_1,…,a_{n−1}` and for `a_0` when `m_d > 0`) plus FirstEmissionFreshness (for the `m_d = 0` boundary). ChainEnumerationInjectivity only establishes strict within-chain monotonicity (`a_i < a_j`) — it yields same-document distinctness but does *not* discharge cross-document (`dom(C)`) or cross-subspace (`dom(L)`) freshness. The claim row therefore under-cites: it names the lemma the body uses for S4 distinctness, not the one that closes the freshness precondition.

**Required**: Replace "ChainEnumerationInjectivity" with "SubsequentEmissionFreshness" in the INS.alloc row (keeping FirstEmissionFreshness for the boundary), matching the body.

### Issue 2: Proof of INS.M-exhaustive embedded in the Formal Contract slot

**ASN-0100, §The Operation: Formal Contract, Effect — Arrangement, Exhaustiveness (INS.M-exhaustive)**: "The exhaustiveness clause is a property of the post-state V_{s_C}(d'), and it follows directly from the composite construction. Steps 1 and 4 … frame M … Step 2's K.μ⁻ … only removes … Step 3's K.μ⁺ adds exactly … no fourth region exists."

**Problem**: A multi-sentence proof sits inside the formal-contract slot, which should state the postcondition only. This is essay content in a structural slot — the reader must skip past the justification to read the contract. The same argument is also the natural content of §Verifying the Invariants (it is reused there for S2 functionality and for the uniqueness argument in §Atomicity).

**Required**: State INS.M-exhaustive as a postcondition in the contract; move the "Steps 1–4 / no fourth region" justification to the verification section that consumes it.

### Issue 3: Duplicate coupling-discharge prose across the two worked examples

**ASN-0100, §A Worked Example** — interior example: "Here the coupling logic instantiates to the two pairs above: J0 pairs each fresh … (J0), J1★ records each newly-arranged content-subspace image, and J1'★ matches each new R'-entry back to a placement — all satisfied when step 4's K.ρ firings commit." Empty example: "Here the coupling logic instantiates to these three pairs — each fresh a_{new k} is placed at [1,1+k] (J0), is a newly-arranged content-subspace image (J1★), and matches its new R'-entry (J1'★) — satisfied when step 3's K.ρ firings commit."

**Problem**: Two paragraphs say the same thing in different words; only the arity (two vs three pairs) and step number differ. The general discharge is already given in §Provenance. The per-example repetition adds no new reasoning.

**Required**: Keep one instantiation (or fold the coupling discharge into a single sentence referencing §Provenance); remove the near-verbatim restatement in the second example.

### Issue 4: Effect Three frame enumeration duplicates the Formal Contract Frame Conditions

**ASN-0100, §Discovering the Three Effects, Effect Three**: the paragraph "INSERT is a substrate composite; each frame is determined by the K-step frames of its decomposition." then enumerates left region / other subspaces / other documents / content-store frames — each subsequently restated formally under §The Operation: Formal Contract → Frame Conditions.

**Problem**: The same four frame facts, with the same per-step justifications (`L' = L` by L12, cross-document frame, content-store preservation), appear in both sections. The discovery narrative for "what shifts" does not need to pre-state the formal frame clauses; this is cross-section duplication.

**Required**: Let Effect Three carry only the discovery-level observation (which positions shift and why); leave the formal per-component frame statements to the Frame Conditions block.

## OUT_OF_SCOPE

### Topic 1: Concrete scenario with empty content subspace but non-empty link subspace
**Why out of scope**: The general contract already covers `V_{s_C}(d) = ∅ ∧ V_{s_L}(d) ≠ ∅` via the empty-content-subspace branch of (INS.μ⁻-fires) and INS.frame.subspace; adding a worked example for it is an expository nicety, not a correctness gap, and the partial-failure-recovery and concurrent-INSERT questions are already correctly listed under Open Questions.

VERDICT: REVISE
