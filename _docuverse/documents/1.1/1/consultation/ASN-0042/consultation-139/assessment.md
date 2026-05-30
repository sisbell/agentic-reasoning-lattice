# Channel Assignment — ASN-0042 review-139

**Date:** 2026-05-30 09:17

## Issue 1: Design-essay content in the O6 corollary slot
Reason: Purely editorial — the corollary's mathematical claim (`pfx(ω(a)) ≼ acct(a)`) and the strict-vs-equality condition are already present in the ASN; the fix removes design-essay prose and a duplicated LM 4/17 quote. No design intent or implementation evidence is needed to trim.

## Issue 2: The "delegate is the strict longest match" argument is reproduced verbatim across sections
Reason: A proof-factoring refactor — the three-case covering-chain argument already exists in full at all four sites (O7a, NestingByDelegation, O3, O10); extracting it into one named lemma and citing it requires only the ASN's own content and the delegation conditions already stated.

## Issue 3: Self-referential scoping notes and section back-pointers in formal slots
Reason: Editorial removal of meta-prose pointing at the document's own structure; the postconditions and contract conjuncts already carry the content, so the fix is internal with no external dependency.
