# Consultation Answers — Transclusion (COPY)

**Inquiry:** What must content sharing through transclusion guarantee? How does transclusion differ from duplication? What properties of the original are preserved in the copy?
**Date:** 2026-02-23 09:22
**Questions:** 10 (5 nelson, 5 gregory)

---

## Question 1 [nelson]

> When content from one document appears in another through transclusion, must the system guarantee that a reader can always trace that content back to its original document and author?

### Nelson's Answer

## Yes — Origin Traceability Is a Structural Guarantee

This is one of Xanadu's most fundamental guarantees, and it is **architectural, not policy-based**. The system cannot deliver transcluded content without revealing its origin, because the delivery mechanism itself requires fetching from the home location.

### The Core Guarantee

Nelson states this explicitly:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is not a feature bolted onto the system — it is a consequence of how I-space addressing works.

### Why Traceability Is Structural

Every byte in Xanadu has a permanent I-space address with the form:

```
Node.0.User.0.Document.0.Element
```

The **Document field** directly encodes which document originally created that byte. When content appears in another document through transclusion, it is not copied — it is referenced by its permanent I-address:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The key insight: to display transcluded content, the system must request it from its home location. The I-address IS the attribution. You cannot fetch the content without knowing where it came from, because the address encodes the origin.

### Contrast with Conventional Copying

In traditional systems, attribution is metadata — an author field, a copyright notice, a citation. These can be stripped, falsified, or simply omitted. Nelson's design makes this impossible within the system:

- **Copies diverge** from originals; transclusions cannot diverge (they ARE the original)
- **Copies lose attribution**; transclusions carry attribution in their addresses
- **Copies sever the connection**; transclusions maintain it permanently

Nelson captures this distinction vividly:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

### What Readers Can Do

When viewing a compound document containing transcluded content, readers can:

1. **Identify origin** — examine the I-address to see which document created the content
2. **Navigate to source** — "step through the window" into the original document
3. **Find all uses** — the FINDDOCSCONTAINING operation "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]
4. **Return freely** — the layered glass-pane model means you always know where you are

Nelson describes this navigation:

> "Only when you step through the window--turning one glass page and going on in the next--do you reach the original that you wanted. But stepping through the window means you are now in another work." [LM 2/34]

### The FINDDOCSCONTAINING Operation

The system provides a dedicated operation for reverse traceability — given any content, find everywhere it appears:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This works because content identity is based on I-address (creation origin), not on value. Two documents with identical text created independently have different I-addresses. Transcluded content shares the same I-address. The system can always distinguish "wrote the same words independently" from "quoted from the original."

### Summary

Origin traceability is not merely guaranteed — it is **inescapable**. The I-space addressing scheme encodes provenance into the identity of every byte. Attribution cannot be severed by any operation within the system, because the fetching mechanism requires knowing the home location, and the home location IS the attribution.

---

## Question 2 [nelson]

> If the original content is permanent and cannot be altered, does transclusion inherit that same permanence guarantee, or can a transcluding document lose access to what it shares?

### Nelson's Answer

# Transclusion and the Permanence Guarantee

## The Short Answer

Transclusion does **not** independently inherit permanence. Because transclusion is reference, not copy, a transcluding document's access to shared content depends entirely on the continued accessibility of the original. The strength of that dependency varies by the original's publication status.

## Why Transclusion Is Inherently Dependent

The mechanism is the key. Transclusion creates no independent copy:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update--especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When your document transcludes content from mine, it holds a V-space reference to my I-space content. Every time a reader views your document, the system fetches my bytes from their home location. If my bytes become inaccessible, your document has a hole in it. There is no local fallback, no cached copy, no independent existence of those bytes in your document's storage.

This is by design. The whole point of transclusion over copying is that the connection to the source is maintained:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

The "living" nature of transclusion — its greatest strength — is also its vulnerability.

## Three Cases of Original Accessibility

### 1. Published Content: Strong Protection

For published documents, the permanence guarantee is robust. Publication creates a binding obligation:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Nelson explicitly ties this to transclusion and linking:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

So if you transclude from a published document, the publication contract protects your access. The original author cannot casually withdraw what you depend on. Your transclusion is safe — not because you have an independent copy, but because the original is contractually obligated to remain.

### 2. Privashed Content: Explicitly Vulnerable

Nelson defines "privashing" as a deliberate alternative to full publication:

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." [LM 2/48]

The consequence for those who depend on privashed content is stark: "Anyone who linked to it has no recourse if you withdraw." The same applies to transclusion. If you build a compound document that transcludes privashed content, and the author withdraws it, your document loses that content with no remedy.

Nelson provides no incentive structure to prevent this — in fact, privashing explicitly forfeits royalties, removing the economic incentive that would otherwise make withdrawal costly.

### 3. Private Content: Owner's Discretion

Private documents are accessible "only to the owner and his or her associates" [LM 2/42]. Transclusion of private content is possible (you can transclude from any document you have access to), but access can be revoked at any time. There is no permanence obligation for unpublished material.

## The Deeper Tension: Storage Funding

Even for published content, permanence is not unconditional. Nelson insists:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage requires ongoing rental paid by the content owner. Nelson does not specify what happens to published content when its owner stops paying storage fees. The permanence of the address is absolute — once assigned, a tumbler is never reused — but permanence of *accessibility* depends on continued funding.

This creates a gap in the transclusion guarantee. Your compound document depends on my content being accessible. My content being accessible depends on someone paying for its storage. If I die, go bankrupt, or simply stop paying, the system has no specified mechanism to ensure my published content remains available — despite the contractual obligation that it should.

The Author's Fund provides a partial safety net for public domain content, but Nelson does not specify it as a backstop for published content whose owner has lapsed.

## The Architectural Insight

Nelson designed this dependency deliberately. The alternative — making transclusion create independent copies — would solve the accessibility problem but destroy everything else:

- Attribution would be severed (copies lose their origin)
- Royalties would be impossible (who gets paid for a copy?)
- Updates would not propagate (copies diverge)
- The web of literature would fragment (connections become illusions)

As Nelson puts it through the water metaphor:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Transclusion's vulnerability to source withdrawal is the price of keeping literature alive and connected. The publication contract is the mechanism that makes this price acceptable — it ensures that the most important content (published work that others depend on) cannot be casually removed.

## Summary

| Source Status | Transclusion Permanence | Mechanism |
|---|---|---|
| **Published** | Strong — contractually protected | Publication contract forbids withdrawal |
| **Privashed** | None — explicitly revocable | Owner retains withdrawal right |
| **Private** | None — at owner's discretion | Access can be revoked at any time |
| **Published but unfunded** | Unspecified gap | Nelson does not resolve this case |

The permanence guarantee flows *through* the publication contract, not through the transclusion mechanism itself. Transclusion is a window, not a vault. The window stays open only as long as the original remains accessible — and the original remains accessible only as long as the publication contract and storage funding hold.

---

## Question 3 [nelson]

> Must links attached to the original content remain visible and functional when that content appears through transclusion in a different document?

### Nelson's Answer

## Yes — Links Follow Content, Not Containers

Nelson's design ensures that links attached to content remain functional when that content appears through transclusion. This is not an explicit rule stated in isolation but a structural consequence of three interlocking design decisions.

### 1. Links Point to I-Space, Not V-Space

Links attach to permanent content addresses (I-space), not to positions in any particular document's arrangement (V-space):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." (4/42)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

The "strap between bytes" metaphor is key. The strap grips the bytes themselves — their permanent identity — not the document that currently displays them.

### 2. Transclusion Preserves I-Space Identity

