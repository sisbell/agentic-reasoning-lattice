# Review of ASN-0093

## REVISE

### Issue 1: Chain length not committed in substrate context

**ASN-0093, Definition of T10a-discipline-satisfying chain**: "a *T10a-discipline-satisfying chain* is a (possibly infinite) sequence `(t_1, t_2, t_3, …)`"

**Problem**: The parenthetical "(possibly infinite)" leaves chain length unspecified. But the substrate's correctness implicitly requires sub-allocator chains `A_C(d)` and `A_L(d)` to be infinite: K.α and K.λ admit unbounded subsequent emissions (B9-style unboundedness from ASN-0040), and the chain lemmas' universals `(A n ≥ 1 :: ...)` are consumed at arbitrary chain indices including those past any finite truncation point. If a chain could be finite of length k, then ChainEnumerationInjectivity at indices m, n with k < m or k < n would be vacuous, and K.α/K.λ's subsequent-emit at the (k+1)-st emission would have no chain element to inhabit. SubAllocatorAxiom.ChainDiscipline says A_C(d) "is rooted at FirstEmission's t_1^C(d)" but does not specify length.

**Required**: Either (a) commit the substrate's sub-allocator chains to be infinite explicitly (e.g., "A_C(d) and A_L(d) are infinite chains extending t_1^C(d) and t_1^L(d) under repeated inc(·, 0)"), or (b) clarify that the chain lemmas' conclusions apply uniformly to chains of any length and add a substrate-level extensibility commitment (e.g., the chain is *defined* up to whatever index has been produced and extends one step further at every K.α/K.λ subsequent-emit). Option (a) matches the conceptual-chain quantifier-scope note in ChainPrefixExtension.

### Issue 2: "T10a-discipline-satisfying chain" terminology overstates the discipline

**ASN-0093, Definition**: "A *T10a-discipline-satisfying chain* is a (possibly infinite) sequence (t_1, t_2, t_3, …) of tumblers satisfying two structural conditions, both stated without reference to allocator-tree membership or spawning triples: (i) FirstElementValidity: t_1 is T4-valid. (ii) SiblingRecurrence: t_{n+1} = inc(t_n, 0) for every n ≥ 1."

**Problem**: T10a's discipline in ASN-0034 is the full *AllocatorDiscipline* including spawning triples `(parent(A), spawnPt(A), spawnParam(A))`, k' ∈ {1, 2} child-spawning, the at-most-once `(t, k')` rule, and tree embedding. The substrate's chain Definition strips all of this away and keeps only the sibling-only `inc(·, 0)` recurrence plus a single T4-validity anchor. Calling this a "T10a-discipline-satisfying chain" is misleading — a reader could reasonably believe the chain satisfies T10a's full discipline (and could be embedded in an allocator tree), when in fact only one stripped-down fragment is asserted. The substrate explicitly disclaims tree embedding ("makes no commitment about whether an implementation realises [these] as standalone T10a allocators...").

**Required**: Rename the concept to something that reflects its actual content — e.g., "sibling-increment chain" or "inc(·, 0)-chain" — and rename the six chain lemmas correspondingly (ChainElementT4Validity, ChainUniformLength, etc. become Sibling*ChainElement*T4Validity, etc.). At minimum, add a one-line warning in the Definition that "T10a-discipline-satisfying chain" is the substrate's term for a fragment of T10a, not equivalent to T10a allocator status.

### Issue 3: K.λ subsequent-emit E₁-preservation underwriting is implicit

**ASN-0093, Discharge matrix L0 entry for K.λ**: "Discharged at new key on L-clause via `E(ℓ)₁ = s_L` precondition"

