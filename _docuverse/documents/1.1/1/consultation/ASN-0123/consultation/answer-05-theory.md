## Question 5 [theory]

> Who owns a newly forked version when the person forking is not the owner of the source, and what editability follows from that ownership rather than from the source's permissions?

## Who owns the forked version

**The person who forks it.** When a non-owner creates a version of a document they do not own, the new version is *theirs*, not the source owner's. Nelson is explicit that a non-owner's version is a separate, self-owned document that pulls the source in by reference:

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion."
> — *windowing* (2/32–2/40)

The operative phrase is "his or her **own** alternative version." This is not a transfer or a sub-grant of the source owner's rights — it is a fresh document the forker owns outright.

This also follows structurally from how ownership and forking work. Ownership in Xanadu is the account (User) field of the tumbler address, and you can only baptize new numbers under addresses you already own:

> "The owner of a given item controls the allocation of the numbers under it."
> — *forking* (4/20)

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."
> — *tumblers* (4/17)

A non-owner therefore cannot place the new version inside the source owner's number space; it lands under the forker's own account, which is precisely what makes the forker its owner. Note too that even where version-numbering is used, it "strictly implies no specific relationship of derivation" (*i-space-addresses*, 4/29) — derivation is recorded by the inclusion links, not by ownership.

## What editability follows from that ownership

Editability follows from **owning the new version**, and from nothing about the source's permissions. The general rule is:

> "Only the owner has a right to withdraw a document or change it."
> — *documents* (2/29)

The forker had *no* right to change the source (they don't own it). The fork hands them a document they *do* own — and ownership confers full modification rights over that document. This is the "writing always succeeds / denial is a fork" principle documented in *session-model*: a non-owner is never returned a permission error; the inability to edit the original is resolved by redirecting them into a version they own and can edit freely. Nelson's words for the same idea:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals. This is done by inclusion links."
> — *publishing / copyright* (2/45)

So the source's permissions are simply not in the causal chain. The forker's edit rights derive entirely from owning the fork, not from any access inherited through the source.

## The boundary of that editability

Ownership of the fork gives full control over the fork's **arrangement** (its Vstream) — inserting new native content, rearranging, and dropping windowed material from view. It does **not** give the power to alter the source's bytes, which remain the source owner's, immutable in Istream and recoverable in the original. Editing a quoted passage means breaking the window around it and splicing in your own content, as in Nelson's Hamlet example:

> "Very well, if Hamlet is already on the system, then E.G. Jewett could publish his own Hamlet very easily: a quote-link to the first part of the original, just up to 'in the soliloquy'; then the word 'luge'; then a quote-link to the rest of the play."
> — *transclusion* (2/32–2/49)

Jewett owns *his* Hamlet and edits it freely; Shakespeare's text is untouched, and a reader can always retrieve it:

> "(The old viewpoint is still present too—you can always say, 'Show me what this originally was.')"
> — *versions* (2/45)

Because the fork is a collage of windowed (source-owned) and native (forker-owned) spans, the consequence at read time is a split:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically."
> — *versions* (2/45)

## Summary

- The forker owns the new version — it is "his or her own alternative version," placed under the forker's account, created by **versioning by inclusion**. The source owner retains an independent, untouched original.
- Editability flows from that ownership: "Only the owner has a right to... change it" (2/29). The forker can fully edit the fork *because they own it*, not because of any permission carried over from the source — indeed they had none on the source.
- That editability is bounded to the fork's own arrangement: native content is fully editable; windowed source content can be included, excluded, or spliced around, but the source's bytes themselves are immutable, with royalties splitting between source owner and forker by who wrote what.