Transcluded content does not receive new addresses. It retains its original I-space identity:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

When Document B transcludes content from Document A, those bytes keep their I-space addresses from Document A. They appear "just as if they were native" in B's V-stream, but their identity is unchanged.

### 3. Therefore Links Are Discoverable Through Transclusion

Since links point to I-space addresses, and transcluded content retains its I-space addresses, any link search for content that happens to appear through transclusion will find the same links as searching for it in the original document. The FINDLINKSFROMTOTHREE operation searches by endset addresses in I-space — it is indifferent to which document's V-space currently displays the content.

Nelson confirms the general discoverability guarantee:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." (2/46)

"A given document or place in the document" includes transcluded content appearing in that document.

### Visibility vs. Discoverability

There is one important distinction Nelson draws: **all links are discoverable, but not all are automatically displayed.** The front end applies filtering:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" (2/47)

So the guarantee is:

- **Functional**: Links to transcluded content are always findable through the standard link search mechanism. The search operates on I-space addresses, which transclusion preserves.
- **Visible**: Whether they are automatically shown is a front-end display decision, subject to user-controlled filtering ("sieving"). But they are always *available* to be shown.

### The Parallel with Version-Spanning Links

Nelson states an analogous principle for versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

Links follow content across versions because versions share I-space. Transclusion is the same mechanism generalized across documents: content retains its I-space identity, so links follow it wherever it appears.

### Summary

Links must remain **functional** (findable, followable) when content appears through transclusion. This is a structural consequence of three design choices: links attach to I-space addresses, transclusion preserves I-space addresses, and link search operates on I-space. Nelson does not need to state this as a separate rule — it falls out of the architecture. The only front-end discretion is in **display filtering**, not in whether the links exist or can be found.

---

## Question 4 [nelson]

> What distinguishes transclusion from copying at the level of identity — does the shared content retain the same identity as the original, or does it acquire a new one?

### Nelson's Answer

Let me check the raw page for the COPY operation to see exactly what Nelson says about identity there.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-234.png"}}
</tool_call>

Let me also check the page describing inclusions and native vs non-native bytes.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-178.png"}}
</tool_call>

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-177.png"}}
</tool_call>

And the page on FINDDOCSCONTAINING, which depends on this identity question.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-237.png"}}
</tool_call>

---

## Transclusion preserves identity. Copying creates new identity.

This is the central architectural distinction, and Nelson builds the entire system around it.

### The I-address IS identity

Every byte created in Xanadu gets a permanent I-space address encoding its origin — which server, which account, which document, which element position. That I-address is the byte's **identity**, not its value.

Two documents containing the word "hello" typed independently have **different** I-addresses. The bytes are value-identical but identity-distinct. Conversely, when content is transcluded, both the original and the transclusion reference the **same** I-address. The bytes are not merely value-identical — they are the *same bytes*.

### Transclusion: same identity, different arrangement

When you transclude content (Nelson's COPY operation in FEBE, or his "quote-window" / "inclusion"), the receiving document's V-space maps to the **original** I-addresses. No new content is created in I-space. The transclusion is a reference, not a reproduction.

Nelson is explicit about the mechanism:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The term "virtual copies" is precise: they appear as if copied but are not. The bytes live at their home location. The receiving document merely points to them.

### INSERT: new identity

By contrast, INSERT creates **new** content in I-space:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Inserted text gets fresh I-addresses under the receiving document. It is new content with a new identity — even if the bytes happen to be identical to something already in the docuverse.

### Why this distinction matters: three consequences

**1. Attribution is structural, not metadata.**

Because transclusions share I-addresses with the original, the system always knows where content came from:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This cannot be stripped or falsified within the system. The fetching mechanism itself requires consulting the home location. Attribution is not a tag on the content — it is the address *of* the content.

**2. FINDDOCSCONTAINING works.**

The operation that finds all documents containing a given piece of content depends entirely on shared I-addresses:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

If transclusion created new I-addresses, this operation would be impossible — you could not trace from a passage in one document to all other documents containing that same passage. Shared identity is what makes the web of transclusion discoverable.

**3. Correspondence across versions is computable.**

SHOWRELATIONOF2VERSIONS returns corresponding span pairs between two versions. This works because versions created by CREATENEWVERSION share I-addresses for unchanged content. Shared I-address *means* correspondence:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The system does not compare text values to find matches. It compares I-addresses. Identity, not equality.

### The glass pane metaphor

Nelson's visual metaphor makes the identity point intuitive:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Painted content (INSERT) is new material — new I-addresses, new identity. Clear glass (transclusion) is a window onto existing material — same I-addresses, same identity. You are not looking at a reproduction of the other document. You are looking *through* to the other document itself.

### Live vs dead

This identity-preservation is what makes transclusions "live" and copies "dead":

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

A transclusion participates in the network because it shares identity with the original. Links made to the original content reach the transclusion. New links made to the transclusion reach the original. A true copy (outside the system) severs this — it creates new bytes with no I-address, no identity, no connection.

### Summary

| Operation | I-addresses | Identity | Nelson's term |
|-----------|-------------|----------|---------------|
| INSERT | Fresh (new content) | New identity | "native bytes" |
| COPY (transclusion) | Shared (same as source) | Same identity | "inclusions," "virtual copies" |
| External copy | None (outside system) | No identity | "frozen and dead" |

The answer to your question is unambiguous: transcluded content retains the **same identity** as the original. It does not acquire a new one. This is not a design choice among alternatives — it is the foundation on which permanence, attribution, correspondence, and the entire economic model rest.

---

## Question 5 [nelson]

> When a document transcludes content, must the system guarantee that the original author receives attribution and compensation, even across arbitrary depths of re-transclusion?

### Nelson's Answer

# Yes — and the guarantee is architectural, not policy

Nelson designs Xanadu so that transclusion depth is irrelevant to both attribution and compensation. This is not a feature bolted onto the system but a consequence of how I-space addressing works.

## Attribution: structural and unseverable

The fundamental mechanism is that transclusion is **reference, not copy**. When Document C transcludes from Document B, which transcludes from Document A, the bytes in C that originated in A still carry A's I-space address. There is no intermediate copy at B's address — B's V-space merely maps positions to A's I-space content.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Nelson explicitly addresses the arbitrary-depth case:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

And guarantees traceability through all layers:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The depth collapses to zero because every byte resolves to exactly one I-space home. There is no chain of custody to trace — there is simply an address that identifies the origin.

## Compensation: per-byte at the origin

The royalty mechanism operates on the same principle. Each published document has a **cash register** that increments whenever its bytes are delivered:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

When a reader views Document C and the system delivers bytes that originated in Document A, it is A's cash register that increments — regardless of whether the request came through zero, one, or fifty layers of transclusion. The bytes are fetched from their home location; the royalty accrues there.

Nelson makes the split explicit for compound documents:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

Each compound document earns royalties only for bytes it actually created (its "painted" content). Bytes visible through windows earn royalties for their respective original authors. This split is computed from the I-addresses, which encode origin directly.

## Why depth is architecturally irrelevant

The key insight is that transclusion **does not create new content**. Document B's V-space points to A's I-space. Document C's V-space points to those same I-space addresses (whether directly or through B's mapping). At every depth, the I-address is the same — A's original address. There is no intermediate "B's copy" to complicate the attribution or payment chain.

This means:
- **Attribution**: always resolves to the original creator via I-address
- **Compensation**: always flows to the original creator via cash register at home document
- **No degradation with depth**: the 50th re-transclusion is identical to the 1st

