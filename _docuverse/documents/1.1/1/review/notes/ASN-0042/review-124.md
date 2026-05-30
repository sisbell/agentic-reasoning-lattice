# Review of ASN-0042

This is a strong, heavily-revised note; the core arithmetic (O1–O10, the delegation predicate, the longest-match function) is sound and the worked example is carefully constructed. My findings are concentrated where the `review-mode.anti-bloat` classifier directs: convention/notation accretion that the precise reader must work around, plus one scope-overreach in O10's prose.

## REVISE

### Issue 1: T4-discharge convention promises non-restatement, then is restated at every use site
**ASN-0042, *State Axioms* (O17) and O6/O9/O10 proofs**: "*T4-discharge convention.* Every proof in this ASN that applies a field operation ... we discharge it uniformly by O17 and do not restate the discharge at each use site."
**Problem**: The convention's sole purpose is to remove repeated discharges, yet the very proofs it governs re-cite it explicitly — O6: "their precondition `T4(a)` is supplied by the T4-discharge convention (O17), since `a ∈ Σ.B`"; O9: "supplied by the T4-discharge convention (O17), since `a ∈ Σ.B` by hypothesis"; O10 similarly. The convention both asserts "we do not restate" and is restated at each site, so it adds a paragraph of meta-prose without removing any of the per-site prose it claims to eliminate. This is the accretion pattern the classifier flags: a use-site inventory standing in for the work it describes.
**Required**: Either delete the convention paragraph and keep the inline `T4(a)`-via-O17 discharges, or keep the convention and strip the per-site re-citations to a bare symbol. Do not keep both.

### Issue 2: Duplicated state-relativization notation
**ASN-0042, *The Exclusivity Invariant* (ω_Σ definition) and *Properties Introduced* table footnote**: The *Notation* paragraph states "We write bare `ω(a)` and `Π` for `ω_Σ(a)` and `Π_Σ` when the state is fixed by context"; the table footnote restates "a bare `Π` (and a bare `ω`) abbreviates the state-relativized `Π_Σ` (resp. `ω_Σ`) ...".
**Problem**: Two paragraphs in different sections say the same thing in different words — the duplicate-prose pattern named in the anti-bloat checklist.
**Required**: Keep one. Remove the table footnote (or the *Notation* block).

### Issue 3: O10(b) asserts a content-invariance guarantee the ownership model cannot establish
**ASN-0042, O10(b)**: "the original address `a` is unchanged — no ownership is transferred, **no content is modified**."
**Problem**: The formal postcondition establishes only `a ∈ Σ'.B` (registry persistence, via B0) and `ω_{Σ'}(a) = ω_Σ(a)` (ownership unchanged). "No content is modified" is a claim about the content model, which the ASN's own *Scope* section lists as out of scope and whose state `Σ` does not carry. The proof discharges registry and effective-owner invariance, not content invariance; the phrase reads as a guarantee but is unprovable here.
**Required**: Drop "no content is modified," or restate it as a frame observation explicitly outside the ownership state ("the fork allocates `a'` and does not invoke any operation on `a`; content effects are governed by the content model").

## OUT_OF_SCOPE

### Topic 1: Provenance/effective-owner divergence under ownership transfer
**Why out of scope**: O6 fixes provenance to the account field while O2 fixes effective owner by longest match; the note correctly observes these coincide *under the system as specified* (no transfer path) and defers the divergence case to the Open Questions. Reconciling O6 and O2 once transfer exists is genuinely new territory, not a defect here.

### Topic 2: Cross-node identity federation consistency with O9
**Why out of scope**: O9 establishes node-locality as a structural barrier; what a federation layer must satisfy to remain consistent with it is correctly listed as an open question and belongs in a later ASN.

VERDICT: REVISE
