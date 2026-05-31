# Review of ASN-0043

## REVISE

### Issue 1: L9's closing paragraph re-states the "open-ended type system" point already made in "The Endset Structure"
**ASN-0043, L9 (closing paragraph) vs. "The Endset Structure" (point 1, Extensibility)**: L9 closes with "new link types can be defined by choosing a fresh tumbler address and using it as a type endset. … No registry needs to be updated. No schema needs to change. … This is what makes the type system 'open-ended' — any user can extend it without coordination or system modification." The Endset Structure section already established: "Extensibility. Any user can define new types by choosing new addresses, without schema changes. Nelson: 'The set of link types is open-ended…'"
**Problem**: The two passages assert the same content (choose a fresh/new address, no schema change, "open-ended," any user, no coordination) in different words. L9's *own* content is the ghost-permission existence result and the "no content needed at the address" consequence; the "open-ended/any-user/no-schema" framing is a duplicate of the earlier extensibility bullet, not advancing L9's reasoning. This is the "two paragraphs in the same document say the same thing in different words" pattern.
**Required**: Trim L9's closing to its load-bearing consequence (a type address is a pure name needing no stored content at the address — the L8+L9 conjunction), and drop the restated open-endedness framing already carried by the Extensibility point.

### Issue 2: L13's bridge sentence restates the quote it cites
**ASN-0043, "Reflexive Addressing" (after the faceted-link/CONS-cell quote)**: "Nelson framed the faceted link this way — built from a chain of links glued by link-to-link references (the quote above)."
**Problem**: This sentence paraphrases the immediately preceding block quote ("Complex relational structures, such as the faceted link, may be constructed with links to links…") and then points back to it with "(the quote above)." The only forward-advancing content is the following sentence ("This model admits both realizations… chaining (L13) or a single link of arity N (L3)"). The intervening restatement is noise the reader must skip past.
**Required**: Delete the restating sentence; let the quote stand and connect it directly to the "both realizations" contrast (chain via L13 vs. arity-N via L3).

VERDICT: REVISE
