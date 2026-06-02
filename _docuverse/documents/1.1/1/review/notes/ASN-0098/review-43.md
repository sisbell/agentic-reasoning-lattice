# Review of ASN-0098

## REVISE

### Issue 1: "Canonical span" is defined twice, with different content, and the decidability bridge is left implicit

**ASN-0098, LP-Fin statement vs. the `tight` definition**:
- LP-Fin: "For every *canonical* span `(s, ℓ)` — meaning `s ∈ F` (so `s = [d_0, 0, s', k_s]` …) and `ℓ = δ(n, #s)` …"
- `tight` definition: "every span `(s, ℓ) ∈ e` is *canonical* — `ℓ = δ(n, #s)` for some `n ≥ 1`, equivalently `#ℓ = #s` with `ℓ` an ordinal displacement …"

**Problem**: The two definitions of "canonical span" do not coincide. LP-Fin's includes the membership conjunct `s ∈ F`; the tightness definition's is only the displacement-shape condition `ℓ = δ(n, #s)`. The sentence immediately following the `tight` definition — "It also confines LP-Fin's universal quantifier to a finite set (LP-Fin, below), so the predicate is decidable at every state" — invokes LP-Fin's finiteness result, but LP-Fin's hypothesis (`s ∈ F`) is *not* among the tightness conjuncts. Tightness instead supplies `s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)`. The decidability claim therefore silently relies on `dom(Σ_e.C) ∪ dom(Σ_e.L) ⊆ F`, which is never stated at this point (the link half is proved only later, inside LP12b's three-step chain; the content half is never discharged at all). So the claim "the predicate is decidable at every state" is asserted from a lemma whose precondition the predicate does not establish.

**Required**: Either (a) unify the two definitions of "canonical span" under one name with one content, or (b) add the explicit bridge lemma `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` (provable from ChainMembershipForOrigin + FirstEmission/ChainDiscipline + M0, ASN-0093, noting every sub-allocator chain element has `#E = 2`) and cite it where tightness's decidability is asserted, so that `s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L) ⟹ s ∈ F ⟹ LP-Fin applies`.

### Issue 2: Repetitive composite-level meta-prose after LP11

**ASN-0098, paragraph following LP11 ("The atomic per-step lemmas LP4–LP10 and LP14 cover every atomic operation kind…")**: "LP11 governs neither atomic step; it reasons about the composite directly … that the LP10-then-LP9 atomic path realises but does not by itself express. A K.μ~ occurrence in a sequence is therefore analysed via its K.μ⁻ + K.μ⁺ decomposition for the per-step coverage, with LP11 supplying the composite net effect."

**Problem**: The paragraph states the same fact — LP11 is a composite-level lemma whose net effect the LP10-then-LP9 decomposition realizes — three times in different words. This is reviser drift: prose explaining the proof architecture rather than advancing a claim, with internal duplication the precise reader must work around.

**Required**: Reduce to one sentence: LP11 is composite-level (K.μ~ = K.μ⁻ + K.μ⁺ per ASN-0047); the atomic decomposition is governed by LP10 then LP9, and LP11 supplies the net effect.

### Issue 3: Citation-choice meta-prose in LP18

**ASN-0098, LP18 proof**: "(Equivalently, LP3★ supplies both `a ∈ dom(Σ'.L)` and the coverage equation in a single step; we cite the persistence half here to highlight the well-definedness obligation.)"

**Problem**: This parenthetical justifies which lemma was cited rather than advancing the proof. It is the "explains why we cite X rather than Y" reviser-drift pattern. The proof already cites both Store Monotonicity★ and LP3★; the editorial note adds nothing the argument needs.

**Required**: Delete the parenthetical; cite the one lemma the step uses.

### Issue 4: Defensive "what we are not doing" prose around the F definition and LP9

**ASN-0098, F-definition discussion and LP9**:
- F discussion: "we do not re-discharge T4's conjuncts here"; "We do not require `d ∈ dom(Σ_e.M)` — future K.σ transitions can register additional documents…"
- LP9: "(The per-subspace dependence of D-CTG★/D-MIN★ in ASN-0047 governs *which* V-positions K.μ⁺_L may select … but does not affect the structural form of (E1)/(E2).)"

**Problem**: These are defensive justifications and "what this step does not depend on" notes — meta-prose that does not advance the reasoning. LP9's argument already states it "consumes only (E1) and (E2)"; the parenthetical about D-CTG★/D-MIN★ then re-establishes the same independence a second time. The F-discussion's disclaimers explain proof-management decisions rather than the construction.

**Required**: State the constructions and the facts used; drop the disclaimers about what is not re-proved or not required.

## OUT_OF_SCOPE

### Topic 1: Reverse discovery, V-order/I-order correspondence, link-to-link induced discovery, fork-without-link-transclusion

**Why out of scope**: These are correctly confined to the Open Questions section as future work, not claimed. No action needed.

VERDICT: REVISE
