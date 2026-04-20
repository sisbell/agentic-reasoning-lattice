# Index Sprawl

A file accumulates an enumeration of named entities whose canonical homes are elsewhere. The list adds nothing the enclosing file's argument requires; it exists because some cycle needed to assert a structural fact about other files, and the assertion was written as prose here.

Index Sprawl is distinct from a legitimate list. A proof's case-split enumerating `(i), (ii), (iii)` is local to the proof; a Depends list enumerating dependencies is structural metadata. Index Sprawl is an enumeration of items with their own separate existences being re-stated here as a directory.

## Forces

**Exhaustiveness obligations.** A sentence claiming completeness about a set of external items — "stated as separate axioms: NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder, NAT-zero, NAT-sub, NAT-cancel, NAT-addassoc" — commits the file to defending that list. Each cycle finds an addition or an asymmetry; reviser extends or re-balances. The list grows and new files that should be simple acquire enumerative preambles.

**Genesis Attractor, migrated.** When a Genesis Attractor has been split, the attractor role persists and the enumerated form re-emerges in the same file (as a catalog of what was moved out). The physical content is gone; the directory-to-other-files takes its place.

**Enumeration propagation across siblings.** An exhaustiveness claim in one file forces related files to re-assert the same enumeration to maintain consistency. A file about one specific axiom ends up listing all its siblings, because a reviewer asked "how does this axiom relate to the enumeration in T0?" and the reviser inlined T0's list.

**Reviewer-offered-escape-not-taken.** Reviews commonly offer two resolutions: (a) extend the enumeration to include the missing item, or (b) soften the framing so the list isn't read as exhaustive. Option (a) produces Index Sprawl; option (b) dissolves it. Revisers default to (a). This is the textual-fix default that drives [Surface Expansion](surface-expansion.md) generally.

## Signal

A file contains a list of named entities (claims, axioms, files) that:

- Have their own canonical homes elsewhere
- Are not consumed by the enclosing file's argument
- Appear together as a group whose groupness is asserted here rather than established structurally

Concrete markers:

- Sentences of the form "X is one of the Ys: Y₁, Y₂, ..., Yₙ"
- Listings of other files' labels inside prose that has no other use for those labels
- A sibling file's prose re-stating an enumeration canonical to another file

Can appear in prose sections or inside Depends entries that have become essays.

## Example: NAT-addassoc listing its siblings

`NAT-addassoc.md` states a single axiom: `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))`. A two-line file would suffice.

During cycle 3 of the TA-assoc cone review, a reviewer found that T0's enumeration claimed exhaustiveness while NAT-addassoc was stated outside it. The review offered two fixes — (a) integrate NAT-addassoc into T0's enumeration, or (b) soften T0's exhaustiveness claim. The reviser chose (a), expanding NAT-addassoc.md to 677 words, including this sentence:

> "T0 lists `NAT-addassoc (NatAdditionAssociative)` explicitly alongside the eight other NAT-* axioms — NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder, NAT-zero, NAT-sub, NAT-cancel — and declares the combined list exhaustive..."

NAT-addassoc is not a Genesis Attractor. Nothing was attracted *to* it. The enumeration migrated *into* it because the exhaustiveness obligation in a different file propagated sibling-to-sibling through a review cycle.

The same force produces Index Sprawl inside Depends entries — ZPD.md's Depends has a paragraph that re-enumerates T0's NAT-* list inside a single dependency entry.

## Resolution

**Drop the exhaustiveness claim at its source.** If no sentence asserts the list is complete, no file needs to track the list's completeness. Most instances of Index Sprawl dissolve once the upstream exhaustiveness assertion is removed.

**Delete the list unless the enclosing file's argument needs it.** A file about one axiom does not need its siblings named. A file about a concept does not need to enumerate other files that state related facts. If the items have their own homes, point readers to the dependency graph or the index of files, not to a prose list.

**Prefer structural fixes over textual ones.** When a reviewer finds an asymmetry between two enumerations, the correct response is usually to delete one or both — not to extend them into alignment. This is the [Surface Expansion](surface-expansion.md) discipline applied to enumerations.

**Use structured metadata for cross-file relationships.** Dependency graphs, note manifests, and claim metadata carry relationship information machines can query. Prose enumerations duplicate this information in a form that attracts review-cycle scrutiny and grows under it.

## Related

- [The Coupling Principle](../principles/coupling.md) — index sprawl is a coupling violation: surface grows without advancing reasoning in either direction. The coupling principle's feedback loop shows how this detection drives V-Cycle prompt calibration.
- [Prose Sprawl](prose-sprawl.md) — enumerations are one specific surface form of Prose Sprawl; Index Sprawl is the subset that specifically lists external entities.
- [Contract Sprawl](contract-sprawl.md) — a Genesis Attractor whose contract has been split often re-grows as an index of what was split out.
- [Surface Expansion](surface-expansion.md) — the shared mechanism across Contract/Prose/Index Sprawl. Index Sprawl is the enumeration-surface manifestation; monitoring and the general discipline live at the Surface Expansion level.
- [Accretion](../patterns/accretion.md) — accreted claims need homes, not a central directory. Accretion without a central list is how the system is supposed to grow.