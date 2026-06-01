# Review of ASN-0047

## REVISE

### Issue 1: GlobalLineage part (iii) reproves by induction what a one-line argument already supplies in part (ii)
**ASN-0047, *Cross-layer invariants*, GlobalLineage derivation**: Part (ii) (content) discharges `origin(a) ≼ a` in a single line — "By S7a, a is allocated under origin(a)'s prefix — formally, origin(a) ≼ a." Part (iii) (links) discharges the structurally identical claim `origin(ℓ) ≼ ℓ` with a full multi-paragraph induction over the L1c chain ("We show the stronger claim that origin(ℓ)'s prefix is preserved across the entire chain... [base, k₁=2 step, k>0 step, k=0 step] ... Instantiating at i = n gives origin(ℓ) ≼ ℓ").

**Problem**: For both content and links the document-level prefix is `N(·).0.U(·).0.D(·)`, which is literally the prefix of the element-level address up to the third zero separator — immediate from T4b's parse given `zeros = 3` (L1 for links). The link branch's chain induction reproves a fact obtainable in exactly the form part (ii) already uses. The asymmetry forces the reader to work through a long induction for a claim the document established trivially one paragraph earlier. (The induction's "stronger claim" is only scaffolding; its sole conclusion `origin(ℓ) ≼ ℓ` is the one-line fact.)

**Required**: Replace part (iii)'s induction with the same one-line T4b truncation argument used in part (ii): `home(ℓ) = N(ℓ).0.U(ℓ).0.D(ℓ)` is the prefix of ℓ to the third zero separator, so `origin(ℓ) ≼ ℓ`; then `n₀ ≼ origin(ℓ) ≼ ℓ` by transitivity. If the chain induction establishes something more than `origin(ℓ) ≼ ℓ`, state what and why it is needed; otherwise delete it.

### Issue 2: K.δ's core discharge is fragmented across the document, with ≥4 sites deferring to one downstream section
**ASN-0047, K.δ definition / §"K.δ case (ii) discharge and parent-allocator activation"**: K.δ's case (ii) precondition says the parent-allocator activation and discipline properties "are discharged in §*K.δ case (ii) discharge and parent-allocator activation*." That same section is then deferred to from ParentAllocatorDispatch ("that discharge ... is given uniformly in §*K.δ case (ii) discharge*"), the *S7d* Class-(a) prose, the *Derived distinctness corollaries*, and the worked examples.

**Problem**: This is the flagged forward-reference accretion pattern — multiple paragraphs in different sections deferring to a single downstream location. The operation's actual obligation discharge is split from the operation definition, so a reader verifying K.δ must assemble the argument from the definition, the discharge section, ParentAllocatorDispatch, and SubAllocatorBundle. The deferrals do not advance the local reasoning; they redirect it.

**Required**: Inline the case-(ii) discharge (k=0/1/2 operand, parent-allocator activation, freshness routing) at the K.δ definition, or collapse the repeated deferrals into a single pointer at one site. Eliminate the chain of cross-section "discharged in §X" redirections.

### Issue 3: P6, P7, P8 each carry a full preservation argument twice
**ASN-0047, *Cross-layer invariants* (P6/P7/P8 *Derivation* boxes) vs. Class (a) verification prose**: P8's definition gives a *Derivation* with base case (`E₀ = {n₀}`) and inductive step (K.δ requires `parent(e) ∈ E ⊆ E'`; all other transitions frame E). The Class (a) verification then restates the same induction — "P8. K.δ adds one entity e to E. (i) Node(e): outside scope... (ii) ¬Node(e): K.δ's case-(ii) precondition requires parent(e) ∈ E ⊆ E'... All other transitions hold E in frame." P6 and P7 repeat their definition-site derivations similarly.

**Problem**: Two paragraphs saying the same thing. The definition-site *Derivation* is already structured as the inductive preservation proof, so the Class (a) restatement is redundant rather than additive. (P6/P7's Class-(a) prose at least opens by pointing back — "Derivations in the *Cross-layer invariants* section above" — then still restates; P8 restates in full with no acknowledgment.)

**Required**: Pick one home for each preservation argument. If the Class (a) matrix/prose is the canonical inductive proof, reduce the definition-site *Derivation* boxes to the statement plus a one-line discharge pointer (or vice versa). Do not carry both in full.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The fork composite (J4) leaves the forked document's link subspace empty and explicitly defers any link-inheritance mechanism. This is correctly scoped out (and already recorded as an open question), not an error in this ASN.

VERDICT: REVISE
