# Review of ASN-0130

I checked every proof obligation in this note: PR-ENC-uniq's prefix-freeness argument, PR-SIG's well-foundedness induction for `sig`, PR0's wp equivalence in both directions, PR1's per-step content induction, PR2's event-wise acyclicity, PR3a's substitution induction in full (WT-α and WT-W provisos, the iterated weakening, the sequential-substitution discharge), the start-exactness argument in PR5's lint, and the worked composition's claims against PD0's rules. I found no defect requiring revision. Detail on the load-bearing checks follows.

**Verification notes (what was checked and held):**

- **PR-ENC / PR-ENC-uniq.** The proper-prefix argument is sound: two parse-valid runs at one start share values at common addresses, so the shorter's sequence is a prefix of the longer's, contradicting prefix-freeness. The overlap caveat (decodable suffixes) is correctly dismissed by start-anchoring. The `shift(x,1) = inc(x,0)` identity is argued from TA5(c)/TA5-SigValid/OrdinalShift, consistent with the foundations' chain enumerations; same-origin preservation under `shift` holds because C1b's `#E(a) ≥ 2` keeps the modified terminal position inside the element field.
- **PR0's wp, both directions.** Sufficiency on hit needs canonical shaping (incumbent `F' = enc({a'})` with `subtree(a') = subtree(a)` forcing `a' = a`) — supplied by the discipline, with the off-discipline counterexample (I0a's separating pair) correctly exhibited. Necessity of C3 at a miss needs "no active tuple denotes `a` at all," which the miss condition plus PR-ENC-uniq plus canonical shaping delivers; the off-discipline failure (raw tuple with `F'' = enc({a})`, unrelated `G''`) is correctly exhibited. The attainability convention is applied consistently to rejections where POST-ref happens to hold at the unchanged state.
- **PR2.** The event-wise formulation survives de-registration/re-registration: (a) gives `e₁(r) <` every deposit event for D, hence `< e₁(D)`; (b) correctly excludes both the deposit and the hit for a self-referencing run by induction along the derivation. Mutual recursion is genuinely unconstructible: a 2-cycle yields `e₁(D₁) < e₁(D₂) < e₁(D₁)`.
- **PR3a.** The freshness inventory matches what each lemma consumes: WT-α's "image occurs nowhere in u" is met by choosing names absent from `expand(r)`; WT-W's "no binder of u" is met because *all* binding sites (the note's own enumeration includes QD filters) are renamed to expansion names disjoint from author names by PR-ENC's reserved supply; the sequential discharge neither captures (target's binders are fresh expansion names) nor interferes (no `yⱼ` occurs in any `Eᵢ`; the `Eⱼ`'s free variables lie in `dom(Γ)` by well-typing). The rank-minimal base (reference-free body) is properly subsumed: the rank hypothesis is invoked only at reference nodes, which a minimal-rank definition cannot contain by PR2(a). The "among" relaxation from the prior revision is used consistently — unused parameters are renamed and substituted away harmlessly, since arguments are pure, total terms.
- **PR5 lint exactness.** The prefix-incomparability of distinct run starts is fully argued: same-origin chain addresses share length (sibling advance preserves length), and equal-length distinct tumblers cannot be prefix-related; cross-origin starts extend prefix-incomparable anchors, and the "two prefixes of one tumbler are length-ordered" step closes the case. This also silently handles overlapping runs — a start interior to another run is still incomparable with the containing start.
- **PR5 parameter reading.** Soundness rests only on fixity of bound values across a step, which PD0's ground consumes; the per-instantiation reading degenerates correctly at `k = 0`. Non-Boolean expansions fall out of certification at check (iii) because no PD0 rule derives them.
- **Worked composition.** Step 4's refusal is checker-correct: `¬(∃ x ∈ A_W :: …)` needs the existential in SF, which no rule gives over a non-grow-only active base; the Marker respelling lands in ST by the grow-only-∃ rule with a step-constant body under the parameter reading. Step 5 correctly distinguishes residence from registration.
- **Scoping discipline.** Every discipline-dependent claim names its scope, the off-discipline failure modes are exhibited rather than ignored, and the entry-point seal makes surface-driven derivations enforcedly disciplined — the same structural move ASN-0128 makes for [R], so the scoping is a fact about the shipped surfaces, not an assumption.

## REVISE

No revise items.

## OUT_OF_SCOPE

### Topic 1: Concurrency contract for the two new surfaces
**Why out of scope**: ASN-0128's I4 settles first-to-commit semantics for emits generically, and the wrapped emits inherit it, but a statement of what the *losing* `register_pred` or `certify_pd_stable` call observes (hit against the winner's deposit, given full re-validation at the loser's pre-state) would be new composition, not an error here.

### Topic 2: De-registration policy for definitions with live referents
**Why out of scope**: The note correctly records this as Open Question 3. Committing a policy — transitive checks at evaluation, blocking `pdef` retraction while referents stand, or a dangling-reference lint class — is a future ASN's decision, and nothing in this note depends on which way it goes.

### Topic 3: The concrete encoding
**Why out of scope**: PR-ENC fixes exactly the properties the proofs consume (injectivity, prefix-freeness, decidable self-delimiting parse, recorded contexts, reserved name supply) and explicitly delegates the byte format as a substrate parameter, parallel to subspace identifiers. Fixing bytes is implementation territory, not a gap in this specification.

VERDICT: CONVERGED
