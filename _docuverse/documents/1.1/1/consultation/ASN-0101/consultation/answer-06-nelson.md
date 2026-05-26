## Question 6 [nelson]

> Must the system preserve the exact boundaries of what was removed — that is, must it remember precisely which content occupied which positions before the removal?

## Yes — the system must preserve exact deletion boundaries

This follows from three interlocking requirements Nelson specifies.

### 1. Historical backtrack demands full reconstruction

Nelson's storage model is append-only. Changes are recorded, not applied destructively:

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

The guarantee is that "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. To reconstruct the pre-deletion state, the system must know exactly which Istream content occupied which Vstream positions before the removal.

### 2. Deleted bytes are explicitly tracked, not forgotten

The diagram on 4/9 shows "DELETED BYTES" as a distinct system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Awaiting historical backtrack functions" means these bytes and their former positions are known to the system — they are pending reconstruction, not discarded. The system retains the V→I mapping from the version before deletion.

### 3. Version comparison requires positional correspondence

SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. For this to work between pre-deletion and post-deletion versions, the system must know the exact Vstream mapping of both. Without the deletion boundaries, it cannot compute which spans in the old version correspond to which spans in the new one.

Nelson motivates this:

> "a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

### The mechanism

The DELETEVSPAN operation takes a span as input: "This removes the given span from the given document" [LM 4/66]. The span itself defines exact boundaries (a Vstream start and width). The operation modifies the Vstream mapping — removing those positions — but the previous mapping persists as a prior version. Since each version is a complete V→I mapping, the exact boundaries of what was removed are preserved structurally in the version that preceded the deletion.

The Istream content, of course, is untouched:

> "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Summary

The system must preserve exact deletion boundaries because:
- **Each version is a complete V→I mapping**, and the pre-deletion version persists
- **Historical backtrack** requires reconstructing any prior state, which requires knowing what was where
- **Version comparison** requires computing positional correspondence, which requires both mappings
- **Deleted bytes** are explicitly in a known state "awaiting historical backtrack functions," not forgotten

The boundaries are not stored as separate "deletion records" — they are implicit in the difference between the pre-deletion and post-deletion Vstream mappings, both of which the system retains.
