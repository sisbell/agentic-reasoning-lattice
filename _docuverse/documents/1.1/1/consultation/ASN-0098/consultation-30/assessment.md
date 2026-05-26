# Channel Assignment — ASN-0098 review-30

**Date:** 2026-05-26 07:08

```
## Issue 1: Working reference frame remark omits LP12b
Reason: Internal consistency fix — LP12b's link-subspace dependencies (S3★, L0, the subspace-partitioned retention pattern) are already documented in its own proof within this ASN, so determining whether it belongs in the "non-surviving" list is a self-contained check against the ASN-0036 base frame's vocabulary as already characterised here.
```

```
## Issue 2: LP19 hypothesis notation type-mismatched
Reason: Pure notational/formalism fix — choosing between graph-subset notation or quantifying over V-positions with `a_new := Σ_{n+1}.M(d)(v_new)` is decidable from standard mathematical convention and the existing arrangement-as-partial-function definition in this ASN.
```

```
## Issue 3: Non-canonical parenthetical in achievability discussion is too narrow
Reason: Internal consistency fix — the three grounds of non-canonical exclusion are fully classified earlier in the same section, so updating the parenthetical to match (or removing the restriction) is a local text-alignment task derivable from the ASN's own content.
```

```
## Issue 4: Sub-case B's "T1 case (i) at position #s" elides the k = k_s sub-case
Reason: Internal proof correction — splitting into the four sub-cases (a) k = k_s via T3, (b)–(d) via T1 case (i) against s or s ⊕ ℓ uses only ASN-0034 foundational definitions already cited throughout the LP-Fin proof.
```

```
## Issue 5: Worked trace e₁ omits explicit account of shift(i₁, 4) in coverage
Reason: Internal exposition fix — either narrowing ℓ to δ(4, #i₁) or explicitly declaring ran(Σ.M(d₁)) = {i₁, …, i₄} is a local choice about how the worked example is set up; both options are derivable from the ASN's own chain-element framework.
```

```
## Issue 6: "ground (iii) for #ℓ > #s" — non-tightness not fully argued
Reason: Internal design-of-predicate decision — the choice between (a) supplying a finitude argument for #ℓ > #s or (b) declaring the tightness predicate's domain to definitionally exclude all non-canonical spans is a local definitional choice within this ASN, independent of Ted Nelson's design intent or udanax-green behaviour.
```
