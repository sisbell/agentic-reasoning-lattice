# Review of ASN-0036

I worked through the substantive proofs (S1, S4, S5, S7, OrdShiftHom, S8, D-CTG-depth, D-SEQ) and the contiguity machinery line by line, checked the boundary cases (empty arrangement, depth m=2 vs m≥3, singleton runs, j=m−1 empty fill-range), and ran the anti-bloat scan the classifier requested.

## REVISE

None. The proofs hold up under the checks that usually break this kind of note:

- **S8 (correspondence-run partition)** discharges every conjunct. The lockstep-successor `succ` is shown to be a partial function (out-degree ≤ 1) and injective + acyclic (in-degree ≤ 1, via TS2 at common depth and TS4 strict-increase), so the finite-graph chain decomposition is justified, not asserted. The displacement-identity induction correctly isolates the `i=0` boundary (where TS3's `n₁ ≥ 1` precondition fails) and routes it through the `shift(t,0):=t` convention. Partition is established in all four parts (empty, coverage, disjointness, finiteness), including the singleton run.
- **D-CTG-depth / D-SEQ** do not hand-wave the "share the middle components" step. The contradiction is built explicitly: a position disagreeing at a mid-component `j` forces (via T0(a) unbounded values + D-CTG) infinitely many distinct intermediates, contradicting S8-fin. The `m=2` vacuous-prefix case and the `j=m−1` empty fill-range are both handled.
- **S5** is correctly scoped as a non-entailment result over S0–S3 (a model exhibition); it does not need S4–S8 to hold in the witness, and the within-document and cross-document constructions are kept distinct rather than collapsed under "similarly."
- **S7** derives all four claims (well-definedness, identification, cross-document uniqueness, permanence) rather than stating them.
- The worked example exercises the lockstep identity at representative `k` (k=1, k=4) and, crucially, demonstrates run-*breaking* at the transclusion/append boundary in Σ₂ — the place where a weaker note would have glossed the gap.

Cross-ASN references are all to ASN-0034 (foundation) — permitted. No reinvented foundation notation.

Anti-bloat scan: clean. I found no forward-reference defenses, no "placed here to avoid circularity" justifications, no `Scope`/`Why-the-axiom-is-needed` sub-paragraphs, no downstream-consumer inventories in definition slots, and no duplicated paragraphs. The S7 permanence claim appears once as motivation and once as a proof step — that is motivation+proof, not duplication. Prior cycles appear to have already removed the meta-prose this classifier targets.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG / D-MIN / S2
The note defines `ValidInsertionPosition` but defers (correctly, per the Scope list and the final Open Question) the proof that INSERT/DELETE/COPY/REARRANGE preserve contiguity, including insertion onto an occupied V-position. This is the natural next ASN, not a defect here.

### Topic 2: Subspace alignment (`subspace(v) = v₁` vs. the element field of `M(d)(v)`)
Explicitly treated as an operations-layer obligation and listed in Open Questions. The strand state model imposes no such state-level invariant, which is internally consistent.

### Topic 3: Canonical choice of V-position depth `m`
The model fixes only `m ≥ 2`; the specific convention is left to the first-placing operation. Appropriate deferral.

VERDICT: CONVERGED
