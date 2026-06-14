# Review of ASN-0134

## REVISE

### Issue 1: V2's soundness justification contradicts the note's own worked trace

**ASN-0134, §8 (the paragraph establishing V2)**: "A foreign writer step that is not Q-affecting (a content allocation `K.α`, or an emission into a type none of `Q`'s `p` reads consults) advances the index, scattering the reads across distinct `Σ_{r₁},…,Σ_{r_p}`, yet **leaves every constituent `Observe_{K_i}` reading identically wherever it lands** — so `g`'s arguments are unchanged and the verdict still equals `Q`."

**Problem**: A step is *Q-affecting* only when it "changes the value of some constituent `Observe_{K_i}` whose read **has not yet been taken**." So a non-Q-affecting step may freely change an *already-read* constituent — and then it does **not** "leave every constituent reading identically." The note's own worked trace exhibits exactly this: the `K₁`-emit between the two reads "flips `A_{K₁}` from `∅` to `{T₁}`" yet is correctly classified "**not** Q-affecting" because "`K₁` was *already read* at `r₁`." The general justification ("every constituent identical") is the *narrow* reason that covers only steps changing no constituent at all (the two parenthetical examples); it is falsified by the very mechanism the trace relies on. The conclusion (sound ⟸ no Q-affecting step) is correct, but the stated reason is not the reason.

**Required**: Reword the justification to match the definition: a non-Q-affecting step leaves every *not-yet-read* constituent unchanged; already-read constituents may change but are *banked*. Then for each `i`, no step between `r₁` and `r_i` changes `Observe_{K_i}` (such a step would be Q-affecting), so `v_i = Observe_{K_i}(Σ_{r_i}) = Observe_{K_i}(Σ_{r₁})`, hence the verdict `= Q(Σ_{r₁})`. That is the argument that actually covers the trace.

### Issue 2: G0 equates a single total order with sequential consistency

**ASN-0134, §3, G0**: "The substrate realizes a single total order of atomic steps (`SequentialTransitionAxiom`); **equivalently, it is sequentially consistent.**"

**Problem**: A single total order of steps is *serializability* (a serial order exists), not sequential consistency. SC additionally requires the order to preserve **each agent's program order**. The note never models per-agent program order, never shows `𝔼` preserves it — and its own thesis runs the other way: G1 advertises freedom to reorder `≺`-incomparable cross-home steps, which would reorder a single agent's cross-home operations, *violating* program order. So under the per-home-minimal schedules the note recommends, a realization need not be sequentially consistent at all. "Equivalently, it is sequentially consistent" therefore equates two non-equivalent properties, and the equivocation is not academic — it is in tension with the note's central liberation result.

**Required**: Either retreat to "a single total order (serializability)" and drop the SC label, or define the program order the substrate is claimed to preserve and reconcile it with G1 — e.g. state explicitly that cross-home operations of one agent carry no program-order obligation, so SC degenerates to serializability here. As written G0 asserts a named property whose defining clause is neither stated nor discharged.

### Issue 3: W5's "simply rejected" omits the self-emit branch of P-tgt

**ASN-0134, §5, W5**: "each `Nullify` evaluates its target precondition `P-tgt` at its own linearization state — so a **nullify ordered before its target exists is simply rejected** (the target is not yet a link address), never producing a dangling retraction."

**Problem**: `P-tgt` is `a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr)`. A pre-target nullify is rejected only when it targets *another* home's not-yet-emitted address. In the self-emit branch — `a = a_emit(Σ, d_retr)`, the retractor's own frontier slot — `P-tgt` holds via the second disjunct and the nullify **fires**, depositing a self-nullified R-tuple at `b = a_emit(Σ, d_retr) = a`. It is not rejected. The "never dangling" conclusion does survive (the tuple lands at `a` and nullifies itself), but the stated mechanism is wrong precisely at the boundary case the foundations single out, and W5's general phrasing ("simply rejected") is the cross-home use case smuggled in as a universal.

**Required**: Qualify W5 — a pre-target nullify *of another's address* is rejected; a *self-emit* nullify of the retractor's own frontier slot fires and pre-nullifies. Neither dangles, but only the first is a rejection.

## OUT_OF_SCOPE

The note's deferrals are correctly placed: read-side batch atomicity (Open Questions 3, 5), cross-server composition of per-home orders (OQ 7), and the weakest primitives realizing the MIC clauses (OQ 1, 2, 3, 8) are genuine future territory, not gaps in this note. No additional out-of-scope items to record — the note's self-scoping is adequate, and its abstention from scheduler/fairness, rule bodies, BEBE, and performance is consistent with the declared scope.

VERDICT: REVISE
