# Review of ASN-0116

## REVISE

### Issue 1: Empty-subspace boundary conflates "empty arrangement" with "empty content region"

**ASN-0116, A worked insertion → "Boundary — empty subspace"**: "Because `d`'s content region is empty here (`{a' ∈ dom(C) : origin(a') = d} = ∅`), the start address is the *first* emission `a = [d.0.s_C.1]`..."

**Problem**: The stated boundary condition is `V_S(d) = ∅` (empty *arrangement*), but the example silently strengthens it to "content region empty" (empty *store slice*) to obtain the first-emission branch. These are not equivalent: content is append-only (IP2), so a document whose text was inserted and then fully contracted (`K.μ⁻` to empty) has `V_S(d) = ∅` while `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`. The genuinely interesting empty-subspace sub-case — re-insertion after full contraction, which exercises K.α's *subsequent*-emission branch alongside a fresh V-arrangement starting at `q_1` and a freely re-pinned depth `m` — is never worked. The main valid-composite argument correctly conditions the K.α branch on the content region, but the only worked verification of the empty-subspace boundary covers the never-allocated sub-case alone. A reader is left to infer (falsely) that `V_S(d) = ∅` selects the first-emission branch.

**Required**: Either work the `V_S(d) = ∅` ∧ content-region-non-empty sub-case explicitly (showing the subsequent-emission K.α start, the fresh `V_S(d') = {q_1, …, q_n}` with `min = q_1` re-establishing D-MIN, and depth re-pinning), or correct the prose so it does not imply `V_S(d) = ∅` entails an empty content region.

### Issue 2: Non-circularity / document-ordering meta-prose in the valid-composite section

**ASN-0116, INSERT as a valid composite, opening**: "We discharge both clauses here, self-contained: every prerequisite is either fixed in the Effect above (the block-disjointness fact, RAN, I-NEW, I-PROV) or derived inline in this section, so the validity conclusion rests on nothing proved in a later section."

**Problem**: This sentence advances no reasoning — it is a justification of *where* the proof sits relative to other sections and a prerequisite inventory, exactly the forward-reference meta-prose the anti-bloat classifier targets. The clause "rests on nothing proved in a later section" is document-ordering / non-circularity prose; the parenthetical list is a use-site inventory.

**Required**: Delete the organizational claim and the inventory; open directly with the sequence and the per-step discharge.

### Issue 3: Mutual-deferral prose splitting the J0/J1★/J1'★ discharge across two sections

**ASN-0116, valid-composite clause 2** ("(The provenance section records this discharge as the named claim PROV and, separately from clause 2, establishes the composite-boundary coverage properties P7a/P7.)") **and provenance section** ("The three couplings J0, J1★, J1'★ were discharged in the valid-composite argument above... Here we record that discharge as the named claim PROV and, separately from clause 2, establish... P7a/P7.").

**Problem**: Two paragraphs in different sections point at each other to explain how a single discharge is partitioned between them. The coupling discharge is done once in clause 2; the provenance section then re-announces it as PROV with prose narrating the split. This is the "multiple paragraphs deferring to the same location" pattern — the explanatory bookkeeping ("Here we record... separately from clause 2") is noise around the genuinely substantive P7a/P7 derivation.

**Required**: Discharge J0/J1★/J1'★ in one place. Keep the substantive P7a/P7 derivation; drop the mutual cross-references and the "we record this as PROV" narration. State the PROV claim once with its derivation, not split with pointers.

## OUT_OF_SCOPE

(none — the open-questions section appropriately defers transclusion, concurrent allocation, and post-edit fragmentation to future ASNs without making in-scope claims about them)

VERDICT: REVISE
