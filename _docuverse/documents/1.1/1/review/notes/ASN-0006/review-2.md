# Review of ASN-0006

## REVISE

### Issue 1: Position space undefined; TC7 and TC8 consistency depends on unstated assumption

**ASN-0006, "The frame" (TC7, TC8)**: TC7 states `(A q : q ≥ p : poom'(target).(q ⊕ w) = poom(target).q)`. TC8 states `(A q ∈ link_subspace(target) : poom'(target).q = poom(target).q)`.

**Problem**: The type `Pos` is never defined. The operator `⊕` is never defined. The set `link_subspace(target)` is never defined. The function `size(poom(d))` presumes a notion of cardinality or extent over the position domain that is never stated. The concrete trace uses integer positions (0, 1, 2, ...); TC8 requires positions to carry subspace structure. These two models are incompatible unless reconciled.

If positions are integers with a total order and `poom(d)` is a single function over all positions (as the state definition says: `poom(d) : Pos → Addr`), then a link position `q ≥ p` is shifted by TC7 but preserved by TC8 — a contradiction. The consistency of TC7 and TC8 depends on the unstated assumption that all link-subspace positions are strictly less than all text-subspace positions in the total ordering on `Pos`. If this structural separation holds (as it would for tumbler positions where 0.x < 1.x), TC8 is a corollary of TC7's `q < p` clause. But the ASN neither states this ordering property nor derives TC8 from TC7.

**Required**: Define `Pos`, `⊕`, `link_subspace(target)`, and `size`. State the ordering relationship between link and text positions that makes TC7 and TC8 jointly consistent. Alternatively, split `poom` into per-subspace functions (matching TC8's subspace confinement) and revise TC7 to quantify within a single subspace. The concrete trace must use the same position model as the formal postconditions.

### Issue 2: Precondition — source V-span coverage ambiguous

**ASN-0006, "The COPY operation"**: Prose says "the source V-span must resolve to content in the source's current POOM." Formal precondition says `iaddrs(source_span) ≠ ∅`.

**Problem**: The prose suggests the entire V-span must resolve — every position maps to an I-address. The formal condition requires only that at least one position resolves. If a V-span [0, 10) is applied to a 5-character document, the formal precondition is satisfied (five addresses, non-empty) while the prose intent is violated (positions 5–9 have no mapping). The downstream consequences differ: TC9's count of mapping groups, TC7's shift width `w`, and TC10's span index entries all depend on whether the source span is fully or partially covered.

**Required**: Either strengthen the formal precondition to require full coverage (e.g., `source_span ⊆ dom(poom(source_doc))`), or weaken the prose to match the formal condition ("resolves to at least one I-address"). If partial coverage is intended, state what `w` equals and how TC9 handles gaps.

### Issue 3: TC2 uses undefined predicate "p is new"

**ASN-0006, TC2**: `{a : (E p : poom'(target).p = a) ∧ p is new} = iaddrs(source_span)`

**Problem**: "p is new" is an English phrase where a mathematical predicate is needed. The new positions after COPY at insertion point `p₀` with width `w` are those in the interval `[p₀, p₀ + w)`. The current formulation cannot be evaluated without knowing what "new" means.

**Required**: Replace "p is new" with: `p ∈ [p₀, p₀ + w)` where `p₀` is the insertion point and `w = |iaddrs(source_span)|`.

### Issue 4: Concrete trace addresses do not match the declared address format

**ASN-0006, "The state we need" and "A concrete trace"**: The state section declares that every I-address has the form `Node.0.User.0.Document.0.Element` (seven positional components with zero-separators). The concrete trace uses addresses with six components: `1.0.1.0.1.1` for document A and `1.0.2.0.1.1` for document B.

**Problem**: Two issues. First, six components do not fit a seven-component template — the zero-separator before Element is missing. Second, TC13 claims `home(a) = fields(a).document`. The addresses for A and B differ in their third component (`1.0.**1**.0.1.x` vs `1.0.**2**.0.1.x`). Under the declared format parsed as `[Node=1, 0, User=?, 0, Document=?, 0, Element=?]`, the third component is the User field, not the Document field. If `fields(a).document` extracts the Document-level component, it returns the same value for both A's and B's addresses — failing to distinguish them.

The likely intent is that `fields(a).document` returns the full document identifier (the `Node.0.User.0.Document` prefix, not just the Document component). This makes TC13 work — different prefixes for A and B — but the notation `.document` suggests single-field extraction, not prefix extraction.

**Required**: Either (a) fix the concrete trace addresses to match the declared format with correct component counts and differing Document components, or (b) redefine `fields(a).document` explicitly as the composite document identifier (the address prefix through the Document level), not a single-field extraction.

## OUT_OF_SCOPE

### Topic 1: AX1 verification for link operations
AX1 is verified for INSERT, DELETE, COPY, and CREATENEWVERSION. MAKELINK and DELETELINK are absent. The universal claim that B is "unconditionally immune to anything D does" depends on AX1 holding for all operations, including unspecified ones.
**Why out of scope**: MAKELINK semantics belong in a link-specific ASN. The universal claim should be hedged to "for the operations defined so far" until link operations are specified.

### Topic 2: Link persistence axiom
TC11's deletion-independence argument requires that D's DELETE does not remove links from the global `links` set. This parallels AX2 (I-space permanence) but no analogous axiom is stated for links.
**Why out of scope**: A link permanence axiom belongs in a link-specific ASN. The assumption is consistent with the design but formalizing it is new territory.

VERDICT: REVISE
