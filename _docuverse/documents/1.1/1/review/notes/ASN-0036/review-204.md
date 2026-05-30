# Review of ASN-0036

I checked every claim against its proof, ran the worked example through the displacement arithmetic, and tested the boundary cases (empty arrangement, single-position run, depth-2 vs depth-≥3 contiguity, the transclusion/append run break). The proofs hold up. Below I record where I looked hardest, then the future-territory items.

## Verification notes (no action required)

- **S8 (correspondence-run partition).** The lockstep-successor construction is sound: `succ` is a partial function (out-degree ≤ 1), injective via TS2 at common depth (in-degree ≤ 1), and acyclic via TS4 + T1 irreflexivity, so the finite graph decomposes into disjoint simple paths. The displacement-identity induction correctly isolates the `i = 0` case (inner shift amount 0, outside TS3's `n₁ ≥ 1` precondition) and discharges it by the `shift(t,0) := t` convention rather than misapplying TS3. The empty case, single-element run, and forward/backward maximality are all handled explicitly. No hand-wave.
- **D-CTG-depth.** The reductio (build infinitely many intermediates `w` differing at component `j+1`, contradict S8-fin) correctly verifies `w` satisfies S8a before invoking D-CTG's consequent, and uses T0(a) to manufacture the unbounded sequence. Correct.
- **Boundary coverage.** Empty-document base case for D-CTG/D-MIN verified vacuously; depth-2 and depth-≥3 contiguity violations both exhibited in the worked example; the run break at the transclusion/append boundary (`…1.5` vs `…2.1`) confirms runs are maximal, not merely contiguous.
- **Cross-ASN discipline.** All external references are to ASN-0034 (foundation) and are used, not reinvented. No non-foundation ASN is cited by number.
- **Anti-bloat scan.** I looked for the flagged patterns — forward-reference deferrals, "why the axiom is needed" sub-paragraphs, use-site inventories in prose, duplicated paragraphs. The dense per-step attributions in the S7 well-definedness paragraph follow the established foundation citation convention rather than accreting meta-prose, and I found no labeled rationale sub-paragraphs or in-body forward-reference chains. The note reads clean; prior cycles appear to have already trimmed the accretion the classifier targets.

## OUT_OF_SCOPE

### Topic 1: Subspace alignment between V-position identifier and I-address element field
The arrangement maps a V-position `v` (with `subspace(v) = v₁`) to an I-address `a` with `zeros(a) = 3`, but no state-level invariant ties `v₁` to the first element-field component of `a`. The note correctly defers this to the operations layer (final Open Question).
**Why out of scope**: Establishing alignment is a per-operation preservation obligation (INSERT/COPY produce the V-positions), and operation frame conditions are explicitly scoped out.

### Topic 2: Strength of the S5 independence result
S5 proves unrestricted sharing is consistent with **S0–S3** only; it does not show consistency with the full strand model (S7b, S8-fin, D-CTG, etc.). The claim is correctly scoped as written, but a future result could strengthen it to the full invariant set.
**Why out of scope**: This is a stronger independence theorem, not a defect in the present claim — the postcondition asserts exactly "model of S0–S3," and the construction delivers it.

VERDICT: CONVERGED
