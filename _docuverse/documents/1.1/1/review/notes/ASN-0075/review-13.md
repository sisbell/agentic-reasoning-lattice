# Review of ASN-0075

## REVISE

### Issue 1: D-DISCR witness construction leaves V-position depth unfixed

**ASN-0075, §"Why the Provenance Relation Is Load-Bearing"**: "(Σ_1.C, Σ_1.L, Σ_1.E, Σ_1.M) = (Σ_2.C, Σ_2.L, Σ_2.E, Σ_2.M) on every component"

**Problem**: Both histories place `a` at `v' = [s_C, 1, ..., 1]` in `M(d')` — the canonical D-MIN★ position for an initially-empty `V_{s_C}(d')`. But the depth `m_C` of this tumbler is operational input (ValidFirstInsertionPosition in ASN-0036 treats `m` as a chosen value `≥ 2`, with the strand model fixing only the lower bound). For `M_1(d') = M_2(d')` as functions, `v'` must be the *same* tumbler across both histories, which requires the same depth choice. The proof leaves this implicit, so the agreement claim has a hidden parameter.

**Required**: Either fix the depth explicitly (e.g., "we choose `m_C = 2` throughout, giving `v' = [1, 1]` in both histories") or state that the construction is parametric over a consistent depth choice. The fix is one sentence; the witness pair otherwise works.

### Issue 2: D-IDENT phrasing about endsets is imprecise

**ASN-0075, §"Identity Preservation"**: "every link in dom(L) references content through endset spans whose entries are I-addresses; the address a is the link's referent"

**Problem**: By ASN-0036's vocabulary, an endset is a *set of spans*; a span is a (start, length) pair. The "entries" of an endset are spans, not I-addresses. The architectural point (links reference content via I-address starts of spans) is correct, but spans don't have "entries" — they have start and length. The phrasing "endset spans whose entries are I-addresses" is ambiguous.

**Required**: Restate as "endsets contain spans, each anchored at an I-address start in dom(C)" or "links reference content via spans whose start fields are I-addresses." The downstream link-survival argument (P3 preserves L; identity-preserving recovery preserves referents) is unchanged.

## OUT_OF_SCOPE

### Topic 1: Concurrent state transitions and joint snapshot consistency

**Why out of scope**: SequentialTransitionAxiom (ASN-0047) fixes the transition relation as single-event sequential. Concurrent semantics is a foundation-level extension, not an issue inside SHOWDELETIONS. Correctly deferred in the Open Questions section.

### Topic 2: Multi-document SHOWDELETIONS (k > 2 inputs)

**Why out of scope**: This ASN defines the binary operation. Generalizing to families of documents and finding the witness structure that replaces the asymmetric pair is a separate operation building on this one. Acknowledged in Open Questions.

### Topic 3: Restoration operation mechanics

**Why out of scope**: §"Composability with Restoration" forward-references restoration but does not specify it. A future ASN would formalize the restoration K.μ⁺ pattern that consumes SHOWDELETIONS output. This ASN's job is to specify the query result, not its consumers.

### Topic 4: Within-document link-subspace deletion comparison

**Why out of scope**: D-SUBSP correctly argues that cross-document deletion comparison is structurally meaningful only on the content subspace (CL-OWN forbids cross-document link sharing). Within-document temporal comparison of link material is a separate operation — not a gap in this ASN's content-subspace specification.

VERDICT: REVISE
