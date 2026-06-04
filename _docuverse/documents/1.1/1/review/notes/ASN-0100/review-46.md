# Review of ASN-0100

## REVISE

### Issue 1: The "non-tight alternative" in the worked example imagines a case the example's own construction excludes

**ASN-0100, §A Worked Example (Projection-shift correspondence, "Non-tight alternative")**: "If `tight(e_1, Σ_{e_1})` does not hold … a freshly allocated `a_{new0}` or `a_{new1}` may land in `coverage(e_1)`. Then `N_I ⊆ {[1,3], [1,4]}` may be non-empty …"

**Problem**: For this example the fresh addresses are determined by K.α's subsequent-emission rule: `a_{new0} = inc(max{a' : origin = d}, 0) = inc([d.0.s_C.5], 0) = [d.0.s_C.6]` and `a_{new1} = [d.0.s_C.7]`. The endset's coverage is `[a_2, a_5) = [[d.0.s_C.2], [d.0.s_C.5])`. Since `[d.0.s_C.6], [d.0.s_C.7] > a_5` under T1 (last component 6, 7 > 5), both fresh addresses lie strictly above the coverage ceiling **for structural reasons (chain monotonicity), independent of tightness**. So `N_I = ∅` here no matter what, and the paragraph's premise ("may land in coverage") is impossible for the concrete addresses it names. The tight construction at `Σ_{e_1} =` pre-state guarantees the fresh chain continues past `a_5`, leaving the non-tight branch with no room.

**Required**: Either remove the non-tight alternative, or illustrate `N_I ≠ ∅` with a genuinely forward-extending endset whose coverage ceiling exceeds the chain frontier (e.g. span `(a_2, δ(10, #a_2))` covering `[a_2, [d.0.s_C.12])`, which would capture `a_{new0} = [d.0.s_C.6]`). As written, the paragraph is reviser drift: a counterfactual the example structurally forbids.

### Issue 2: §Cross-document independence applies single-step LP4/LP5 to the composite without chaining — contradicting the document's own later rigor

**ASN-0100, §Verifying the Invariants → Cross-document independence (Q3)**: "the projection from `d'` is unchanged … This is LP4 (ArrangementSpecificity; ASN-0098) applied to the unchanged `M'(d') = M(d')` together with LP5 … on the substrate's cross-document frame."

**Problem**: LP4 and LP5 (ASN-0098) are single-step lemmas ("for every transition `Σ → Σ'`"). INSERT is a `2n+1`/`2n+2`-step composite. The later §Coverage and link discoverability ("For `d' ≠ d`") explicitly recognizes this: "LP4 … and LP5 … are single-step lemmas …, so we must chain them rather than cite them once," and then chains across each elementary step. The earlier §Cross-document independence cites the same lemmas one-shot for the composite, which is exactly the gap §Coverage warns against. The same fact is thus discharged twice at two different rigor levels, and the earlier treatment is under-rigorous by the ASN's own standard.

**Required**: Either delete the redundant §Cross-document independence derivation and forward-point to the chained §Coverage argument, or give the chaining inline. A one-shot LP4/LP5 citation for a composite is not a proof.

### Issue 3: Presentation meta-prose around the non-import principle

**ASN-0100, §Discovering the Three Effects → Effect Three ("The foundation's frozen-store frames do not transfer")**: "We state this non-import principle once here; the sections below re-derive silently rather than re-explain it."

**Problem**: This sentence justifies document organization rather than advancing the argument (anti-bloat: prose justifying presentation ordering). The substantive content — that I3-C/I3-S7/I3-S3 rest on the failed `Σ'.C = Σ.C` frame, so S2/S3★/S8a/S8-depth/S8-fin/S7 are re-derived — is the load-bearing part and is fine; the meta-commentary about how the rest of the document will handle it is not. The same redundancy recurs in the INS.inv.refint claim row ("re-derived directly (not via I3-S3 …)").

**Required**: Drop the presentation-justifying clause; keep only the object-level statement that the frozen-store frames fail and which invariants are re-derived.

## OUT_OF_SCOPE

### Topic 1: Recovery to canonical order after partial composite failure
**Why out of scope**: Listed in the ASN's own Open Questions; concerns implementation crash-recovery, below this ASN's abstraction level.

### Topic 2: Self-composition closure of INSERT (`Σ →INSERT→ Σ_1 →INSERT→ Σ_2`)
**Why out of scope**: A legitimate algebraic question about the operation family, but a distinct property belonging to a later compositional ASN, not a defect in the per-operation specification given here.

VERDICT: REVISE
