# Review of ASN-0111

I checked every claim against the foundations, verified the worked example arithmetic, and dispatched the boundary cases (empty to-set, ghost type, orphaned link, link→link nesting, arity N>3).

## REVISE

(none)

The proof obligations are discharged completely:

- **RL0/RL7 wp.** The ASN does not hide behind a trivial single-state wp — it states plainly that the read is stateless so the single-state wp *is* the precondition, then supplies the substantive composite wp (`Σ →* Σ'` then read) and grounds it in LP13 rather than the single-step L12. The L12-vs-LP13 distinction is exactly the multi-step lift a careful reader would demand, and it is made explicit.
- **Worked example checks out.** `home(a)`, `subspace_I(a)=s_L`, `[1.0.1.0.1.0.1.1] ⊕ δ(2,8) = [1.0.1.0.1.0.1.3]`, the half-open interval / subtree reading by T1 case (ii), the `inc(a,0)=[1.0.1.0.1.0.2.2]` sibling, and the canonical reflexive span all compute correctly. The content-I-address count inside `coverage(F)` (two under d₁ from n=2, one under d₂ from n=1) is consistent with LP-Fin.
- **RL8 orphan dispatch.** Discoverability is refuted slot-by-slot via LP12 (from-set unwitnessed by hypothesis, empty to-set trivially, ghost type via S3★) — not by "similar reasoning." The `coverage(Θ) ∩ ran(Σ.M(d)) = ∅` conclusion holds (the ghost document hosts no content, and the subtree's element field forces s_C so it cannot meet `dom(Σ.L)` either).
- **RL5** correctly refuses the tempting overstatement that only the type slot may name empty addresses, citing L4/L9 — a genuine correction, not a hand-wave.
- **Cross-references** are confined to foundation ASNs (0034, 0043, 0047, 0093, 0098); Nelson "LM" citations are primary-source, not ASN cross-refs.

## OUT_OF_SCOPE

The Open Questions correctly defer follow/search/count semantics and cross-state validity guarantees to neighbouring operations (FOLLOWLINK, ASN-0110, etc.), and the ASN does not smuggle any of those into its claims. Nothing to flag.

The ASN defines state (`Σ.L`), an operation (`readlink`), and invariants on the returned structure (RL-WF, RL-ARITY, RL-GEN, RL-REP) stated abstractly enough to bind any implementation. No drift.

VERDICT: CONVERGED
