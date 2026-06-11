# Review of ASN-0118

This ASN is in strong shape: the composite decomposition is exhibited rather than asserted, the K.μ⁻/K.μ⁺ split in the displacing case is argued step-by-step with the link-subspace retention handled explicitly, the J1★/J1'★ discharge covers all three provenance branches (including the re-COPY-of-deleted-content case via P2 and the not-range-new case via P4★ at a composite boundary), the no-holes tiling is derived from TS1/TS3/TS4 rather than waved at, the wp analysis for link discoverability is non-trivial, and the worked two-source example checks CP1/CP2/CP3a/CP8/CP11 numerically including the self-transclusion provenance variant. Three issues remain.

## REVISE

### Issue 1: V-spec definition silently weakens ASN-0058's ContentReference condition (iii)
**ASN-0118, "What a spec-set names, and what resolution recovers"**: "A *V-spec* is an ASN-0058 *ContentReference* `ρ = (d_s, σ)` … It is *level-uniform* (ASN-0058 condition (iii); ASN-0053, S6): `#s = #ℓ`" and later "The span's boundary tumblers are constrained no further: the start `s` need not be a bound position of `d_s`, nor an S8a-well-formed V-position at all … a start with a zero component or an unbound shape selects less, never errors."

**Problem**: ASN-0058's condition (iii) is `#ℓ = #u = m`, where `m` is the common V-position depth of the source subspace (S8-depth) — it pins the span's depth to the subspace depth. The ASN restates (iii) as bare level-uniformity `#s = #ℓ`, dropping the `= m` conjunct without comment, while simultaneously claiming the V-spec "is an ASN-0058 ContentReference." The two readings diverge on a live admissibility boundary: a depth-mismatched span can still capture active positions. Concretely, in a depth-2 text subspace, `s = [1,1,5]`, `ℓ = [0,9,0]` is T12-well-formed, level-uniform, and non-ordinal-level (which the ASN explicitly admits); its denotation `{t : [1,1,5] ≤ t < [1,10,0]}` contains the bound positions `[1,2], …, [1,9]`. Under full inheritance of (iii) this spec is inadmissible (`#ℓ = 3 ≠ m = 2`); under the ASN's restatement it is admissible and resolves. The "constrained no further" / "unbound shape" prose is only consistent with the relaxed reading, so the document contradicts its own claim of inheritance. Nothing downstream actually needs the depth pin — resolution's single-subspace and single-depth facts are recovered from `act(ρ, Σ) ⊆ V_{s_C}(d_s)` plus S8-depth on the active positions, as the ASN itself argues — so this is a definitional-honesty defect, not a soundness hole, but as written the operation's precondition is ambiguous.

**Required**: Pick one. Either (a) inherit conditions (i)–(iii) verbatim, in which case the start *is* depth-constrained to `m`, and the "constrained no further" sentence and the Gregory "unbound shape" gloss must be narrowed to within-depth freedom (unbound positions, zero components at positions 2..m); or (b) define V-spec admissibility natively (T12 + `#s = #ℓ` + `V_{subspace(s)}(d_s) ≠ ∅`), state explicitly that ASN-0058's depth pin `#u = m` is deliberately relaxed, and stop calling the object "an ASN-0058 ContentReference" simpliciter — it is a relaxation of one. In either case, say whether the depth-mismatched example above is admissible.

### Issue 2: CP11's multiset gloss contradicts its own formula and the worked example
**ASN-0118, "Non-contiguous assembly, and the boundary between reuse and replication"**: "written with multiset brackets `⦃·⦄`, so a home shared by several fragments is counted once per fragment — `⦃ origin(cᵢ) : 0 ≤ i < W ⦄`"

**Problem**: The formula counts once per placed *address* — it has `W` elements — and the worked example confirms this: source A contributes one two-address fragment, and the placed multiset is `⦃d_A, d_A, d_B⦄`, with `d_A` counted twice. But "fragment" in the surrounding prose means a contiguous block/run ("one mapping block per run," "each fragment retains its distinct home"), and counting once per *fragment* would give `⦃d_A, d_B⦄`. The gloss and the formula disagree under the document's own usage of "fragment."

**Required**: Correct the gloss to per-address counting ("counted once per placed address, so a home contributing several addresses appears with that multiplicity"), or explicitly define "fragment" as a single placed address — and make the usage consistent with the block-level sense used two sentences later.

### Issue 3 (anti-bloat): REPLICATE is defined twice
**ASN-0118, "The transclusion frame" and "Non-contiguous assembly"**: "Suppose an operation REPLICATE did the second thing: allocate fresh `c'ᵢ ∉ dom(Σ.C)`, set `Σ'.C(c'ᵢ) = Σ.C(cᵢ)`, and bind `Σ'.M(d)(p+i) = c'ᵢ`. Then … `origin(c'ᵢ) = d`" versus "REPLICATE would allocate `W` fresh contiguous addresses under the destination and copy the values; every placed address would have `origin = d`, collapsing the origin multiset…"

**Problem**: The second passage re-defines the rejected operation and re-derives the `origin = d` consequence already established in the transclusion-frame section; only the multiset collapse and seam erasure are new content there. This is the same-content-in-different-words pattern this note's anti-bloat classifier asks to be caught at source. (The third, brief REPLICATE mention in the link-survival section adds a genuinely new consequence — link loss — and is fine.)

**Required**: Define REPLICATE once, in the transclusion-frame section; have the non-contiguous section state only its new consequence (`⦃d, d, …, d⦄` collapse, seam erasure) by reference to that definition.

## OUT_OF_SCOPE

### Topic 1: Transclusion into the link subspace
**Why out of scope**: The ASN restricts placements to `s_C` by precondition and parks "placing a link by reference" as an Open Question. That is the right disposition — link-subspace placement interacts with CL-OWN/CL-UNIQ (a document's link subspace may contain only its own links, per ASN-0047), so it is a future ASN's problem, not a gap here.

### Topic 2: Undiscoverability after later removal of transcluded positions
**Why out of scope**: The Open Question about when a COPY-acquired link becomes undiscoverable again is contraction-side weakest-precondition territory (LP12a), which belongs to the DELETE reframing, explicitly excluded from this ASN's scope.

### Topic 3: Width guarantee under partial binding
**Why out of scope**: The shortfall of resolved width `W` below a partially-bound span's nominal extent (the C2 analogue) is correctly identified as an Open Question; specifying a guarantee there is new design territory, not an error in this ASN — though note its resolution couples to Issue 1's admissibility decision.

VERDICT: REVISE
