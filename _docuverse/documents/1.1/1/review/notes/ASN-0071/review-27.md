# Review of ASN-0071

## REVISE

### Issue 1: `actionPoint(ℓ) ≥ 2` analysis imagines a case its sibling precondition already excludes

**ASN-0071, The query**: "(A displacement with `actionPoint(ℓ) = 1` at a deeper anchor, such as `u = [1, 5]` with `ℓ = [2, 0]` where `actionPoint = 1 ≠ 2 = #u`, is *already* rejected by `actionPoint(ℓ) = #u` and so cannot witness what `actionPoint(ℓ) ≥ 2` contributes.)"

**Problem**: This is reviser-drift meta-prose. The paragraph constructs a displacement, then notes the carrier precondition `actionPoint(ℓ) = #u` already excludes it — so the example witnesses nothing and exists only to argue about what one precondition "adds" relative to another. Given `actionPoint(ℓ) = #u`, the constraint `actionPoint(ℓ) ≥ 2` is *equivalent to* `#u ≥ 2`; the entire multi-clause analysis of "the sole thing `actionPoint(ℓ) ≥ 2` adds is the floor `#u ≥ 2`" is justifying the existence of a precondition rather than stating it.

**Required**: State the precondition (`#u ≥ 2`, or both forms) and drop the analysis of what each clause contributes, including the excluded-case parenthetical.

### Issue 2: Numeric worked examples duplicated between "The query" and the worked scenario

**ASN-0071, The query** (interior-action-point): "consider a source `d_s` of common depth `m = 3` ... `σ' = ([s_C, 1, 2], ℓ')` ... `σ'' = ([s_C, 1, 2], δ(1, 3))` ..." and (cross-depth) "suppose the user submits a *shallow* vspec `u = [s_C, 1]`, `ℓ = δ(1, 2)` ..."

**Problem**: Both numeric examples are then re-run concretely against `d_E` in the worked scenario ("Interior action point, rejected against an arrangement" and "A cross-depth query"). The "The query" section even admits its versions are abstract — "the `#u ≥ 3` case the depth-2 worked scenarios below cannot exercise" — so it pre-stages worked examples that the worked-scenario section repeats against a live arrangement. Two passages carry the same `σ'/σ''` and shallow-vspec computations.

**Required**: Keep the numeric demonstrations in the worked scenario (against `d_E`) and reduce the "The query" treatment to the abstract discrimination (depth-wise descent permitted vs breadth-wise sweep forbidden) without the standalone numeric instances.

### Issue 3: Subspace confinement proven twice with mutually-deferring prose

**ASN-0071, The query / Resolution**: PC is proven in full in "The query" ("its position-1 instance `t₁ = u₁` is the base case the Resolution section reuses"), then "Resolution" re-derives the same position-1 fact ("This is the position-1 instance of prefix confinement (PC), spelled out here for the routing argument").

**Problem**: Two paragraphs in different sections establish the identical fact (`t₁ = u₁`) and each points at the other. The position-1 TumblerAdd/T1 argument appears verbatim in both places.

**Required**: Prove PC once; in "Resolution" cite the position-1 instance of PC and apply S3★, without re-running the TumblerAdd/T1 derivation.

### Issue 4: Forward-reference pointers and defensive precondition justification

**ASN-0071, multiple**: "We rely on this property in the codomain argument below."; "(justified below)" (F-FILT); "the depth-2 worked scenarios below cannot exercise"; and in F-find — "P1 makes the gap benign only under that ordering, which the type signature does not enforce, so the precondition must be stated rather than assumed."

**Problem**: The first three are use-site forward pointers the reader must skip. The last explains *why* the precondition is stated rather than *what* it requires — defensive meta-prose around a precondition.

**Required**: Remove the forward pointers; state the `wp-defined` precondition and its content directly without the justification for its presence.

### Issue 5: Home-vs-transcluding distinction restated in three places

**ASN-0071, A worked scenario / Discovery through sharing**: The "find does not distinguish home from transcluding; recover via `origin(a)`" point appears as the worked-scenario "Home/transcluding recovery" bullet, then again in "Discovery through sharing" ("The find operation does not distinguish home from transcluding document"), then a third time in the same section ("The result does not, on its own, distinguish *how* each reported document references...").

**Problem**: The same guarantee and the same `origin(a)`-comparison recovery recipe are stated three times across two sections.

**Required**: State the recovery recipe once; the other occurrences should reference it rather than re-derive it.

## OUT_OF_SCOPE

### Topic 1: Historical-containment (`R`-based) query operation
**Why out of scope**: The Open Questions correctly defer the `R`/history query to a separate operation; ASN-0071 specifies only current-state `find`. The currency-vs-history contrast it draws is adequate framing, not a gap.

### Topic 2: Visibility filtering and replica consistency
**Why out of scope**: Access-control post-filtering and distributed-replica completeness are correctly listed under "What we do not specify" and the Open Questions as separable specifications.

VERDICT: REVISE
