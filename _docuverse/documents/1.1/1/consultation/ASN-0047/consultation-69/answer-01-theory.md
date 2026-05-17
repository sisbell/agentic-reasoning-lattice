## Question 1 [theory]

> Did the Xanadu design intend each document to host a distinct "version sub-allocator" analogous to its content and link sub-allocators, or is version allocation simply a tumbler-level inc-extension of the document address with no separate allocator namespace?

# Version Allocation: Tumbler-Level Inc-Extension, Not Separate Sub-Allocator

The design intent is clearly the second option: **version allocation is a tumbler-level extension of the document address with no separate allocator namespace**. There is no "version sub-allocator" analogous to the byte (`0.1`) and link (`0.2`) subspaces.

## Nelson's Direct Statement

Nelson states this explicitly at 4/29:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The phrase "accidental extension of the document number" is decisive — versions are not a separate namespace at all; they are simply continuations of the Document field using the same digit-forking mechanism that creates documents themselves.

## The Universal Forking Mechanism

Nelson designed forking as a single uniform mechanism across all levels:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

The phrase "compressed into a single mechanism" tells us Nelson explicitly *rejected* per-level allocator distinctions. Versions are forked exactly like daughter documents — there is no separate version namespace because there is no separate version allocator.

## Contrast With Real Sub-Allocators

The byte and link sub-allocators are genuinely distinct because they appear within the **Contents** field (after the third major divider), with their own conventional digits:

| Subspace | Pattern | Description |
|----------|---------|-------------|
| Bytes | `…0.1.N` | Byte subspace, position N |
| Links | `…0.2.N` | Link subspace, sequential creation order |

From `prompts/shared/agents/personas/nelson/concepts/links.md`:
> "Breaking down the address:
> - `N.0.U.0.D` = node, account, document
> - `V` = version
> - `0.2` = delimiter + link subspace (vs `0.1` for bytes)
> - `N` = link instance number (sequential)"

Notice that `V` (the version) sits **before** the major divider that introduces the Contents field. Each version then has its own `0.1` byte subspace and its own `0.2` link subspace. The sub-allocators are scoped *within* a version, not parallel *to* it.

## Architectural Implication

Because versions live in the Document field, they inherit the document-creation semantics directly:
- A version's ID encodes its ancestry through digit position
- Each version is its own forkable point (you can fork versions of versions)
- A version is, structurally, "a subdocument" — Nelson uses these terms interchangeably ("version, or subdocument number")

This is why `CREATENEWVERSION` returns an ID whose ancestry is visible in the tumbler itself, and why links to one version can refractively follow correspondence into other versions — the version structure is the document structure, just one digit deeper.
