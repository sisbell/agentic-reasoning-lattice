# Review of ASN-0051

## REVISE

### Issue 1: SV0 framing conflates schema citation with logical derivation
**ASN-0051, SV0 (NoStaleResolutionState)**: "Three clauses: (i) Link-store signature... (ii) State-schema closure... (iii) Operational closure... *Consequence — every conforming resolution function reduces to (e, Σ.M(d)).* Because (i)–(iii) deny any resolution function the inputs needed to consult prior or cached arrangement state..."

**Problem**: SV0 is presented as having a logical structure (clauses → consequence → corollary), but the structural roles are mixed. Clauses (i)–(iii) are *citations* of foundation ASN definitions (ASN-0043's L3, ASN-0047's state schema, ASN-0047's K transition list), not derived facts. The "Consequence" is a meta-observation: any function defined over a schema lacking historical fields cannot consult them. This isn't a derivation requiring proof — it's a property of the schema definition. The dense framing makes SV0 read like a theorem with a proof when it's actually a schema observation / lemma-by-inspection.

**Required**: Either (a) explicitly label SV0 as a schema observation with each clause citing its foundation source, or (b) restructure to distinguish "what the schema is" (foundation citations) from "what this means for admissible functions" (the meta-observation). The current prose treats both as if they require proof; one is definitional, the other is trivial inspection.

### Issue 2: SV13(g) "equivalently" misrepresents count relationship
**ASN-0051, SV13(g)**: "the surviving text-subspace projection in any document is the union of m · p decomposition terms `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)`, equivalently the union of at most m · p maximal ordinal-contiguous fragments within mapping blocks"

**Problem**: The two unions are equal as sets, but the count distinction is load-bearing throughout SV11 and the worked examples. Decomposition terms are *exactly* m · p (some may be empty); maximal fragments are *at most* m · p (with strict inequality under coalescence). The non-injective worked example exhibits 4 decomposition terms coalescing to 2 maximal fragments — a strict inequality the synthesis statement compresses to "equivalently".

**Required**: Reword (g) to make the count distinction explicit: "the union of m · p decomposition terms (some possibly empty), equivalent as a set to the union of at most m · p maximal ordinal-contiguous fragments, with strict inequality under coalescence".

### Issue 3: SV6 scope for k ≤ p₃ left implicit
**ASN-0051, SV6 (CrossOriginExclusion)**: "*Precondition.* ... the precondition is k > p₃."

**Problem**: The precondition is clearly stated, but the ASN never explains the structural reason for the bound or what happens when k ≤ p₃. The case is constructible: take s = 1.0.1.0.1.0.1.1 (element-level, p₃ = 6) and ℓ = 0.0.1.0.0.0.0.0 (k = 3); then s ⊕ ℓ = 1.0.2.0.0.0.0.0, and t = 1.0.1.0.5.0.1.1 satisfies s ≤ t < reach with origin(t) = 1.0.1.0.5 ≠ origin(s) = 1.0.1.0.1. So k ≤ p₃ spans *can* contain cross-origin tumblers — by design (these are Nelson's broader-level spans for spanning accounts/nodes per [LM 4/25]). The ASN's same-origin coverage growth section gestures at this but doesn't tie it back to SV6's precondition.

**Required**: Add a brief note alongside SV6 stating that k ≤ p₃ spans cross document boundaries by design, with a forward pointer to broader-level spanning. Without this, a reader cannot tell whether the k > p₃ precondition is a technical artifact of the proof or a structural feature.

### Issue 4: Bilateral vitality terminology for vacuous and asymmetric cases
**ASN-0051, Bilateral Vitality definition**: "When both F = ∅ and G = ∅, both disjunctions are satisfied by the left branch, making the link bilaterally vital in every document — vacuously. ... The asymmetric cases — exactly one of F, G empty — also follow mechanically from the disjunction structure."

**Problem**: Calling (∅, ∅, Θ) "bilaterally vital in every document" stretches the word "bilateral". Calling (∅, G, Θ) with G vital "bilaterally vital" stretches it further — there's only one side. The formal disjunction structure handles these correctly, but the term mismatches the semantic content (which is really "every non-empty content endset is vital").

**Required**: Either rename to something like "endpoint-vital" (which doesn't presuppose two sides), or state explicitly that "bilateral vitality" in the (∅, ∅, Θ) and asymmetric cases is a degenerate satisfaction of the disjunction, not a substantive claim. The current framing oscillates between treating empty endsets as trivially satisfying and as structurally absent.

### Issue 5: SV0 functional equivalence dependency claim is misleading
**ASN-0051, SV0**: "The functional equivalence — `Σ₁.L = Σ₂.L ∧ Σ₁.M(d) = Σ₂.M(d) ⇒ locate_{Σ₁}(e, d) = locate_{Σ₂}(e, d)` — is then an *immediate corollary* of the definition (and L-equality, while vacuous for the function locate as written, is a witness that the architectural denial in (i) is being respected..."

**Problem**: The L-equality precondition is described as a "witness that the architectural denial in (i) is being respected". This is a strange characterization — a precondition in a conditional cannot "witness" anything beyond its conditional content. The functional equivalence stated would also be trivially true with the L-equality dropped (since locate doesn't reference L). The current text suggests the L-equality has epistemic content it doesn't formally carry.

**Required**: Drop the "witness" framing. Either state the functional equivalence without L-equality (since L doesn't appear in locate's definition) and note this directly, or drop the functional-equivalence corollary entirely since SV0's substance is the architectural denial, not any locate-level equivalence.

## OUT_OF_SCOPE

### Topic 1: Formal characterization of same-origin coverage growth
**Why out of scope**: The "Same-origin coverage growth" section explicitly notes "We make no formal SV claim about same-origin coverage growth in this ASN" and defers the allocator-discipline conditions to ASN-0034. The descriptive treatment (sequential overshoot, child-depth entry) and concrete counterexample are sufficient to motivate SV6's element-level scope and to disclaim universal same-origin exclusion.

### Topic 2: Link-subspace endset projection and reflexive addressing
**Why out of scope**: The ASN states that "the detailed analysis of link-referencing endsets and reflexive addressing to the Link Subspace ASN" is deferred. SV2's unified statement covers K.μ⁺ and K.μ⁺_L monotonicity correctly; the per-subspace strictness analysis (when K.μ⁺_L can enlarge a reflexively-addressed endset's projection via L13) is properly future work.

### Topic 3: Open Questions section items
**Why out of scope**: Discovery latency, fork preservation of bilateral vitality, fragment ordering canonicality, link home vs vital documents disjointness, upper bounds on fragment counts — all genuine future ASN topics, intentionally enumerated as open.

VERDICT: REVISE
