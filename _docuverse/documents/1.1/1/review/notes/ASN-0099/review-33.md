# Review of ASN-0099

This ASN provides a thorough specification of FINDLINKS with a clean two-phase factoring (V→I via `image`, I→Link via `findlinks`), explicit conformance contracts separating abstract operations from implementation functions, a parametric realizability argument for match-predicate uniqueness (F4), and an extensive worked example exercising most claims. The major interpretive commitment (A1b's closed-world reading of the substrate effect-clause convention) is explicitly flagged with convergent non-constitutive grounding. The REVISE items below are minor.

## REVISE

### Issue 1: Notation typo in Query 11 cross-step precondition list
**ASN-0099, "Query 11: F9★ verification via a K.μ-only two-step chain (cross-step precondition transfer)"**: "K.μ⁺_L's precondition `ℓ ∈ dom(M.L)`"
**Problem**: "dom(M.L)" doesn't parse against the state-component vocabulary established in ASN-0047 and ASN-0093. M is the family of arrangements, L is the link store; they are separate top-level components of Σ. "M.L" is not a defined notation, and a reader trying to trace the cross-step precondition transfer hits an undefined symbol immediately.
**Required**: Change to "dom(L)" or "dom(Σ.L)", matching the form used in ASN-0047's K.μ⁺_L precondition `ℓ ∈ dom(L)`. The subsequent text "ℓ ∈ dom(Σ'.L) = dom(Σ.L) (preserved by A1b across the K.μ⁻ step...)" already uses the correct form, so this is an isolated typo.

### Issue 2: F10-filt/F10-sco derivations route through implementation conformance rather than direct comprehension structure
**ASN-0099, derivation paragraph following F10-filt/F10-sco**: "For F10-filt: by F3-filt, `result_filtered(C, Σ) ⊆ dom(Σ.L)`; L-fin gives `|dom(Σ.L)| < ∞`; so `findlinks_filtered(C, Σ)` is finite as a subset of a finite set."; "For F10-sco: by F3-sco, `result_scoped(I, S, Σ) ⊆ dom(Σ.L) ∩ S ⊆ dom(Σ.L)`; L-fin gives finiteness; ..."
**Problem**: F10-filt and F10-sco are claims about the *abstract* `findlinks_filtered` and `findlinks_scoped` sets. The cited F3-filt and F3-sco are conformance contracts on the implementation functions `result_filtered` and `result_scoped`. The intended conclusion (finiteness of `findlinks_filtered` / `findlinks_scoped`) follows directly from the comprehension structure — `findlinks_filtered(C, Σ) = {a ∈ dom(Σ.L) : ...} ⊆ dom(Σ.L)` and `findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S ⊆ dom(Σ.L) ∩ S` by F14. The routing through result_filtered/result_scoped is technically rescuable via the conformance bridge (F2-filt ∧ F3-filt gives `result_filtered = findlinks_filtered`), but the route is unnecessary and obscures what the structural derivation requires.
**Required**: Cite the comprehension structure directly: "findlinks_filtered(C, Σ) ⊆ dom(Σ.L) by the comprehension's source set; L-fin gives `|dom(Σ.L)| < ∞`; so findlinks_filtered(C, Σ) is finite as a subset of a finite set." Symmetrically for F10-sco.

### Issue 3: F10's pairwise-to-n-document lift relies on T1 restriction being a strict total order without citing the source
**ASN-0099, F10 "Result Ordering" section, paragraph beginning "The reader sees results in a canonical..."**: "T1's restriction to any subset of T is itself a strict total order — irreflexivity, trichotomy, and transitivity all transfer to any subset of T under T1's restriction — so the restriction of T1 to the finite set of link addresses across the n documents is itself a strict total order, and the pairwise strict inequalities supplied by the per-pair F10a + PrefixOrderingExtension applications are exactly the constituents of that strict total order."
**Problem**: The transfer of T1's strict-total-order properties (irreflexivity, trichotomy, transitivity) to any subset is asserted but not derived. The derivation is straightforward — universal quantification over T specializes to universal quantification over any S ⊆ T — but the assertion is load-bearing for the cross-document ordering claim and deserves a discrete derivation step or an explicit citation of T1's postconditions (a), (b), (c) from ASN-0034.
**Required**: Either state the specialization explicitly ("T1's postconditions (a) irreflexivity, (b) trichotomy, and (c) transitivity quantify universally over T, so each specializes by instantiation to any S ⊆ T, yielding a strict total order on S"), or note that this is a standard restriction-of-relation property requiring no further argument.

## OUT_OF_SCOPE

None to flag. The "What We Have Not Specified" section and Open Questions enumerate legitimate future-ASN topics (phantom addresses, multi-server semantics, access control composition, inverse direction / FOLLOWLINK, auditability witnesses, latency bounds, combined filtered-and-scoped form, minimum substrate commitment for the non-allocating fragment). These are correctly deferred and do not constitute REVISE items for this ASN.

VERDICT: REVISE
