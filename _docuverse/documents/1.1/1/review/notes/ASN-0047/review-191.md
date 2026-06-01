# Review of ASN-0047

## REVISE

### Issue 1: Foundation citation "SubAllocatorAxiom / ContentLinkSubAllocatorExistence" cannot be reconciled with ASN-0093's claim set
**ASN-0047, *Allocator hierarchy under documents***: "SubAllocatorAxiom (per ASN-0093, ContentLinkSubAllocatorExistence). The axiom is taken from ASN-0093 directly." — invoked repeatedly (K.α/K.λ freshness, FirstEmission, Namespace, T10aConformance, Disjointness, L1b first-link discharge, worked examples).
**Problem**: ASN-0093's provided claims contain no axiom named `ContentLinkSubAllocatorExistence` and no axiom named `SubAllocatorAxiom`. What ASN-0093 actually supplies are *lemmas* — `FirstEmission`, `FirstEmissionFreshness`, `DisjointSubAllocatorChains`, `ChainElementT4Validity`, `ChainDiscipline` — themselves *derived* from ASN-0040's `SiblingStream`, not posited axiomatically. ASN-0047 bundles several ASN-0093 lemmas under an invented axiom name and labels the result "axiom … taken directly." A reviewer cannot verify the citation against the foundation, and the lemma-vs-axiom status is materially different (the foundation *proves* sub-allocator existence; ASN-0047 *assumes* it). The five sub-clauses are load-bearing for K.α/K.λ freshness throughout, so the discharge chain rests on an unverifiable foundation reference.
**Required**: Replace the `SubAllocatorAxiom (ContentLinkSubAllocatorExistence)` citations with the actual ASN-0093 claim names (e.g. `FirstEmission`, `FirstEmissionFreshness`, `DisjointSubAllocatorChains`, `ChainDiscipline`, `ChainElementT4Validity`). If "SubAllocatorAxiom" is genuinely new structure assembled in *this* ASN, mark it "introduced here" and prove it from the cited ASN-0093 lemmas rather than attributing it to ASN-0093 as an axiom.

### Issue 2: Verification matrix and per-invariant prose triple-state the trivial rows
**ASN-0047, *Class (a)* matrix + following per-invariant prose + Properties tables**: The matrix preamble says "each cell summarises the load-bearing argument," then ~30 prose paragraphs "substantiate each matrix entry."
**Problem**: For the frame/precondition-only rows the prose adds nothing beyond the cell. *S7a*: cell "precondition origin(a)∈E_doc; preserved by P0" — prose "Established by K.α's precondition…; preserved by P0 thereafter." *S7b*, *C1b*, *L1*, *L1a*, *L3*, *L-fin*, *C-fin* are each pure restatements of their cell, and several are restated a third time in the Properties tables. This is distinct from the previously-declined "expand the cells" finding — the issue is *duplication of trivial content*, not under-specification. A reader follows the same claim three times. (Non-trivial rows — S8★, K.μ~, D-SEQ★ — legitimately need prose; those are fine.)
**Required**: For frame/precondition-only invariants, keep the matrix cell and delete the restating prose paragraph (or vice-versa); reserve prose for rows whose discharge is non-trivial.

### Issue 3: Defensive justification and use-site inventory around the M-totality override and foundation provenance
**ASN-0047, *Typing note (M total — overrides foundation)*** and scattered axiom restatements: The typing note enumerates which foundation results "carry verbatim under the substitution" (M0, M1, K.α/K.λ binding precondition, K.σ effect, SubAllocator activation); "The axiom is taken from ASN-0093 directly" recurs for SequentialTransitionAxiom, SubspaceConventionAxiom, SubAllocatorAxiom, L0, L3.
**Problem**: The override statement `d ∈ dom(M) ⟺ d ∈ E_doc` and the M2 exception are load-bearing and should stay; the *inventory* of downstream foundation results that "read verbatim" is the use-site-enumeration pattern, and the repeated "taken from ASN-0093 directly" is provenance noise. This is prose the precise reader skips to reach the claim.
**Required**: Keep the override identity and the M2 carve-out; drop the verbatim-carryover inventory and collapse the repeated provenance annotations into a single statement.

## OUT_OF_SCOPE

### Topic 1: J4 "Definition (Fork)" specifies CREATENEWVERSION
**ASN-0047, *J4 (Fork composite)***: gives Fork a formal `Definition` with precondition (`d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅`) and a three-step characterization, explicitly identified with "Nelson's … CREATENEWVERSION (LM 4/66)."
**Why out of scope**: The scope list names CREATENEWVERSION among excluded named operations with their preconditions/postconditions. Demonstrating that fork *decomposes* into K.δ+K.μ⁺+K.ρ is legitimate transition-taxonomy, but the formal precondition-bearing `Definition (Fork)` (and likewise the three replacement-form specs) leans into named-operation specification that belongs in a future operations ASN. Recommend retaining the decomposition observation and deferring the operation-level precondition.

VERDICT: REVISE
