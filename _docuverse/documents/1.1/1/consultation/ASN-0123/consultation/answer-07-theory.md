## Question 7 [theory]

> What invariant must the fork operation maintain about the source document — must its identity, its content, and its own version history remain completely untouched by the creation of a descendant?

# The Fork Invariant: Absolute Non-Destruction of the Ancestor

Yes — and the requirement is stronger than "should." It is a **conservation law**. The creation of a descendant is a purely *additive* act in the docuverse; it may add a new document, a new address, and a new relationship, but it may **touch nothing about the source**. All three of the things you name — identity, content, and the source's own version history — must remain completely invariant. This is not an incidental property of my fork operation; it is the whole reason the operation is worth having.

The protocol command itself states the shape of it: `CREATENEWVERSION` is defined so that

> "This creates a new document with the contents of document `<doc id>`. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

Notice every clause is about the *new* document. It **creates a new document**. It **returns the new id**. The **new** id carries the ancestry. Nothing in the definition reaches back and mutates `<doc id>`. The source is named only as a *source* — read from, never written to.

Let me take your three invariants one at a time, because each rests on a different part of the architecture.

## 1. Identity is untouched

The source keeps its tumbler address, permanently and unchanged. The descendant is a *new baptism* in tumbler-space — a fresh address forked under the parent to record lineage — but forking never renumbers or relocates what already exists:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The phrase to hold onto is **"the other addresses remain valid."** Baptizing a descendant cannot invalidate, move, or overwrite the ancestor's address. A reference made to the source yesterday resolves to exactly the same thing after the fork as before it.

And here is a subtlety that matters for your question. The fact that the descendant's address sits *under* the source's is a fact about the addressing coordinate, **not** a claim imposed on the source:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

So even the addressing relationship is non-committal — it imposes no obligation, no flag, no mutation on the parent. The derivation relationship, where there is one, is carried on the *descendant's* side (its id, and a link recording the lineage), not stamped into the ancestor.

> NEED_RAW: [4/29] — the page I read continues "The relationship of derivation, where there is one, is shown by links," which strengthens this point (ancestry is recorded as a link, not as a modification of the source), but that exact sentence is beyond the verified curated extract, so treat it as needing confirmation.

## 2. Content is untouched

This is the deepest of the three, and it is what separates my system from "Save As." A fork does **not copy** the source's bytes — it *shares* them by reference. The descendant's virtual byte stream includes the source's content as inclusions:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Native bytes of a document are those actually stored under its control... all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The content lives once, at its permanent Istream home, and Istream is immutable. So the source's bytes are not merely "left alone" by the fork — they *cannot* be reached and changed through the descendant at all. Even when the descendant is subsequently edited into something quite different, the ancestor is insulated absolutely:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

That is the guarantee in its purest form. A deletion in the child is a Vstream operation in the child's arrangement; it never propagates into the parent. This is why I have always insisted you may

> "create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

**"Without damaging the originals."** That clause is the content invariant, stated plainly.

## 3. The source's own version history is untouched

A descendant created by forking is **its own document, with its own ongoing braid.** It does not become an entry *in the source's* history. The source's braid — the sequence of arrangements its owner has made over time — is neither extended nor edited by the existence of a child elsewhere.

The mechanism that guarantees this is the ownership asymmetry of relationships. The ancestry connection is an *in-link* to the source, and in-links do not live in, and are not controlled by, the source:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links... By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

So when someone forks your document, the record of that fork sits on *their* side, at *their* address. Your document does not have to consent, register the child, or even be aware of it — and crucially, its stored history is not amended to mention the descendant. The integrity of each document is preserved precisely because the two aspects are kept separate:

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

The *derivative* is defined in terms of the original. The original is defined in terms of nothing downstream of it.

## Why the invariant has to be this strict

I did not make forking non-destructive for tidiness. I made it non-destructive because every other guarantee in the system is a corollary of it.

- **Historical backtrack** is only meaningful if forking a new branch never disturbs the old states. The diagram of a document's technical contents shows even *deleted* material held aside, "awaiting historical backtrack functions, may remain included in other versions" [LM 4/9] — nothing is ever truly destroyed, and a fork certainly destroys nothing.
- **"Show me what this originally was"** — the promise that an old viewpoint is always recoverable — is exactly the statement that descendants leave ancestors intact:

> "(The old viewpoint is still present too — you can always say, 'Show me what this originally was.')" [LM 2/45]

- And because there is **"no 'basic' version of a document set apart from other versions"** [LM 2/19], a fork cannot be allowed to privilege or degrade its parent. Each arrangement stands on its own permanent footing.

## The invariant, stated once

> **Forking is monotonic.** Creating a descendant may only add to the docuverse — a new document, a new permanent address, a new in-link recording lineage. It may not subtract from or alter the source in any respect. The source's tumbler identity remains valid and unchanged; its content bytes, held immutably in Istream and merely *referenced* by the child, are never touched or copied; and its own braid of versions is neither extended nor edited, because the ancestry relationship is owned and stored on the descendant's side as an in-link the source does not control.

A correct implementation must therefore treat the source as strictly read-only during a fork. If a `CREATENEWVERSION` ever caused so much as one byte, one address, or one history entry of the source to change, that is not a Xanadu fork — it has broken the law that makes the whole prismatic, backtrack-capable design coherent.
