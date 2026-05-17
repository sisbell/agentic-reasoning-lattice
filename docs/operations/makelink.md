# MAKELINK

*Doc filename uses LM's canonical name. Green renamed it CREATELINK during implementation; the project's deprecated note (ASN-0063) followed Green's name. The wire-level call is CREATELINK at opcode 27. See LM vs Green divergence below.*

| | LM | Green | This project |
|---|---|---|---|
| **Label** | MAKELINK | CREATELINK | CREATELINK Operation (note title) |
| **Opcode** | 4 | **27** (renumbered) | — |
| **Source** | LM 4/68 | `requests.h:36`, `fns.c:100`, dispatch at `init.c:60` | ASN-0063 (retired, pending regen) |
| **Status** | Specified | Shipped | Note retired |
| **Deps** | — | — | **(none registered)** — substrate-migration anomaly; original YAML declared `[34, 36, 43, 47, 53, 58]` but didn't survive migration. See Open questions. |

## What it does

Create a new link in the link store, with endsets identifying the content the link connects. Per LM 4/68:

> *"This creates a link in document `<doc id>` from `<from set>` to `<to set>` connected to `<three set>`. It returns the id of the link made."*

The link's home document is specified explicitly — *"because that determines the actual residence of the link — since a document may contain a link between two other documents"* (LM 4/68). Endsets address content by **permanent I-address**, not V-position, which is what gives links their survivability under editing: *"links are 'straps between bytes' that survive deletions, insertions and rearrangements, if anything is left at each end"* (Nelson, paraphrased in ASN-0063).

## Structure (ASN-0063)

CREATELINK is the **only LM operation that creates links** (INSERT/DELETE/REARRANGE/COPY all operate on content and arrangements only). It introduces the **resolution bridge**: the translation from user-facing V-references to storage-facing I-references at link-creation time.

### The resolution bridge — V-span → I-span at creation time

User-facing inputs are V-spans (positions in a current arrangement). The link's endsets are I-spans (positions in permanent storage). CREATELINK is the operation that bridges them.

- **Definition — VSpanImage** (line 20): the image of a V-span under M(d) — the I-addresses currently bound to those V-positions
- **CL0 — BlockProjection** (line 33): a V-span overlapping a single mapping block (β = (v_β, a_β, n)) projects to a contiguous run of I-addresses, representable as a single well-formed I-span. The proof uses block decomposition (ASN-0058) and ordinal arithmetic (ASN-0034 T1, T12) for both V- and I-discreteness.
- **CL1 — ResolutionExistence** (line 39): for any document with arrangement satisfying ASN-0036's S2/S8-fin and a text-subspace-confined V-span-set, an endset exists with image ⊆ coverage
- **CL2 — ResolutionContainment**: under the same precondition, `image(d, Ψ) ⊆ coverage(resolve(d, Ψ))`

A single V-span crossing multiple mapping blocks produces **multiple I-spans** — one per overlapping block. This is the normal case when selected content was assembled from multiple sources via transclusion. "AABB" where "AA" is transcluded from X and "BB" from Y produces two I-spans, one in each source's I-space.

### Link subspace ownership

- **CL-OWN — LinkSubspaceOwnership**: in every reachable state, link allocations live in the link subspace (s_L) and content allocations live in the content subspace (s_C); the two domains are disjoint. This is the structural invariant that makes "create a link without affecting content" well-defined.

### The CREATELINK composite (transition framework)

CREATELINK is a K.λ (link allocation) transition followed by K.μ⁺_L (link-arrangement extension to record the link's V-position in its home document). The composite has explicit frame conditions:

- **CL4 — ContentNonInterference**: `C' = C` — no content is created or modified
- **CL5 — LinkPreservation**: every pre-existing link survives unchanged (L is append-only)
- **CL6 — ArrangementConfinement**: only the home document's arrangement is modified (and only by appending the new link's V-position)

### The discovery function

