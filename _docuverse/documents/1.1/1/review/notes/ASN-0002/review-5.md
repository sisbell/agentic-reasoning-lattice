# Review of ASN-0002

## REVISE

### Issue 1: COPY's V-space effect is underspecified
**ASN-0002, COPY / Effect on vspace**: No V-space effect section exists for COPY. The section says COPY "creates a V-space mapping in the target document to existing I-addresses" and Gregory's evidence says it "inserts those I-addresses... into the target document's mapping at new V-positions," but the ASN does not specify:
- Whether existing V-positions in the target shift (as they do for INSERT).
- The insertion point parameter (INSERT takes a position; COPY's parameters are unstated).
- Subspace isolation within the target (INSERT has AP6; COPY has no equivalent).

**Problem**: Every other mutating operation has an explicit V-space effect section. INSERT specifies shifting, subspace isolation (AP6), and frame conditions. DELETE specifies removal and leftward shift. REARRANGE specifies permutation. COPY specifies only its ispace non-effect and its cross-document frame condition (source unchanged). The target document's V-space behavior is left to inference. A future ASN reasoning about the state of a target document after COPY cannot ground that reasoning in any stated property.

**Required**: Add a V-space effect subsection for COPY that specifies: (a) the insertion point parameter, (b) shifting of existing V-positions at or beyond the insertion point, (c) a labeled subspace isolation property analogous to AP6 (COPY into text subspace shifts only text V-positions of the target, etc.).

---

### Issue 2: DELETE subspace isolation asserted by "mirrors," not independently established
**ASN-0002, DELETE / Frame conditions**: "DELETE's subspace isolation mirrors INSERT's: the leftward shift is confined to the subspace of the deletion."

**Problem**: The review standards require "No proof by similarly — if cases differ, show each case." The ASN then acknowledges the mechanisms differ: INSERT uses a "two-blade boundary" while DELETE uses an "exponent guard that makes cross-subspace subtraction a no-op." Different mechanisms require independent argument. INSERT's subspace isolation is formally labeled (AP6); DELETE's is stated only in a frame-condition paragraph with no label. A future ASN citing DELETE's subspace isolation has nothing formal to cite.

**Required**: State DELETE's subspace isolation as a labeled property (parallel to AP6) with its own justification. The exponent-guard evidence is already present — it needs to anchor a formal statement rather than a "mirrors" assertion.

---

### Issue 3: AP14 verification relies on "analogous confinement"
**ASN-0002, Cross-document isolation**: "INSERT, DELETE, REARRANGE: target is `d`, and the operation's V-space effects are confined to `d` (AP6 for INSERT; analogous confinement for DELETE and REARRANGE)."

**Problem**: AP6 is stated for INSERT only. For DELETE and REARRANGE, the verification says "analogous confinement" — this is proof by "similarly" applied to the verification of a key cross-cutting property. AP8a constrains REARRANGE's subspace behavior but does not state cross-document confinement. DELETE has no labeled property establishing confinement of any kind.

**Required**: Verify AP14 independently for each operation. For DELETE: the operation takes a single target document; its V-space effect (removal + leftward shift) is confined to that document because [state reason]. For REARRANGE: the operation takes a single target document; its permutation is confined to that document because [state reason]. These arguments are straightforward — the operations take one document parameter and have no mechanism to access another document's V-space — but they must be shown, not analogized.

---

### Issue 4: CREATELINK home/endpoint distinction is ambiguous
**ASN-0002, CREATELINK**: "The home document is an explicit parameter of the operation; it is distinct from the documents whose content the endsets reference."

**Problem**: It is unclear whether "it is distinct from" is a **precondition** (CREATELINK rejects the case where home = endpoint) or a **clarification** of typical usage. If it is a precondition, it should be labeled and justified — why should a document be forbidden from linking to its own content? If it is not a precondition, the case home = endpoint must be analyzed: the V→I lookup reads from the home document's text subspace while the link insertion writes to its link subspace. AP16 already constrains the blast radius to the link subspace, so there is no conflict, but this should be stated explicitly.

**Required**: Either (a) label home ≠ endpoint as a formal precondition with justification, or (b) remove the "distinct from" claim and add one sentence confirming that home = endpoint is valid because the read (text subspace) and write (link subspace) do not interfere.

## OUT_OF_SCOPE

### Topic 1: Ghost address / content address collision
AP2 guarantees freshness relative to `dom.ispace`, but ghost addresses (document identities, account positions) are outside `dom.ispace`. No formal property prevents a content allocation from landing on a ghost address. The structural hierarchy (ghost addresses are prefixes; content addresses are deeper leaves) presumably prevents collision, but this non-collision property is not stated. The ASN acknowledges this gap: AP4a is "not a formal invariant over Σ" and the formal model extension is deferred.

**Why out of scope**: Formalizing the allocation tree (the `alloc : Range → Entity` mapping mentioned in the AP4a discussion) is new machinery, not an error in the existing analysis.

### Topic 2: Spanindex forward correspondence maintenance
The ASN states the forward correspondence `(A d, a : (E p : vspace(d).p = a) ⟹ (a, d) ∈ spanindex)` as the "intended design property" but explicitly defers verification: "We do not verify this invariant here." Verification requires specifying which operations must write spanindex entries.

**Why out of scope**: The maintenance obligation is a separate concern from the permanence of existing records (AP11). The ASN correctly separates them.

### Topic 3: Link discovery mechanism
The ASN notes that AP13 "does not establish the discoverability of the link through the target document" and that "a link-discovery mechanism... is needed but is not defined in this ASN." This is listed as an open question.

**Why out of scope**: Link discovery requires indexing infrastructure (I-address → link mapping) that is architecturally distinct from the permanence properties.

VERDICT: REVISE
