## Question 14 [evidence]

> Does `docopyinternal` copy the source's text-subspace POOM entries (V-displacement, V-width, I-displacement, I-width bottom crums) verbatim into the version's new POOM, or does it re-derive the V→I mapping from a retrieved vspanset, potentially consolidating adjacent I-spans differently than the source's tree?

## KB Synthesis

`docopyinternal` re-derives the V→I mapping from a retrieved vspanset — it does not copy source POOM bottom crums verbatim.

**The call chain** is documented in [ST-VERSION] (Finding 0077):

```
docreatenewversion
  → doretrievedocvspanfoo        (produces one text-subspace V-span from root cdsp/cwid)
  → docopyinternal
      → specset2ispanset         (queries source POOM: V-span → I-spans)
      → insertpm                 (builds version's POOM from I-spans)
      → insertspanf              (records DOCISPAN entries)
```

`doretrievedocvspanfoo` calls `retrievedocumentpartofvspanpm()` which reads the root node's `cdsp.dsas[V]` and `cwid.dsas[V]` directly — a single bounding V-span for the text subspace [ST-VERSION-CREATE, Finding 0043]. This single V-span is then passed to `docopyinternal`.

`specset2ispanset` walks the **source's POOM** to convert that V-span back to I-spans. For a source with n fragmented crums (from editing history), this produces n I-spans, one per contiguous I-address region [SS-POOM-MULTIMAP, Finding 0039]. Each I-span is then fed into the version's `insertpm`.

**Consolidation consequence**: `insertpm` applies the `isanextensionnd` coalescing test before creating new crums [ST-INSERT, Finding 0062; PRE-COPY, Finding 0046]. `isanextensionnd` checks two conditions: (1) same `homedoc` as an existing crum, and (2) new content starts exactly at the existing crum's reach. If the source's I-spans happen to be I-address-contiguous and from the same origin document, consecutive `insertpm` calls will coalesce them into a single crum in the version's POOM. If not (e.g., content from multiple transclusion sources, or editing has fragmented the I-space), each non-contiguous I-span becomes a separate crum.

**Net result**: The version's POOM encodes the same V→I mapping as the source's text subspace, but the crum tree topology may differ:
- More consolidated: if adjacent source crums cover contiguous I-space from the same homedoc (coalescing fires)
- Identical fragmentation: if I-spans are non-contiguous or from different homedocs (no coalescing possible)
- The source's crum boundaries from prior cut/split operations are **not preserved** — they are an artifact of the source's edit history, invisible after re-derivation

Finding 0077 makes this explicit with a test: `INSERT "ABC" → VERSION → INSERT "XYZ"` yields one contiguous shared span pair across all 6 characters, confirming the version did not introduce any I-address gaps or structural artifacts from copying — it inherited the source's I-space as a clean contiguous mapping.
