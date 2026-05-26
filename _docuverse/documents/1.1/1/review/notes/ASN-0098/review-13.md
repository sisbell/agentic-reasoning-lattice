# Review of ASN-0098

## REVISE

### Issue 1: LP-Fin is false for non-canonical spans

**ASN-0098, LP-Fin (claim and proof)**: "For every well-formed span (s, ℓ) (T12, ASN-0034), the set F ∩ [s, s ⊕ ℓ) is finite."

**Problem**: Counter-example. Take s = [1, 0, 1, 0, 1, 0, 1, 1] (#s = 8, structural form [d₀, 0, 1, 1] with d₀ = [1, 0, 1, 0, 1], zeros(d₀) = 2 ✓), and ℓ = [0, 0, 0, 1] (#ℓ = 4). T12 holds: Pos(ℓ) ✓, actionPoint(ℓ) = 4 ≤ #s = 8 ✓. Then s ⊕ ℓ = [1, 0, 1, 1] (#(s⊕ℓ) = #ℓ = 4 per TumblerAdd's result-length identity).

For each n ≥ 1, define a_n = [d_n, 0, 1, 1] where d_n = [1, 0, 1, 0, 1, 1, 1, ..., 1] has length 5 + n with zeros only at positions 2 and 4. Then zeros(d_n) = 2, T4 holds (no adjacent zeros, first/last non-zero), so a_n ∈ F. Check a_n ∈ [s, s ⊕ ℓ): at position 4, a_n[4] = 0 < 1 = (s⊕ℓ)[4], so a_n < s⊕ℓ by T1 case (i); at position 6, a_n[6] = 1 > 0 = s[6], so a_n > s by T1 case (i). Hence |F ∩ [s, s ⊕ ℓ)| ≥ ℵ₀.

The proof's step "the divergence at position j lie strictly within d's admissible value range (a_j < (s ⊕ ℓ)_j, finite) bounds #d to a finite range" does not follow: once (s⊕ℓ)'s prefix-agreement region already contains d's two zeros (here at positions 2, 4 of d), d's tail (positions ≥ 5) is unconstrained by zeros(d) = 2 and can extend indefinitely with non-zero components consistent with T4.

**Required**: Either (a) restrict LP-Fin to spans with #ℓ = #s (the canonical / ordinal-displacement form, where the structural-rigidity argument actually closes — d's tail beyond the prefix-agreement cannot extend because position #s of a is the chain index, forcing #d = #s − 3), or (b) supply a different proof that handles #ℓ < #s. The current general statement is unsound.

### Issue 2: Tightness predicate is structurally unsatisfiable for non-canonical spans

**ASN-0098, "tight" definition**: "every span (s, ℓ) ∈ e satisfies: s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L) ∧ (A t ∈ F : s ≤ t < s ⊕ ℓ : t ∈ dom(Σ_e.C) ∪ dom(Σ_e.L))"

**Problem**: For any span where F ∩ [s, s ⊕ ℓ) is infinite (Issue 1 shows such spans satisfy T12), the universal quantifier ranges over an infinite set, while dom(Σ_e.C) ∪ dom(Σ_e.L) is finite (C-fin, L-fin of ASN-0093). The predicate is therefore unsatisfiable on any endset containing such a span — at any state, ever.

The ASN's discussion ("Tightness is a construction discipline, not a structural invariant the system enforces. The system permits endsets whose spans extend past the relevant sub-allocator's current emission frontier; such endsets are not tight, and an a_new allocated within their forward extent...") characterises non-tight endsets as those with extended forward reach, suggesting tightness is achievable for any span with appropriate construction discipline. This understates the situation: for non-canonical spans, no construction discipline makes the endset tight.

**Required**: Either restrict the tightness predicate to endsets whose spans satisfy #ℓ = #s, or add an explicit clause acknowledging that non-canonical spans are unconditionally non-tight (with the distinction between "could be made tight with discipline" and "cannot be tight at any state").

### Issue 3: Descendant document achievability argument requires canonical ℓ

**ASN-0098, achievability section, "Descendant documents" case**: argues chain elements b of A_C(d') (with d₀ ≺ d') satisfy b > s ⊕ ℓ via T1 case (i) at divergence position #d₀ + 1, citing prefix-copy reasoning that (s⊕ℓ)_{#d₀ + 1} = s_{#d₀ + 1} = 0.

**Problem**: The prefix-copy step requires position #d₀ + 1 to lie within s⊕ℓ, i.e., #(s ⊕ ℓ) ≥ #d₀ + 1. Since #(s ⊕ ℓ) = #ℓ, this requires #ℓ ≥ #d₀ + 1. The canonical form #ℓ = #s = #d₀ + 3 satisfies it; non-canonical forms with #ℓ ≤ #d₀ do not. The Issue 1 counter-example (d₀ = [1, 0, 1, 0, 1], #d₀ + 1 = 6, #ℓ = 4) produces a descendant chain element b = [1, 0, 1, 0, 1, 1, 0, 1, 1] of d' = [1, 0, 1, 0, 1, 1] (a valid depth-1 descendant via inc(d₀, 1)) that lies in F ∩ [s, s ⊕ ℓ) — directly contradicting the case's conclusion.

The Ancestor case carries an analogous dependency: the position-(#d' + 1) argument also assumes #(s ⊕ ℓ) ≥ #d' + 1.

**Required**: State the canonical-ℓ assumption explicitly at the achievability section header (it is mentioned for the construction but treated as derivable thereafter), and rederive the cross-document interference arguments to flag that they conclude only under #ℓ = #s.

### Issue 4: Trace example's composite is not ValidComposite★ as written

**ASN-0098, "A Worked Trace" — Σ → Σ_2**: "Now suppose another document `d₂` is registered and transcludes `i₄` via K.σ followed by K.μ⁺, producing state `Σ_2`."

**Problem**: K.μ⁺ on d_2 introduces (i_4, d_2) as a new range entry in the content subspace. ASN-0047's J1★ requires every such content-subspace range extension to be accompanied by K.ρ adding (i_4, d_2) to R, evaluated over the composite. The two-step "K.σ + K.μ⁺" violates ValidComposite★'s J1★ coupling. The trace's projection conclusions are unaffected (project ignores R), but a reader checking the composite against the transition model would find it ill-formed.

**Required**: Either insert a K.ρ step in the composite, or add a parenthetical noting that R bookkeeping is elided since it does not affect projection.

## OUT_OF_SCOPE

None. The ASN's question (projection displacement) is well-scoped, and the Open Questions section appropriately defers reverse discovery, finite V-range expressibility, V-order preservation, cross-document operation equivalence, and partial-transclusion fork scenarios to future ASNs.

VERDICT: REVISE