Nelson captures this with the analogy of live versus dead content:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage... Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Only a copy *outside* the system (paper, disk) severs the connection. Within the system, at any depth, the connection is permanent.

## Summary

| Property | Mechanism | Depth-independent? |
|----------|-----------|-------------------|
| **Attribution** | I-address encodes home document | Yes — same address at every depth |
| **Compensation** | Cash register at home document | Yes — bytes delivered from origin |
| **Traceability** | "Ascertain the home document of any character" | Yes — structural, not metadata |

The system guarantees both attribution and compensation across arbitrary transclusion depth, not through tracking chains of re-use, but through the simpler and more robust mechanism of permanent content identity: every byte has exactly one home, and that home is where credit and payment flow.

---

## Question 6 [gregory]

> When COPY (vcopy) transfers a V-span from source to target, does the target POOM receive entries pointing to the exact same I-addresses as the source, or does any intermediate step (such as vspanset2sporglset or insertpm) ever allocate fresh I-addresses for the copied content?

### Gregory's Answer

## KB Synthesis

Looking at the knowledge base, **COPY (vcopy) transfers the exact same I-addresses from source to target — no fresh I-addresses are ever allocated during the operation.**

## The Evidence

**Core Postcondition** [ST-VCOPY from Finding 0002]:
"No new content identities are created. The target gains references to exactly the content identities specified in the source specset."

**Mechanism** [INT-SPORGL-TRANSCLUSION from Finding 0013]:
"The data flow is: source V-spec → sporgls (via `vspanset2sporglset`) → `insertpm` into destination document. The sporgl carries the content's I-address identity through the copy operation. Because the sporgl preserves the original I-address (not a new one), the destination document ends up referencing the same content identities as the source."

**Conversion is Read-Only** [ST-VSPAN-TO-SPORGL from Finding 0013]:
"This conversion is a pure function over the document's current V→I mapping — it reads the enfilade but does not modify it."

## Contrast with INSERT

The critical distinction is revealed in [INV-DELETE-NOT-INVERSE from Finding 0064]:

**INSERT path:**
```
State: "Original text" at I(5.1)-I(5.13)
DELETE → INSERT same text:
Result: "Original text" at I(5.14)-I(5.26)  # NEW I-addresses allocated
```

**VCOPY path:**
```
VCOPY from version sharing I(5.1)-I(5.13):
Result: restores identity at I(5.1)-I(5.13)  # SAME I-addresses preserved
```

## The Complete Data Flow

**INSERT:**
1. `doinsert` calls `inserttextingranf` → allocates FRESH I-addresses from granfilade
2. `docopy` receives those fresh I-addresses
3. `insertpm` writes those fresh I-addresses to target POOM

**COPY/VCOPY:**
1. `vspanset2sporglset` reads source POOM → extracts EXISTING I-addresses (no allocation)
2. `docopy` receives those existing I-addresses
3. `insertpm` writes those SAME I-addresses to target POOM

[ST-COPY from Finding 0064] confirms: "Unlike INSERT (which allocates fresh I-addresses), COPY shares the source's existing I-addresses in the target document's POOM via `insertpm`."

[INV-IADDR-PROVENANCE from Finding 0046] states it directly: "INSERT allocates fresh I-addresses under the target document; COPY references existing ones."

## What insertpm Does

[PRE-COPY from Finding 0046] clarifies that `insertpm` creates new POOM tree structures (crums), not new I-addresses: "When COPY inserts V→I mappings into a POOM, the insertion follows an extension-or-create rule... If [conditions hold], the existing crum's width is extended in place. Otherwise, a new crum is created."

The crums are POOM data structures that map V-positions to I-addresses. Creating a new crum means allocating a new tree node, but the I-addresses stored in that node are the input parameters — they are never freshly allocated by `insertpm`.

## Final Answer

**No intermediate step allocates fresh I-addresses.** The target POOM receives entries pointing to the identical I-addresses from the source. This identity preservation is the defining characteristic of transclusion and is what enables `compare_versions`, cross-document link discovery, and provenance tracking to function correctly.

## Code Exploration

Now I have traced the complete execution path. Let me write a comprehensive answer with all citations.

---

# Answer: COPY Preserves I-addresses

When `COPY` (vcopy) transfers a V-span from source to target, **the target POOM receives entries pointing to the exact same I-addresses as the source**. No intermediate step allocates fresh I-addresses for the copied content.

## Evidence from Source Code

### 1. The COPY Entry Point

At **`do1.c:45-65`**, the `docopy` function executes these key steps:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // Line 54
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)        // Line 55
    && acceptablevsa (vsaptr, docorgl)                                   // Line 56
    
    /* the meat of docopy: */
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)        // Line 60
    
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // Line 62
    );
}
```

The critical operation is **line 54**: `specset2ispanset` converts the source V-spans into I-spans by **looking up** the existing V↔I mapping.

### 2. V-to-I Conversion via POOM Lookup

At **`orglinks.c:397-402`**, `vspanset2ispanset` calls `permute`:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, 
                                 typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

At **`orglinks.c:425-454`**, `span2spanset` performs the actual lookup:

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, 
                          typespanset restrictionspanptr, INT restrictionindex, 
                          typespanset *targspansetptr, INT targindex)
{
    typecontext *context, *c, *retrieverestricted();
    typespan foundspan;
    
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, 
                                 restrictionindex, (typespan*)NULL, 
                                 targindex, (typeisa*)NULL);              // Line 435
    
    for (c = context; c; c = c->nextcontext) {
        context2span (c, restrictionspanptr, restrictionindex, 
                     &foundspan, targindex);                              // Line 443
        nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, 
                                         (typeitemset*)targspansetptr);
    }
}
```

**Line 435** calls `retrieverestricted`, which **searches the source POOM** for existing V↔I mappings.

### 3. Retrieving Existing I-addresses from POOM Crums

At **`retrie.c:55-84`**, `retrieverestricted` searches the POOM tree:

```c
typecontext *retrieverestricted(typecuc *fullcrumptr, typespan *span1ptr, 
                                INT index1, typespan *span2ptr, INT index2, 
                                typeisa *docisaptr)
{
    // ... setup span bounds ...
    temp = retrieveinarea (fullcrumptr, &span1start, &span1end, index1, 
                          &span2start, &span2end, index2, 
                          (typebottomcruminfo*)infoptr);                  // Line 82
    return(temp);
}
```

At **`retrie.c:229-268`**, `findcbcinarea2d` traverses the POOM tree:

```c
int findcbcinarea2d(typecorecrum *crumptr, typedsp *offsetptr, 
                    tumbler *span1start, tumbler *span1end, INT index1, 
                    tumbler *span2start, tumbler *span2end, INT index2, 
                    typecontext **headptr, typebottomcruminfo *infoptr)
{
    for (; crumptr; crumptr = getrightbro (crumptr)) {
        if (crumptr->height != 0) {
            // Recurse into children
            findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, 
                           span1start, span1end, index1, 
                           span2start, span2end, index2, headptr, infoptr);  // Line 259
        } else {
            context = makecontextfromcbc ((typecbc*)crumptr, 
                                         (typewid*)offsetptr);                // Line 262
            incontextlistnd (headptr, context, index1);                       // Line 263
        }
    }
}
```

**Line 262** creates a context from each matching bottom crum, which contains the **existing I-address and V-address stored in that crum**.

### 4. Extracting I-addresses from Context

At **`context.c:176-212`**, `context2span` extracts the I-address:

