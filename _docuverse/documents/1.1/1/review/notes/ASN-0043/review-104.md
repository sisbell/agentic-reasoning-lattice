# Review of ASN-0043

## REVISE

### Issue 1: home(a) well-definedness stated twice in adjacent passages
**ASN-0043, "Definition — home" / "Home and Ownership"**: Definition — home closes with "Every link address meets the precondition: `zeros(a) = 3` by L1, and T4-validity by L1c (LinkAllocatorConformance)." The "Home and Ownership" section then opens: "A link's home document is `home(a)` (Definition — home), well-defined on every link address by L1 (`zeros(a) = 3`) and L1c (T4-validity)."
**Problem**: The second sentence re-establishes exactly what the definition just established — same two premises (L1 for `zeros = 3`, L1c for T4-validity), same conclusion (well-definedness on every link address). This is the "two paragraphs say the same thing in different words" pattern: the precise reader reads the well-definedness justification, then reads it again one paragraph later before any new content arrives.
**Required**: Drop the well-definedness restatement from the "Home and Ownership" opener (the Definition already discharges it). Open the section directly with the ownership content ("The home document determines the link's owner…").

### Issue 2: the L5↔L6 within/across-endset duality is narrated in both L5 and L6
**ASN-0043, L5 / L6**: L5's body already previews the contrast — "By contrast, slot access *across* endsets is positional (L6, SlotDistinction)." L6 then re-narrates the same duality at length — "L6 is the structural dual of L5. L5 forbids any positional accessor *within* an endset — span access reduces to membership… L6 provides one *across* endsets within a link… The two together carve out the structural primitive: at the link level, position matters; within an endset, it does not."
**Problem**: The within-vs-across distinction is the substantive content of L6, but L5 forward-points to it and L6 restates L5's own clause back. The duality is told once in L5's closing sentence and again, more fully, in L6's opening — redundant cross-referencing that the reader must reconcile.
**Required**: State the duality once, in L6 (its natural home). Remove the forward-pointing "By contrast, slot access across endsets is positional (L6)" preview from L5; L5 should state only the within-endset set-semantics, leaving the contrast to L6.

## OUT_OF_SCOPE

### Topic 1: global content-subspace invariant
**Why out of scope**: The content-side disjointness is correctly scoped to the `s_C`-resident slice, and Open Question #1 already defers a global content-subspace constant to a future ASN. The scoping is acknowledged, not erroneous — this is new territory, not a defect here.

VERDICT: REVISE