**Problem**: The precondition `E(ℓ)₁ = s_L` is listed as if it were a caller-supplied fact, but the parameter semantics note says the address `ℓ` is "deterministically pin[ned] from `(d, Σ)`" — so the precondition is automatically satisfied by the emission rule, not freely chosen. For the subsequent-emit branch where `ℓ = inc(ℓ_prev, 0)`, what guarantees that the inc operation preserves `E(·)₁ = s_L`? The answer is DisjointSubAllocatorChains (and implicitly TA5(b)/(c) + TA5-SigValid + ChainUniformLength on E₁'s position within the chain element). But neither the precondition list nor the matrix entry cites DisjointSubAllocatorChains for this; it appears only as a chain-indexed lemma whose conclusion is silently relied on. The K.α/K.λ subsequent-emit precondition derivations cite ChainEnumerationInjectivity, ChainPrefixExtension, ChainMembershipForOrigin, etc., but not DisjointSubAllocatorChains for the E₁-preservation step.

**Required**: Add explicit cross-references showing that `E(a)₁ = s_C` (resp. `E(ℓ)₁ = s_L`) is preserved at every subsequent-emit via DisjointSubAllocatorChains (which itself derives the conclusion from FirstEmission's structural form + ChainUniformLength + ChainElementT4Validity + TA5-SigValid + TA5(b)/(c)). Either add a precondition-derivation bullet ("E(ℓ_new)₁ = s_L is automatic under the subsequent-emit rule by DisjointSubAllocatorChains") or note this in the discharge matrix L0 entries.

### Issue 4: ChainUniformZeroCount proof's TA5(b) citation is at k=0, not k>0

**ASN-0093, ChainUniformZeroCount Proof step**: "TA5(b) (positional agreement at positions 1..#t_n) holds for inc(t_n, 0) (TA5(c)'s single-position-modification clause: positions other than sig(t_n) are unchanged)"

**Problem**: TA5(b) in ASN-0034 has *two distinct clauses* for k=0 and k>0:
- When k=0: `(A i : 1 ≤ i ≤ #t ∧ i ≠ sig(t) : t'ᵢ = tᵢ)` — agreement *except at sig(t)*.
- When k>0: `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` — agreement at all positions up to #t.

The proof cites "TA5(b) (positional agreement at positions 1..#t_n)" as if invoking the k>0 form, but the chain step is `inc(t_n, 0)` (k=0). For k=0, TA5(b) gives agreement at positions *other than sig(t_n)*, which is what's actually needed. The parenthetical citation "(TA5(c)'s single-position-modification clause)" is correct, but the lead-in description "positional agreement at positions 1..#t_n" misstates the k=0 clause as if it were the k>0 form.

**Required**: Reword to "TA5(b) for k=0 (positional agreement at positions 1..#t_n *except sig(t_n)*) holds for inc(t_n, 0)" — or just cite TA5(c)'s single-position-modification clause directly as the source of preservation outside sig.

### Issue 5: SubAllocatorAxiom.Exists "remain active" claim relies on M1, which is the inductive invariant

**ASN-0093, SubAllocatorAxiom.Exists**: "By M1 (ArrangementMonotonicity), once d ∈ dom(M) it remains so at every successor state, and the sub-allocator chains correspondingly remain active permanently."

**Problem**: The axiom's "remain active" conclusion is stated as a consequence of M1. But M1 is one of the substrate's *invariants* established by induction over transitions, not an external axiom. The axiom thus depends on an invariant that the substrate itself must prove. This creates a subtle layering: SubAllocatorAxiom is presented as an axiom (top of the dependency order), but its persistence clause is parasitic on M1 (which is later established inductively). The simultaneous-induction framing handles this by treating M1 as part of the IH, but the axiom statement reads as if "permanence of activation" is axiomatic when it is really inductive.

**Required**: Either (a) rephrase the axiom's third sentence to say "Given M1, once d ∈ dom(M) it remains so..." — making the dependency explicit; or (b) move the "remain active permanently" conclusion out of the axiom into a Corollary that explicitly cites M1; or (c) note in the axiom that the persistence portion is *equivalent* to M1 and consumed only via M1's separate inductive establishment.

### Issue 6: The Open Questions item on link withdrawal contradicts L12's stated permanence

**ASN-0093, Open Questions**: "Link withdrawal. The substrate admits no withdrawal of dom(L) entries (L12 enforces immutability). Nelson's tombstone-style withdrawal (LM 4/9) is not expressible at this layer. Closing the gap is deferred to a higher-layer ASN that may extend the substrate with an explicit retraction mechanism — e.g., a future tombstoning ASN."

**Problem**: A "higher-layer ASN that may extend the substrate with an explicit retraction mechanism" cannot extend this substrate while preserving L12 (which is `(A Σ → Σ' : (A a : a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a)))`). Any retraction mechanism that removes an entry from dom(L) violates L12 directly. So either (i) L12 is wrong (over-strong) and Nelson's tombstoning requires a weaker variant (e.g., L'(a) becomes a tombstone-marked value rather than disappearing), or (ii) tombstoning can't be a *higher-layer extension* of this substrate — it would have to be a *replacement* of the substrate with a different one having a weaker L12. The current text suggests a non-existent compositional path.

