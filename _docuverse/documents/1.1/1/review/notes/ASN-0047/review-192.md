# Review of ASN-0047

## REVISE

### Issue 1: Reference to non-foundation ASN-0040
**ASN-0047, SubAllocatorBundle.T10aConformance**: "*Discharge:* ChainDiscipline (ASN-0093) identifies each chain as an ASN-0040 `SiblingStream` (hence a T10a-conforming `inc(·, 0)` allocator); ChainEnumerationInjectivity (ASN-0093) gives the strictly increasing (injective) enumeration..."

**Problem**: ASN-0040 is referenced by number, and it is not in the foundation set (ASN-0034, 0036, 0043, 0045, 0093). Standard 7 forbids cross-ASN references except to foundation ASNs. The discharge should rest on the ASN-0093 lemma (a foundation result) without naming the ASN-0093-internal source ASN-0040. As written, a reader must reach past the foundation boundary to a non-stable ASN to follow the claim.

**Required**: Drop the `ASN-0040` mention; cite only the ASN-0093 lemma (ChainDiscipline) as the T10a-conformance source. If "SiblingStream" notation is load-bearing here, it must be re-expressed in terms ASN-0093 exposes, not borrowed from ASN-0040.

### Issue 2: ASN overrides a foundation's type signature for M
**ASN-0047, Typing note (M total — overrides foundation)**: "ASN-0036 and ASN-0093 type the arrangement family as *partial*... This ASN *overrides* that typing: here M is *total* on T... Every `dom(M)`-phrased foundation result reads under (†) with `dom(M) ↦ E_doc`."

**Problem**: A foundation ASN is "verified and stable," and downstream ASNs are meant to *use* its definitions, not contradict them. Overriding ASN-0093/0036's typing of M creates a divergence: every inherited result phrased over partial M must be silently re-read under the (†) translation, and `dom(M)` now means two different things depending on which ASN's statement is being read (the trivial set `{t : M(t) defined}` = all of T under the total typing, vs. the allocated-document set under the partial typing). This is exactly the self-containment hazard standard 7 warns against — the ASN re-types a foundation primitive rather than relying on it. The reader cannot tell, at an inherited-result citation, whether the partial- or total-M reading is intended without consulting (†).

**Required**: Either (a) carry the document-set role entirely in E_doc and leave M with the foundation's partial typing (so no override is needed and inherited results apply verbatim), or (b) if the total typing is genuinely required, justify why the foundation typing is insufficient and state the (†) translation as a single named bridging lemma that every inherited `dom(M)`-result citation routes through explicitly, rather than a prose aside.

### Issue 3: S8-fin discharge argument duplicated across matrix cells
**ASN-0047, Class (a) verification matrix, K.μ~ column**: The S8a/S8-depth/S8-fin cell states "S8-fin(Σ') discharged independently of K.μ~-FIX through the K.μ⁻ + K.μ⁺ decomposition: K.μ⁻ restricts dom(M(d)) (a subset of a finite set is finite) and K.μ⁺ adds finitely many positions (finite + finite = finite)..."; the D-SEQ★ cell repeats "S8-fin(Σ') discharged independently of K.μ~-FIX through the K.μ⁻ + K.μ⁺ decomposition (subset of a finite set is finite; finite + finite is finite), per the S8-fin cell above."

**Problem**: This is the anti-bloat pattern of two passages stating the same argument in different words. The D-SEQ★ cell already back-references "per the S8-fin cell above" yet restates the full reasoning anyway, so the restatement carries no additional content — it is noise the precise reader must recognize as a duplicate. (This is duplication, not the under-specification concern of the previously declined matrix finding.)

**Required**: In the D-SEQ★ cell, keep only the back-reference ("S8-fin(Σ') per the S8-fin cell") and delete the restated "subset of a finite set is finite; finite + finite is finite" parenthetical.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The fork composite (J4) starts the forked document's link subspace empty and notes that a link-inheritance mechanism "would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred and belongs in a future operations ASN.

### Topic 2: Interior link withdrawal / tombstoning
D-CTG★/D-MIN★ confine K.μ⁻ to link-subspace suffix truncations; interior link withdrawal requires a separate mechanism. The ASN catalogues this in Open Questions rather than specifying it — appropriate, as it is new territory.

VERDICT: REVISE
