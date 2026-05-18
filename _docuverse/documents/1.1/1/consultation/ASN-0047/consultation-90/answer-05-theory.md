## Question 5 [theory]

> Did the Xanadu design explicitly consider links with both F and G empty (referencing only a type via Θ), and if so, was such a "type-only marker" link intended, excluded, or left unspecified?

# Type-Only Marker Links (F=∅, G=∅, Θ populated)

## Short answer

**Left unspecified.** Nelson explicitly considered the case of *one* endset being empty (one-sided links), but the curated sources show no explicit discussion of links with *both* from-set and to-set empty, leaving only the type as a "marker."

## What Nelson DID consider

**One-sided links** (one endset populated, one empty):

> "An important variation where a link has only one side - something pointing to material, but not from other material. The paragraph designator is an example. This avoids terminological confusion by using only the from-set to designate the matter pointed at." (curated `links.md`, citing 4/48)

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." (4/48)

The **paragraph link** is given as the worked example — a link with no semantic "from," used purely as a navigational marker.

**Ghost-element type endsets** (the type points to an address with nothing stored):

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

So Nelson is comfortable with the *type* endset pointing into empty space — that is different from the *type* itself being absent.

## What the design implies against type-only markers

Two structural signals suggest the design assumed at least one of F or G is populated:

1. **The MAKELINK signature** takes three explicit endsets:
   > "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>." (4/68)

2. **The link-search satisfaction rule**:
   > "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)
   
   A link with both F and G empty cannot satisfy this rule against any non-empty from/to constraint — making such a link effectively invisible to the canonical link-search machinery, except when searching by type alone.

3. **The Tumbler Square visualization** (4/46-4/47) explicitly diagrams "three endsets map to the other sides" of the square, implying the design's conceptual frame treats all three as participating reach-outs.

## What is not in the curated sources

- No worked example of a link with both F and G empty
- No discussion of whether MAKELINK accepts an empty from-set *and* empty to-set
- No type-only marker types in the standard type listings (4/52-4/55): every listed type either annotates content, connects two endpoints, or (paragraph link) uses one endset as a navigational pointer

NEED_RAW: 4/48-4/50 (raw 215-217) for the full one-sided-link discussion to confirm no ancillary mention of empty-on-both-sides; 4/62-4/68 (raw 229-235) for the FEBE MAKELINK definition to check whether empty endsets are admitted syntactically.

## Verdict

The design pattern in Literary Machines is **one-sided** (paragraph-style markers), not **zero-sided**. A "type-only marker" link with both F and G empty was not part of the worked design — neither explicitly excluded nor explicitly endorsed. An implementor extending the system in that direction would be filling a gap rather than realizing a stated Nelson intent.
