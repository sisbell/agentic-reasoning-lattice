# Review of ASN-0036

## REVISE

### Issue 1: Triple-repeated maximal-run disclaimer in the worked example
**ASN-0036, Worked example (states Σ₁, Σ₂, Σ₃)**: Σ₁ — "a concrete instance, not a claim S8 proves in general"; Σ₂ — "This is a concrete instance verifying (b), not content S8 establishes."; Σ₃ — "As above, these maximal runs are concrete instances verifying (b), distinct from S8's singleton existence claim."
**Problem**: The same disclaimer — by-hand maximal runs are not what S8 proves — is restated three times in different words across the three states. This is reviser drift (the recent "clarify S8 singleton scope vs by-hand maximal runs" cycle left residue): two-plus paragraphs saying the same thing, each re-deferring to the same point already made in S8's postcondition ("the existence and uniqueness of maximal runs is deferred to Open Questions"). A reader must skip past the repetition to follow each state's actual check.
**Required**: State the singleton-vs-maximal distinction once (it already lives in S8's postcondition). In the worked example, present the by-hand runs without the recurring "not what S8 proves" gloss, or fold a single sentence into the example's opening.

### Issue 2: S5 cross-document construction over-justifies witness validity, contradicting its own frame
**ASN-0036, S5 proof, cross-document construction**: "Each `dᵢ` is a valid document-level tumbler: `zeros(dᵢ) = 2` with no adjacent zeros, positive endpoint components, and the three fields `N(dᵢ) = [1]`, `U(dᵢ) = [1]`, `D(dᵢ) = [i]` populated by strictly positive natural numbers (T4, HierarchicalParsing, ASN-0034)."
**Problem**: S5's claim is consistency with S0–S3 only, and its frame states "the witnesses are not claimed to satisfy later invariants." S0–S3 quantify over `d` as an index into `M`; they place no T4-validity requirement on document tumblers. The only property actually needed is pairwise distinctness of the `dᵢ` (to make the pairs `(dᵢ, v)` distinct), which the proof already establishes separately via T3. The full T4-validity argument (zeros = 2, no adjacent zeros, positive fields) certifies a later-invariant-style property the frame disclaims, and is unused. The asymmetry is telling: the within-document construction correctly justifies only distinctness of `vₖ` and does not certify S8a-validity of its V-positions.
**Required**: Drop the T4-validity certification of the `dᵢ`; retain only the distinctness argument (distinct last components ⇒ distinct by T3). Likewise trim the NAT-closure aside establishing that `1, …, N+1 ∈ ℕ`.

### Issue 3: S7b depends on S0 with a cross-transition persistence rationale it does not need
**ASN-0036, S7b Depends**: "S0 (content immutability) — keeps `a ∈ dom(C')` across transitions, so the zero-count condition continues to hold on the same address."
**Problem**: S7b is a per-state axiom ("design requirement"): `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` asserted in every state `Σ`. A per-state axiom does not need S0 to "continue to hold across transitions" — it holds in each state by assertion, not by propagation. This is justification accretion: prose explaining why a dependency might be wanted rather than what S7b needs to state its content. The dependency also appears in the Properties table row ("design; uses T4, T4b, T10a.4, S0").
**Required**: Remove the S0 dependency (and its rationale clause) from S7b's Depends and the Properties table, unless S7b is restated as a preservation claim rather than a per-state axiom.

### Issue 4: S8-depth inline notation is ambiguous
**ASN-0036, S8-depth (inline statement)**: "`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`"
**Problem**: `v₁` and `v₂` are bound variable names, so `(v₁)₁` overloads the subscript to mean both "the variable `v₁`" and "first component of." A precise reader must disambiguate from context. The formal contract below uses `subspace(v₁) = subspace(v₂)`, which is unambiguous.
**Required**: Use distinct variable names (e.g., `u, w`) in the inline statement, or use `subspace(·)` there as the formal contract does.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG/D-MIN/S2
**Why out of scope**: The Open Questions on whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants, and what the displacement mechanism must guarantee at a ValidInsertionPosition, are correctly deferred — operation frame/postconditions are out of scope per the ASN's Scope section. No action needed.

### Topic 2: Maximal correspondence runs (existence/uniqueness)
**Why out of scope**: S8 honestly establishes only the singleton decomposition (conjunct (a) and (b)'s base case) and defers maximal-run existence/uniqueness to Open Questions. That deferral is legitimate; the only problem is the repeated re-statement of it (Issue 1), not the deferral itself.

VERDICT: REVISE
