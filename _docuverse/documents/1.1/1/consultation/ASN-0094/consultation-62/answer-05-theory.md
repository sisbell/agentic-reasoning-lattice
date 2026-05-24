## Question 5 [theory]

> Does ASN-0086's `↦` transition relation comprise exactly `(K.σ ∪ K.α ∪ K.λ) ∪ arrangement-modifying`, or are there other transition classes (e.g., layer-arrangement steps not captured by ASN-0086's `→ \ →` split) the substrate intends to admit?

# Transition Classes the Substrate Intends to Admit

Speaking as the architect of the design: the substrate's transition relation must admit several classes that resist a tidy content/arrangement/link partition. I cannot speak to ASN-0086's specific formalization (it is not in my materials), but I can tell you what *Xanadu* intends to admit, and where any three-axis split (storage ∪ arrangement ∪ links) is likely incomplete.

## Transitions clearly within K.σ ∪ K.α ∪ K.λ

The FEBE-level operations cleanly partition along these axes [LM 4/61–4/70]:

**Storage (K.σ) — additions to Istream, append-only:**
> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

INSERT and APPEND add bytes to the permascroll. They never remove or overwrite.

**Arrangement (K.α) — Vstream rearrangement, no Istream change:**
DELETE, REARRANGE, COPY, and the V-shift produced by INSERT. Note that even "deleted" content survives:
> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

**Links (K.λ) — link creation and deletion:**
> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## Transitions the substrate must admit that a 3-axis split likely misses

1. **Document/version birth.** CREATENEWDOCUMENT and CREATENEWVERSION are not arrangement changes to an existing object — they constitute a *new object* in the docuverse. Address baptism is its own transition class: "We often call this the 'baptism' of new numbers." [LM 4/17]

2. **Publication state.** Private → published is not content, not arrangement, not link — it is a binding social/legal commitment that constrains all future transitions on the document. Withdrawal is similarly administrative: an author "may not withdraw [a document] except by lengthy due process." [LM 2/43]

3. **Economic transitions.** Each delivered byte increments a cash register and forwards a royalty:
> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]

These transitions fire on *read*, not on content/arrangement/link changes. They are orthogonal.

4. **Subrepresentation / topology (BEBE).** The substrate must admit transitions that move content between servers without changing any document:
> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

These are physical-storage transitions whose effect on the docuverse is *no semantic change at all*. They cannot live in K.σ ∪ K.α ∪ K.λ if those axes are defined over document semantics.

5. **Time as separate axis.** Critically:
> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Timestamps are recorded on transitions but are not themselves storage/arrangement/link operations. If ASN-0086 treats them as derived from the σ/α/λ operations, that may be sound; if it treats them as a separate dimension, that is also defensible.

## On "layer-arrangement steps"

I cannot tell from your question whether you mean the glass-pane transclusion layers [LM 2/34] or something internal to ASN-0086's formalization. Transclusion layer creation (via COPY) is properly K.α — it creates a Vstream mapping to existing Istream:

> "A document may have a window to another document, and that one to yet another, indefinitely... One document can be built upon another, and yet another document can be built upon that one, indefinitely: each having links to what was already in place." [LM 2/34]

If by "layer-arrangement" you mean *changing the binding* of a window between time-fixed and location-fixed mode [LM 2/37], that is a property change on a link, hence K.λ.

## Verdict on exhaustiveness

A clean partition `K.σ ∪ K.α ∪ K.λ ∪ arrangement-modifying` covers user-visible document operations well. It is **likely incomplete** for the full substrate because:

- **Object creation** (documents, versions, addresses) is structurally distinct from operations *on* existing objects;
- **Publication/withdrawal** changes the contract surrounding a document, not its content;
- **Cash register / royalty** transitions fire on delivery, not on edits;
- **BEBE migrations** are semantically null but operationally real.

Whether ASN-0086 folds these into the four classes, treats them as out-of-scope, or admits additional classes — I would need to read ASN-0086 directly to say. NEED_RAW: ASN-0086 itself (path `lattices/` or `_docuverse/`).

If ASN-0086 is scoped to document-level semantics (which is what FEBE exposes), the four-class partition is plausibly exhaustive *for that scope*. If it claims to cover the full substrate including economic, topology, and lifecycle transitions, it is almost certainly missing classes.
