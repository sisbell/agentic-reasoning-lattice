## Question 8 [theory]

> How must the result behave under editing — if material is removed from one document or new copies appear in another, which parts of the answer may change and which must remain stable?

## The governing law: identity is stable, arrangement is mutable

Every result of this kind decomposes into two layers, and editing touches only one of them. This is the whole point of separating the **Istream** (where content permanently lives, by absolute address) from the **Vstream** (a document's current arrangement, a mutable *view* onto Istream content).

The rule follows directly:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

So **any part of the answer that names content by its identity (Istream origin) must remain stable; any part that names content by its current position or live membership may change.** Editing never *destroys* — it only changes what is currently presented. Every prior state stays queryable:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

---

## What MUST remain stable

1. **The identity of the material in question** — its Istream address. The subject of the query is anchored and never moves.

2. **Its origin / home document.** Attribution is structural, not strippable metadata: "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

3. **The historical answer.** "Which documents contained this as of version/time T" is immutable, because nothing is ever overwritten — modifications happen "without damaging the originals." [LM 2/45]

4. **Links anchored to the material.** Because a link is "not between points, but between spans of data... if any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42] Reordering doesn't shake them loose either: "since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

5. **Presence in other documents.** Removing material from one place does not remove it from elsewhere (see Scenario A).

## What MAY change

1. **The Vstream positions** of surviving occurrences — V-addresses shift as surrounding content is inserted or deleted.

2. **The live membership of the result set** — *which documents currently present* the material. This set both shrinks (deletions) and grows (new inclusions). The *current* answer and the *historical* answer may therefore diverge — but you can always ask the historical question and get a stable answer.

---

## Scenario A — material removed from one document

`DELETE` is a Vstream operation, not Istream destruction. The bytes leave the current arrangement but persist:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Crucially, deletion is **local to the editor's own version**:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**Effect on the result:** the editing document drops out of the *current* answer; everything else holds. The material's identity, its origin, the previous versions that still contain it, every other document that included it, and every link attached to it are all untouched. Nothing that was true historically becomes false.

## Scenario B — new copies appear in another document

A "copy" here is `COPY`/transclusion — inclusion by reference. The new occurrence is the **same Istream content seen through a new window**, not a fresh independent piece of content:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

**Effect on the result:** the new document *joins* the live answer — precisely because identity is shared. This is exactly why `FINDDOCSCONTAINING` "returns a list of all documents containing any of the material specified by the span addresses, **regardless of where the native copies are located**." [LM 4/63] The query keys on Istream origin, so a transclusion is found wherever it appears. What does *not* change: the material's identity and origin. A new window adds a viewer, not a new owner of the content.

---

## The subtlety that trips people up

"New copies appear" means **transclusions that share the Istream address** — and those join the answer. If instead someone *independently retypes* the same words, that is different content with a different Istream identity (in the model, content identity is by creation, not by value [LM 4/10–4/11]). It correctly does **not** appear in the result, and that exclusion is itself a stable, principled outcome — the answer tracks the *same* material, not look-alike strings.

The same shared-Istream basis is why links and correspondence ride through edits: "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26] And why `SHOWRELATIONOF2VERSIONS` can always recompute correspondence — it "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70] from shared origin, for any version where the content still exists.

---

## Summary

| Aspect of the answer | Under DELETE | Under COPY (transclusion) |
|---|---|---|
| Material's Istream identity | **stable** | **stable** |
| Origin / home document (attribution) | **stable** | **stable** |
| Links to the material | **stable** (survive) | **stable** |
| Historical / version-scoped answer | **stable** | **stable** |
| Vstream positions of survivors | may shift | may shift |
| Live set: which docs *now* contain it | editing doc **drops out** | new doc **joins** |

In one sentence: **the editing operations move the boundary of what is *currently shown*, never the identity, origin, or history of what is *shown*** — so an answer phrased in terms of identity and provenance is invariant, while an answer phrased in terms of the live arrangement breathes in and out, with every prior state preserved and re-askable.