```c
int context2span(typecontext *context, typespan *restrictionspanptr, 
                INT idx1, typespan *foundspanptr, INT idx2)
{
    tumbler upperbound, lowerbound;
    typedsp grasp, reach;
    
    movetumbler (&restrictionspanptr->stream, &lowerbound);
    tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
    prologuecontextnd (context, &grasp, &reach);                          // Line 188
    
    // ... handle boundary clipping ...
    
    movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);               // Line 206
    tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);// Line 207
}
```

**Line 206** copies the I-address from the context's `grasp` (the crum's displacement) into the found span's stream. This is the **original I-address from the source POOM**.

### 5. Inserting the Same I-addresses into Target POOM

At **`orglinks.c:75-134`**, `insertpm` inserts these I-addresses into the target:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, 
             tumbler *vsaptr, typesporglset sporglset)
{
    tumbler lstream, lwidth;
    type2dbottomcruminfo linfo;
    typewid crumorigin, crumwidth;
    
    for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);              // Line 101
        
        movetumbler (&lstream, &crumorigin.dsas[I]);                      // Line 105
        movetumbler (&lwidth, &crumwidth.dsas[I]);                        // Line 109
        movetumbler (vsaptr, &crumorigin.dsas[V]);                        // Line 113
        
        // ... calculate V-width ...
        
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, 
                 &linfo, V);                                              // Line 130
        tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);                 // Line 131
    }
    return (TRUE);
}
```

**Line 105** places the I-address (from `lstream`) into the crum origin's I-dimension. **Line 113** places the target V-address into the crum origin's V-dimension. **Line 130** creates a new crum in the target POOM with these exact I and V addresses.

At **`sporgl.c:178-188`**, `unpacksporgl` simply extracts the stored values:

```c
int unpacksporgl(typesporglset sporglptr, tumbler *streamptr, 
                tumbler *widthptr, type2dbottomcruminfo *infoptr)
{
    if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
        movetumbler (&((typeispan *)sporglptr)->stream, streamptr);       // Line 181
        movetumbler (&((typeispan *)sporglptr)->width, widthptr);        // Line 182
    }
}
```

The I-addresses passed through this entire chain came from **looking up existing POOM crums**, not from any allocation function.

### 6. Contrast with INSERT (Which Does Allocate)

For comparison, `INSERT` operations **do** allocate fresh I-addresses. At **`do1.c:87-123`**, `doinsert` calls `inserttextingranf`:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, 
             typetextset textset)
{
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // Line 118
        && docopy (taskptr, docisaptr, vsaptr, ispanset)                 // Line 119
    );
}
```

**Line 118** allocates fresh I-addresses for the new text content. **Line 119** then copies those newly-allocated I-addresses into the target POOM using the same `docopy` path.

The I-address allocation occurs in **`granf2.c:130-156`**:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);           // Line 142
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);       // Line 152
    }
}
```

This function **allocates new I-addresses** by finding the highest existing I-address and incrementing. This is **only called during INSERT**, never during COPY.

## Conclusion

The complete execution path is:

**COPY path** (preserves I-addresses):
1. `docopy` → `specset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`
2. Searches source POOM tree via `findcbcinarea2d` → `makecontextfromcbc`
3. Extracts existing I-addresses via `context2span`
4. Inserts same I-addresses into target POOM via `insertpm` → `insertnd`

**INSERT path** (allocates new I-addresses):
1. `doinsert` → `inserttextingranf` → `findisatoinsertgr` → allocates new I-addresses
2. Then calls `docopy` to insert the newly-allocated I-addresses

Therefore, when COPY transfers content, **both source and target POOMs point to identical I-addresses**. The permascroll identity is preserved—no fresh I-addresses are allocated during copy.

---

## Question 7 [gregory]

> If document A contains text at I-addresses [.0.1.1,.0.1.5] and document B transcludes that same span, then document A DELETEs the text from its POOM, does find_links on document B still discover links whose endsets reference those I-addresses — confirming that the transcluding document's copy is fully independent of the source document's subsequent edits?

### Gregory's Answer

## KB Synthesis

Yes, `find_links` on document B will still discover those links. Here's the complete logical chain:

## Transclusion Preserves I-Addresses

When document B transcludes from document A via vcopy, B's POOM receives V→I mappings to the **same** I-addresses that A references [ST-VCOPY]. The sporgl (provenance-carrying data structure) carries the I-address identity through the copy operation [INT-SPORGL-TRANSCLUSION]. Both documents now reference I-addresses [.0.1.1,.0.1.5], but each maintains its own **independent** POOM mapping.

## DELETE is Document-Local

When document A DELETEs the text, the operation modifies **only** A's POOM [FC-DELETE-CROSS-DOC]. The concrete example from that entry shows exactly this scenario:

```
D has "ABCD", T transcluded "BC" from D (sharing I(5.2), I(5.3))

After DELETE "BC" from D:
  D's POOM: mappings gone from D
  T's POOM: UNCHANGED, T still has "BC"
  Granfilade: content bytes persist
```

As stated: "DELETE in one document has zero effect on any other document's POOM mappings" [FC-DELETE-CROSS-DOC].

## Link Discovery Works on B's Intact POOM

`find_links` discovers links by **I-address intersection**, not by document or V-address matching [ST-FIND-LINKS]. The operation converts the search V-span to I-addresses, then queries the spanfilade index. Since B's POOM still maps V-positions to I-addresses [.0.1.1,.0.1.5], those I-addresses are present in B's content identity [INT-LINK-TRANSCLUSION].

[INT-TRANSCLUSION-LINK-SEARCH] directly addresses this scenario:

> "When content is transcluded (vcopy'd) to another document, the copy retains the original content identity (I-stream addresses). If the original content is deleted, links referencing that content become undiscoverable from the original document but **remain discoverable from the copy**, because the copy's V-stream still contains content at those I-stream addresses."

The concrete example confirms:
```
- vcopy("linked") from Original to Copy
- Delete "linked" from Original
- find_links(Original) → []
- find_links(Copy) → [link_id]  ✓
```

## Supporting Invariants

This behavior follows from core system invariants:
- **Content identity is permanent** [INV-CONTENT-IMMUTABILITY]: I-addresses are never destroyed
- **POOMs are independent** [FC-DELETE-CROSS-DOC]: each document's V→I mapping is isolated
- **Links track identity** [INV-LINK-CONTENT-TRACKING]: links reference I-addresses, which persist across document mutations
- **Global link visibility** [INV-LINK-GLOBAL-VISIBILITY]: "A link created in any document is discoverable from every document in the system that shares the linked content's identity"

## Conclusion

Yes, `find_links(B)` discovers the links. Document B's transclusion is **fully independent** of A's subsequent edits. A's DELETE removes only A's V→I mappings; B's mappings to those same I-addresses remain intact, preserving link discoverability.

The only scenario where links become undiscoverable is if **all** documents delete the content [EC-GHOST-LINK] — but as long as any document (including B) retains V→I mappings to those I-addresses, links remain discoverable from that document.

## Code Exploration

Now I'll provide the complete answer based on my code analysis:

---

# Answer: YES - Transclusion is Fully Independent

**When document A contains text at I-addresses [.0.1.1,.0.1.5] and document B transcludes that span, then document A DELETEs the text from its POOM, `find_links` on document B WILL still discover links whose endsets reference those I-addresses.**

The transcluding document's copy is **fully independent** of the source document's subsequent edits.

---

## Code Analysis: Three-Layer Independence

### Layer 1: Document B's POOM Contains Its Own V→I Mappings

When document B transcludes content from document A (either via `COPY` or `CREATE_LINK`), the operation creates **independent V→I mappings in B's POOM**:

**File: `do1.c:45-65` — The `docopy` function:**

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
  // ...
  
  return (
     specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
  && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && acceptablevsa (vsaptr, docorgl)

  /* the meat of docopy: */
  && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // Line 60

  &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // Line 62
  );
}
```

