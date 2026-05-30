# Review of ASN-0043

## REVISE

### Issue 1: PrefixSpanCoverage's "equivalently" mislabels a foundation definition as equivalent to the substantive claim
**ASN-0043, Axiom — PrefixSpanCoverage**: "`coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}` equivalently `x ⊕ δ(1, #x) = shift(x, 1)`."
**Problem**: The two statements are not equivalent. `x ⊕ δ(1, #x) = shift(x, 1)` is nothing more than OrdinalShift's defining equation `shift(v, n) = v ⊕ δ(n, #v)` (ASN-0034) unfolded at `n = 1` — it holds unconditionally and definitionally. The coverage identity `coverage(...) = {t : x ≼ t}` is the actual substantive set-theoretic claim and cannot be derived from the shift identity alone. Presenting them as "equivalent" is a logical error: it dresses a foundation triviality up as a restatement of the real claim, and it makes half the "axiom" redundant with OrdinalShift rather than axiomatic. The same mischaracterization is repeated in the Properties Introduced table.
**Required**: Drop the "equivalently …" clause, or relabel it accurately — e.g., "(note `x ⊕ δ(1, #x) = shift(x, 1)` by OrdinalShift, ASN-0034)" as a supporting identity, not an equivalent form. The axiomatic content is the coverage set identity alone.

### Issue 2: L12 carries an out-of-scope implementation essay on deletion/POOM mechanics
**ASN-0043, L12 (LinkImmutability)**: "(Gregory's implementation reveals that links do occupy V-positions … `deletevspan` removes only the POOM entry while leaving the link's own orgl and spanfilade entries intact … Accommodating this in the abstract model would require extending the arrangement semantics beyond S3 …)"
**Problem**: Deletion mechanics, POOM structure, and V-stream effects of editing are all explicitly OUT OF SCOPE for this ASN. This parenthetical does not advance L12's claim (address persistence and value fixity); it is essay content about an out-of-scope operation, accreted around the invariant. It sits alongside a separate "Note what L12 does not address" scope disclaimer in the same section — two scope blocks for one invariant.
**Required**: Delete the parenthetical. If the S3/link-V-position tension needs recording, it belongs in Open Questions as a one-line pointer, not as implementation narrative attached to L12.

### Issue 3: L14a closes with a speculative defensive justification
**ASN-0043, L14a (NonTranscludability)**: "L14a stands as an independent design requirement — if S3 is later extended to accommodate link V-positions in the arrangement layer (as Gregory's implementation evidence suggests may be necessary), non-transcludability of links must still hold by its own force, not merely as a side effect of referential integrity."
**Problem**: This paragraph imagines a hypothetical future revision of S3 and justifies *why* L14a is stated separately rather than stating what L14a *is*. It is a defensive justification anticipating a case the current model does not contain — the kind of meta-prose the anti-bloat classifier flags. The substantive content (L14a holds independently of S3) is already carried by stating it as its own invariant.
**Required**: Remove the speculative paragraph. The preceding sentence ("Under the current model, S3 together with L0+L0a satisfies L14a …") already records the relationship; the independence is established by L14a being a stated invariant, not by prose arguing for it.

### Issue 4: L1c restates its own existential formula in prose
**ASN-0043, L1c (LinkAllocatorConformance)**: "The existential binds the seed `s` alongside the spawning parameters `k₁, ..., kₙ` and the intermediate tumblers `t₀, ..., tₙ`: the chain identifies the seed, the path, and the specific T10a steps that traverse it."
**Problem**: This sentence narrates what the formula immediately above it already says — it inventories the bound variables without adding reasoning. It is meta-prose describing the structure of a claim rather than advancing it.
**Required**: Delete the sentence. The formula and the subsequent per-step admissibility explanation ("Each step is locally T10a-admissible …") carry the content.

### Issue 5: Repeated tagline duplicated across L9 conclusions
**ASN-0043, L9 (TypeGhostPermission)**: the phrase "by subspace separation under L0 and the L9 precondition" closes both the `g ∉ dom(Σ.C) ∪ dom(Σ.L)` derivation (construction of `g`) and the near-identical `g ∉ dom(Σ'.C) ∪ dom(Σ'.L)` derivation at the end of the witness.
**Problem**: Two paragraphs reach the same disjointness conclusion by the same one-line argument, restated verbatim. The second is a relocation of the first applied to `Σ'` where `Σ'.C = Σ.C` and the only new address `a ≠ g` (already in subspace `s_L ≠ s_X`).
**Required**: Establish `g ∉ dom(Σ.C) ∪ dom(Σ.L)` once, then note it transfers to `Σ'` in a clause ("unchanged at `Σ'` since `Σ'.C = Σ.C` and `a` is in `s_L ≠ s_X`") rather than re-deriving with the duplicated tagline.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as a resident axiom
**Why out of scope**: The coverage/prefix identity is a pure span/tumbler-algebra fact (it mentions only `coverage`, `δ`, `shift`, `≼`), and the ASN itself states it is "adopted here as an axiom pending a span-algebra ASN." Its permanent home is the tumbler/span-algebra layer, not the link ontology. This is correctly acknowledged as interim and is not an error in this ASN — but once a span-algebra ASN exists, L10 and L13 should consume it from there rather than from a local axiom. (Per Issue 1, the local statement still needs the "equivalently" defect fixed in the meantime.)

VERDICT: REVISE