**Required**: Clarify in the Open Question whether tombstoning is (a) a value-level marker preserved by L12 (so `L'(a) = TOMBSTONE` doesn't violate the equality form, only its semantic interpretation changes), or (b) a different substrate that this one explicitly forecloses. If (a), say so. If (b), say so.

### Issue 7: Cross-document disjointness Case A "d₂[#d₁+1] ≠ 0" argument needs more care for d₁'s zero positions

**ASN-0093, Cross-document disjointness Case A**: "By M0 at d₁, zeros(d₁) = 2, so d₁ has exactly two zero positions within 1..#d₁. The prefix relation gives d₂[k] = d₁[k] for 1 ≤ k ≤ #d₁, so d₂ inherits those two zero positions at the same indices. By M0 at d₂, zeros(d₂) = 2, so d₂ has no further zeros in its native domain; in particular d₂[#d₁+1] ≠ 0."

**Problem**: The argument is correct but elides a precondition check: it relies on `#d₁ + 1 ≤ #d₂` to assert that position `#d₁ + 1` exists in `d₂`. This follows from `d₁ ≼ d₂ ∧ d₁ ≠ d₂ ⟹ #d₁ < #d₂ ⟹ #d₁ + 1 ≤ #d₂` (Prefix's derived postcondition), but the proof doesn't cite this step. Without `#d₁ + 1 ≤ #d₂`, the position `d₂[#d₁ + 1]` might not even be defined.

**Required**: Add one sentence before the "By M0 at d₁" derivation: "Since `d₁ ≺ d₂` (proper prefix), `#d₁ < #d₂` (Prefix derived postcondition), so position `#d₁ + 1` lies within d₂'s native domain."

### Issue 8: "T10a-conforming step sequence" vs "structural inc-chain" relationship not explicit

**ASN-0093, L1c restatement**: "Every link address ℓ ∈ dom(L) has a *structural inc-chain* from its home document to ℓ..."

**Problem**: ASN-0043's L1c uses the phrase "T10a-conforming step sequence" while the substrate uses "structural inc-chain". The text claims these are equivalent ("This is ASN-0043's L1c restated for the substrate; the k₁ = 2 and length-increasing clauses are preserved verbatim from the foundation form, not weakened."). But the substrate also disclaims allocator-tree embedding, and ASN-0043's L1c is presented in its per-step admissibility form (not requiring tree embedding). The relationship to T10a is per-step admissibility *only*; the term "structural inc-chain" is the substrate's renaming of the same concept. The substrate could be clearer that the rename is purely terminological.

**Required**: Add a sentence after L1c's restatement noting: "The term 'structural inc-chain' is the substrate's nomenclature for what ASN-0043's L1c calls a 'T10a-conforming step sequence'; the per-step admissibility content is identical."

### Issue 9: Discharge matrix doesn't explicitly check C1b under K.σ at prior keys

**ASN-0093, Discharge matrix C1b entry**: "Preserved: C in frame"

**Problem**: At K.σ, the existing content keys' `#E(a) ≥ 2` invariant transfers because C is in frame, but the entry doesn't address whether the *projection* `E(a)` itself depends on M (it doesn't — it's T4b's structural projection on the address alone), nor that origin(a) ∈ dom(M') is preserved by M1 (relevant for C2 but not C1b). The matrix entry is correct but minimal; for a Dijkstra-level review, the "preserved by frame" claim should specify exactly why frame on C suffices for C1b (E(·) is structural).

**Required**: Strengthen "Preserved: C in frame" to "Preserved: C in frame (E(·) is T4b's structural projection on the address alone, depending on no state component)". Same applies to L1b under K.σ and K.α.

### Issue 10: Worked example Step 9 misclassifies sub-case at #d = #d_alt

**ASN-0093, Worked Example Step 9**: "Case B.i (since #d = 5 = #d_alt)."

**Problem**: Case B.i is defined as `#d₁ ≤ #d₂`. At equality `#d = #d_alt`, *both* B.i and the mirror B.ii (i.e., `#d₂ ≤ #d₁`) hold trivially — they're symmetric and not exclusive. The proof of Cross-document disjointness in Case B says "exhaustive by NAT-order's at-least-one trichotomy at (#d₁, #d₂)", and the three trichotomy disjuncts are `<`, `=`, `>`. The proof's sub-cases B.i (#d₁ ≤ #d₂) and B.ii (#d₂ < #d₁) cover all three disjuncts (with B.i covering both `<` and `=`). At equality the proof's WLOG is essentially trivial — either direction works. The worked example's "Case B.i (since #d = 5 = #d_alt)" is fine but the sub-case naming convention could be more transparent: at equality, *both* directions of ⋠ require component-failure witnesses, and the example only exhibits one.

**Required**: Either rename sub-cases to use strict inequalities (B.i for `<`, B.ii for `>`, B.iii for `=`), or clarify in Step 9 that at equality both B.i and B.ii would fire symmetrically and the example arbitrarily chooses B.i's extraction direction.

## OUT_OF_SCOPE

No issues — the ASN's Scope section explicitly delegates arrangement mutation, entity stratification, provenance recording, coupling constraints, link withdrawal, concurrency, and sub-allocator stratification beyond C/L to higher-layer or future ASNs. These are appropriately deferred.

VERDICT: REVISE
