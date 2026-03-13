# Sub-Questions — Tumbler Algebra

**Inquiry:** What algebraic properties must the Xanadu addressing system satisfy? What ordering, arithmetic, and structural guarantees do tumblers provide?

1. [nelson] Must every address in the system be comparable to every other — can the system ever encounter two addresses where neither is "before" the other?
2. [nelson] Between any two adjacent addresses, must there always be room to assign a new address, or can the address space between two points ever be exhausted?
3. [nelson] What distinct levels does an address contain, and what does each level uniquely identify — a user, a document, a position within content?
4. [nelson] Must newly assigned addresses always be greater than all previously assigned addresses, or may the system fill in gaps retroactively?
5. [nelson] Must a contiguous range of addresses be expressible as a compact pair (start, end), and must every such range denote an unbroken sequence of content units?
6. [nelson] What is the finest granularity an address can identify — a single character, a byte, or some other atomic unit of content?
7. [nelson] When two addresses share a common prefix, what relationship must hold between the things they identify — must they belong to the same containing scope?
8. [nelson] Must the difference between two addresses within the same level be arithmetically meaningful — for instance, must it tell you how many content units lie between them?
9. [nelson] If a user creates content across multiple sessions, must the addresses assigned in each session form a contiguous block, or may they be interleaved with other users' addresses?
10. [gregory] Is `tumblersub(a, b)` intended to be a true group subtraction (always yielding a valid distance), or are there tumbler pairs where the negative result is a representation artifact that should never appear in practice?
11. [gregory] The `strongsub` exponent guard (line 544 of `tumble.c`) returns `a` unchanged when `b.exp < a.exp` — was this an intentional algebraic design choice to make subtraction a no-op across exponent classes, or a defensive guard against a specific bug?
12. [gregory] Is the tumbler number line dense — can you always construct a tumbler strictly between any two distinct tumblers — or does the fixed 16-digit mantissa impose a minimum gap where no intermediate value can be represented?
13. [gregory] Are `tumbleradd` and `tumblersub` inverses of each other for all representable tumblers, i.e., does `tumbleradd(tumblersub(a, b), b)` always recover `a` exactly, or are there precision-loss cases from the fixed mantissa?
14. [gregory] What was the design rationale for sign-magnitude representation instead of two's complement — was it to make the total order (negative < zero < positive) straightforward in `tumblercmp`, or was there a deeper reason related to hierarchical addressing?
15. [gregory] Does `tumblerincrement` always produce the immediate successor in the total order, or does it increment only the least-significant nonzero digit — and if the latter, what is the formal successor relation between tumblers?
16. [gregory] The `.0.` digit acting as a hierarchical separator is described as convention, not enforcement — were there ever plans to make the algebra aware of hierarchy (e.g., parent-child ordering guarantees), or is hierarchy purely an interpretation layer above flat digit sequences?
17. [gregory] When two tumblers have different exponents, `tumblercmp` compares them — is the ordering purely lexicographic on the (exponent, mantissa) pair, or does the exponent shift the mantissa digits before comparison so that `2.1` (exp=0) and `0.21` (exp=-1) compare as equal?
18. [gregory] What happens when `tumbleradd` or `tumblerincrement` would produce a result requiring more than 16 mantissa digits — is there silent truncation, wraparound, or an error condition, and has this limit ever been hit in practice?
19. [gregory] `tumblerjustify` normalizes a tumbler before equality comparison — what invariant does it restore (leading-zero removal, trailing-zero trimming, exponent normalization), and can two tumblers that are `tumblercmp`-ordered but not `tumblerjustify`-normalized produce an inconsistent ordering?