The new link must be discoverable by anyone searching from any I-address it references. This is the link-discovery contract that **FINDLINKSFROMTOTHREE relies on** (see [`findlinksfromtothree.md`](findlinksfromtothree.md)).

- **CL7 — DiscoveryMonotonicity**: once a link is discoverable from address `a` in role `r`, it remains discoverable in every reachable future state
- **CL8 — DiscoveryCompleteness**: after CREATELINK produces link ℓ with value (F, G, Θ), ℓ is in `disc(a, r)` for every (a, r) where the role is satisfied
- **CL9 — DiscoveryIndependence**: `disc(a, r)` depends only on the I-address and role — not on any document or arrangement

### Latent links

- **CL10 — LatentLinks**: a link whose endsets cover I-addresses not currently in any document's arrangement is *latent*. It exists in L. `disc(a, r)` includes it. But no document-scoped query encounters it because no arrangement provides a V-path to those I-addresses. This is the formal handle on links to orphaned or not-yet-arranged content.

## LM vs Green divergence

**This is the canonical name + opcode mismatch case in the catalog.**

| | LM | Green |
|---|---|---|
| Opcode | 4 | **27** |
| Name | MAKELINK | **CREATELINK** |

Both renamed and renumbered. LM's opcode 4 was vacated; Green moved the link-family operations into a contiguous block at opcodes 27-31 (CREATELINK=27, RETRIEVEENDSETS=28, FINDNUM=29, FINDLINKS=30, FINDNEXT=31). LM's interleaved numbering became Green's taxonomic grouping.

**The wire protocol uses Green's numbering and naming** (per `init.c:60`'s `requestfns[CREATELINK] = createlink`). A client wanting to talk to a real Green backend must send opcode 27 with the CREATELINK request shape — not opcode 4 / MAKELINK.

### BNF / request shape

| | LM | Green |
|---|---|---|
| Request shape | `<doc id> <doc vsa> <from set> <to set> <three set>` | matches LM |
| Returns | `<link id>` | matches LM |

Wire format is identical except for the opcode prefix. The semantic content of the request and response carried through unchanged.

### Safe-mode behavior

CREATELINK is never safe-mode-disabled — it's a core write operation.

## Current project state

ASN-0063 was retired along with the other 5 deprecated operations and is pending regen. The retired note is substantial and unusual in scope: it introduces both the operational semantics (CL4-CL6 frame, CL-OWN ownership) AND the link-discovery contract (CL7-CL10) that downstream operations like FINDLINKS depend on.

The retired note's structure has three layers worth keeping on regen:

1. **Resolution bridge** (CL0-CL2): the V-span → I-span translation at creation time — this is *the* mechanism by which links are stable under editing
2. **Composite + frame** (CL4-CL6, CL-OWN): standard operation-note shape
3. **Discovery contract** (CL7-CL10): the read-side guarantees that CREATELINK's write must satisfy so that FINDLINKS works

Layer 3 is conceptually a separate concern — it specifies the discovery function — but it's stated here because CREATELINK is the operation that populates the discovery index. Worth considering whether the discovery contract should be hoisted into a separate "link discovery foundation" ASN that both CREATELINK (writer) and FINDLINKS (reader) cite.

## Pending absorptions

CREATELINK's absorption profile is different from INSERT/DELETE/REARRANGE/COPY because it operates in the link subspace, not content arrangements. The shared shift-increment / ord-vpos / contiguity-preservation batch from the content operations does **not** apply here.

### Candidate absorptions (operation-specific)

