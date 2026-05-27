# Review of ASN-0099

## REVISE

### Issue 1: A1 introduced as applications-level axiom but is substrate-scope

**ASN-0099, "Arrangement Independence" section**: The ASN introduces axiom A1 (LinkStoreInertOfNonAllocatingOperations) at the applications level, with explicit acknowledgement: "This ASN is consequently not finally converged: its derivations are correct as written but rest on a hypothesis (A1) that should migrate out of this document and into ASN-0047 in a subsequent substrate revision."

**Problem**: A1's scope is substrate-wide — it constrains every operation in V at the frame level. By the ASN's own analysis, A1 is load-bearing for F9, F9★, F9★-cor, F9-cor, F17, F18, F19-filt, and F19-sco at the three operations K.μ⁺, K.μ⁻, and K.ρ whose ASN-0047 frames currently omit `L`. Without A1, F9's equality claim collapses to F19's monotonicity-only inclusion. The ASN explicitly admits non-convergence pending substrate revision.

**Required**: One of three resolutions: (a) ASN-0047 adds `L' = L` to the frames of K.μ⁺, K.μ⁻, K.ρ, after which A1 becomes a derived consequence and can be removed from this ASN's Claims Introduced table; (b) restructure ASN-0099 to use only monotonicity (F19-family) and weaken F9, F9★, F9★-cor, F9-cor accordingly; (c) commit to A1 as a permanent applications-level axiom, with separate justification for why a substrate-wide frame constraint properly lives outside the substrate (the ASN currently endorses only the transitional reading). Until one of these is taken, the ASN's main edit-survivability promise stands on consultative rather than derived ground.

### Issue 2: F4 weakening direction proof is brief and load-bearing

**ASN-0099, F4 weakening direction**: "The dual direction is discharged by F3 (Soundness): an implementation conforming to a weakening `P_w` of F1 ... would return links satisfying `P_w` but not F1, violating F3 which requires `a ∈ result(I, Σ) ⟹ matches(a, I, Σ)` with `matches` read as F1."

**Problem**: The "matches read as F1" stipulation is doing significant work. The F3 conformance contract is stated *parametrically* in `matches`; the weakening argument requires reading F3 against F1 specifically, but the prose only flags this informally. A reader could ask: "If `P_w` is the match predicate, then F3 with `matches := P_w` is satisfied by the alternative implementation — why is F1 privileged?" The answer is in the framing paragraph above but is not closed inside the weakening proof itself.

**Required**: A sentence inside the weakening direction making the meta-level fixing of F1 explicit — something like "F3 is invoked here with `matches` *fixed* to F1 (per the framing paragraph above); the alternative implementation, by hypothesis, conforms to F3 with `matches := P_w`, and the discrepancy at the F1-non-admitted pair `(a*, I*)` is precisely the operationally observable gap." The argument is correct as written but the load-bearing meta-level fixing should be cited at point-of-use rather than relying on the reader to carry it forward from the framing paragraph.

### Issue 3: F10's chronological reading needs sharper boundary

**ASN-0099, F10 derivation**: "the chain index of a link within `A_L(d)` equals the K.λ event count for `d` at the moment of that allocation."

**Problem**: This identification rests on ChainMembershipForOrigin's contiguous-prefix claim plus K.λ's subsequent-emission precondition pinning `ℓ = inc(ℓ_prev, 0)` with `ℓ_prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}`. The derivation invokes "ChainMembershipForOrigin" and "ChainEnumerationInjectivity" but doesn't explicitly establish that the chain-prefix maximum coincides with the most recently allocated link under `d`. ChainMembershipForOrigin gives `{t_1, …, t_{m_d}}` as a contiguous prefix, but the identification "max of this prefix = the previously-most-recently-allocated link" needs explicit appeal to ChainEnumerationInjectivity's strict-increase property.

**Required**: One sentence connecting the dots: "ChainEnumerationInjectivity gives `t_1 < t_2 < … < t_{m_d}` under T1, so `max{t_1, …, t_{m_d}} = t_{m_d}` is the chain element at index `m_d` — which equals the K.λ event count `m_d` for `d` at this allocation moment by the contiguous-prefix invariant."

### Issue 4: F15/F16/F17/F18/F19-filt/F19-sco derivations lean on "same structural argument"

**ASN-0099, multiple sections**: F15's derivation says "by the same per-slot coverage equality that drives F8's derivation"; F17 says "per F9's derivation, invoking A1 at the K.μ⁺ and K.μ⁻ cases"; F19-filt says "tracks F11 directly"; etc.

**Problem**: These derivations point to structural similarity rather than re-deriving in the filtered/scoped context. While the structural similarity is real and the conclusions sound, the filtered form has a *universal* rather than *existential* quantifier over slots, and a careful reader needs to verify that the F8/F9/F11 arguments transfer through the universal. Specifically: F8's argument that "per-slot coverage equality forces predicate equality" used the existential's monotone preservation; for the universal, the equally-correct argument is "per-slot coverage equality forces each conjunct to evaluate identically at the two states" — but this requires verifying the slot-index range is equal (which follows from `|Σ.L(a)| = |Σ'.L(a)|` via L6, but should be stated).

