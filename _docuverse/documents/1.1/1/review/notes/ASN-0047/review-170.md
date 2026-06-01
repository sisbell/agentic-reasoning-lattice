# Review of ASN-0047

## REVISE

### Issue 1: J2's isolation argument cites an invariant that is false in the extended state

**ASN-0047, *Coupling and isolation*, J2 (Contraction isolation)**: "For the provenance bound Contains(Σ) ⊆ R: contraction can only remove pairs from Contains, so Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'."

**Problem**: The middle inclusion `Contains(Σ) ⊆ R` does not hold in any reachable state where a link has been arranged. `Contains(Σ)` is the *unscoped* relation `{(a, d) : a ∈ ran(M(d))}`, so for an arranged link `ℓ`, `(ℓ, d) ∈ Contains(Σ)`. But P7 + L14 give `(ℓ, d) ∉ R`: P7 forces `(ℓ, d) ∈ R ⟹ ℓ ∈ dom(C)`, while `ℓ ∈ dom(L)` and `dom(C) ∩ dom(L) = ∅`. Hence `Contains(Σ) ⊄ R` once any link is arranged. The ASN itself acknowledges this exact unsatisfiability when motivating P4★ ("P4 is unsatisfiable for the unscoped relation once link-subspace mappings exist"), yet J2's derivation is stated against the superseded unscoped bound. J2 is positioned after K.μ⁺_L and S3★ are introduced, so it is squarely in the extended-state regime.

**Required**: Restate J2's provenance-bound step against the operative bound P4★: `Contains_C(Σ') ⊆ Contains_C(Σ) ⊆ R = R'`. The conclusion (K.μ⁻ needs no coupling) is unaffected, but the cited invariant must be the one that actually holds.

### Issue 2: J4 fork mischaracterizes version-chain k=0 emissions and does not cover versions 2+

**ASN-0047, *Coupling and isolation*, J4 (Fork composite)**: "The k = 0 sibling allocation under the source's account ... and the k = 2 hierarchical descent are *not* forks under this definition; they are independent K.δ + K.μ⁺ + K.ρ composites *without the ancestry-by-address indication*."

**Problem**: This contradicts the ASN's own `A_v(d)` definition (*Sub-allocator names*): "Its first emission is `inc(d, 1)` ... subsequent emissions are T1 sibling-increments `inc(prev_version, 0)` ... Its outputs are versions of d." So the *second* version of `d_src` is created by a K.δ **k=0** event whose operand is version 1 (`inc(version₁, 0)`), and it shares `d_src`'s document-field prefix — it genuinely carries ancestry-by-address. The blanket claim that k=0 emissions lack ancestry indication is therefore false for version-chain k=0 steps. Consequently J4 (restricted to k=1) captures only the *first* version: K.δ's per-`(t,1)` uniqueness blocks `inc(d_src,1)` after the first fork, so a second J4 fork of `d_src` cannot fire, and version 2+ creation falls outside J4 entirely despite J4 claiming to model "version creation with ancestry indication."

**Required**: Either narrow J4's stated scope to "first-version creation," correcting the prose that attributes ancestry only to k=1; or extend the fork definition to admit the version-chain k=0 case (operand on `A_v(d_src)`'s frontier), so that the composite covers all versions it claims to model.

### Issue 3: Framing/meta-prose accretion in the K.δ case (ii) discharge

**ASN-0047, *K.δ case (ii) discharge and parent-allocator activation* and *ParentAllocatorDispatch (sub-lemma)***: e.g. "this is the activation case, and care is required to identify *which* allocator is being spawned ... We name the participants explicitly"; "The split is based on which allocator's tracked domain `d` inhabits, not on which K.δ event minted `d` — and these framings differ"; ParentAllocatorDispatch opens with "Which allocator minted an entity ... is a structural fact of the present state ... independent of the minting event's kind. ... The minting event's kind is immaterial to membership; only the present-state membership matters."

**Problem**: Per the forward-reference-accretion directive: this is essay-style prose explaining *why* the dispatch is framed as it is and *what care the reader should take*, rather than advancing the dispatch rule itself. The load-bearing content (cases a'/b', the T2 spawnPt premise, the GlobalUniqueness discharge) is repeatedly preceded and interleaved with restatements of the same "membership, not minting event" thesis across the sub-lemma statement, its proof, and the k=1/k=2 discharge paragraphs.

**Required**: Reduce ParentAllocatorDispatch to the dispatch rule (cases a'/b', their T10a.6 justification) and the per-case T2-admissibility premise, and delete the repeated framing commentary ("care is required," "we name the participants explicitly," "these framings differ," "the minting event's kind is immaterial").

## OUT_OF_SCOPE

### Topic 1: Abstract specification of the node-allocation registry
**Why out of scope**: NodeUniqueAllocation / NodeRegistryBootstrap depend on an external registry not modeled as a component of Σ. Whether to specify its issuing protocol, persistence, and concurrency discipline is genuinely new territory and is already flagged in Open Questions; it is not an error in this ASN.

META: not applicable — the ASN remains squarely about state, transitions, and invariants; the issues above are correctable inconsistencies, not drift.

VERDICT: REVISE
