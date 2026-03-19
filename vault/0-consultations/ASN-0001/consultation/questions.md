# Sub-Questions — Tumbler Algebra

**Inquiry:** What algebraic properties must the Xanadu addressing system satisfy? What ordering, arithmetic, and structural guarantees do tumblers provide?

1. [nelson] Must every address in the system be permanently unique — can an address, once assigned, ever be reused for different content?
2. [nelson] Must all addresses within a single document admit a total ordering, so that "before" and "after" are always well-defined?
3. [nelson] When new content is inserted into a document, must every previously assigned address remain unchanged and continue to designate the same material?
4. [nelson] Must an address by itself reveal which account, document, and version it belongs to — is containment readable from the address alone?
5. [nelson] Must the system be able to identify a contiguous range of content purely from the addresses at its endpoints, without consulting any external index?
6. [nelson] Must addresses from different documents be comparable, or does ordering only need to hold within a single document?
7. [nelson] Must the addressing scheme guarantee that content positions, link positions, and structural positions can never collide — that their regions are permanently disjoint?
8. [nelson] Must the system support unbounded growth — can new accounts, new documents, and new content be allocated without ever exhausting the address space?
9. [nelson] Must new addresses always be allocated beyond all existing addresses, or may the system fill gaps left by earlier operations?
10. [nelson] If two users independently add content to different documents, must the design guarantee that neither allocation can interfere with or constrain the other?
11. [gregory] When `tumbleradd` produces a carry that propagates past the 16th mantissa digit (NPLACES), does the result silently truncate, wrap around, or is this condition impossible given the allocation pattern?
12. [gregory] Does `tumblerincrement` always advance the least-significant non-zero digit, or does the digit it increments depend on `tumblerlength` or the exponent field — and can increment ever change a tumbler's exponent?
13. [gregory] Was the `strongsub` exponent guard (returning `a` unchanged when `b.exp < a.exp`) designed specifically to protect subspace isolation during DELETE, or was it written for a different purpose that happens to produce that effect?
14. [gregory] Is there any tumbler multiplication, division, or scaling operation in the system, or is the full arithmetic limited to add, subtract, increment, and compare?
15. [gregory] Can two distinct tumblers (different mantissa digits) compare as equal under `tumblercmp` — for example, if trailing zeros or exponent differences create aliasing — or does `tumblerjustify` guarantee a canonical form that prevents this?
16. [gregory] Is the zero tumbler (sign=0, exp=0, all-zero mantissa) ever used as a valid address or sentinel value, and what does `tumblercmp` return when comparing zero against a positive tumbler with exponent -1?
17. [gregory] Between any two positive tumblers `a < b`, can you always construct a tumbler `c` such that `a < c < b` (density property), or are there adjacent pairs with no tumbler between them given the fixed 16-digit mantissa?
18. [gregory] Does the hierarchical parent-child relationship (e.g., `1.1.0.2` is parent of `1.1.0.2.0.5`) follow from the tumbler total order alone, or does the code use a separate prefix-matching predicate distinct from `tumblercmp`?
19. [gregory] When `findaddressofsecondcutforinsert` computes the subspace boundary tumbler, what specific tumbler arithmetic does it use — does it zero out digits below a certain level and increment, or does it construct the boundary from the document address prefix?
20. [gregory] In the 2D enfilade displacement arithmetic (where root displacement tracks minimum child addresses via `setwispnd`), are V-displacements and I-displacements added and subtracted independently, or is there ever a cross-dimensional arithmetic operation that combines them?
