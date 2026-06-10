# Review of ASN-0126

The framework is mathematically sound, and I want to say so plainly before the findings: the projection bridge (ProjectionBridge / B1 / B2) correctly transfers ASN-0086's three-component results to the four-component states, the effect-identity argument is right, the wp `g → S` decomposition is applied correctly with the partiality of `Sh-conf` handled (conditional conjunction, false-not-undefined at unregistered K), and the three-move R-Scope transfer for the Binary wrapper checks out — `A_rel^{π(Σ')} = A_rel^{Ψ}` because `a_emit` is blind to F, so the differing from-sets don't reach the address-domain conclusion. The boundary cases I checked (empty-F → no `→_sh` image, `|G|=0` → Unary, arity > 3 → excluded by (0), unregistered K → (i) fails, self-nullifying / pre-covered → born nullified) are all handled, and the born-nullified worked example is correct address-by-address (`g = …2.4` is the lower endpoint of `[…2.4, …2.7)`, so the citation lands in `nullified`). The remaining issues are accreted prose, which the active anti-bloat classifier asks be flagged at source.

## REVISE

### Issue 1: The naming digression in "The registry" is non-load-bearing justification with a downstream forward reference
**ASN-0126, The registry**: "A type's identity is purely positional: Nelson makes the type an address the search mechanism matches blindly... A capability that read a type's name back could not survive such a ghost, so none is part of the model... The permanence guarantees below (P1 registry-invariance, P2 shape-stability) concern that shape, which — unlike a name — *is* observable, through emit success or failure under the gate."

**Problem**: This ~150-word paragraph argues *why* the registry stores shape-not-name. No proof in the note depends on the absence of a name field — `RegisteredAdmissible`, the (i)-decidability argument, P1/P2, and P6 all use only "registry maps coverage class → shape," never "no name." The passage is removable without touching a single derivation. It matches two flagged patterns: essay content in a definitional slot (the Nelson motivation plus the "could not survive such a ghost" defensive justification), and a definition's introduction reaching forward to its downstream consumers (the P1/P2 "is observable" aside). This reads as the residue of the commit that dropped the name field — the rationale stayed after the thing it justified left.

**Required**: Reduce to the design statement actually used downstream — e.g., "The registry records only the shape, keyed by coverage class; any human-readable type label is an app-side convention over addresses, not substrate state." Cut the Nelson paragraph, the ghost-survival argument, and the P1/P2 observability sentence.

### Issue 2: "The registry" restates ASN-0086's TypeEquivalence inline
**ASN-0126, The registry**: "Keying by coverage class rather than raw endset honours ASN-0086's TypeEquivalence (lifting L8, ASN-0043), which identifies type endsets by coverage — `K ~ K' ≡ coverage(K) = coverage(K')` — and treats the type subscript as a coverage-class index, so `L_K = L_{K'}` whenever `K ~ K'`."

**Problem**: `K ~ K' ≡ coverage(K) = coverage(K')` and `L_K = L_{K'}` are verbatim ASN-0086 (TypeEquivalence and its "subscript read modulo `~`" notation). Restating a foundation the reader already holds is redundancy the precise reader skips past.

**Required**: "Keying by coverage class honours ASN-0086's TypeEquivalence" carries the point; drop the restated equation and its consequence.

## OUT_OF_SCOPE

### Topic 1: How `Σ_init.registry` is populated, and runtime/mutable registration
**Why out of scope**: The registry is immutable (P1) and fixed at `Σ_init`, so "an app registers a type" necessarily happens at initialization. The mechanism for populating `Σ_init.registry` (Open Question 4) and any loosening toward richer arity or `|F| > 1` (Open Question 6) are correctly deferred — not errors in this note. I note it only to confirm the immutable-registry choice was considered and is a defensible integration with ASN-0086's transition framework, not drift.

VERDICT: REVISE
