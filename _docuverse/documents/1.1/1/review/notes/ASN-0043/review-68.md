# Review of ASN-0043

## REVISE

(No REVISE items. The ASN is rigorous, the proofs are explicit, edge cases are handled, and the worked example exercises all state-local invariants across multiple state extensions.)

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage axiom belongs in a future span/tumbler-algebra ASN

**Why out of scope**: The identity `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}` has no link-specific content — it is a pure span/tumbler algebra fact about prefix coverage of unit-depth spans. The author has explicitly axiomatized it with a "pending relocation" annotation and provides a derivation sketch through PrefixRelation, OrdinalShift, T1, Divergence, and NAT-discrete. The properties table labels it "axiomatized pending relocation to span/tumbler-algebra ASN," and the Open Questions section flags the same. The fact belongs in a future span/tumbler-algebra ASN where it can be derived from foundations rather than axiomatized in-place. The interim axiomatization is a reasonable scope decision recorded in memory (`span-algebra-gap.md`).

### Topic 2: L0a content-subspace scope absorption requires a future ASN-0036 revision

**Why out of scope**: L0a scopes the content/link disjointness to the `s_C`-resident slice (`dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`) because ASN-0036's S-invariants do not fix a global content-subspace constant. The author has explicitly flagged this for future absorption: "A future ASN-0036 revision that fixes a content-subspace constant would lift L0a's scope from '`s_C`-resident slice' to 'all of `dom(Σ.C)`' without requiring changes to this ASN's other claims." The scope limitation is honestly disclosed in the L14 statement ("disjoint over the `s_C`-resident slice"), the L14a derivability discussion (where the joint argument from L0+L0a is explicitly noted as `s_C`-regime-only), and the Open Questions section. The scope lift is mechanical once ASN-0036 fixes the constant.

VERDICT: CONVERGED
