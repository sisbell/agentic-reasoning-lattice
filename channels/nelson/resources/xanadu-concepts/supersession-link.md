# Supersession Link

Source: Literary Machines, 4/52-4/53

## Semantic Intent

### What It Means

A supersession link declares that one document or version has been replaced by another. Unlike the general version history that tracks how content evolves through editing, a supersession link makes an explicit claim: "This replaces that." It is the system's way of announcing obsolescence.

This addresses a real user problem that versioning alone doesn't solve. Just because a document has version history doesn't tell you whether a newer, authoritative version exists elsewhere. The supersession link is the canonical answer to the question: "Am I reading the latest?"

### User Guarantee

**You can always find out if what you're reading has been superseded.** Before reading any document, you can check whether it has been declared obsolete and follow the chain to the current version.

### Principle Served

Nelson places the supersession link in the "metalinks" category—links that apply to whole documents rather than passages. This reflects the principle that documents exist in a web of relationships, not just as isolated content. A document's relationship to its successors is as important as its content.

The supersession link also serves the principle of transparent authority. Anyone can create a version, but the supersession link lets the authoritative source declare what is current. Without this, users would have to guess which of many versions is "the" version.

### How Users Experience It

- Open a document; front-end automatically checks for supersession links
- If superseded, user sees notice: "This has been replaced by [newer version]"
- User can follow the supersession chain to reach the current version
- User can also choose to read the superseded version anyway (nothing is deleted)
- Authors can declare their own work obsolete when publishing corrections or updates

### Nelson's Words

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52-4/53)