- **CL0 BlockProjection's V-discreteness sub-lemma → ASN-0058?** CL0's proof argues that depth-`#v_β` tumblers in a half-open ordinal range `[v_β + k, v_β + (k+1))` are exactly the singleton `{v_β + k}`. The same argument is then repeated for I-addresses. This is a general property of ordinal-increment sequences at fixed depth — convex subsets correspond to contiguous index sub-ranges. It may belong in ASN-0058 (Mapping Block Algebra) as a reusable lemma rather than being derived twice inside CL0. Reassess on regen.
- **CL-OWN LinkSubspaceOwnership** depends on the s_L vs s_C partition. The pending **S7e (ContentSubspacePartition) absorption in ASN-0036** (memory: `project_asn36_pending_absorptions.md`) is the content-side half; once S7e lands, CL-OWN becomes a direct corollary of S7e + L0a's link-side analogue. Worth checking whether CL-OWN can then be discharged by citation rather than local derivation.
- **Discovery contract (CL7-CL10) hoisting.** Not strictly an absorption, but a re-layering question: should CL7-CL10 move out of CREATELINK into a "Link Discovery Foundation" ASN that both CREATELINK and FINDLINKS cite? FINDLINKS (ASN-0079) currently assumes a discovery function without specifying its contract; CREATELINK (ASN-0063) specifies the contract without naming it as a separable layer. The two sides would compose more cleanly with an explicit shared layer. Worth deciding on regen.

### Inherited from operation-set (does not apply)

- Shift-increment commutativity, ord/vpos, contiguity preservation — these are content-arrangement primitives. CREATELINK doesn't operate on content arrangements, so none of these apply.

## Open questions

- **Missing `citation.depends` registrations (substrate-migration anomaly).** ASN-0063's substrate has **zero** `citation.depends` edges, despite its original project-model entry (commit `8fb45c2d`, 2026-03-21) declaring `depends: [34, 36, 43, 47, 53, 58]` — the canonical full-surface dep set for link-touching operations, matching DELETE/COPY/FINDLINKS. The commit message: *"Both [ASN-0063 and ASN-0064] depend on Link Ontology (43) in addition to the standard operations stack (34, 36, 47, 53, 58)."* The deps were declared correctly; they just didn't survive the project-model → substrate migration. Sibling deprecated ops (0059/0061/0065/0067/0079) all have their deps in substrate; ASN-0063 was likely missed because it was already retired before the backfill pass ran. **On regen, declare deps in the new note's frontmatter (or inquiry frontmatter) and the substrate machinery will emit the `citation.depends` edges.** Verify with `python3 scripts/diagnostics/note_graph.py 63`.
- **Cross-subspace V-spans.** CL1/CL2 require V-spans to be confined to the text subspace. What happens to a CREATELINK request whose `<from-set>` includes a span crossing subspace boundaries? Likely a precondition violation; worth verifying Green's actual behavior.
- **Empty endsets.** What if all three endsets are empty? Does the resulting link have any meaning? The protocol BNF doesn't appear to forbid empty endsets, but the retired note's CL8 implicitly assumes at least one endset has coverage.
- **The "three-set" type endset.** LM calls the third endset "three-set" and the BNF generalizes types as endsets pointing at type-bearing addresses. ASN-0063 treats it the same way as from-set and to-set in CL8. Worth a separate doc on how "type" is encoded as a tumbler set rather than a discrete tag.
- **Discovery index materialization.** CL7-CL10 specify the discovery function abstractly. Green's actual implementation maintains an index (per `disc(a, r)`'s O(1)-ish access in the safe-mode-live FINDLINKS path). Is the index materialization specified anywhere, or is it left as an implementation detail?

## Cross-references

- [`catalog.md`](catalog.md) — Full operations inventory; CREATELINK row at LM opcode 4 / Green opcode 27
- [`findlinksfromtothree.md`](findlinksfromtothree.md) — Read-side companion; relies on CREATELINK's discovery contract (CL7-CL10)
- LM source: page 4/68
- Green source: `channels/gregory/resources/udanax-test-harness/backend/{requests.h, fns.c, init.c}`
- Project note: `_docuverse/documents/1.1/1/note/ASN-0063-createlink-operation.md` (retired, pending regen)
- Foundation: ASN-0043 (Link Model), ASN-0058 (Mapping Block Algebra), ASN-0036 (Strand Model)
- Pending S7e absorption: memory `project_asn36_pending_absorptions.md`
