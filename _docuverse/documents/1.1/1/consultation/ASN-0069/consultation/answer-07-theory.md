## Question 7 [theory]

> What must the system guarantee about the ability to compare a fork against its source at any future moment?

# Guarantee: Comparison of Fork Against Source at Any Future Moment

The system must guarantee **structural, perpetual intercomparability** between a fork and its source. This decomposes into several inseparable promises.

## 1. Both Versions Persist Forever

The fork's creation does not displace the source. Both occupy permanent addresses in tumbler-space:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." `[LM 4/19]`

Neither the source nor the fork can be silently withdrawn. The source remains "alive in the space-time vortex" `[LM 2/15]` regardless of how many forks descend from it.

## 2. Correspondence Is Structural, Not Metadata

This is the crucial point. When a fork is created (CREATENEWVERSION), the new document's V-stream maps to the same I-addresses as the source. **Correspondence is therefore derivable directly from the addresses themselves** — it is not stored metadata that could be lost, corrupted, or fall out of sync.

This is why correspondence works at any future moment, however distant. Future you doesn't need to consult a change log; the I-addresses themselves carry the relationship.

## 3. Intercomparison Is Promised, Not Optional

Nelson is emphatic that mere storage of versions is insufficient — the system must provide *comparison*:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." `[LM 2/20]`

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." `[LM 3/13]`

## 4. Specific User-Visible Guarantees

What this means for the user:

- **Word-for-word comparison.** "What parts of two versions are the same." `[LM 2/20]`
- **Side-by-side navigation.** "The user may scroll through any two versions to see corresponding parts; and much more." `[LM 2/21]`
- **Direct jumping between counterparts.** Click a passage in the source, land on the corresponding passage in the fork.
- **Highlighted differences.** Changes are visible against the backdrop of what stayed the same.

## 5. The Protocol-Level Commitment

FEBE exposes this as a primitive operation:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." `[LM 4/70]` (SHOWRELATIONOF2VERSIONS)

The operation does not approximate or estimate — it returns the *exact* set of corresponding span-pairs, computed from the shared Istream origin.

## 6. Links Survive the Fork

A link made against the source must remain followable from the fork, and vice versa:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." `[LM 2/26]`

This means comparison is not just textual — the *connective tissue* (citations, comments, marginalia) carries across the fork relationship.

## 7. The Source Is Never Damaged by Forking

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." `[LM 2/45]`

The fork does not eat the source. Both are independently accessible, and the comparison is between two genuinely existing documents — not between a current state and a reconstructed memory of a former one.

---

## Why This Works At *Any* Future Moment

The four pillars that make this guarantee perpetual rather than merely current:

1. **Permanent addresses** (`[LM 4/19]`) — the fork and source remain locatable forever.
2. **Append-only storage** (`[LM 2/14]`) — neither can be overwritten.
3. **Structural correspondence via shared Istream** — the relationship is in the addresses, not in metadata that decays.
4. **No "lengthy due process" exception erodes this** — even withdrawal requires preserving links others depend on (`[LM 2/43]`).

A reader in the year 2500 must be able to ask the system: "Show me how this fork differs from its source," and receive the same word-for-word, span-paired answer that a reader in the year of forking would have received. The mechanism is identical; only the elapsed time differs.

That is the guarantee.
