# Review of ASN-0100

## REVISE

### Issue 1: Unresolvable external references (Q1, Q3, Q5, Q8)
**ASN-0100, Effect One / Cross-document independence**: "Nelson is unambiguous (Q1, Q5, Q8)" and the heading "Cross-document independence (Q3)".
**Problem**: The ASN's own framing names "three sub-questions" but never labels them Q1…Q8. These Q-labels point at an external Nelson question taxonomy that is not reproduced here or in any foundation. A precise reader cannot verify what Q5 or Q3 actually assert, so the citations are inert. The ASN is meant to be self-contained.
**Required**: Either inline the substance of each cited question at the point of use, or drop the Q-labels and state the design requirement directly.

### Issue 2: Anti-bloat — vocabulary inventory and re-narration around the decomposition
**ASN-0100, The Operation: Formal Contract**: "It is not a new elementary primitive; the substrate transition vocabulary is not amended. The operative substrate is ValidComposite★ (ASN-0047), whose atomic vocabulary is {K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), and K.ρ}."
**Problem**: Two noise patterns flagged by the anti-bloat mandate. (a) A defensive justification ("not a new elementary primitive; … not amended") explaining what INSERT is *not*, advancing no reasoning. (b) A full 7-element vocabulary inventory of which INSERT uses only 4 — a use-site inventory immediately superseded by the Substrate Decomposition that selects and re-lists the actual 4 steps. Separately, the bolded "Identification with the foundation's post-insertion shift" paragraph in §Effect Three re-narrates the Shifted-right effect already stated immediately above it (signalled by "just described"); only the gap-vacating decomposition is load-bearing.
**Required**: Cut the defensive sentence and the full-vocabulary list; let the decomposition introduce the four steps directly. In §Effect Three, keep the I3 gap-vacating decomposition; drop the re-narration of the shift effect.

### Issue 3: No concrete example exercises m_C ≥ 3
**ASN-0100, A Worked Example / Sequential text-subspace structure**: both worked examples use `m_C = 2`; the D-CTG★ closed-interval reduction's hardest step — excluding off-prefix slice tuples such as `[s_C, 2, 1, …, 1]` at depth `m ≥ 3` — is verified only abstractly.
**Problem**: Standard 6 requires the key postconditions to be checked against a concrete scenario. The subtlest content-subspace invariant (off-prefix exclusion at `m ≥ 3`, where `V_{s_C}` is multi-level) never appears in any worked instance, so the part of the proof most likely to hide an error is exercised only in prose.
**Required**: Add one concrete `m_C = 3` instantiation (e.g. `V_{s_C}(d) = {[1,1,1],[1,1,2],…}`) and verify D-CTG★/D-MIN★/D-SEQ★ on the post-state, including that an off-prefix tuple lies outside `[min, max]`.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
