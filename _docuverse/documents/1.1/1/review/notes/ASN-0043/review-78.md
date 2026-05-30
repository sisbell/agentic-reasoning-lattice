# Review of ASN-0043

## REVISE

### Issue 1: L1b carries a "why the axiom is needed" rationale paragraph
**ASN-0043, L1b (LinkElementFieldDepth)**: "The degeneracy at depth 1 sits in TA5 sibling allocation, not in shift mechanics. Consider a link address with element field `[s_L]`... TA5 sibling allocation via `inc(·, 0)` advances the rightmost component... L1b is the depth threshold that makes TA5 sibling allocation subspace-stable for link addresses..."
**Problem**: L1b's content is `#E(a) ≥ 2`. The surrounding paragraph is a rationale explaining *why* the constraint exists (so sibling allocation preserves subspace), not what it asserts. This is exactly the "new prose around an axiom explains why it is needed rather than what it says" accretion pattern. The reader must skip the whole worked-counterexample to reach the actual invariant. The trailing pointer "The worked example below uses element field `[2, 1]`... consistent with this constraint" is a use-site inventory item.
**Required**: Reduce to the invariant plus at most one sentence noting that depth ≥ 2 keeps `subspace_I(a) = E(a)₁` stable under `inc(·, 0)`. Drop the counterexample walkthrough and the worked-example pointer.

### Issue 2: L1c preamble and "Joint floor with L1b" are meta-prose / reviser drift
**ASN-0043, L1c (LinkAllocatorConformance)**: "L1c is a single chain-existential clause, quantified over `a ∈ dom(Σ.L)`. The clause asserts the existence of a T10a-valid step sequence... it is a structural producibility statement about each address presently in `dom(Σ.L)`." and "*Joint floor with L1b.* L1c's local floor is `n ≥ 1`... L1b sharpens this to `n ≥ 2`... The existential here states the local producibility chain; the joint constraint with L1b is implicit and tightens the structural floor to `n ≥ 2`."
**Problem**: The preamble describes what the clause *is* before stating it — content-free framing. The "Joint floor" paragraph reconciles L1c against L1b and concludes the constraint is "implicit"; but L1c's existential as written carries no `#E` clause, so the paragraph advances no part of L1c's stated content. It is a paragraph imagining the interaction of two invariants and deferring the resolution ("implicit"). Both match the flagged reviser-drift patterns.
**Required**: Delete the preamble; lead with the *Chain* clause directly. Remove the "Joint floor with L1b" paragraph — if the `n ≥ 2` floor matters it belongs as a single clause inside the existential, not as cross-invariant commentary.

### Issue 3: Home and Ownership re-derives the L1c `s = h(a)` postcondition
**ASN-0043, Home and Ownership**: "The equality `home(a) = d`... is structural and already discharged: by L1c, the T10a-conforming allocator chain producing `a` starts from the T4-valid document-level seed `s = d`... and L1c's `s = h(a)` postcondition identifies that seed with the link's home-document prefix. That postcondition is itself derived from CPP. Hence `home(a) = h(a) = s = d`."
**Problem**: This re-walks the chain/CPP/`s = h(a)` reasoning that L1c already establishes as a named postcondition, then re-derives `home(a₁) ≠ home(a₂)` from it. Multiple sections now defer to and restate the same `s = h(a)` postcondition (the "single `k₁ = 2` step" paragraph in L1c, the L1c postcondition itself, and here). This is "multiple paragraphs in different sections defer to the same downstream location" plus restatement.
**Required**: Cite L1c's `s = h(a)` postcondition once and state `home(a) = s = d` in one line. Drop the re-derivation of CPP and the chain.

### Issue 4: L7 "Scan of the L-invariants" restates every invariant
**ASN-0043, L7 (DirectionalFlexibility)**: "*Scan of the L-invariants.* ... L0 partitions subspaces by tumbler address. L1, L1a, L1b, L1c constrain the link address itself... L5 makes each endset a set. L6 establishes positional addressability... L-fin is a finiteness clause..."
**Problem**: The scan re-describes the content of each of L0–L14 to conclude none mentions directionality. The re-description duplicates each invariant's own statement; the load-bearing observation is the single sentence that follows ("No invariant uses the words 'from,' 'to,' 'source,' 'target'..."). The per-invariant inventory is the "use-site inventory" pattern.
**Required**: Collapse the scan to the one-sentence observation that no invariant references slot directionality or the source/target roles, verified by inspection. Drop the line-by-line restatement.

### Issue 5: Open Questions item justifies document organization
**ASN-0043, Open Questions**: "*Relocation of PrefixSpanCoverage.* The PrefixSpanCoverage identity is axiomatized in this ASN but has no link-specific content... It should be re-homed as a derived lemma in a span-algebra or tumbler-algebra ASN once that ASN exists..."
**Problem**: This is prose about where the axiom *should live*, not a system-guarantee question about the link model. It matches "prose justifies document ordering / re-homing." An axiom the ASN itself labels as having "no link-specific content" is better resolved by stating its provenance inline (one sentence at the axiom) than by an open-question paragraph arguing for future relocation.
**Required**: Remove the relocation open-question; if provenance is worth noting, attach one clause to the PrefixSpanCoverage axiom ("a span/tumbler-algebra fact, adopted here as an axiom pending a span-algebra ASN").

## OUT_OF_SCOPE

(none — the substantive content is sound and within the link-model boundary; the findings above concern accreted prose, not missing guarantees.)

VERDICT: REVISE
