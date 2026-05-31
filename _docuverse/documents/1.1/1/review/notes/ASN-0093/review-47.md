# Review of ASN-0093

This note is technically sound — the sub-allocator chain machinery, the freshness split (within-document / cross-document / cross-subspace), the simultaneous induction, and the worked example all check out, and the C1b/L1b element-field-depth preservation arguments (TA5(b) + TA5-SigValid + B5a) are correct. The findings below are all of the kind this `review-mode.anti-bloat` cycle targets: the same constructions stated three times over, deferral-and-repeat, and justification asides that do not advance any claim.

## REVISE

### Issue 1: The anchor/chain construction is derived three times — and the third derivation both defers to and repeats the first
**ASN-0093, "Discharge of stated invariants" matrix (C1c/L1c rows) and "C1c chain exhibition" / "L1c chain exhibition"**: the matrix cell reads "Discharged at new key via the T10a-conforming step sequence (see *C1c chain exhibition* below — first-emit and subsequent-emit cases)", and the exhibition below then says "Per-step admissibility of both steps `t₁ = inc(d, 2)` and `t₂ = inc(b_C(d), 1)` is the *anchor-construction admissibility* established in the FirstEmission lemma" — and *then re-states the structural forms anyway* ("TA5(d) at `k = 2` gives `zeros(t₁) = 3`...").
**Problem**: The construction `d → b_C(d) → [d.0.s_C.1]` (with its TA5a side conditions) appears in full in (a) the FirstEmission lemma's "Anchor-construction admissibility" block, (b) the C1c/L1c chain exhibitions, and (c) every relevant worked-example step. The chain exhibition simultaneously defers ("is the anchor-construction admissibility established in the FirstEmission lemma") and repeats the derivation it just deferred. This is the deferral-and-repeat pattern; the reader is sent to FirstEmission only to find the same steps re-spelled in place.
**Required**: Pick one home for the anchor-construction admissibility (the FirstEmission lemma). In the chain exhibitions, cite it once and state only what is *new* there (the chain index bookkeeping and the strengthened `k₁ = 2` / `#tᵢ > #origin` clauses). Drop the re-derivation of `zeros`/`#E` structural forms.

### Issue 2: Justification asides explaining *why* the SubspaceConventionAxiom is invoked, rather than what the step computes
**ASN-0093, "Address sub-allocators under documents"**: "`b_C(d) = inc(d, 2)` (TA5(d), `k = 2`, whose result `[d.0.1]` equals `[d.0.s_C]` only because `s_C = 1` by SubspaceConventionAxiom) and `b_L(d) = inc(b_C(d), 0)` (TA5(c), depending substantively on `s_L = s_C + 1` by SubspaceConventionAxiom)."
**Problem**: "only because `s_C = 1`" and "depending substantively on `s_L = s_C + 1`" are defensive notes about which axiom clause is load-bearing — meta-prose that does not advance the construction. The construction is fully determined by stating `b_C(d) = [d.0.s_C]` and `b_L(d) = [d.0.s_L]`; the dependency on the axiom is already implicit in the `s_C`/`s_L` symbols.
**Required**: State the anchor forms directly; drop the "only because" / "depending substantively on" clauses.

### Issue 3: Premise inventories duplicated from the lemma bodies into the Properties Introduced table
**ASN-0093, "Properties Introduced" table**: e.g. FirstEmissionFreshness — "Premises: first-emit predicate; FirstEmission structural form; L0; L1; SC-NEQ; ChainPrefixExtension; ChainMembershipForOrigin; ChainUniformZeroCount; ChainElementT4Validity; StoreT4Validity; Cross-document disjointness; T7; T10." (SubsequentEmissionFreshness lists 14.)
**Problem**: A 13–14 item dependency list in a summary index is a use-site inventory, not a source attribution. Each lemma already names its premises inline at the point of use; re-listing the full set in the table adds maintenance surface (premise drift between the two) without advancing anything.
**Required**: In the table, give a one-phrase source (as the other rows do — "Substrate", "ASN-0043"); keep the full premise set only at the lemma's single inline home.

### Issue 4: C1b and L1b matrix cells restate the identical content↔link argument in full, against the note's own established symmetry convention
**ASN-0093, "Discharge of stated invariants" matrix (C1b and L1b rows)**: both cells spell out the entire "by TA5(b) the step preserves every position except `sig(·)`, and for the T4-valid `·_prev`, TA5-SigValid places `sig = #·` ... `zeros(·) = zeros(·_prev)` by B5a ... `#E = #E(·_prev) ≥ 2`" argument verbatim, once for content and once for links.
**Problem**: Elsewhere the note collapses exactly this symmetry — L1c's subsequent-emit case ("Identical to the C1c subsequent-emit case above under the content↔link substitution") and FirstEmissionFreshness's link case ("Identical to the content case above under the content↔link substitution"). C1b/L1b break that convention and pay the full duplication cost.
**Required**: State the argument once (C1b) and discharge L1b by the content↔link substitution pointer the note already uses.

## OUT_OF_SCOPE

### Topic 1: `origin` vs `home` naming for link addresses
The substrate restates ASN-0043's L1a/L1c using `origin(·)` (ASN-0036's name) where the foundation uses `home(·)`; both denote the identical `N(a).0.U(a).0.D(a)` projection. This is a harmless unification of two foundation aliases, not an error — noting only so it is not mistaken for a reinvented notation.

VERDICT: REVISE
