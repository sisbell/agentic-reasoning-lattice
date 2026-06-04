# Review of ASN-0091

## REVISE

### Issue 1: First worked example — incorrect composite-boundary witnesses
**ASN-0091, "Worked Example" (final bullet, composite-boundary properties)**: "`Contains_C(Σ') = {(a₂, d), (b₁, d), (a₁, d)} = Contains_C(Σ) ⊆ Σ.R = Σ'.R` for P4★, and `(b₁, d), (a₁, d'), (a₂, d') ∈ Σ'.R covering the three displayed content addresses for P7a.`"

**Problem**: Two errors.
- `Contains_C` (ASN-0047) ranges over *all* documents, not just `d`. The setup says "`Σ.M(d')` populates its own content subspace," so `Contains_C(Σ')` necessarily contains `d'`'s content pairs too. The displayed equality `Contains_C(Σ') = {(a₂,d),(b₁,d),(a₁,d)}` is therefore false as written.
- The P7a witnesses `(a₁, d')` and `(a₂, d')` are not justified by the stated setup. The setup leaves `Σ.M(d')` "immaterial" and never establishes that `d'` ever contained `a₁` or `a₂` in its content range, which is what a provenance record `(a₁, d')` would require. The witnesses that *are* guaranteed are `(a₁, d), (a₂, d), (b₁, d)`: these I-addresses sit in `d`'s content range at Σ', so by P4★ (`Contains_C(Σ') ⊆ R`) they lie in `Σ'.R`.

**Required**: State the P4★ check as `Contains_C(Σ')` restricted to `d` equals the three displayed pairs (or include the `d'` pairs and note they are framed-invariant under RE-other), and use the `(·, d)` provenance witnesses guaranteed by P4★ for P7a — or explicitly add to the setup that `a₁, a₂` were allocated into `d'`'s own content arrangement so `(a₁, d'), (a₂, d') ∈ R` is justified.

### Issue 2: Binary-transition-invariant enumeration omits P3
**ASN-0091, "State-Component-Only Invariants"**: "The class — ASN-0036's S0, S1; ASN-0047's P0, P1, P2, L12; ASN-0093's M1, C0 — is therefore discharged uniformly by RA-frame, with no per-invariant argument required."

**Problem**: This presents itself as the complete class of binary (Σ → Σ') invariants, but ASN-0047's **ExtendedTransitionInvariants** delivers **P3** (ArrangementMutabilityOnly), which is also a `(A Σ → Σ' :: …)` invariant the REARRANGE transition must satisfy. It is not listed. (It is in fact trivially covered by the same RA-frame equalities, since P3's conjuncts constrain C, L, E, R with monotonicity/value-preservation — all fixed.) But the enumeration claims completeness, and P3 is absent.

**Required**: Add P3 to the enumerated class, noting it is the synthesis P0 ∧ P1 ∧ P2 ∧ L12 and so discharged by the same principle.

### Issue 3: Forward-reference accretion (anti-bloat)
**ASN-0091, end of "Run Decomposition Is Not Invariant"**: "Fragmentation is exhibited concretely in the Worked Example below (the RE-frag bullet), where a 3-cut pivot raises the content-subspace run cardinality from 2 to 3."

**Problem**: A standalone forward pointer to a downstream worked example that advances no reasoning at its site — the kind of use-site/forward-reference prose the anti-bloat classifier targets. The RE-frag claim is already proved as an existential by the surrounding paragraph; the existence of a later illustration does not need announcing here.

**Required**: Delete the sentence. The worked example stands on its own; readers reaching it will see it exercises RE-frag.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
The ASN restricts REARRANGE_K cuts to the content subspace (CS3) and leaves the link subspace fixed (RE-sub). The Open Questions correctly defer link-subspace reordering to a future ASN; this is new territory, not a gap in ASN-0091.

### Topic 2: Joint reconstitution of fragmented transcluded spans
The ASN proves each fragment retains its origin (RE-origin) but explicitly declines to establish whether two fragments *jointly reconstitute* the original source span. This is a legitimate future question (first Open Question), not an error here.

VERDICT: REVISE