**Line 60**: `insertpm` inserts V→I mappings into **document B's POOM** (its orgl enfilade in granf). Document B now has its own independent reference to the I-addresses.

**Line 62**: `insertspanf` registers document B in the spanfilade as containing those I-addresses, enabling `find_links` and `finddocscontaining` queries.

---

### Layer 2: Document A's DELETE Affects Only A's POOM

When document A deletes content, **only A's POOM is modified**:

**File: `do1.c:158-167` — The `dodeletevspan` function:**

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)  // Line 165
  );
}
```

**File: `orglinks.c:144-151` — The `deletevspanpm` function:**

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
  if (iszerotumbler(&vspanptr->width))
    return (FALSE);
  deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // Line 148
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

**Line 148**: `deletend` removes V→I mappings from **document A's orgl only**. It operates on a single enfilade tree (`docorgl`), with no cross-document side effects.

**File: `edit.c:31-76` — The `deletend` function:**

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
  typeknives knives;
  typewid offset, grasp, reach;
  typecuc *father, *ptr, *next;
  // ...
  
  makecutsnd (fullcrumptr, &knives);                   // Cut THIS tree only
  newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
  
  for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:
        disown ((typecorecrum*)ptr);        // Line 59
        subtreefree ((typecorecrum*)ptr);   // Line 60
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // Line 63
        break;
    }
  }
  setwispupwards (father,1);
  recombine (father);
}
```

**Lines 59-60**: Crums are disowned and freed from **this document's tree only** (`fullcrumptr`, which is document A's orgl).

**Line 63**: Displacements are adjusted in **this document's crums only**.

**Critical observation**: `deletend` receives `fullcrumptr` (a pointer to document A's orgl root) and operates exclusively on that tree. Document B's orgl is **never accessed** or **modified**.

---

### Layer 3: Frame Axiom F0 — No Cross-Document Side Effects

**Finding 0067** confirms that document operations have no cross-document side effects:

> The low-level enfilade operations (`insertnd`, `deletend`, `cutcrumseq`, `rearrangend`) operate exclusively on the target document's orgl (POOM enfilade in granf). They do NOT:
> - Modify other documents' orgls
> - Corrupt links (either in the target document's link subspace or in other documents)
> - Alter the spanfilade in ways that corrupt queries

Document A's `deletend` operates on A's orgl. Document B's orgl remains **completely unchanged**.

---

### Layer 4: Spanfilade Entries Are Never Cleaned Up

**Finding 0057** documents that DELETE does NOT remove spanfilade entries:

> When a document DELETEs content that was previously COPYed (transcluded) into it, **the DELETE operation does NOT clean up the spanfilade entries** that were created by the COPY. The `deletevspanpm` function only removes the V→I mapping from the document's POOM (in granf), but there is no corresponding call to remove the I-address-to-document association from the spanf index.

When document B transcluded A's content:
- `insertspanf` (invoked at `do1.c:62`) registered B in the spanfilade

When document A deletes:
- **No corresponding `deletespanf` call exists**
- The spanfilade entry for document B persists

**File: `spanf1.c` (entire file inspection):**

**Functions that exist:**
- ✅ `insertspanf` — adds spanfilade entries
- ✅ `findlinksfromtothreesp` — searches spanfilade for links
- ✅ `retrieveendsetsfromspanf` — retrieves link endsets
- ✅ `finddocscontainingsp` — finds documents containing I-addresses

**Functions that DO NOT exist:**
- ❌ `deletespanf` — no such function
- ❌ `removespanf` — no such function

The spanfilade is **write-only** for this operation — entries are added but never removed by DELETE.

---

## How find_links Works After A's DELETE

When `find_links` is called on document B searching for links whose endsets reference the I-addresses:

**File: `do1.c:348-353` — The `dofindlinksfromtothree` function:**

```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, 
                            typespecset tovspecset, typespecset threevspecset, 
                            typeispan *orglrangeptr, typelinkset *linksetptr)
{
  bool findlinksfromtothreesp();

  return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, 
                                 threevspecset, orglrangeptr, linksetptr);
}
```

**File: `spanf1.c:55-102` — The `findlinksfromtothreesp` function:**

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr, 
                            typespecset fromvspecset, typespecset tovspecset, 
                            typespecset threevspecset, typeispan *orglrange, 
                            typelinkset *linksetptr)
{
  typesporglset fromsporglset;
  // ...
  
  if (fromvspecset) {
    specset2sporglset (taskptr, fromvspecset, &fromsporglset,NOBERTREQUIRED);  // Line 70
  }
  
  if (fromvspecset) {
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, 
                      &fromlinkset, orglrange, LINKFROMSPAN);  // Line 76
    if (!fromlinkset) {
      *linksetptr = NULL;
      return (TRUE);
    }
  }
  // ...
  intersectlinksets(taskptr,fromlinkset,tolinkset,threelinkset,linksetptr);  // Line 99
  return (TRUE);
}
```

**Line 70**: Converts V-specs (from document B) to I-addresses by looking up B's POOM. Since B's POOM is unchanged, this succeeds and returns the I-addresses.

**Line 76**: Searches the spanfilade for links whose FROM endset overlaps those I-addresses. The spanfilade entries persist (no cleanup), so the links are found.

**Line 99**: Returns the discovered links.

**Result**: `find_links` succeeds because:
1. Document B's POOM still maps V-positions to I-addresses (unchanged by A's delete)
2. The spanfilade entries for B's links persist (no cleanup mechanism)
3. The link orgls themselves are permanent (stored at I-addresses)

---

## The I-Addresses Are Permanent and Shared

The crucial architectural insight: **I-addresses are permanent identifiers in the permascroll**, independent of any document's POOM:

- Document A's POOM mapped V-positions to I-addresses `[.0.1.1, .0.1.5]`
- Document B's POOM also maps V-positions to **the same** I-addresses `[.0.1.1, .0.1.5]`
- When A deletes, it removes A's V→I mappings
- The I-addresses themselves continue to exist
- Document B's V→I mappings are **unaffected**

**File: `do2.c:14-46` — How V-specs convert to I-addresses:**

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, 
                      typeispanset *ispansetptr, int type)
{
  typeorgl docorgl;
  typeispanset *vspanset2ispanset();
  // ...
  
  for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    // ...
    if (((typeitemheader *)specset)->itemid == VSPECID) {
      if (!(
        findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl,type)  // Line 35
      && (ispansetptr = vspanset2ispanset (taskptr, docorgl, 
                                           ((typevspec *)specset)->vspanset, 
                                           ispansetptr)))) {  // Line 36
        return (FALSE);
      }
    }
  }
  return (TRUE);
}
```

**Line 35**: Looks up the **document's orgl** (POOM) in granf.

**Line 36**: Converts V-spans to I-spans by reading that document's POOM mappings.

When processing a V-spec from document B, this looks up **B's orgl**, which contains **B's independent V→I mappings**. Document A's delete has no effect on B's orgl.

---

## Summary: Three Layers of Independence

| Layer | What It Stores | Modified by A's DELETE? | Why B Is Unaffected |
|-------|----------------|------------------------|---------------------|
| **I-space** | Permanent content at I-addresses | ❌ No (permanent) | I-addresses exist regardless of POOM mappings |
| **A's POOM** | A's V→I mappings | ✅ Yes | Only A's mappings removed, not I-addresses themselves |
| **B's POOM** | B's V→I mappings | ❌ No (Frame F0) | Each document has independent orgl enfilade |
| **Spanfilade** | I→document index | ❌ No (no cleanup) | Entries added but never removed (Finding 0057) |

