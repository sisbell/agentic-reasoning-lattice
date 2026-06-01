# Review of ASN-0047

## REVISE

### Issue 1: Reinvented notation for foundation predicates
**ASN-0047, Notation**: "`IsElement(a)`, `IsNode(a)`, `IsAccount(a)`, `IsDocument(a)`: pure abbreviations for ASN-0045's level predicates `Element(a)`, `Node(a)`, `Account(a)`, `Document(a)` respectively … `ValidAddress(t) := T4-valid(t)` (ASN-0045) throughout this ASN; the two spellings are synonyms."

**Problem**: This is exactly the case Standard 7 forbids — inventing new spellings (`IsElement`/`IsNode`/`IsAccount`/`IsDocument`, `ValidAddress`) for predicates a foundation already defines (`Element`/`Node`/`Account`/`Document`, `T4-valid`). The ASN then uses *both* spellings interchangeably (e.g. `T4-valid(s)` in L1c, `ValidAddress(e)` in K.δ; `Element(a)` is never used but `IsElement` is). Dual synonyms for a foundation concept are precisely the reinvented-notation noise the foundation rule targets, and the inconsistent mixing forces the reader to track two names per concept.

**Required**: Use the ASN-0045 spellings (`Element`, `Node`, `Account`, `Document`, `T4-valid`) directly throughout, or, if the `Is*` prefix is genuinely preferred for readability, drop the foundation spellings entirely and use the synonyms uniformly. Do not carry both.

### Issue 2: Forward-reference accretion — repeated deferrals to the same downstream sections
**ASN-0047, multiple sites**: J1★/J1'★ are used in the elementary-transition narrative, in the J0 paragraph, and in the P4a definition, each time deferring to the same place: "The operative provenance couplings — J1★ … and its converse J1'★ … are stated in their operative content-subspace form in *Scoped coupling constraints* below." K.μ~ is likewise deferred from several sites to "§*Decomposition of K.μ~* below." Accompanying meta-prose includes "The discharge sites below cite this mechanism rather than restate it" (P4a box) and "the prose below does not repeat that justification per row" (verification matrix).

**Problem**: This is the flagged forward-reference accretion pattern — multiple paragraphs in different sections deferring to one downstream location, plus prose whose only function is to announce that other prose will not repeat itself. None of it advances a claim; the reader must skip past it to follow the argument, and these pointers compound across cycles.

**Required**: State each coupling (J1★, J1'★) and the K.μ~ composition once at first use and reference by name thereafter without the "stated below / will not repeat / discharge sites cite this" scaffolding. Remove the meta-sentences that only describe the document's own organization.

### Issue 3: Motivation-of-clause prose imagining excluded cases
**ASN-0047, Decomposition of K.μ~ (admissibility clause iii)**: "Without clause (iii), a bijection meeting clauses (i)–(ii) could carry a subspace's canonical sequence onto one of greater depth (e.g. depth-2 `{[1,1],[1,2]}` onto depth-3 `{[1,1,1],[1,1,2]}` …), and the Domain-fixity result below would fail."

**Problem**: This paragraph reasons about a state the clause it accompanies explicitly excludes, and exists to justify *why* clause (iii) is present rather than to state *what* it requires. Combined with the K.δ k=1 "The operation is uniform across operand provenance — only the surface predicate `t ∈ E_doc` is checked at firing time," these are the "explain why needed / imagine an excluded case" patterns the anti-bloat classifier targets.

**Required**: Keep the clause statement and a one-line consequence (clause (iii) ⟹ depth fixity, hence K.μ~-FIX); drop the counterfactual depth-2→depth-3 elaboration and the firing-time-uniformity aside.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The fork composite (J4) starts d_new's link subspace empty and the ASN notes a link-inheritance mechanism "is outside this ASN's scope." This is correctly deferred (a future ASN), not a gap here.

### Topic 2: Tombstoning / interior link withdrawal
D-CTG★/D-MIN★ confine K.μ⁻ on the link subspace to suffix truncation, so interior link withdrawal needs a separate mechanism. This is appropriately raised as an open question rather than specified here.

VERDICT: REVISE
