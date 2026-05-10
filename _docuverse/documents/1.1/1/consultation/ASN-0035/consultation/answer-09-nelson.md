## Question 9 [nelson]

> Must the identity of a node remain stable across all subsequent versions, or does versioning produce a new node with a new identity?

## Versioning Produces a New Node; the Original's Identity Is Absolutely Stable

The answer is unambiguous across multiple parts of Literary Machines: **versioning creates a new entity with its own distinct identity. The original node retains its address and identity unchanged.**

### The Operation Itself

CREATENEWVERSION is defined as:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

Three things to note: it creates a **new document**, it returns a **new id**, and that id **indicates ancestry**. The original document is not modified or replaced.

### Address Permanence

The tumbler guarantee is absolute:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The original's tumbler address does not change, expire, or redirect.

### How Version Identity Works in the Address Structure

Versions are encoded as subdivisions of the Document field in the tumbler:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

So if the original document is `1.0.3.0.7`, a version might be `1.0.3.0.7.1` — a sub-address under the original. But Nelson adds a critical caveat:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The tumbler **encodes** lineage structurally but does **not enforce** that the relationship is one of semantic derivation. The address tells you where the version came from in the forking tree, not what its content relationship is to its parent.

### Both Versions Are Equally Valid

Nelson explicitly rejects the notion of a "primary" version:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Both the original and the new version are first-class documents with their own addresses, their own ownership, and their own V-space arrangements.

### What They Share: I-Space Content

The two versions share I-space content. The new version starts with the same V-to-I mappings as the original. This shared I-space origin is what enables **correspondence** — the system can compute which parts match:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

And links made to one version can follow through to corresponding content in another:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

### Why This Matters

The permanence of published documents depends on this design. Once others have linked to your document:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

If versioning mutated the original's identity, every link made to it would be disrupted. Instead, the original stands, the new version stands beside it, and the correspondence mechanism connects them.

### Summary

| Aspect | Original Document | New Version |
|--------|-------------------|-------------|
| **Identity (tumbler)** | Unchanged | New address (sub-address of original) |
| **I-space content** | Unchanged | Initially shares I-space; may diverge with edits |
| **V-space arrangement** | Unchanged | Initially identical; independent thereafter |
| **Status** | First-class document | First-class document (no hierarchy) |
| **Correspondence** | Computable via shared I-addresses | Computable via shared I-addresses |
| **Links to it** | Still valid | New links go to new address |

Versioning is forking, not mutation. The original is permanent; the version is new.