**Required**: One sentence in F15's derivation noting that the universal `(A (i, J) ∈ C : ...)` is evaluated against the same slot-index range at both states (since `|Σ.L(a)| = |Σ'.L(a)|` from L6's component-wise tuple equality) and against equal per-slot coverages (the same fact F8 used). The same one-sentence noting applies to F17 (with K.μ-family frame condition). F16, F18, F19-sco are clean (intersection preservation is elementary); F19-filt should make explicit that the universal-quantifier structure carries through LP13's value preservation just as the existential does in F11.

### Issue 5: Empty endset and arity-out-of-range conjuncts together can deceive

**ASN-0099, "Empty endsets at non-type slots" paragraph**: The discussion of empty endsets at non-type slots together with the filtered form's `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅` guard treats two failure modes uniformly.

**Problem**: The filtered match treats "slot `i` exists and is empty" and "slot `i` does not exist" with the same outcome (constraint unsatisfiable at that link), but for different reasons. The ASN's treatment is correct, but a reader trying to verify the conformance contract for `findlinks_filtered({(4, J)}, Σ)` against a link with `|Σ.L(a)| = 3` and against a link with `|Σ.L(a)| = 5` and `Σ.L(a).e₄ = ∅` will follow two different short-circuit paths through the conjunct. The ASN should explicitly note both paths.

**Required**: A sentence after the "Empty endsets at non-type slots" paragraph: "Note two distinct short-circuits for an unsatisfied per-constraint conjunct: `i > |Σ.L(a)|` short-circuits the left conjunct (the slot does not exist on this link); `i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = ∅` short-circuits the right conjunct (the slot exists but its coverage is empty). Both produce the same outcome (constraint unsatisfiable at `a`), via distinct argumentative paths — implementation-relevant for distinguishing 'wrong link kind' from 'incomplete link'."

### Issue 6: Worked example Query 10's d_b chain-position assumption

**ASN-0099, Query 10 step (i)**: "K.δ case (ii) at `k = 0` from `d_b` creates a fresh document `d_c = inc(d_b, 0)` with `d_c ∉ E`. The K.δ preconditions are satisfied: ... `inc(d_b, 0) ∉ E` (the freshness condition for d_c — d_b is itself the chain successor of d_a under the same account, so the next chain element is unused at Σ)..."

**Problem**: The original worked-example setup says "We assume `d_a` was allocated before `d_b` under the same account, so by SubAllocatorAxiom.ChainDiscipline and T10a, `d_a < d_b` under T1" — but does NOT establish that `d_b = inc(d_a, 0)` (consecutive siblings with no intervening allocations). The Query 10 parenthetical asserts this without it having been stated in setup. If another document had been allocated between d_a and d_b under the same account, inc(d_b, 0) might still be fresh or might not be, depending on the chain state.

**Required**: Either tighten the setup to specify `d_b = inc(d_a, 0)` (so that inc(d_b, 0) is the next chain element and is fresh by ChainEnumerationInjectivity + freshness of unused chain elements), or rewrite Query 10 step (i) to use a document known to be at the chain frontier — for example, by introducing a fresh K.σ step at the beginning of Query 10 that creates a new document whose chain successor is then exercised.

### Issue 7: "Without appreciable delay" cited from Nelson without ASN-internal grounding

**ASN-0099, "Local Atomicity and the Single-State Setting" section**: "This atomicity is what underwrites the *immediate* component of Nelson's 'without appreciable delay' promise within a single instance."

**Problem**: The phrase "without appreciable delay" is attributed to Nelson and used as motivational framing for the atomicity guarantee. The ASN does not cite a foundation source for this phrase, and the abstract specification does not formalize any timing bound. The cite-without-cite invites a reader to ask "where in the foundations is this commitment?" — it is design intent rather than a foundation invariant.

**Required**: Either drop the Nelson attribution (the atomicity claim stands on its own from SequentialTransitionAxiom of ASN-0093 without rhetorical framing), or qualify it as "Nelson's design intent for Xanadu reader experience" with no foundation-level claim attached. The opening paragraph ("we adopt this as our starting obligation") similarly leans on the Nelson framing — both should be qualified the same way.

## OUT_OF_SCOPE

### Topic 1: Query I-sets with addresses outside dom(C) ∪ dom(L)
The ASN flags this in "What We Have Not Specified". The match predicate works mechanically against any `I ⊆ T`, but the operational meaning of phantom-address queries belongs in a future ASN handling pathological query semantics.

### Topic 2: Inverse direction (I→V resolution for FOLLOWLINK)
Belongs to FOLLOWLINK/RETRIEVEENDSETS as the ASN explicitly notes.

### Topic 3: Multi-instance / partition-tolerance semantics
Replication, BEBE protocol, and cross-instance consistency belong to a future ASN per the user-supplied scope restriction.

### Topic 4: Access control formalization
Mentioned as an orthogonal scope filter; deserves its own ASN.

### Topic 5: Endset spans referencing V-positions
An endset *could* technically reference a V-position tumbler (per L4's generality), but V-positions and I-addresses occupy disjoint structural regions of T (zeros = 0 vs zeros = 3), so such a link would never match a normal `image(R, d, Σ)`. Edge-case handling for non-standard endset targets is a future ASN concern.

### Topic 6: Implementation strategies (indexes, caching, push-based notification)
The ASN intentionally is index-agnostic. Implementation guidance is non-normative and out of scope.

### Topic 7: Composite filtered-and-scoped operation
The ASN notes that `result_filtered_scoped(C, S, Σ) = findlinks_filtered(C, Σ) ∩ S` is the intended composition, with no new structural content. Future ASNs needing this composed form should restate the conformance contract; the omission here is deliberate.

VERDICT: REVISE
