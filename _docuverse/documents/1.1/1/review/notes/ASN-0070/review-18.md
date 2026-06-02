# Review of ASN-0070

## REVISE

### Issue 1: "Single-valued both directions ⟹ partition into chains" is not valid without acyclicity

**ASN-0070, F-canonical Step 2 ("Maximal runs partition X")**: "A relation that is single-valued in both directions partitions any set into disjoint maximal chains: the connected components of such a relation are themselves chains, and distinct components are disjoint, so every element of X lies in exactly one maximal run."

**Problem**: The general set-theoretic claim is false. A relation that is single-valued in both the successor and predecessor directions decomposes into disjoint *paths and cycles*, not paths alone. (Counterexample: `1→2→3→1` on `{1,2,3}` is single-valued both ways, but its connected component is a cycle, not a chain.) The proof needs acyclicity to conclude that components are chains, and acyclicity is never invoked. The partition of `X` into maximal runs — which the entire uniqueness argument (unique reconstruction `(s_j, c_j) = (min(run), |run|)`) rests on — is therefore not yet established by the stated justification.

**Required**: Add the acyclicity observation: consecutivity `t consec t'` implies `t < t'` under T1, and `<` is irreflexive (T1(a)) and transitive (T1(c)), so following consecutive-successors strictly increases under T1 and can never return to a prior element. This rules out cycles, leaving only chains, and the partition claim then goes through. One clause citing T1(a)/(c) closes the gap; the conclusion is correct, only its justification is incomplete.

## OUT_OF_SCOPE

### Topic 1: Reporting of partially-unreached coverage, transclusion-lineage relationships, concurrency semantics, canonical-form contracts for citation

**Why out of scope**: These are raised explicitly in the Open Questions section and concern future system-level contracts (citation artifacts, concurrency guarantees, cross-document derivation relationships) rather than the inverse-image query specified here. They are correctly deferred, not gaps in this ASN.

VERDICT: REVISE
