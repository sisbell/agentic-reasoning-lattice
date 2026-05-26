# Review of ASN-0076

## REVISE

### Issue 1: Composite notation makes outputs look like inputs

**ASN-0076, "The Composite"**: "EDITLINK(ℓ_old, (e'_1, ..., e'_N), d_new, τ_sup) ≡ K.λ(d_new, ℓ_new, (e'_1, ..., e'_N)); K.λ(d_new, ℓ_sup, (E_from, E_to, E_type))"

**Problem**: K.λ in ASN-0047 does not take `ℓ` as an input — `ℓ` is determined by the allocator rule (first-emission or subsequent-emission predicate) from the current state. The notation `K.λ(d_new, ℓ_new, ...)` reads as if ℓ_new is passed in. A naive reader could conclude EDITLINK requires a free choice of ℓ_new, which would violate K.λ's allocation discipline. The body of the proof relies on ℓ_new being determined by the rule (not free), but the surface syntax misleads.

**Required**: Rewrite the composite definition with output-binding notation, e.g.:
```
Step 1: emit ℓ_new ← K.λ(d_new, (e'_1, ..., e'_N))
Step 2: emit ℓ_sup ← K.λ(d_new, (E_from, E_to, E_type))
```
making explicit that ℓ_new and ℓ_sup are produced by the K.λ rule, and that Step 2's endsets reference the ℓ_new produced by Step 1.

### Issue 2: Ownership prose unsupported by formalism

**ASN-0076, throughout (E6 prose, "On Identity," etc.)**: "Bob may assert that his link `ℓ_new` supersedes Alice's `ℓ_old`"; "anyone — not merely the original link's owner — may publish a supersession"; "Alice's link is untouched"; "Bob's claim is published in his own namespace, attributable to him, without Alice's participation."

**Problem**: The formal model has no ownership concept. K.λ's preconditions require only `d ∈ E_doc`; nothing in ASN-0047 or this ASN constrains *who* may invoke K.λ on which document. The prose builds intuition by assuming an ownership policy that the formalism does not impose, and E6 conflates "the model permits d_new ≠ home(ℓ_old)" (true, formally) with "anyone owning d_new may publish a claim" (which presumes an unstated authorization model).

**Required**: Either (a) explicitly label these passages as informal motivation grounded in an implementation-layer authorization policy that this ASN does not formalize, or (b) state the actual formal claim (d_new ∈ E_doc suffices; the question of who is authorized to fire K.λ on d_new is outside the abstract specification).

### Issue 3: E5 inductive hypothesis omits invariant preservation

**ASN-0076, E5 proof**: "For the inductive step, assume the inductive hypothesis: `Σ_{k-1}` contains `k-1` distinct supersession links..."

**Problem**: The hypothesis carries only the structural content (k-1 supersessions exist). The discharge of K.λ's preconditions at Σ_{k-1} (in particular `home(ℓ_old) ∈ Σ_{k-1}.M`) appeals to L1a evaluated at Σ_{k-1}, which requires Σ_{k-1} to satisfy the per-state invariants. This is true (each EDITLINK is ValidComposite★, which preserves invariants by ExtendedReachableStateInvariants), but the proof should carry "Σ_{k-1} satisfies the per-state invariants" explicitly as part of the inductive hypothesis. Without it, the step's "L1a applies at Σ_{k-1}" sub-step lacks an explicitly stated premise.

**Required**: Extend the inductive hypothesis to include "Σ_{k-1} satisfies all per-state invariants of ASN-0047's extended reachable state," and discharge this at the step via "Σ_{k-1} → Σ_k is a ValidComposite★ + ExtendedReachableStateInvariants closure."

### Issue 4: E2 proof structure is imprecise about intermediate states

**ASN-0076, E2 proof**: "By L12a (LinkStoreMonotonicity, ASN-0043), `dom(L) ⊆ dom(L_i)` at every intermediate state `L_i` along the chain leading to the K.λ step..."

**Problem**: For the first K.λ step there *is* no chain — it fires directly from Σ, so the monotonicity appeal is vacuous. K.λ's precondition `ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)` evaluated at Σ together with `ℓ_old ∈ dom(Σ.L)` (from EDITLINK's precondition) immediately gives `ℓ_new ≠ ℓ_old`. The L12a invocation is needed only for the second step (to carry ℓ_old ∈ dom(L) forward to Σ_1). The current proof conflates the two cases under one citation.

**Required**: Separate the two K.λ steps in the proof. Step 1: direct from K.λ's precondition at Σ. Step 2: L12a (or L12 applied to step 1) carries ℓ_old into dom(Σ_1.L), then K.λ's precondition at Σ_1 gives ℓ_sup ∉ {ℓ_old, ℓ_new}.

### Issue 5: E5 theorem statement leaves ℓ_old unbound

