# Review of ASN-0101

## REVISE

### Issue 1: D1 justification cites wrong lemma in the order-preservation step

**ASN-0101, D1 Justification**: "By T1 (a) irreflexivity, v₁ < v₂ gives v₁ ≠ v₂; the contrapositive of TS2 (ShiftInjectivity, ASN-0034) then yields u₁ ≠ u₂ from shift(u₁, n) = v₁ ≠ v₂ = shift(u₂, n)."

**Problem**: TS2 is "shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂"; its contrapositive is "v₁ ≠ v₂ ⟹ shift(v₁, n) ≠ shift(v₂, n)" — going from input inequality to output inequality. The step actually used goes the other direction (output inequality to input inequality), which is the contrapositive of *function equality* ("u₁ = u₂ ⟹ shift(u₁, n) = shift(u₂, n)"), not of TS2. TS2 *is* correctly cited earlier in D1 for the well-definedness of σ_d as inverse; the misattribution here is in the order-preservation paragraph.

**Required**: Replace "the contrapositive of TS2" with "function equality (distinct outputs imply distinct inputs since shift is a function)" or simply drop the citation as a triviality.

### Issue 2: Boundary case enumeration has unacknowledged overlap

**ASN-0101, Boundary cases**: The cases "Singleton interior deletion (n = 1, 1 < p < n_S)" and "Non-singleton interior deletion (n ≥ 1, 1 < p, p + n − 1 < n_S)" both admit n = 1 with 1 < p < n_S — they overlap.

**Problem**: The section earlier notes that "Singleton subspace deletion ... is a specialisation of the empty post-state case above," signalling the convention that overlaps should be flagged. The singleton/non-singleton interior overlap is not noted, leaving the reader to wonder whether the cases form a partition.

**Required**: Either disambiguate (e.g., "Non-singleton interior deletion (n ≥ 2, ...)") or add a parenthetical noting that singleton interior is the n = 1 specialisation of the non-singleton case.

### Issue 3: D10 promotes K.σ alongside DEL, exceeding ASN-0101's charter

**ASN-0101, D10 vocabulary note**: "We promote K.σ alongside DEL because downstream specifications that invoke 'ValidComposite★ chains' should range over the full substrate vocabulary; K.σ's promotion carries no independent burden of proof..."

**Problem**: ASN-0101's stated subject is the DELETE operation. K.σ is an ASN-0093 substrate operation introduced after ASN-0047's ValidComposite★ was defined; its promotion is a substrate housekeeping issue independent of DELETE. Bundling it into D10 muddles the ASN's scope.

**Required**: Either split K.σ's promotion into a separate item attributed to ASN-0093 housekeeping, or remove the K.σ discussion from D10 and confine D10 to DEL.

### Issue 4: Notation Ρ is visually indistinguishable from Latin P

**ASN-0101, D0 effect**: "The capitals Λ (Greek lambda) and Ρ (Greek rho) are chosen to avoid notational collision with the link store Σ.L and the provenance relation Σ.R."

**Problem**: Greek capital Ρ is visually identical to Latin P in every common font. A reader rendering the ASN on a typical terminal or PDF cannot distinguish Ρ from P; the explicit note documents the intent but does not eliminate the ambiguity at the point of use. This is load-bearing because Ρ appears in many subsequent claims (D1, D9, D11) where a reader may wonder whether "P" means region-Ρ or some other P.

**Required**: Switch to a typographically distinct symbol (e.g., `R_right`, `Σ_R`, or a subscript like `V_>`).

## OUT_OF_SCOPE

None. The ASN's "Scope" section properly excludes INSERT/COPY/REARRANGE, link semantics, versioning, and BEBE replication. The "note on recoverability" discusses J4 ForkComposite contextually without making normative claims about versioning, and the "boundaries the abstract specification does not cross" section explicitly disclaims implementation-level concerns.

VERDICT: REVISE
