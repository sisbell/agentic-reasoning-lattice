# Review of ASN-0091

## REVISE

### Issue 1: dom(Σ.M) preservation not explicit in RA-frame
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: RA-frame asserts `Σ'.C = Σ.C ∧ Σ'.L = Σ.L ∧ Σ'.E = Σ.E ∧ Σ'.R = Σ.R ∧ (A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`.
**Problem**: RA-frame does not state `dom(Σ'.M) = dom(Σ.M)`. The clause `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))` quantifies over d' without restriction to dom(M), and could fail to be meaningful (or vacuous) if d' ∉ dom(Σ.M) ∪ dom(Σ'.M). Downstream claims implicitly require it:
- RE-disc applies LP12 at Σ', which requires `d ∈ dom(Σ'.M)`.
- RE-other is quantified `(A d' ∈ dom(Σ.M) : d' ≠ d : Σ'.M(d') = Σ.M(d'))` — the statement only covers pre-state dom(M); documents in dom(Σ'.M) \ dom(Σ.M) (if any) are not addressed.
- RE-trans concludes "the home document origin(a)'s arrangement is unchanged" via RE-other applied to d' = origin(a), which requires origin(a) ∈ dom(Σ.M) and origin(a) ∈ dom(Σ'.M).

**Required**: Add `dom(Σ'.M) = dom(Σ.M)` as a fifth conjunct of RA-frame, or insert a lemma deriving it from `Σ'.E = Σ.E` plus the foundation chain `a ∈ dom(C) ⟹ origin(a) ∈ E_doc` (P6, ASN-0047) and `dom(M) = E_doc` (substrate semantics).

### Issue 2: "Covering exactly the I-addresses" misstates coverage type
**ASN-0091, "Worked Example"**: "e₁ = ⟨(b₁, δ(1, 8))⟩ is a canonical single-span endset covering exactly the I-addresses in [b₁, b₁ ⊕ δ(1, 8)) = [[1, 0, 1, 0, 1, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1, 2])"
**Problem**: Coverage is defined (per ASN-0098) as a set of tumblers in the interval, not "I-addresses." The interval [b₁, b₁ ⊕ δ(1, 8)) under T1 contains many tumblers that are not I-addresses (e.g., longer tumblers like [1, 0, 1, 0, 1, 0, 1, 1, 5] that lie between b₁ and b₁ ⊕ δ(1, 8) by T1 case (ii) + case (i)). The intersection with dom(C) ∪ dom(L) is what reduces to {b₁}, but this requires explicit appeal to LP-Fin Corollary (ASN-0098), which the example does not cite.
**Required**: Either restate as "coverage(e₁) = {t ∈ T : b₁ ≤ t < b₁ ⊕ δ(1, 8)}, with coverage(e₁) ∩ (dom(Σ.C) ∪ dom(Σ.L)) = {b₁} (by LP-Fin Corollary)", or remove the "exactly the I-addresses" phrasing.

### Issue 3: RE-sub verification in worked example is vacuous
**ASN-0091, "Worked Example", RE-sub clause**: "No link-subspace V-positions in dom(Σ.M(d)) in this configuration — the link subspace at d is empty — so RE-sub holds vacuously."
**Problem**: The worked example is the ASN's only concrete verification of RE-sub, and it discharges the lemma vacuously. RE-sub is the one REARRANGE_K-specific claim (not abstract-class); its load is precisely to show that link-subspace V-positions in d are preserved by a content-subspace cut sequence. A vacuous discharge does not test the lemma at all.
**Required**: Extend the worked example (or add a second example) to include at least one link-subspace V-position in dom(Σ.M(d)), e.g., `[s_L, 1] ↦ a_link` populated alongside the content-subspace positions, then verify RE-sub against this position concretely.

### Issue 4: RE-trans★ omits the home-arrangement clause without comment
**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"**: "RE-trans★: transclusion relationships present at Σ₀ persist at Σ_n with identical multiplicity, since RE-trans persists across each step."
**Problem**: The single-step RE-trans makes three assertions: (i) the (a, d) relationship persists; (ii) multiplicity is preserved; (iii) origin(a)'s arrangement is unchanged. The multi-step ★ form addresses (i) and (ii) but is silent on (iii). Yet (iii) can fail across multi-step sequences if some step targets origin(a): origin(a)'s arrangement is then itself reordered, even though the transclusion at d persists. The ASN should either explicitly drop (iii) from RE-trans★ with explanation, or restrict RE-trans★ to sequences where no step targets origin(a).
**Required**: Either rewrite RE-trans★ to explicitly state that (iii) is conditional ("if no step in the sequence targets origin(a), the source arrangement is unchanged"), or note that RE-trans★ deliberately weakens the single-step form to (i) + (ii) and explain why.

### Issue 5: π = id exclusion attribution is muddled
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "REARRANGE_K excludes this degenerate case via ASN-0084's K.μ~ admissibility (clause (ii): π ≠ id) together with its existence precondition `|dom_C(M(d))| ≥ 2`"
**Problem**: The two conditions do not jointly exclude π = id — clause (ii) does it alone. `|dom_C(M(d))| ≥ 2` is independently needed (to make non-identity permutations exist on V_S(d)) but does not by itself exclude the identity (which exists for any non-empty set). The "together with" phrasing implies a joint role that is not the case.
**Required**: Rephrase as "REARRANGE_K excludes π = id via K.μ~ admissibility clause (ii); the existence precondition `|dom_C(M(d))| ≥ 2` is independently needed to ensure non-identity permutations on V_S(d) exist."

### Issue 6: π non-uniqueness under shared I-addresses not addressed
**ASN-0091, abstract class definition**: "there exists a bijection π : dom(Σ.M(d)) → dom(Σ.M(d)) satisfying [RA-π]"
**Problem**: When M(d) has shared I-addresses (allowed by foundation S5/UnrestrictedSharing — same I-address at multiple V-positions), multiple bijections π satisfy RA-π simultaneously. The ASN refers to "the bijection π" as if uniquely determined, and RE-proj states `project(e, d, Σ') = π(project(e, d, Σ))` as if there were a single π. With non-unique π, RE-proj holds *for some* π — but the equality depends on which π is the witness. The non-uniqueness should be acknowledged, and RE-proj's dependence on the specific π made explicit (it holds for whichever π witnesses the transition).
**Required**: Add a sentence after the abstract class definition noting that π is not unique when M(d) has shared I-addresses (S5 of ASN-0036), and clarify that RE-proj's transport statement is parameterised by the specific π witnessing the transition.

## OUT_OF_SCOPE

(All open questions in the ASN's Open Questions section are appropriately scoped as future work and need not be flagged.)

VERDICT: REVISE
