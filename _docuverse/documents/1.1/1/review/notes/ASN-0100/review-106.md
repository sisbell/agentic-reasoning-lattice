# Review of ASN-0100

This is a thorough, largely correct specification. The forward verification (effects → post-state), invariant discharge, two worked examples, and two non-trivial `wp` computations are present and sound. My findings are anti-bloat (the note carries `review-mode.anti-bloat`), targeting accreted redundancy around the allocation-freshness justification and repeated deferral parentheticals. I found no correctness error in the effect contract, the S2/S3★/D-SEQ★ discharge, or the INS.proj derivation.

## REVISE

### Issue 1: Freshness justification restated with a back-reference in a structural slot
**ASN-0100, §The Operation: Formal Contract → Substrate Decomposition, step 1**: "*Each K.α firing satisfies its freshness precondition a_k ∉ dom(C) ∪ dom(L) against the intermediate state immediately preceding it (justified by SubsequentEmissionFreshness, with FirstEmissionFreshness covering the first-emission boundary; ASN-0093 — see Effect One above).*"
**Problem**: The full freshness derivation (the `Σ_k` intermediate-state argument, SubsequentEmissionFreshness, FirstEmissionFreshness, chain discipline) is already given normatively in §Effect One: Allocation. The decomposition-list slot re-states the same justification and then back-points with "see Effect One above" — a structural slot deferring to essay content. The list step needs only to name the obligation and cite the carrier (INS.alloc / ASN-0093), not re-explain it.
**Required**: Reduce step 1 to the decomposition fact plus a bare citation (e.g., "freshness per INS.alloc"); drop the restated lemma names and the "see Effect One above" pointer.

### Issue 2: Identical S8a-deferral parentheticals in two sections
**ASN-0100, §A Worked Example (empty-document case)** and **§Verifying the Invariants → Sequential text-subspace structure (empty case)**: both contain verbatim "*(S8a for the Insertion region — empty and non-empty cases alike — is established once in §Post-state V-position well-formedness.)*"
**Problem**: Two paragraphs in different sections defer to the same downstream location with the same sentence — the named "multiple paragraphs defer to the same downstream location" pattern. One deferral suffices; the second is noise the reader must skip.
**Required**: Keep a single deferral (or simply let §Post-state V-position well-formedness own S8a without parenthetical pre-announcements in both sites).

### Issue 3: Duplicated provenance-discharge prose across worked examples
**ASN-0100, §A Worked Example**: the interior-insertion "*Provenance discharge (J0, J1★, J1'★)*" paragraph and the empty-document "*Discharge of J0, J1★, J1'★ (empty case)*" paragraph restate the same coupling reasoning (fresh Insertion images recorded by K.ρ; J0 pairs allocation with placement; J1★/J1'★ match new R-entries to placements) in different words.
**Problem**: The empty-case discharge adds nothing the interior-case discharge plus the general frame/coupling claims (INS.R, §Provenance) do not already establish — "two paragraphs say the same thing in different words." Worked examples should exercise what *differs* (here: only the absence of Left/Shifted-right and of K.μ⁻), not re-run identical coupling text.
**Required**: In the empty case, state only the delta (no K.μ⁻; pre-state `ran(M(d)) = ∅` so all three images are range-new) and cite the interior discharge for the shared J0/J1★/J1'★ logic.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L semantics)
**Why out of scope**: The note explicitly restricts to the content subspace `s_C`; link-subspace extension is a structurally distinct operation. Correctly deferred in §Bounding the Scope and the Open Questions.

### Topic 2: Crash-recovery / partial-failure recovery of canonical order
**Why out of scope**: Raised as an Open Question; it concerns implementation realization of the abstract sequential transition model, not the per-state effect this ASN specifies.

VERDICT: REVISE
