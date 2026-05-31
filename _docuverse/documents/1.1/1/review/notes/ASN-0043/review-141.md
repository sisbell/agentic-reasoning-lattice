# Review of ASN-0043

I checked every L-invariant proof, the local lemmas (CPP, FSP, FSE, PrefixSpanCoverage), the L9/L11b extension constructions, and recomputed the entire six-step worked example by hand. I also scanned specifically for the forward-reference/meta-prose accretion patterns flagged for this note.

## REVISE

None. The proofs hold up under the checks that matter here:

- **CPP** correctly separates the child-spawn branch (TA5(b) agreement on `1..#tᵢ₋₁ ⊇ 1..p`) from the sibling-advance branch (TA5(c)/TA5-SigValid place the modified `sig` strictly beyond `p`), with the `#tᵢ₋₁ > p` precondition explicit rather than smuggled.
- **L1c's `s = home(a)`** derivation is sound: the `(kᵢ=2 ⟹ zeros(tᵢ₋₁) ≤ 2)` guard plus `zeros(a)=3` forces `k₁` to be the unique separator-seating step, fixing the third zero at `#s+1`; FSP restates the same argument in fuller form, and the two presentations agree.
- **FSP** discharges each state-local invariant for the single added entry; `Σ'.C=Σ.C`/`Σ'.M=Σ.M` carry the ASN-0036 invariants verbatim, and L0b follows from preserved L1c.
- **L9 Case A/B**, **FSE**, and **L11b** chain together correctly; the `inc(·,0)` enumeration is infinite by T10a.7, finite `dom(Σ.L)` by L-fin yields a fresh sibling, and home/subspace/depth are preserved.
- **PrefixSpanCoverage** mutual-inclusion proof handles both the `k<m` and `k=m` subcases at the divergence position; the L8 coverage-vs-decomposition crux (Step 6: `Θ_split` vs `Θ_single` both cover `[g,h)`) is verified by adjacent-interval union, not hand-waved.
- Worked-example arithmetic recomputes exactly: `c₁⊕δ(1,8)=c₂`, the L1c chain `inc(d,2)→inc(·,0)→inc(·,1)=a`, and the L10 cone `g ∈ [p, 1.0.1.0.1.0.4)` all check.

On the anti-bloat mandate: the apparatus around L1c (CPP, DocVal, L0b) and the FSP/FSE factoring are load-bearing and reused across L9/L11a/L11b — this is DRY factoring, not accretion. I found no document-ordering justifications, no use-site inventories in definitions, and no duplicated paragraphs restating the same claim. The L5/L8 "singleton case" notes at Σ honestly flag that the static state cannot witness the substantive content and discharge it in the extension steps.

## OUT_OF_SCOPE

### Topic 1: Unconditional content/link disjointness
The disjointness `dom(Σ.L) ∩ dom(Σ.C) = ∅` is scoped to the `s_C`-resident slice because no invariant forces content into `s_C`. Lifting this requires a new content-side subspace-constant invariant in ASN-0036, which the note already records as an Open Question. This is future territory, not a defect here.

VERDICT: CONVERGED