**ASN-0076, E5**: "For any state `Σ` satisfying all invariants and any natural number `k`, there exists a sequence of transitions `Σ →* Σ_k` such that `Σ_k` contains `k` distinct supersession links each naming `ℓ_old` in its from-endset..."

**Problem**: `ℓ_old` is referenced as if globally fixed but never bound in the theorem's quantifier. The proof later refers to "the outer hypothesis `ℓ_old ∈ dom(Σ.L)`" but this hypothesis is not stated in the theorem.

**Required**: Rewrite as "For any state Σ satisfying all invariants, any `ℓ_old ∈ dom(Σ.L)`, and any natural number k, there exists a sequence of transitions Σ →* Σ_k such that Σ_k contains k distinct..."

### Issue 6: ℓ_sup ≠ ℓ_old in E2 needs the post-step-1 state

**ASN-0076, E2 proof**: "The same argument applied to the second K.λ step (which sees both `ℓ_old` and `ℓ_new` in its pre-state link store)..."

**Problem**: The "same argument" is asserted but the second step has a distinct precondition state Σ_1 that contains *both* ℓ_old and ℓ_new. The L11a structural argument that follows ("More structurally: L11a...") is cleaner and doesn't require this case split; it should be the primary argument, with the per-step precondition argument as a corollary.

**Required**: Reorder the proof to lead with L11a (three distinct atomic K.λ events by SequentialTransitionAxiom; distinct events produce distinct addresses by L11a). The K.λ-precondition argument becomes redundant but can stay as a confirmation.

### Issue 7: Appendix conflates concepts deferred to future ASNs

**ASN-0076, "Appendix: An Illustrative Reader Procedure"**: The four-step procedure references "filter to those whose type-endset coverage matches a designated supersession address" (no convention exists), "read each candidate's to-endset to obtain a successor address" (no semantics fixed), and "optionally recurses on each successor" (no termination guarantee, since the supersession DAG isn't constrained — see Open Questions).

**Problem**: While the appendix is labeled illustrative, it presents a procedure as if compositions of the missing pieces would work, without flagging that the recursion has no terminating story (E5 admits arbitrary fan-out and the Open Questions admit cycles).

**Required**: Either (a) cut the appendix entirely (Open Questions already gesture at these), or (b) state explicitly that the sketched procedure is not known to terminate, is not known to be well-defined when the supersession structure is a DAG with cycles, and depends on conventions deferred to future ASNs.

### Issue 8: Element-field length preservation under inc(·, 0) is glossed

**ASN-0076, E0 successor-step proof**: "TA5(c) gives `#t' = #t` ... With `#t` and `zeros(t)` both preserved, T4b's field decomposition is identical between `t` and `t'`, so `#E(t') = #E(t)`."

**Problem**: T4b decomposes a T4-valid tumbler into N, U, D, E fields based on the positions of the three zeros. The argument claims that since #t and zeros(t) are preserved, the decomposition is identical — but TA5(c) modifies position sig(t). Need to argue that this position is in the element field (i.e., after the third zero), so the boundary positions of the four fields are unchanged. This follows from TA5-SigValid (sig(t) = #t for T4-valid t, so the modification is at the last position, which lies in the element field), but the proof doesn't cite this explicitly at this step.

**Required**: Add the citation: "By TA5-SigValid, sig(t) = #t, so the modification falls at position #t which lies in the element field. The three zero positions and the field boundaries are therefore identical between t and t', so T4b's decomposition is preserved, hence #E(t') = #E(t)."

## OUT_OF_SCOPE

### Topic 1: Resolution policy for divergent successors

**Why out of scope**: E5 establishes that multiple supersessions of the same original may coexist; the question of which successor is "current" is a reader-side policy decision. Already noted in Open Questions; properly belongs to a future ASN on link-discovery or reader policy.

### Topic 2: Supersession type convention

**Why out of scope**: The `τ_sup` parameter is treated as an external input; the convention pinning a particular address to mean "supersession" is explicitly deferred. Properly belongs to a future ASN on type-endset conventions.

### Topic 3: Counter-claims and supersession retraction

**Why out of scope**: E9 establishes that supersession links are themselves permanent under L12; the "retract via counter-claim" pattern is sketched but not formalized. Listed in Open Questions; properly a future ASN.

### Topic 4: Discovery operations on `covers(Σ, a)`

**Why out of scope**: E7 establishes only the structural witness; the operational realization of discovery — its termination, completeness, fairness across endset slots — is the proper subject of a link-search ASN.

### Topic 5: Multi-way supersession (one-to-many, many-to-one)

**Why out of scope**: This ASN fixes arity 3 for the supersession link, expressing only binary supersession. Variations (merge supersession, split supersession) are listed in Open Questions and properly belong to a future ASN.

### Topic 6: Authorization model

**Why out of scope**: K.λ's precondition is `d ∈ E_doc` only; who may fire K.λ on a given document is not constrained by the abstract specification. An implementation-layer ASN on authorization is appropriate but outside the abstract model.

VERDICT: REVISE
