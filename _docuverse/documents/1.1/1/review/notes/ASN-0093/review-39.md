# Review of ASN-0093

## REVISE

### Issue 1: Dangling reference to dropped lemma `ChainUniformLength`

**ASN-0093, Discharge of stated invariants → "Derived lemmas at Σ₀"**: "The other chain-indexed disciplines (ChainElementT4Validity, **ChainUniformLength**, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains) are state-independent ASN-0040 citations…"

**Problem**: `ChainUniformLength` is not defined anywhere in the note. It is absent from the *Per-chain disciplines* section (which lists only ChainElementT4Validity, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension) and absent from the *Properties Introduced* table. The recent revision ("drop ChainUniformLength") removed the lemma but left this enumeration citing it. A reader cannot resolve the name.

**Required**: Delete `ChainUniformLength` from the Σ₀ enumeration. Confirm (it appears so) that no proof step relies on a uniform-length discipline — C1b preservation and the cross-document properly-prefixing argument both derive lengths directly from TA5(c)/TA5(d), not from this lemma.

### Issue 2: Scope opening paragraph is citation-strategy meta-prose

**ASN-0093, Scope**: "Downstream ASNs that operate on the link store without needing arrangement mutation… can cite this substrate directly. Downstream ASNs that need any of the deferred machinery cite a higher-layer transition model that itself depends on this substrate."

**Problem**: This advances no reasoning about the substrate's state, operations, or invariants — it prescribes how *other* ASNs should choose what to cite. It is layering rationale, the forward-reference accretion pattern the anti-bloat classifier targets.

**Required**: Remove. The "Provided"/"Deferred" lists immediately below already delimit scope.

### Issue 3: Properties Introduced table CITATION rows duplicate the *Per-chain disciplines* section

**ASN-0093, Properties Introduced (ChainElementT4Validity, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension rows)**

**Problem**: Each CITATION row restates the full claim *and* source already given verbatim in the *Per-chain disciplines* bullets (e.g., ChainEnumerationInjectivity's "strictly increasing under T1… order-preserving in both directions… cites S0" appears in both places). The table entries are full-sentence restatements rather than terse index lines — two passages saying the same thing in different words.

**Required**: Reduce the CITATION rows to one-line index pointers (name + source), or drop them and let the *Per-chain disciplines* section carry the content.

### Issue 4: StandardTriple "default not enforced" disclaimer repeated across slots

**ASN-0093, L3** ("The StandardTriple default is retained… not enforced structurally — the substrate admits arbitrary arity N ≥ 3") and **K.λ binding precondition** ("The StandardTriple default is retained for worked examples and notational compactness; the substrate admits arbitrary arity N ≥ 3.")

**Problem**: The same disclaimer appears in the invariant statement and again in the operation precondition (and a third time in the worked example's arity convention). The K.λ restatement is redundant with L3, which already carries the structural commitment.

**Required**: State once at L3; drop the duplicate from K.λ.

## OUT_OF_SCOPE

### Topic 1: Concurrent emission discipline across allocators
The Open Questions raise concurrency; SequentialTransitionAxiom commits to atomic/sequential transitions, so multi-allocator concurrency is genuinely new territory for a higher-layer ASN, not a gap here.

### Topic 2: Third-subspace (s ≥ 3) sub-allocator coordination
SubspaceConventionAxiom pins exactly two subspaces; extending to `s_C`/`s_L` beyond content and link belongs to a future ASN.

VERDICT: REVISE