**Result**: Document B's transclusion is **fully independent**. Links in B whose endsets reference the I-addresses remain discoverable via `find_links` because:

1. **B's POOM is unchanged** (Frame Axiom F0, confirmed at `edit.c:31-76`)
2. **The I-addresses are permanent** (permascroll identity)
3. **Spanfilade entries persist** (no cleanup mechanism exists, Finding 0057)
4. **Link orgls are permanent** (stored at I-addresses, independent of POOMs)

---

## Files Referenced

| File | Lines | Content |
|------|-------|---------|
| `do1.c` | 45-65 | `docopy` — creates B's independent V→I mappings via `insertpm` |
| `do1.c` | 158-167 | `dodeletevspan` — deletes from A's POOM only |
| `do1.c` | 348-353 | `dofindlinksfromtothree` — searches spanfilade for links |
| `orglinks.c` | 74-133 | `insertpm` — inserts V→I mappings into document's POOM |
| `orglinks.c` | 144-151 | `deletevspanpm` — removes V→I from POOM, no spanf cleanup |
| `edit.c` | 31-76 | `deletend` — operates on single orgl tree only |
| `do2.c` | 14-46 | `specset2ispanset` — converts V-specs to I-spans via POOM lookup |
| `do2.c` | 116-128 | `insertendsetsinspanf` — indexes link endsets in spanfilade |
| `spanf1.c` | 14-53 | `insertspanf` — adds spanfilade entries (no delete exists) |
| `spanf1.c` | 55-102 | `findlinksfromtothreesp` — searches for links via spanfilade |

---

## Related Findings

- **Finding 0057**: Spanfilade entries are not cleaned up on DELETE
- **Finding 0067**: Frame Axiom F0 confirmed — no cross-document side effects
- **Finding 0040**: Links can be removed from POOM while persisting in I-space
- **Finding 0012**: Dual enfilade architecture — granf (POOMs) vs spanf (index)

---

## Question 8 [gregory]

> When COPY creates DOCISPAN entries in the spanfilade for the target document, does it create one entry per contiguous I-span in the copied specset, and are these entries structurally identical (same I-address range, different document ID) to the source document's existing DOCISPAN entries?

### Gregory's Answer

## KB Synthesis

Yes, COPY creates **one DOCISPAN entry per contiguous I-span** in the copied specset, and these entries have **identical I-address ranges** to the source document's DOCISPAN entries but **different document IDs** (pointing to the target document).

## Key Evidence

### Entry Granularity
[ST-COPY] Finding 0047: "COPY creates DOCISPAN entries proportional to the number of contiguous I-spans in the source content, not the number of bytes. COPY of contiguous source content (1 I-span) creates 1 DOCISPAN entry."

[SS-DOCISPAN] Finding 0047: "DOCISPAN entries in the spanfilade have per-span granularity, not per-byte. When `insertspanf` is called, it iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct."

### I-Address Preservation
[ST-VCOPY] Finding 0002: "The postcondition for vcopy is: `references(target) = references(target_before) ∪ {content_ids referenced by source_specset}`. No new content identities are created."

[INV-IADDR-PROVENANCE] Finding 0046: "COPY does not allocate new I-addresses; it creates V→I mappings that reference existing ones."

### Structural Relationship
The COPY operation flow ([SS-DOCISPAN] Finding 0036):
```
docopy → specset2ispanset → insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

The `docisaptr` parameter is the **target document's ISA**, not the source's. This means:
- **I-address range**: Identical to source (from preserved `ispanset`)
- **Document ID**: Different (target doc ISA, from `docisaptr` parameter)
- **Entry count**: 1:1 correspondence with source's contiguous I-spans

## Concrete Example
```
Source doc S has "ABCDEFGHIJ" at I-addresses α₁..α₁₀ (1 contiguous I-span)
  DOCISPAN: (α₁, width 10) → S

After COPY to target doc T:
  Target DOCISPAN: (α₁, width 10) → T

