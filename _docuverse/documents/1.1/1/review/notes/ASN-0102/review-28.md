# Review of ASN-0102

## REVISE

### Issue 1: Redundant rationale paragraph in the ValidComposite★ amendment

**ASN-0102, "Definition of COPY" (Amendment to ValidComposite★)**: "This restriction is not arbitrary fiat. COPY writes provenance *directly* into `Σ.R` and can place *already-referenced* content, so its J1'★ discharge has an `Old`-branch (X14) that leans on P4★ ... Confining COPY to a standalone composite makes its pre-state a boundary, supplying the P4★ on which X14's discharge rests; X14 carries the full argument."

**Problem**: This paragraph restates the operative chain already established one paragraph earlier ("its endpoints Σ and Σ' are composite boundaries, at which the composite-boundary properties ... in particular P4★ ... hold") and then defers the actual argument downstream ("X14 carries the full argument") to a location that does in fact carry it. The reader must skip past motivational rationale (why the restriction is needed, which downstream proof leans on it) to reach the only object-level content in the paragraph — the scope consequence that a COPY whose source/target is mutated mid-composite is out of scope. This is the flagged forward-reference pattern: rationale prose around the restriction explaining *why* it is needed rather than *what* it does, plus a deferral to the same downstream location (X14) the first paragraph already pointed at.

**Required**: Trim the rationale and deferral; retain only the scope-consequence sentence ("a COPY whose source or target is mutated earlier in the same composite is outside this note's scope; ... must be expressed as a separate standalone COPY against the already-committed boundary state"). The P4★-availability fact is already stated in the preceding paragraph and proved in X14.

### Issue 2: Duplicated provenance-vs-derived-containment distinction

**ASN-0102, Definition ("Provenance")** states: "This is a state component distinct from the *derived* containment relation `Contains_C` (which reads off `Σ'.M` automatically); the provenance relation `Σ.R` records the fact persistently." **X14** restates the same distinction: "Containment is read off `Σ'.M` and is therefore automatic; the *provenance* relation `Σ.R` is a separate state component, which COPY's effect populates explicitly."

**Problem**: Two paragraphs in different sections make the identical point (Σ.R is a stored component, Contains_C is derived). The Definition's statement is sufficient; X14 re-establishes it before the discharge rather than using it.

**Required**: State the distinction once (in the Definition) and have X14 use it rather than re-assert it.

## OUT_OF_SCOPE

### Topic 1: Re-displacement and continued discoverability of copied content
The Open Questions correctly defer the interaction of a later displacing operation with origin-traceability and discoverability to a future note; this depends on INSERT/DELETE mechanics that are out of scope here.

VERDICT: REVISE
