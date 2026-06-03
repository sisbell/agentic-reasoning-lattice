# Review of ASN-0100

This is a careful, thorough specification — the disclaiming of ASN-0082's I3-V/I3-CS/I3-CX, the forced-ordering analysis, and the composite-atomicity precondition are genuinely rigorous. The problems below are citation-grounding defects: several proofs invoke foundation lemmas under the wrong ASN number or under names that do not exist in the foundation. Because each cited lemma is the load-bearing step of its proof, a reader cannot verify the proof as written.

## REVISE

### Issue 1: OrdAddHom misattributed to ASN-0036
**ASN-0100, Effect Two (and §Post-state V-position well-formedness, §Projection-shift correspondence)**: "By OrdAddHom clause (b) (ASN-0036) applied to `w = δ(k, m_C)`…" and "By OrdAddHom (b clause, ASN-0036), `subspace(shift(p, k)) = subspace(p) = s_C`".
**Problem**: OrdAddHom (OrdinalAdditionHomomorphism), with clause (b) `subspace(p ⊕ w) = subspace(p)`, is defined in **ASN-0082**, not ASN-0036. ASN-0036 contains only OrdShiftHom (OrdinalShiftPreservation), a differently-stated lemma. A reader checking ASN-0036 for "OrdAddHom (b)" finds nothing. The subspace-preservation step underpins S8a, S8-depth, and the Right-branch closure of π — it must cite a real source.
**Required**: Correct the citation to ASN-0082 (or invoke OrdShiftHom (a), ASN-0036, in the shift form), consistently across all occurrences.

### Issue 2: S7c cited as an ASN-0036 invariant — does not exist
**ASN-0100, §Verifying the Invariants / S7 invariants**: "`#E(a_k) ≥ 2` discharges S7c (ElementFieldDepth)…" and "S7a, S7b, S7c, S7d, and the derived theorem S7, ASN-0036".
**Problem**: ASN-0036 defines S7a, S7b, S7d, and S7 — there is **no S7c**. The "element field depth `#E(a) ≥ 2`" invariant is **C1b** (ContentElementFieldDepth), defined in ASN-0093 / ASN-0047. The atomicity section repeats the error ("Per-state invariants on C (C-fin, S7a, S7b, S7c) hold…"). Relatedly, **C1c** (ContentAllocatorConformance) — a per-state invariant in ASN-0047's ExtendedReachableStateInvariants — is never explicitly discharged for the fresh `a_k`, having been displaced by the nonexistent S7c in the verification list.
**Required**: Replace S7c with C1b (and add an explicit C1c discharge for each fresh `a_k` via the A_C(d) chain conformance), citing ASN-0093/ASN-0047.

### Issue 3: M2's precondition list overstated
**ASN-0100, §Per-subspace span decomposition (S8★)**: "the post-state's standing preconditions for M2 (DecompositionExistence; ASN-0058) — S8-fin, S2, S3★, S8a, S8-depth, S7b, S7c…"
**Problem**: ASN-0058's M2 states its preconditions as "S8-fin, S2, S3, S8a, and S8-depth" — it does **not** require S7b or S7c, and S7c does not exist. The added preconditions misrepresent the foundation lemma being invoked.
**Required**: List M2's actual preconditions; drop S7b/S7c.

### Issue 4: ChainUniformLength and ChainUniformZeroCount cited as ASN-0093 lemmas — do not exist
**ASN-0100, INS.chain-shift and claims table**: "preserves length (ChainUniformLength; ASN-0093)"; **§S7 invariants**: "`zeros(a_k) = 3` discharges S7b … by ChainUniformZeroCount (ASN-0093)".
**Problem**: Neither lemma appears in ASN-0093. Uniform length under `inc(·, 0)` is **TA5(c)** (ASN-0034); `zeros = 3` for content addresses is **C1** (ASN-0093). The ASN itself elsewhere correctly cites TA5(c) for length preservation, making the invented names inconsistent within the document.
**Required**: Cite TA5(c) (ASN-0034) for uniform length and C1 (ASN-0093) for the zero count.

### Issue 5: "SubAllocatorAxiom.{Disjointness, Subspace, FirstEmission}" — reinvented naming for foundation lemmas
**ASN-0100, §Effect One, §Cross-subspace, corollaries**: "by SubAllocatorAxiom.Disjointness (ASN-0047)", "SubAllocatorAxiom.Subspace (ASN-0047)", "SubAllocatorAxiom.FirstEmission (ASN-0093)".
**Problem**: There is no "SubAllocatorAxiom" in ASN-0047 or ASN-0093. The cross-document/cross-subspace disjointness is **SubAllocatorBundle** (ASN-0047) / **DisjointSubAllocatorChains** and **CrossDocumentDisjointness** (ASN-0093); the subspace identifier is **DisjointSubAllocatorChains** (ASN-0093); first-emission structure is **FirstEmission** (ASN-0093). Per standard 7, inventing notation for something a foundation already names is a REVISE item.
**Required**: Replace each "SubAllocatorAxiom.X" with the actual foundation lemma name and ASN number.

## OUT_OF_SCOPE

None. The ASN respects the declared scope boundaries — COPY, DELETE, version creation, and link-subspace insertion are mentioned only to fix INSERT's identity character and are explicitly deferred.

VERDICT: REVISE
