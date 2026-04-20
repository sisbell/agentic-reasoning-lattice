# Review of ASN-0025

## REVISE

### Issue 1: State model codomain excludes structural allocations

**ASN-0025, State Model**: "The I-space content function maps I-addresses to byte values: Σ.ι : IAddr ⇸ Byte"

**Problem**: Three of seven operations allocate entries that are not bytes. CREATE VERSION allocates an orgl address (structural entry). CREATE DOCUMENT allocates an orgl address. CREATE LINK allocates a link address (structured endset data). Each claims `Σ'.A = Σ.A ∪ {o}` where `Σ.A = dom(Σ.ι)`, which requires `Σ'.ι(o)` to be defined as a `Byte`. An orgl is not a byte. A link is not a byte. The P0 ∧ P1 verifications for these three operations are formally unsound under the stated type — the new addresses cannot inhabit `dom(Σ.ι)` if `Σ.ι` maps to `Byte`.

No argument in the ASN actually depends on the codomain being `Byte` specifically. The proofs all work if the codomain is generalized to `Value` (or `ContentUnit`), encompassing bytes, structural entries, and link data. The fix is a definition change, not an argument change.

**Required**: Generalize the codomain of Σ.ι from `Byte` to a type that accommodates structural entries (orgls, links), or separate structural entries into their own state component with parallel permanence properties. Verify that P0 ∧ P1 cover all components.


### Issue 2: CREATE LINK has conditional J0 verification and no document target

**ASN-0025, CREATE LINK**: "If the link is placed in a document's V-space, the new V-entry points to l ∈ Σ'.A."

**Problem**: Every other operation's J0 verification is unconditional. CREATE LINK's is conditional on "if the link is placed in a document's V-space." This raises two questions the ASN does not answer: (a) Is a link always placed in some document's V-space, or can it exist in I-space only? (b) Which document receives the link entry? Without a target document, UF-V ("every operation targeting document d leaves other documents unchanged") cannot be applied — there is no d. The operation's V-space effect is unspecified where every other operation's is explicit.

**Required**: Either specify which document receives the link (making CREATE LINK parallel to INSERT in structure), or state that links reside in I-space only and have no V-space representation (making J0 trivially preserved). Whichever choice, make the J0 verification unconditional.


### Issue 3: Structural consequences depend on unmodeled link state

**ASN-0025, Structural Consequences**: "Links attach to I-space addresses. By P0 ∧ P1, these addresses are permanent and their content immutable."

**Problem**: The state model Σ has three components: Σ.ι, Σ.A, Σ.v. None of these model what a link is, what it contains, or how its endsets reference I-space. The claim "links attach to I-space addresses" is taken from the vocabulary, not derived from or formalized in the model. Link survivability is therefore not a consequence of P0 ∧ P1 alone — it is a consequence of P0 ∧ P1 *plus the assumption that links reference I-space addresses*. The ASN presents this as a derivation ("By P0 ∧ P1...") when it is actually conditional on an unmodeled premise.

The same issue affects the attribution consequence to a lesser degree: it relies on `fields()` being the sole attribution mechanism, which is reasonable from T4 but not formally connected to any link or attribution component in Σ.

**Required**: State the dependency explicitly. Either: (a) add minimal link state to Σ (e.g., `Σ.links : LinkId → Endsets` where endsets reference I-space addresses) and derive survivability from the model, or (b) present survivability as conditional — "if links reference I-space addresses (as established in a future link ASN), then P0 ∧ P1 guarantee survivability."


## OUT_OF_SCOPE

### Topic 1: V-space contiguity invariant
The ASN describes V-position shifts (INSERT shifts forward, DELETE shifts backward to "close the gap") but does not formalize a tiling property — that V-positions form a contiguous, gap-free sequence. This is a V-space structure property, not a permanence property.
**Why out of scope**: Belongs in a V-space operations ASN, not in address permanence.

### Topic 2: Whether COPY should require source visibility
COPY's precondition is `S ⊆ Σ.A` — the source addresses exist in I-space. It does not require that S is visible in any document. This means COPY can make invisible content (deleted from all V-spaces) visible again. Whether this is intentional or whether COPY should require source visibility is a design question.
**Why out of scope**: This is an operation-design decision for a future ASN on editing semantics, not an error in the permanence model.

### Topic 3: Complete link model and endset semantics
The ASN allocates link addresses and notes subspace disjointness but does not model link structure, endset resolution, or how links interact with editing operations beyond survivability.
**Why out of scope**: A full link ASN is needed. ASN-0025 correctly identifies the permanence foundation that links will depend on.

VERDICT: REVISE
