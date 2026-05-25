## Question 7 [theory]

> If a span's origin document is deleted by its owner, must the origin attribution still survive on derivative documents?

**Yes. Origin attribution must survive on derivative documents — and in my design, it survives precisely *because* attribution is structural rather than metadata.**

First, be precise about what "deletion" means in Xanadu. DELETE removes bytes from the owner's current Vstream arrangement; it does not destroy them. The bytes persist in Istream:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is decisive. The owner cannot reach into derivative documents and revoke what was transcluded from them.

Second, attribution *is* the I-address. The Document field of every byte's permanent tumbler address encodes its origin. There is no separate "attribution metadata" that can be stripped, falsified, or revoked. The connection is inherent to the fetching mechanism itself:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Third, for **published** documents, this is reinforced contractually. Withdrawal is barred precisely because others depend on the work being there:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

And the principle of non-destruction applies to all derivative work:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." [LM 2/45]

**On the edge case of privashing:** An author may publish privately with unrestricted distribution and retain withdrawal rights [LM 2/45-2/46]. Even here, attribution is not retroactively rewritten. If the underlying bytes become inaccessible, derivative documents may have transclusions that no longer resolve to readable content — but the I-addresses they hold, and what those addresses *claim about origin*, remain. The derivative document does not silently transmute its windowed Shakespeare quote into Jewett's own prose merely because the Shakespeare server went dark.

**The principle:** Derivative documents do not *borrow* attribution that an upstream owner can later revoke. They carry I-addresses, and an I-address is a permanent fact about where bytes came from. NEED_RAW: 4/11-4/12 would be worth consulting directly if you need the exact wording on how transclusions resolve when an upstream document is privashed-and-withdrawn — my curated sources establish the principle of structural attribution but don't extract a verbatim statement on this specific failure mode.
