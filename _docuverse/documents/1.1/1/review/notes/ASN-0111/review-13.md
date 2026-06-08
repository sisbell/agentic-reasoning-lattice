# Review of ASN-0111

I checked the definition, every RL claim, the wp analysis, and worked the example arithmetic and the orphan proof end-to-end.

## REVISE

None. The specification holds up under scrutiny on the points where ASNs of this kind usually fail:

- **Definedness / wp (RL0, RL7).** The single-state wp is correctly identified as trivial *because the read is stateless*, and the substantive wp is the temporal one (read after `Σ →* Σ'`), discharged by LP13's closure of both definedness and value-preservation across `→*`. The chain `readlink(a,Σ') = Σ'.L(a) = Σ.L(a) = readlink(a,Σ)` is explicit, not hand-waved. The distinction between L12 (single-step) and LP13 (closure) is correctly drawn — a common place to cheat, handled here.

- **N > 3 generalization (RL2).** The per-slot-copy argument genuinely establishes the arity-3 instance as standing in for `N ≥ 3`; since `readlink ≡ Σ.L(a)` returns all slots verbatim, no slot-count-dependent step exists. The abstract-reachability vs. udanax-green-realizability split is accurate against ASN-0093's `N ≥ 3` precondition.

- **Worked example.** Arithmetic verified: `a = [1.0.1.0.1.0.2.1]` has `zeros = 3`, `E = [2,1]`, `subspace_I = s_L`; `s ⊕ δ(2,8) = [1.0.1.0.1.0.1.3]`; `a' = inc(a,0) = [1.0.1.0.1.0.2.2]`. Coverage treated correctly as infinite interval (T1 case (ii)), not point-set.

- **Orphan proof (RL8).** The hardest argument, and it is sound. The `dom(C)` exhaustion via `#E = 2` (ChainDiscipline/FirstEmission) correctly rules out deeper subtree members; the `dom(L)` emptiness via T7 correctly restricts the universal to the `zeros = 3` intersection where `subspace_I` is defined (the subtlety that `subspace_I` is undefined on non-T4-valid deeper extensions is explicitly handled). All three slots dispatched against both stores, then closed via `ran(Σ.M(d)) ⊆ dom(C) ∪ dom(L)` (S3★).

- **Edge cases.** Undefined-at-non-member, empty connective slot, mandatory non-empty type, ghost type, nested link→link, cross-document endset, and orphaned link are all addressed. Self-reference is covered implicitly by RL6's link→link case.

- **Cross-ASN references.** All references (ASN-0034/0043/0047/0093/0098) are to foundation ASNs; no reinvented notation.

- **Scope.** Contrasts to follow/search are motivational; `discoverable_from` is used to *prove* RL8's orphan property, not to specify discovery. No out-of-scope operation is specified.

## OUT_OF_SCOPE

None to flag — the Open Questions section correctly defers durability-of-validity, empty-vs-unwitnessed distinguishability, and identity-vs-value distinguishability to future work rather than claiming them here.

VERDICT: CONVERGED
