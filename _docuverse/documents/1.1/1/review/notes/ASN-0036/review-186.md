# Review of ASN-0036

## REVISE

### Issue 1: OrdShiftHom labeled (b) and (c) with no (a)
**ASN-0036, "Shift preservation for V-positions"**: "**OrdShiftHom** ... (b) `subspace(shift(v, n)) = subspace(v)`. (c) When `v` satisfies S8a, `shift(v, n)` satisfies S8a."
**Problem**: The lemma states postconditions (b) and (c) with no (a) anywhere — in the statement, the proof, the Formal Contract, or the Properties table. This is residue from the recorded collapse ("collapse ord/vpos/w_ord/OrdAddHom/OrdAddS8a into OrdShiftHom"): the surviving labels point at a prior decomposition that no longer exists. A reader hunting for (a) must verify it was deliberately dropped, not accidentally omitted.
**Required**: Relabel to (a)/(b), or state explicitly what (a) was and why it is gone. Do not leave dangling enumeration from a prior structure.

### Issue 2: S7c, `subspace_I`, and ShiftPreservation (iii)/(iv) have no in-ASN consumer
**ASN-0036, ShiftPreservation conclusions (iii)–(iv) and S7c**: "(iii) `#E(shift(a, k)) = #E(a)` ... (iv) `subspace_I(shift(a, k)) = subspace_I(a)`."
**Problem**: Nothing in this ASN consumes `#E` preservation or `subspace_I` preservation. S8's proof invokes ShiftPreservation only for "structurally valid element-level I-address" (conclusions (i)/(ii)); where it does name conclusion (iv) — "`shift(a, 1)` is again an element-level, T4-valid I-address with `subspace_I(shift(a, 1)) = subspace_I(a)`" — the `subspace_I` clause is decorative: the sentence's conclusion ("equates two structurally valid I-addresses") needs only (i)/(ii). Conclusion (iii) is never mentioned again. The supporting chain S7c → `subspace_I` → ShiftPreservation(iv) is a dead branch, and the note's own Open Questions explicitly defer subspace alignment to the operations layer ("treats subspace alignment ... as an operations-layer preservation obligation rather than a state-level invariant"). This is machinery derived ahead of any need.
**Required**: Either exhibit the in-ASN claim that consumes (iii)/(iv)/S7c, or remove them and let the deferred operations ASN introduce them where they are actually used.

### Issue 3: Coined label "Nat-pos"
**ASN-0036, ShiftPreservation conclusion (i)**: "`a_{#a} ≥ 1` by **Nat-pos** — the elementary fact that for `n ∈ ℕ`, `n ≠ 0 ⟹ n ≥ 1` (immediate from NAT-discrete at `m = 0`)."
**Problem**: The foundation vocabulary already supplies NAT-discrete; coining a new inline name "Nat-pos" for a one-line consequence invents notation a foundation covers (Standard 7). The derivation is correct, but the label is unnecessary and risks future citations to a non-existent foundation claim.
**Required**: Drop the "Nat-pos" name and cite NAT-discrete directly at the point of use.

### Issue 4: S8 partition does not address the empty arrangement
**ASN-0036, S8 proof**: the construction walks orbits of `succ` over `dom(M(d))` and concludes "the maximal runs partition `dom(M(d))`."
**Problem**: The proof never states the `dom(M(d)) = ∅` case. It is vacuously true (zero orbits, empty partition), and the D-CTG section does check the empty base state — but S8 itself, the ASN's "central architectural claim about arrangements," should not leave its own boundary case to be inferred from a different section.
**Required**: One sentence in the Partition paragraph: when `dom(M(d)) = ∅` there are zero runs and the empty union partitions the empty set.

### Issue 5: Editorializing in the S8 lead
**ASN-0036, "Correspondence-run partition" intro**: "This run structure, not a position-by-position listing, is the strand model's central architectural claim about arrangements; we establish it here."
**Problem**: Per the anti-bloat mandate, this is a self-importance assertion that advances no reasoning — the reader must skip it to reach the claim. The contrast with "position-by-position listing" is not a property being used anywhere.
**Required**: Cut to the structural statement, or replace with a sentence that states what S8 *says*, not how central it is.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN/S2
The final Open Question ("What must each well-formed editing operation ... guarantee in order to preserve the contiguity invariants") correctly defers INSERT/DELETE/COPY/REARRANGE frame conditions to a future ASN. No finding — flagged only to confirm the deferral is appropriate, not a gap in this ASN.

### Topic 2: Computability of the sharing inverse and `Val` typing
The Open Questions on `Val`'s structure and the cost bound for the I-address→documents inverse are genuine future territory, not omissions here.

META: not applicable — the ASN defines state (`Σ.C`, `Σ.M`), operation-independent invariants (S0–S8, D-CTG/D-MIN/D-SEQ), and abstract guarantees implementations must satisfy; it has not drifted into implementation mechanics.

VERDICT: REVISE
