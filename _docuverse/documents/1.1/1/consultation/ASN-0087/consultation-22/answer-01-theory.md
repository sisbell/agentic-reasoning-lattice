## Question 1 [theory]

> Does the design fix every link's V-position at the canonical depth-2 link subspace (`version.0.2.serial`) as a system-wide invariant, or is depth 2 only the intended placement for the standard link-creation path, leaving other depths admissible for links seeded by other means?

Depth 2 is the **canonical placement for the standard link-creation path, not a rigid system-wide invariant that forbids other depths.** Nelson's own text leaves deeper subdivision explicitly open.

## What Nelson fixes

The standard link address places a link at the depth-2 link subspace, with the serial being permanent order of arrival:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

So `version.0.2.serial` is the *intended* shape produced when a link is created and assigned its arrival number. The `2` distinguishes the link subspace from the byte subspace (`1`), and the trailing digit is the serial position.

## What Nelson explicitly leaves open

Crucially, Nelson does **not** declare depth 2 a closed invariant. He anticipates further digits beyond `2.serial`:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

This sentence is decisive for your question. "Further digits (after '2' and the position)" means addresses *deeper* than `version.0.2.serial` are contemplated by design — i.e., a link's address may legitimately extend below depth 2. Nelson treats depth 2 as the floor of the standard path, with deeper structure as a "distinct possibility," not a violation.

## Conclusion

- The standard creation path canonically yields `version.0.2.serial` (depth 2), with permanent order-of-arrival serials.
- This is the *intended placement* for that path, not a guarantee that every link's V-position is pinned at exactly depth 2 forever.
- Nelson reserves room for links subdivided "by further digits," so deeper addresses are admissible for other purposes.

The right reading is therefore the **second** one in your question: depth 2 is the intended placement for the standard link path, while other (deeper) depths remain admissible by Nelson's own anticipation.

One caveat on framing: the word "invariant" is implementation-level vocabulary; Nelson writes at the design level. He never asserts a system-wide rule that all links sit at depth 2 — he describes the canonical address and then opens the door to deeper subdivision. If you need to confirm no stronger invariant is stated in the surrounding link-address discussion, NEED_RAW: 4/30–4/32.