Same I-address range (α₁, width 10), different document ID (T vs S)
```

The entries are **structurally similar** but **not identical** — they differ in exactly one field: the document ID they map to.

## Code Exploration

Based on my code analysis, I can now answer your question with specific citations.

## Answer

**Part 1: One entry per contiguous I-span?**

**YES.** COPY creates one DOCISPAN entry per item in the converted I-spanset.

**Evidence:**

1. In `do1.c:62`, `docopy` calls:
   ```c
   insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
   ```

2. In `spanf1.c:25-51`, `insertspanf` loops through each item in the sporglset (ispanset):
   ```c
   for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
           if (((typeitemheader *)sporglset)->itemid == ISPANID) {
                   movetumbler (&((typeispan *)sporglset)->stream, &lstream);
                   movetumbler (&((typeispan *)sporglset)->width, &lwidth);
                   movetumbler (isaptr,&linfo.homedoc);
           }
           movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
           movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
        insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
   }
   ```
   Each iteration creates one spanfilade entry via `insertnd` [`spanf1.c:51`].

3. The ispanset structure comes from `specset2ispanset` [`do1.c:54`], which converts V-space specifications to I-space by calling `vspanset2ispanset` → `permute` → `span2spanset` [`orglinks.c:397-454`]. This preserves the structure: each contiguous I-span becomes one list item.

**Part 2: Structurally identical entries?**

**NO.** The entries share the **same I-address range** but have **different document identity**.

**Evidence:**

Target document's DOCISPAN entry structure [`spanf1.c:22-51`]:
- **ORGLRANGE dimension**: Created by `prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE])` where `isaptr` is the **target** document ISA and `spantype` is `DOCISPAN` [`spanf1.c:22`]
- **SPANRANGE dimension**: `crumorigin.dsas[SPANRANGE] = lstream` (I-address), `crumwidth.dsas[SPANRANGE] = lwidth` (I-width) [`spanf1.c:49-50`]
- **Info payload**: `linfo.homedoc = isaptr` (target document ISA) [`spanf1.c:29`]

Source document's DOCISPAN entry structure:
- Created identically when the source content was inserted
- Same SPANRANGE coordinates (same I-addresses)
- Different ORGLRANGE coordinates (source doc ISA + DOCISPAN prefix, not target)
- Different homedoc field (source doc ISA, not target)

**Summary:**
- ✅ Same I-address range in SPANRANGE dimension
- ❌ Different document ID in ORGLRANGE dimension (target vs source)
- ❌ Different homedoc pointer in info payload (target vs source)

The entries are **content-identical** (point to the same permascroll addresses) but **structurally distinct** (belong to different documents' indices).

---

## Question 9 [gregory]

> If a user INSERTs the string "Hello" into document A and separately INSERTs the identical string "Hello" into document B, do find_links and compare_versions treat these two instances as completely unrelated content (distinct I-addresses), whereas a COPY of document A's "Hello" into document B would make them appear as shared content — and is this the sole behavioral distinction between duplication and transclusion?

### Gregory's Answer

## KB Synthesis

Yes, your understanding is exactly correct. This is the fundamental architectural distinction in the Xanadu content model.

## Independent INSERT: Distinct Identities

When "Hello" is INSERTed into document A and separately INSERTed into document B:

**Document A:**
- `[ST-INSERT]` allocates fresh I-addresses (say I.1–I.5) for the 5 bytes
- `[INV-IADDR-PROVENANCE]` establishes A as the native document for I.1–I.5

**Document B:**  
- `[ST-INSERT]` allocates NEW I-addresses (say I.10–I.14) for the identical bytes
- `[INV-IADDR-PROVENANCE]` establishes B as the native document for I.10–I.14

**Result:** Completely distinct content identities despite identical textual value

## COPY: Shared Identity

When "Hello" is INSERTed into A and then COPYed into B:

**Document A:**
- `[ST-INSERT]` allocates I.1–I.5

**Document B:**
- `[ST-VCOPY]` shares the SAME I.1–I.5 (no new allocation)
- `[SS-CONTENT-IDENTITY]`: "The vcopy operation adds references to existing content identities into the target document. It does not copy the content itself"

**Result:** Both documents reference identical I.1–I.5

## Behavioral Consequences

### compare_versions

**Independent INSERT:**
```
compare_versions(A, B) → []  # empty
```
- `[INV-DOC-ISOLATION-IDENTITY]`: "Documents created independently share no content identity, even if they contain identical text"
- `[ST-COMPARE-VERSIONS]`: Operates by I-address intersection; I.1–I.5 ∩ I.10–I.14 = ∅

**After COPY:**
```
compare_versions(A, B) → [("Hello", "Hello")]  # shared content detected
```
- Same I-addresses I.1–I.5 in both documents

### find_links

**Independent INSERT:**
```
create_link(source=A's "Hello")
find_links(B's "Hello") → []  # not found
```
- `[INT-LINK-TRANSCLUSION]`: "Links are indexed by content identity"
- Link endpoints reference I.1–I.5; B contains I.10–I.14; no intersection

**After COPY:**
```
create_link(source=A's "Hello")  
find_links(B's "Hello") → [link_id]  # found via shared identity
```
- `[INT-LINK-TRANSCLUSION]`: "Any document referencing those identities can discover the link"
- Both documents reference I.1–I.5, so intersection succeeds

## This IS the Sole Distinction

The allocation vs sharing of I-addresses is the **only** structural difference:

- `[FC-INSERT-IADDR]`: "INSERT does not modify the I-address of any pre-existing content... The operation's effect on the identity layer is purely additive"
- `[ST-VCOPY]`: "No new content identities are created. The target gains references to exactly the content identities specified in the source specset"

All observable behavioral differences (comparison, link discovery, provenance tracking, transitive identity) flow from this single fact:
- **Duplication** = distinct I-addresses = no identity relationship
- **Transclusion** = shared I-addresses = permanent identity relationship

`[INV-IADDR-IMMUTABILITY]` guarantees these I-addresses never change after allocation, making the identity relationship permanent and immutable.

## Code Exploration

Perfect! I've traced through the complete code path and verified against existing findings. Let me provide you with the comprehensive answer:

---

## Answer: Yes, independently inserted identical strings are treated as completely unrelated content

Your hypothesis is **entirely correct**. The distinction between duplication and transclusion in Udanax Green is precisely about I-address allocation and sharing.

### Code Evidence: How INSERT Allocates New I-Addresses

**INSERT operation flow** [do1.c:87-123]:
1. `doinsert()` calls `inserttextingranf()` [do1.c:118]
2. Which calls `inserttextgr()` [granf2.c:82-108]
3. Which calls `findisatoinsertgr()` [granf2.c:91] to **allocate a NEW I-address**
4. For text (ATOM type), this calls `findisatoinsertmolecule()` [granf2.c:157-180]
5. Which calls `findpreviousisagr()` [granf2.c:163] to find the highest existing I-address
6. Then `tumblerincrement()` [granf2.c:168] to get the **NEXT available I-address**
7. `insertseq()` [granf2.c:98] stores the text at this NEW I-address
8. `docopy()` [do1.c:119] links the V-address to this NEW I-address

**Result:** Each INSERT allocates a fresh, unique I-address, even for identical text.

### Code Evidence: How COPY Reuses Existing I-Addresses

**COPY operation flow** [do1.c:45-65]:
1. `docopy()` receives an existing `ispanset` (I-addresses) [do1.c:54]
2. Calls `insertpm()` [do1.c:60] to link the V-address to **the SAME I-addresses**
3. Calls `insertspanf()` [do1.c:62] to index the transclusion
4. **No new I-addresses are allocated** — the existing ones are reused

### Code Evidence: How find_links Uses I-Addresses

**find_links operation flow** [do1.c:348-352, spanf1.c:56-103]:
1. `dofindlinksfromtothree()` calls `findlinksfromtothreesp()` [spanf1.c:56]
2. Which calls `specset2sporglset()` [spanf1.c:71] to convert V-spans to I-spans
3. This calls `vspanset2ispanset()` [orglinks.c:397-402, sporgl.c:35-65]
4. Which calls `retrieverestricted()` [orglinks.c:435] on the POOM to **look up which I-addresses exist at that V-position**
5. Then `sporglset2linkset()` [spanf1.c:77] searches the spanfilade for links with those I-addresses

**Result:** Two documents with identical text inserted independently have **different I-addresses**, so find_links finds no relationship between them.

### Code Evidence: How compare_versions Uses I-Addresses

**compare_versions operation flow** [do1.c:428-449]:
1. `doshowrelationof2versions()` converts both V-specs to I-spans [do1.c:444-445]
2. Calls `intersectspansets()` [do1.c:446] to find **common I-addresses**
3. Returns the intersection as the "shared content"

**Result:** Two documents with identical text inserted independently have **different I-addresses**, so compare_versions returns an empty intersection (no shared content).

### Empirical Evidence: Finding 0018

From [findings/0018-content-identity-tracking.md:13-26]:

> **1. Identical text has different I-addresses when created independently**
>
> Two documents with identical text do NOT share content identity:
>
> ```
> Source1: "From source one"  (I-address: X)
> Source2: "From source two"  (I-address: Y)
>
> compare_versions(source1, source2) → [] (empty - no shared content!)
> ```
>
> Content identity is based on **when and where** content was created, not its textual value.

### The Sole Behavioral Distinction

Yes, this **is** the sole behavioral distinction between duplication and transclusion:

| Aspect | Independent INSERT | COPY (Transclusion) |
|--------|-------------------|---------------------|
| **I-address allocation** | Allocates NEW I-address via `findisatoinsertgr()` [granf2.c:129] | Reuses EXISTING I-address from source |
| **find_links result** | No shared links found | Links discovered through both documents [Finding 0026] |
| **compare_versions result** | Empty (no shared content) | Returns intersection of shared I-spans |
| **find_documents result** | Returns only the queried document | Returns all documents sharing that I-address [Finding 0018:77] |
| **Transitive discovery** | Not possible | Works across chains: A←B←C [Finding 0018:28-42] |

### Key Source Citations

- **INSERT path:** `doinsert()` → `inserttextingranf()` [do1.c:118] → `inserttextgr()` [granf2.c:82] → `findisatoinsertgr()` [granf2.c:129] → **allocates new I-address**
- **COPY path:** `docopy()` [do1.c:45] → `insertpm()` [do1.c:60] → **reuses existing I-address**
- **V→I lookup:** `vspanset2ispanset()` [orglinks.c:397] → `permute()` [orglinks.c:404] → `span2spanset()` [orglinks.c:425] → `retrieverestricted()` [orglinks.c:435] → **queries POOM for I-addresses at V-position**
- **find_links:** `findlinksfromtothreesp()` [spanf1.c:56] → converts V-spans to I-spans → searches spanfilade by I-address
- **compare_versions:** `doshowrelationof2versions()` [do1.c:428] → `intersectspansets()` [do1.c:446] → **finds common I-addresses**

### Summary

Your understanding is **precisely correct**. The entire Xanadu content identity model is built on I-address allocation:
- **INSERT** = new content = new I-address
- **COPY** = transclusion = shared I-address
- All discovery operations (find_links, compare_versions, find_documents) work by intersecting I-addresses, making this the **fundamental and sole** distinction between duplication and transclusion.

---

## Question 10 [gregory]

> When isanextensionnd detects that copied I-addresses are contiguous with an existing POOM entry in the target document (reach == origin), does the silent coalescing into a single crum preserve the property that find_links discovers links to the coalesced content, or could the merge alter the I-span boundaries reported during sporgl conversion in a way that affects link endpoint overlap detection?

### Gregory's Answer

## KB Synthesis

# Answer: Coalescing Preserves Link Discovery

**Yes, the silent coalescing preserves link discovery.** The merge cannot alter I-span boundaries in a way that affects link endpoint overlap detection. Here's why:

## The I-Address Invariant

From [INV-IADDR-IMMUTABILITY] and [ST-VCOPY] (Finding 0046): `isanextensionnd` only coalesces when two conditions hold:
1. **Same homedoc**: Both the existing crum and new content originate from the same source document
2. **I-contiguity**: The new content's I-address origin equals the existing crum's I-address reach

This means coalescing happens precisely when the I-addresses form a single contiguous range. Consider:
- **Before extension**: Crum₁ covers I[100, 103), Crum₂ would cover I[103, 105)
- **After extension**: Crum₁' covers I[100, 105)

The I-address range is **identical** in both cases: [100, 105).

## Link Discovery Operates on I-Addresses

From [INT-LINK-TRANSCLUSION] (Finding 0028) and [INT-SPORGL-LINK-INDEX] (Finding 0013):
- Links are indexed by I-address in the spanfilade
- `find_links` converts search specsets to I-addresses and checks for overlap: `I-addresses(search) ∩ I-addresses(link.endpoint) ≠ ∅`

The POOM crum structure is **transparent** to this process. Whether the POOM internally uses one crum or two crums, the conversion from V-span to I-span produces the same I-address range when the underlying I-addresses are contiguous.

## Sporgl Conversion Reflects I-Address Structure

From [SS-LINK-ENDPOINT] (Finding 0037) and [ST-VSPAN-TO-SPORGL] (Finding 0013):
- Multiple I-spans arise when content is transcluded from **multiple sources** (different homedocs)
- The fragmentation boundary is content identity, not POOM structure
- A V-span that maps to contiguous I-addresses from the **same** homedoc produces a single I-span

Since `isanextensionnd` only merges crums with the same homedoc and contiguous I-addresses, the merged crum represents what was already a single I-span from the link system's perspective.

## Concrete Example

```
State A (before coalescing):
  POOM: Crum₁[V:1.1→1.4, I:100→103, homedoc=D]
        Crum₂[V:1.4→1.6, I:103→105, homedoc=D]
  Link endpoint: I[101, 104)
  find_links search: V[1.1, 1.6) → converts to I[100, 105)
  Intersection: I[101, 104) ∩ I[100, 105) = I[101, 104) ≠ ∅ ✓

State B (after coalescing):
  POOM: Crum₁'[V:1.1→1.6, I:100→105, homedoc=D]
  Link endpoint: I[101, 104) (unchanged per [INV-LINK-PERMANENCE])
  find_links search: V[1.1, 1.6) → converts to I[100, 105)
  Intersection: I[101, 104) ∩ I[100, 105) = I[101, 104) ≠ ∅ ✓
```

The intersection is **identical** because the I-address range is identical.

## Why This Matters

From [FC-CONTENT-SPANF-ISOLATION] (Finding 0012): The POOM (granf) and link index (spanf) are separate structures. The POOM's internal representation (one crum vs. two) is an optimization that doesn't affect the abstract V→I mapping. Link discovery queries the spanf index using I-addresses derived from that abstract mapping, making it immune to POOM internal structure changes.

**Conclusion**: The coalescing is a POOM-internal optimization that preserves all observable properties including link discovery. The invariants [INV-LINK-CONTENT-TRACKING] and [INV-LINK-GLOBAL-VISIBILITY] depend on I-address overlap, which remains unchanged regardless of whether the POOM uses one crum or two to represent the same I-address range.

## Code Exploration

Based on my code analysis, I can now provide a complete answer to your question about whether coalescing preserves link discovery properties.

## Answer: YES, coalescing preserves link discovery correctly

The silent coalescing that occurs when `isanextensionnd` detects contiguous I-addresses (reach == origin) **does preserve** the property that `find_links` discovers links to the coalesced content. The I-span boundaries reported during sporgl conversion are maintained correctly.

### Evidence from the code:

**1. The coalescing condition** [insertnd.c:301-309]:
```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
    return (FALSE);
  prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
  return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

When this returns TRUE, coalescing happens at [insertnd.c:250-257]:
```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
```
This simply extends the existing crum's width without creating a new crum.

**2. Link discovery during follow** [sporgl.c:67-95]:

The `link2sporglset` function retrieves link endpoints:
```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);
tumblerincrement (&zero, 0, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan ,V, (typespan*)NULL, I, (typeisa*)NULL)) {
  for (c = context; c; c = c->nextcontext) {
    sporglptr = (typesporgl *)taskalloc(taskptr,sizeof (typesporgl));
    contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
```

**3. I-span extraction** [sporgl.c:205-220]:

The `contextintosporgl` function extracts I-spans from contexts:
```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
  movetumbler(&context->totaloffset.dsas[index],&sporglptr->sporglorigin);
  movetumbler(&context->contextwid.dsas[index], &sporglptr->sporglwidth);
}
```

### Why coalescing preserves correctness:

**Scenario without coalescing:**
- Crum A: cdsp=(V:1.1, I:100), cwid=(V:0.5, I:10), homedoc=D1
- Crum B: cdsp=(V:1.6, I:110), cwid=(V:0.4, I:5), homedoc=D1
- Retrieving V-span [1.1, 2.1) produces TWO contexts:
  - Context 1: totaloffset=(V:1.1, I:100), contextwid=(V:0.5, I:10) → I-span [100, 110)
  - Context 2: totaloffset=(V:1.6, I:110), contextwid=(V:0.4, I:5) → I-span [110, 115)

**Scenario with coalescing:**
- Coalesced crum: cdsp=(V:1.1, I:100), cwid=(V:0.9, I:15), homedoc=D1
- Retrieving V-span [1.1, 2.1) produces ONE context:
  - Context: totaloffset=(V:1.1, I:100), contextwid=(V:0.9, I:15) → I-span [100, 115)

**Both produce the same I-span coverage: [100, 115)**

### Handling partial overlaps:

The `context2span` function [context.c:176-212] handles cases where the query V-span partially overlaps a crum by performing proportional clipping:

```c
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
  tumblerincrement (&grasp.dsas[idx2], 0, (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound)  == GREATER) {
  tumblerincrement (&reach.dsas[idx2], 0, - tumblerintdiff (&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);
}
```

This proportional clipping preserves the V↔I correspondence because the V-width encoding [orglinks.c:115-117] maintains a linear relationship between V and I coordinates within each crum.

### Conclusion:

The coalescing optimization is **semantically transparent** to link discovery. Whether stored as one coalesced crum or multiple adjacent crums, the final I-spans returned during link following represent the identical mathematical set of I-addresses. The merge does not alter I-span boundaries in any way that would affect link endpoint overlap detection.
