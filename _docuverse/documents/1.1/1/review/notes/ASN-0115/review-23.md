# Review of ASN-0115

I verified the four load-bearing arguments in detail before reaching the findings below. The Confinement lemma proof (T5 + TumblerAdd + T12) is correct; R6's gap analysis is airtight across all three cases (`V_S(d) = ∅`, `V_S(d) ≠ ∅ ∧ act = ∅`, `act ≠ ∅` forcing a canonical start), and its restriction of the no-interior-hole guarantee to the bindable depth-`m_S` slice correctly forecloses the deeper-tumbler interspersal case (e.g. `[1,2,1]` between `[1,2]` and `[1,3]`); R7's WLOG and the divergent-branch justification are sound and load-bearing; R8's subspace dispatch and the CL-OWN/CL-UNIQ link-vacuity argument are both correct. The findings are narrow.

## REVISE

### Issue 1: Mis-citation "(S7b)" for origin attribution
**ASN-0115, R9 worked instance**: "to a content address `a₁ ∈ dom(Σ.C)` that `d₁` itself allocated, so `origin(a₁) = d₁` (S7b)"

**Problem**: `S7b` is the ASN-0036 foundation claim *ElementLevelIAddresses* — `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` — which does not establish that `origin(a)` is the allocating document. The fact actually being cited ("`origin(a₁) = d₁`, the document that allocated `a₁`") is ASN-0036 **S7 (StructuralAttribution) postcondition (b)**. The bare `S7b` both points at the wrong foundation claim and is inconsistent with the ASN's own convention: two clauses later it correctly writes "`S7(c)` (StructuralAttribution)" with the parenthetical-index notation.

**Required**: change `(S7b)` to `(S7(b))` (or `(S7, StructuralAttribution post. (b))`).

### Issue 2: R9 states its determinacy citation-chain twice (anti-bloat)
**ASN-0115, R9 boxed statement and the "Two obligations" paragraph**: the boxed claim already fixes per-position home determinacy — "the document-level prefix `origin(a)` (S7); for a link position … `home(a)` (ASN-0043, L1a), which coincides with `origin` … (ASN-0086, HomeOriginCoincidence)". The following paragraph re-states the identical chain — "`origin(a)` for a content address (S7), `home(a)` for a link address (ASN-0043, L1a; coinciding with origin by ASN-0086, HomeOriginCoincidence)".

**Problem**: the same three citations (S7 / L1a / HomeOriginCoincidence) and the same content (each fragment's home is determinate from the resolution mapping) are asserted in both the formal claim and the prose justification — the "two paragraphs say the same thing in different words" pattern this review mode is meant to catch. The paragraph's genuine additive value is the Nelson grounding (4/10, 4/11) and the "lose-first → fragments, lose-second → blob" motivation; the citation chain and the closing restatement ("RETRIEVEV must give one coherent delivery and a resolution whose origins stay determinate") duplicate the box.

**Required**: keep the per-position determinacy chain in the boxed claim only; let the "Two obligations" paragraph carry the Nelson grounding and the opposing-pull motivation, referring back to the claim rather than re-deriving its citations.

## OUT_OF_SCOPE

### Topic 1: Delivery of a single boundary-straddling span
**Why out of scope**: A span whose denotation crosses from `s_C` into `s_L` is excluded by the V-spec's ordinal-level precondition, and the ASN handles the multi-subspace request by *composition* of per-subspace ordinal spans (R10) rather than one straddling span. The straddling-span semantics is correctly deferred to the matching Open Question; it is new territory, not a gap in this ASN. The remaining Open Questions (inline provenance, outright-failure semantics, unbound-reference resolution, channel faithfulness) are likewise correctly scoped out.

VERDICT: REVISE
