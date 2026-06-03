# Review of ASN-0070

I worked through the foundations, the F-canonical existence/uniqueness theorem (Steps 0–5), the contiguity proof, the weakest-precondition analysis, and all six worked configurations. The mathematical content is rigorous: the case split in Step 1 (`k < m_S(d)` excluded by infinitude, `k = m_S(d)` proved by mutual inclusion), the consecutivity characterisation in Step 2 (both directions, with the discreteness/irreflexivity appeals discharged), and the per-subspace uniqueness reconstruction in Step 4 (right- and left-closure both handled, including the `s_j.m = 1` positivity sub-case) all hold. Boundary cases — empty document, vacuous subspace, empty endset, `i` out of range, interior-offset clip — are covered by F-empty, the Vacuous-subspace convention, and Configurations 2/5/6.

I found one issue.

## REVISE

### Issue 1: Stale structural meta-prose in the Derived Properties preamble

**ASN-0070, "Derived Properties" (opening paragraph)**: "We catalogue them as F-det, F-sound, etc., and present each with explicit preconditions, postconditions, dependencies, and frame."

**Problem**: This sentence is structural meta-prose — it describes the *format* of the entries that follow rather than advancing any reasoning, exactly the "essay content in structural slots" pattern. Worse, it is now factually wrong. After the recent revision dropped the Frame sentences, none of the derived-property entries (F-det, F-sound, F-complete, F-empty, F-multi, F-slot, F-origin, F-persist, F-state, F-multidoc, F-contig) actually carries a Frame field. The preamble promises "and frame" for each, but no frame is presented for any of them. A reader who trusts the preamble will look for a frame field that does not exist. The remaining sentences of the paragraph (the F-sound/F-complete = two-halves-of-the-set-equality observation) do advance understanding and should stay.

**Required**: Delete the sentence "We catalogue them as F-det, F-sound, etc., and present each with explicit preconditions, postconditions, dependencies, and frame." (The catalog format is self-evident from the entries themselves; the load-bearing F-sound/F-complete relationship in the following sentence is unaffected.)

VERDICT: REVISE
