# Review of ASN-0026

## REVISE

### Issue 1: Derived definitions not catalogued in Properties Introduced

**ASN-0026, Consequences**: `correspond(d_1, p_1, d_2, p_2) == Sigma.V(d_1)(p_1) = Sigma.V(d_2)(p_2)` and `origin(content at V-position p in document d) = fields(Sigma.V(d)(p))`

**Problem**: Both `correspond` and `origin` are formally defined in the Consequences section and relied upon in the version correspondence and origin traceability arguments. Neither appears in the Properties Introduced table. Future ASNs that formalize version comparison or attribution will need to reference these definitions by label.

**Required**: Add both to the Properties Introduced table with status "introduced" (or "derived"), giving each a stable label.

### Issue 2: Nelson's FEBE operations not reconciled with ASN operation set

**ASN-0026, P3 section**: "Nelson's FEBE protocol defines exactly five editing operations (INSERT, APPEND, COPY, DELETEVSPAN, REARRANGE). None performs transformation."

**Problem**: The P3 section cites Nelson's five FEBE operations as evidence, but the Operations Classification table lists a different set: INSERT, DELETE, REARRANGE, COPY, CREATENEWVERSION. The mapping is nowhere stated: INSERT subsumes APPEND (since P9 allows `p = n_d + 1`), DELETE corresponds to DELETEVSPAN, and CREATENEWVERSION is additional (not one of the five editing operations). A reader cannot verify whether the ASN's operation set covers Nelson's without this correspondence.

**Required**: One sentence after the Operations Classification table stating the mapping between Nelson's five FEBE operations and the ASN's operation set, and noting that CREATENEWVERSION is a document-level operation outside the five.

## OUT_OF_SCOPE

### Topic 1: Document creation bootstrapping

The initial state has `Sigma_0.D = emptyset`. The five text-content operations all require an existing document (INSERT, DELETE, REARRANGE operate on `d in Sigma.D`; COPY reads from a source in `Sigma.D`; CREATENEWVERSION requires a source in `Sigma.D`). No operation can produce the first document. A CREATEDOCUMENT operation (or equivalent administrative command) is needed to reach non-trivial states.

**Why out of scope**: Document creation is not a text-content operation. The ASN correctly restricts itself to the five text-content operations. A document lifecycle ASN would introduce the creation operation and verify that it establishes P2, P7, etc. for the newly created (presumably empty) document.

### Topic 2: DELETE, REARRANGE, COPY, CREATENEWVERSION formal postconditions

The ASN gives P9 for INSERT but defers full postconditions for the other four operations. Each needs an analogous mapping-preservation statement (surviving positions retain I-addresses, positions renumber to maintain the dense interval).

**Why out of scope**: The ASN explicitly says "Full definitions are deferred to their respective operation ASNs." P9 is included because it is needed for the worked example and the P2/REF-STABILITY arguments.

### Topic 3: Version DAG structure

CREATENEWVERSION creates parent-child relationships between documents, forming a DAG. The ASN does not formalize this structure. The open questions section asks whether the derivation relationship must be explicitly recorded.

**Why out of scope**: The version DAG is a versioning concern, not an I-space/V-space concern. The current ASN establishes that CREATENEWVERSION shares I-addresses, which is the prerequisite for a versioning ASN.

### Topic 4: Empty document well-formedness

The ASN raises whether `n_d = 0` is a valid state as an open question. P9's precondition handles it correctly (INSERT at `p = 1` into an empty document), but whether the state model permits empty documents is unresolved.

**Why out of scope**: Resolving this requires deciding whether CREATEDOCUMENT produces an empty document or whether every document must be born with content. That decision belongs in a document lifecycle ASN.

### Topic 5: Link model formalization

Link survivability is correctly stated as a claim. The partial proof (I-addresses persist by P1) is sound as far as it goes. Discoverability depends on the link index, which is not modeled here.

**Why out of scope**: The link model is separate territory. The current ASN provides the I-space persistence guarantee that a link ASN will build on.

VERDICT: CONVERGED
