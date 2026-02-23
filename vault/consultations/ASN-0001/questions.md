# Sub-Questions — Tumbler Algebra

**Inquiry:** What algebraic properties must the Xanadu addressing system satisfy? What ordering, arithmetic, and structural guarantees do tumblers provide?

1. [nelson] Must every address the system assigns be permanently ordered relative to every other address, and what does that ordering represent — creation sequence, containment, or both?
2. [nelson] When the system computes "the next available address" for new content, what guarantees prevent two different pieces of content from ever receiving the same address?
3. [nelson] Must the address of a piece of content reveal which document, which version, and which user account it belongs to — and is this hierarchical containment an essential design property or merely convenient?
4. [nelson] If content is inserted into the middle of a document, must the addresses of all surrounding content remain unchanged, or may the system renumber positions?
5. [nelson] Must it always be decidable from two addresses alone — without consulting any index — whether they refer to the same document, the same version, or entirely separate accounts?
6. [gregory] When `tumbleradd(a, b)` is used to shift V-positions during INSERT, is the addition associative — does `tumbleradd(tumbleradd(a, b), c)` always equal `tumbleradd(a, tumbleradd(b, c))` — and does it preserve the total order, so that `a < b` implies `tumbleradd(a, c) < tumbleradd(b, c)` for all positive `c`?
7. [gregory] What happens when tumbler arithmetic produces a result that exceeds the 16-digit mantissa (`NPLACES`): does `tumbleradd` or `tumblerincrement` silently truncate, wrap around, or is the 16-digit limit simply assumed never to be reached in practice?
8. [gregory] Does `tumblerincrement` always advance the least significant non-zero digit by one, or does its behavior depend on the tumbler's exponent — specifically, does incrementing `1.1.0.2` (a document-level address) produce `1.1.0.3` (next document) rather than `1.1.0.2.0.0.0.0.0.0.0.0.0.0.0.1` (next sub-position)?
9. [gregory] Does `tumbleradd` have an exponent guard analogous to `strongsub`'s — where adding a width with a lower exponent than the target is a no-op — or is the exponent guard unique to subtraction, making INSERT's subspace isolation depend on the two-blade mechanism rather than on arithmetic properties?
10. [gregory] Can two distinct tumbler representations (different exponent/mantissa combinations) compare as equal under `tumblercmp` but unequal under `tumblereq`, or does `tumblerjustify` guarantee a canonical form so that order-equivalence and equality always agree?
