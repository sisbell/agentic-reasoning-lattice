# Review of ASN-0075

## REVISE

### Issue 1: Σ.R type imprecision in Foundation Recap

**ASN-0075, Foundation Recap**: "Provenance relation `Σ.R ⊆ T × E_doc` (ASN-0047): `(a, d) ∈ R` records that document `d` has..."

**Problem**: ASN-0047 defines `Σ.R ⊆ T_elem × E_doc` where `T_elem = {a ∈ T : IsElement(a)}` — a strict subset of `T`. The foundation recap weakens the type to `T × E_doc`. While operationally harmless (the operation only consults R(a, d) for a ∈ dom(C), and content addresses are elements by S7b), the citation should match the foundation's actual typing because the element restriction is structurally meaningful — it links R's domain to T4's hierarchical parsing.

**Required**: Change to `Σ.R ⊆ T_elem × E_doc` (or note that `T_elem ⊆ T` is the actual typing).

### Issue 2: Forward reference to non-existent "worked example above"

**ASN-0075, D-DISCR proof setup**: "K.α must be bundled with an immediately-following K.μ⁺/K.ρ pair into a single composite... The bundling pattern matches the worked example above."

**Problem**: At this position in the document (inside the proof setup of D-DISCR), there is no "worked example above." The "A Worked Example" section appears later, after the SHOWDELETIONS definition and wp computations. The forward/backward reference is inconsistent with the document's actual structure.

**Required**: Either replace "above" with "below," or change the reference to point to History 1 (which does appear above), or remove the phrase entirely.

### Issue 3: "L : T ⇀ Endset^N" citation in D-IDENT

**ASN-0075, D-IDENT, Link survival**: "By L3 (NEndsetStructure, ASN-0047) together with the link-store definition `L : T ⇀ Endset^N`..."

**Problem**: The signature `L : T ⇀ Endset^N` is presented as if it were a definition cited from the foundation, but no entry with this explicit signature appears in the provided foundation. L3 supplies the cardinality/structure constraint but is not itself a signature declaration. The signature is implicit in the foundation but warrants a precise source.

**Required**: Either cite the specific foundation entry that defines the signature, or replace with a phrase like "the link store L, characterized by L3 (NEndsetStructure, ASN-0047) as a partial function from tumblers to N-tuples of endsets."

## OUT_OF_SCOPE

### Topic 1: Restoration operation semantics

**Why out of scope**: The ASN explicitly defers restoration to future work in the "Composability with Restoration" section, noting only that the output's form makes restoration possible. The actual specification of a restore operation is correctly deferred.

### Topic 2: n-ary SHOWDELETIONS

**Why out of scope**: Acknowledged in Open Questions ("How does SHOWDELETIONS generalise to families of more than two documents..."). The binary cross-document case is the natural starting scope.

### Topic 3: Concurrency consistency model

**Why out of scope**: Acknowledged in Open Questions ("If the system supports concurrent state transitions, what consistency model must SHOWDELETIONS observe..."). The current ASN assumes the sequential transition axiom from ASN-0047.

VERDICT: REVISE
