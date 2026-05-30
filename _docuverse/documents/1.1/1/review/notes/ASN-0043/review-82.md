# Review of ASN-0043

## REVISE

### Issue 1: L1c axiom wrapped in rationale prose

**ASN-0043, L1c (LinkAllocatorConformance)**: "This is the same system-wide allocation discipline that ASN-0034 establishes for all address allocation — link allocation is not exempt. L1a (LinkScopedAllocation) constrains where link addresses end up (under the creating document's prefix); L1c constrains how they are produced (by T10a-conforming allocators)."

**Problem**: This is the reviser-drift pattern "new prose around an axiom explains why the axiom is needed rather than what it says." The axiom's content is the formal chain statement that follows; the quoted paragraph contrasts L1a vs L1c and asserts non-exemption — rationale, not content. A precise reader must skip it to reach the chain.

**Required**: Delete the quoted paragraph. The formal chain and its postconditions carry the axiom.

### Issue 2: L9 and L11b duplicate the entire "fresh sibling preserves all invariants" verification

**ASN-0043, L9 witness ("State-local L-invariants verified at Σ'") and L11b ("Conformance of Σ'")**: Both proofs construct a fresh link by `inc(·, 0)` sibling advance (or a short chain), then re-verify the same invariant set — L0, L1, L1a–c, L3, L5, L6, L11a, L12, L14, L14a, L-fin, and S0–D-SEQ — with arguments that depend only on (i) the new address being a fresh sibling in `s_L` and (ii) `Σ'.C = Σ.C`, `Σ'.M = Σ.M`. The endset payload differs (ghost type vs. copied triple) but the conformance arguments are identical line-for-line.

**Problem**: This is "two paragraphs say the same thing in different words" at proof scale. The shared machinery is verified twice.

**Required**: State the "appending one fresh sibling link with stores otherwise unchanged preserves all L- and S-invariants" argument once (as a lemma or in one of the two proofs), and have the other cite it, noting only the payload-specific delta (ghost-type disjointness for L9; endset equality for L11b).

### Issue 3: Worked example re-lists the full state-local invariant set five times

**ASN-0043, Worked Example, Steps 1–4**: Each of Σ, Σ₁, Σ₂, Σ₃, Σ₄ receives a complete "State-local L-invariants … (one-line confirmations)" walkthrough. Steps 1 and 2 add only a fresh sibling link (`a'`, `a₂`) and reproduce identical one-line confirmations for L0, L1, L1a, L1b, L1c, L5, L11a, L14, L14a.

**Problem**: The incremental value of Steps 3 (arity-4) and 4 (type discrimination) is L3/L6/L8 in new regimes — worth showing. The surrounding mechanical re-lists for each added sibling are repetition, not depth.

**Required**: Keep the substantive new checks (arity-4 L3/L6/L8; discrimination L8 at Σ₄). Collapse the mechanical per-sibling confirmations into a single "each added sibling preserves L0/L1/L1a–c/L11a/L14/L14a by the same argument as `a'`" statement rather than re-enumerating per state.

### Issue 4: PrefixSpanCoverage asserted as an axiom but derivable from the foundation

**ASN-0043, Axiom — PrefixSpanCoverage**: "`coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`" introduced with the label *axiom* and no derivation.

**Problem**: This equality is a consequence of foundation results — `x ⊕ δ(1,#x) = shift(x,1)` (OrdinalShift), `s ≤ t < s⊕ℓ` (Span/T12), contiguity of the prefix subtree (T5), and T1 case (ii). It is a *claim*, and "claims without proofs are REVISE." Labeling a derivable theorem an axiom imports an obligation the foundations already discharge and hides the inclusion `[x, shift(x,1)) = subtree(x)` step that L10 and L13 lean on.

**Required**: Reclassify as a lemma and give the derivation (both inclusions), citing T5, OrdinalShift, T12, and T1 case (ii) — or cite the foundation result that establishes it directly.

### Issue 5: L2's two-state framing contradicts L12

**ASN-0043, L2 (OwnershipEndsetIndependence)**: "for any two states Σ, Σ' with `a ∈ dom(Σ.L) ∩ dom(Σ'.L)` and `Σ.L(a) ≠ Σ'.L(a)`, the home document of `a` is identical in both."

**Problem**: L12 (LinkImmutability) forbids `Σ.L(a) ≠ Σ'.L(a)` for the same address across any reachable transition. The antecedent describes a configuration the model excludes, so the chosen framing is self-contradictory with a sibling invariant. The intended content — `home(a)` is a function of the address alone — does not need a two-state hypothesis.

**Required**: State L2 as `home` being computed by T4 projection on `a` alone (endsets never appear in the computation), without positing two states that differ at `a`.

## OUT_OF_SCOPE

### Topic 1: Resolution semantics for link-to-link references (L13)
**Why out of scope**: Whether/how a meta-link's endset resolves to the targeted link's content is an operation/resolution question, correctly deferred.

### Topic 2: Subtype-aware query operations (L10)
**Why out of scope**: L10 establishes the structural affordance; query-interface obligations are operations, correctly deferred.

VERDICT: REVISE
