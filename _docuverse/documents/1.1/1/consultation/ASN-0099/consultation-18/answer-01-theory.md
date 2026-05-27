## Question 1 [theory]

> Was the design intent that content-editing operations (K.μ⁺, K.μ⁻) and provenance recording (K.ρ) leave the link store completely unmodified, with link allocation reserved exclusively to K.λ?

Yes, the design intent strongly supports this separation, though the notation K.μ⁺/K.μ⁻/K.ρ/K.λ is implementation-specific and doesn't appear in Literary Machines.

**Evidence from Nelson's FEBE specification:**

Of the 17 commands in XU.87.1, only **MAKELINK** allocates a link:

> "MAKELINK... This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." [LM 4/68]

The content operations (INSERT, DELETEVSPAN, COPY, REARRANGE, APPEND) have no link-allocation behavior in their specifications. Their effects are confined to byte-level Vstream mutation. See the operation definitions [LM 4/66–4/67].

**Link addressing requires permanence:**

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Permanent order-of-arrival addressing is only coherent if link allocation is reserved to a single creation primitive — if content edits could allocate links, the "order of arrival" address would be unstable.

**The survivability invariant requires content ops to leave links untouched:**

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

This survivability property only holds if content-editing operations leave the link store unmodified — links persist *because* μ⁻ and μ⁺ do not touch them. The strap-between-bytes model [LM 4/42] makes content edits invisible to the link layer.

**On provenance (K.ρ):**

Nelson has no explicit "provenance recording" operation. Provenance is **structural**, not operational — it emerges automatically from the I-address itself:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

COPY produces transclusion (shared I-addresses) without allocating any link. The I-address *is* the provenance record. So any operation reified as K.ρ in an implementation should likewise be link-store-inert.

**Conclusion:** The architectural separation you describe — link allocation reserved exclusively to K.λ, with K.μ⁺/K.μ⁻/K.ρ link-store-inert — is consistent with and required by my design. Link survivability, stable order-of-arrival link addresses, and structural (not metadata-based) provenance all depend on it.

NEED_RAW: 4/63 (MAKELINK home-document semantics, to confirm Nelson never authorizes side-effect link creation from content ops).
