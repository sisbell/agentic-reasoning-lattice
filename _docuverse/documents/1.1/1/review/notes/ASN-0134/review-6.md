# Review of ASN-0134

This is a careful, well-structured consistency model, and several things I went looking for are already handled: the first-emission boundary of the same-home collision (H2, §7) is treated explicitly rather than waved past; K.σ is scoped out of the conflict analysis deliberately and the scoping is justified; the worked scenario in §7 is arithmetically checked; and the two operation-level non-confluences are flagged rather than hidden under the step-level confluence of G1. The findings below are real, but mostly precision-level — except Issue 2, which is a genuine inconsistency with a foundation.

## REVISE

### Issue 1: A6's "per-state invariant package" includes invariants that are not per-state
**ASN-0134, A6 (CanonicalState)**: "Call a state *structurally canonical* iff it satisfies the per-state invariant package of the `→_sh` stack (ASN-0093's store invariants `C0`/`L12`/`SD`/`C1c`/`L1c`, …)."

**Problem**: `C0` and `L12` are *transition* invariants, not per-state predicates. From the foundation:
- `C0 = (A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a ∈ dom(C) : C'(a) = C(a)))`
- `L12 = (A Σ → Σ' : (A a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a)))`

Both quantify over a transition `Σ → Σ'`. A single state `Σ_k` cannot satisfy or fail them — they have no single-state form (the immutability content is inherently relational; the only single-state shadow is the trivial "C is a function"). So defining a *state* predicate ("structurally canonical") whose package includes `C0`/`L12`, and then asserting "Every state on `𝔼` is structurally canonical," is ill-typed. The remaining members (`SD`, `C1c`, `L1c`, `P6`, `P1`, `P2`, `R1`, `R2`) genuinely are per-state; the package is heterogeneous and mislabeled. Notably, A6's own proof already treats `C0`/`L12` correctly as transition invariants ("being quantified over steps, riding `B2`'s transition clause across each genuine `→_sh` step" / `RP-b`) — so the defect is in the *statement*, which the proof contradicts. This matters because A6 is the definition G1(i) and M1(a) lean on, and because A6's whole point is "what a reader sees at one index `Σ_k`" — and a reader cannot verify `C0`/`L12` from `Σ_k` alone (no-overwrite is W0's model-intrinsic property, not a snapshot's shape).

**Required**: Split A6 into a per-state conjunct (evaluated at `Σ_k`: `SD`, `C1c`, `L1c`, `P6`, `P1`, `P2`, `R1`, `R2`) and a transition conjunct (evaluated across the incoming step: `C0`, `L12`), with the quantifiers the proof actually uses; and rename "per-state invariant package" accordingly. Alternatively drop `C0`/`L12` from "structurally canonical" entirely and let W0 carry them, since they describe steps, not states.

### Issue 2: the BH4-age observability witness for the first non-confluence contradicts BH4's `idem = ⊥` requirement
**ASN-0134, §4 (first operation-level non-confluence)**: "two concurrent operations that are `idem = ⊤` with coverage-equal `(F, G)` … this *is* observable: `Observe_K` returns the survivor's address (`a` vs `a'`), and a home-relative behavior — BH4 `age`, denominated in the survivor's own home's traffic — reads differently across the two outcomes."

**Problem**: The scenario fixes `idem(K) = ⊤`. But BH4 (AgeStaleness) "**Applies to:** any shape, with `idem = ⊥`," and R-C0 makes it a construction-failing requirement: "age-staleness (BH4) requires `idem = ⊥`, with no shape clause." So BH4 cannot be attached to the very type `K` whose `idem = ⊤` emissions are racing — `age(a)` for the survivor (a `K`-tuple) is not a defined query on that type. The cited "BH4 `age` … reads differently" witness is therefore unavailable for this scenario. The *conclusion* (observability) still stands, because `Observe_K` returning `a` vs `a'` already establishes it — but the second witness is invalid as written, and reveals a tension worth stating: the only way `age` enters is *indirectly* (the survivor landing at home `d` rather than `d'` shifts `f_d`, perturbing `age(·)` of co-homed `idem = ⊥` tuples of *some other* type), which is a different claim than "age of the survivor."

**Required**: Remove the BH4 clause (the `Observe_K` witness is sufficient and correct), or rephrase it to the indirect effect — the survivor's deposit advances its home's chain frontier, shifting the age of co-homed `idem = ⊥` tuples — and make clear that age is read on those tuples' type, not on `K`.

### Issue 3: V2's "Q-affecting step" and the decomposition of `Q` are left undefined
**ASN-0134, §8 / V2 (VerdictReaderSnapshot)**: `Q` is "a predicate over states"; V2 then reasons about "`p ≥ 2` constituent `Observe_K` reads composing one `Q`" and a "*`Q`-affecting step* — one that changes the value of some conjunct of `Q`."

**Problem**: The soundness chain `[all reads at one index] ⟹ [no Q-affecting step between reads] ⟹ [sound]` is the central content of §8, and its middle term, "`Q`-affecting step," is the linchpin — yet it rests on an undefined decomposition. "Conjunct of `Q`" presumes `Q` is a conjunction of per-type predicates `Q = ⋀ Q_{K_i}`, but the realistic case the note itself cites (a verdict joining across types, "ASN-0128's `targets_keyed` already *joins across every Binary type*") need not be a conjunction. Likewise "a predicate over several types or homes" asserts that a multi-type/per-home `Q` is realized as `p` per-type `Observe_K` reads without showing how a per-home condition is recovered from the per-type surface. Without a definition of how `Q` is computed from the `p` reads, "`Q`-affecting" has no precise referent.

**Required**: State the realization model explicitly — `Q` is computed as `g(Observe_{K_1}(Σ_{r_1}), …, Observe_{K_p}(Σ_{r_p}))` for a combining function `g` over the `p` type-views — and define a `Q`-affecting step as one that changes some `Observe_{K_i}` value in the read window (dropping "conjunct," which over-specializes to conjunctions). The chain then holds for general `g`.

### Issue 4: §8's read-count dichotomy overstates the "otherwise" horn
**ASN-0134, §8**: "the `p` reads observe one state iff no foreign step at all interleaves among them, and `p` *different* states otherwise."

**Problem**: The second horn is false. The `p` zero-step reads sit at non-decreasing indices `r_1 ≤ … ≤ r_p`; a single interleaved foreign step yields exactly two distinct observed states, not `p`. With `p = 3` and one step between reads 1 and 2, the reads land at `{Σ_r, Σ_{r+1}}` — two states, not three. The count of distinct states is anywhere in `2..p` once any foreign step interleaves.

**Required**: Replace "`p` different states otherwise" with "possibly several (between 2 and `p`) distinct states otherwise." The downstream argument (soundness requires no `Q`-affecting step in the window) is unaffected.

## OUT_OF_SCOPE

### Topic 1: a completeness theorem for the operation-level non-confluences
The note identifies two operation-level non-confluences (idem=⊤ coverage-equal cross-home emissions; cross-home `Nullify`/emit race) and is careful to claim only that each is *necessary* for order-stability ("order-stable *only* absent both" = each is a genuine obstruction), routing M1's safety around both rather than relying on their joint absence. A *sufficiency* result — that the absence of both implies operation-level confluence, i.e. these are the only two sources — would require enumerating every way an operation's step/zero-step realization can depend on its linearization state. That is a worthwhile future characterization, but the present note neither needs nor claims it, so its absence is not a defect here.

VERDICT: REVISE
