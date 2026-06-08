# Review of ASN-0112

## REVISE

### Issue 1: V0's codomain conflates two distinct ASN-0053 types
**ASN-0112, "What the caller must be handed" / V0**: "`RETRIEVEDOCVSPAN : dom(M) → Span + {⟨⟩}` … where `Span` is the type of T12 spans (a pair `(s, ℓ)`) and `⟨⟩` is the empty span-set of ASN-0053".

**Problem**: The two summands are not the same kind of object. The non-empty branch returns a bare `Span` (a pair), while the empty branch returns a `span-set` (a *sequence* of spans, ASN-0053). The codomain is therefore `Span ⊎ SpanSet`, a heterogeneous union. The note asserts the summands are "genuinely distinct" but never justifies why the populated case is a `Span` rather than the singleton span-set `⟨σ_d⟩` — which would make the codomain uniformly `SpanSet` and would let `⟨⟩` sit in the same type as the non-empty result. As written, a precise reader must hold two ASN-0053 types in one return position.

**Required**: Either (a) return a span-set uniformly (`⟨σ_d⟩` when non-empty, `⟨⟩` when empty), so both summands inhabit one ASN-0053 type, or (b) use a span-option (`Span + {⊥}`) and stop borrowing ASN-0053's span-set `⟨⟩` for the sentinel. Pick one and state why the asymmetry, if retained, is intended.

### Issue 2: V-frame is over-justified — prose explains why the frame matters rather than what it asserts
**ASN-0112, opening / Claims table (V-frame)**: "This is the operation's defining frame: an alternative implementation of 'boundary query, not a content read' must satisfy it, distinguishing the query from any transition that edits the arrangement it measures." and the table parenthetical "(purity of the transition, distinct from V16's purity of the returned value)".

**Problem**: `Σ' = Σ` for a pure query is self-evident; the claim states what it says in one symbol. The surrounding prose and the table parenthetical are defensive disambiguation — they argue why V-frame deserves to exist and pre-empt confusion with V16 rather than advancing the claim. This is the anti-bloat pattern (prose around a frame explaining its necessity, plus a use-distinction the reader must parse). The reach is the only thing under genuine tension in this note; the no-mutation frame is not.

**Required**: Reduce V-frame to its assertion (`Σ' = Σ`, components enumerated) and drop the "an alternative implementation must satisfy it" justification and the "distinct from V16" parenthetical. If the transition-purity vs value-purity distinction is worth stating, state it once, not in both the intro and the table.

## OUT_OF_SCOPE

(none — the note correctly excludes content delivery, per-subspace reporting, version reports, and link operations, routing the corresponding questions to Open Questions.)

VERDICT: REVISE
