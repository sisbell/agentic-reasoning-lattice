# Review of ASN-0100

## REVISE

### Issue 1: S8★ manual run construction is redundant with the C1a appeal and mis-framed as the discharge

**ASN-0100, §Per-subspace span decomposition (S8★)**: "We discharge this collapse through the M7 merge condition (ASN-0058)... Both adjacencies holding, the n Insertion blocks merge into a single length-n block (p, a_0, n)... The Left and Shifted-right portions are derived from the pre-state decomposition as follows. A pre-state block (v', a', m') whose V-extent straddles p... is first split at the interior offset c..." followed by "This discharges S8★ conditions (a)... and (b)..., together with existence via C1a."

**Problem**: S8★ requires only the *existence* of a decomposition satisfying conditions (a)–(c). The preceding `INS.C1a-app` appeal already delivers the unique maximally-merged decomposition, whose blocks are maximal runs (M12b) and therefore satisfy lockstep (a) and label well-definedness (b) inherently. The M4-split / M7-merge derivation re-derives a decomposition the C1a appeal already settles, and its only genuinely *additional* content — the *shape* claim that the Insertion region is a single width-n run (which needs INS.chain-shift) — is information beyond what S8★ demands. As written, the construction is presented as the discharge of (a),(b) when C1a alone discharges them; the reader must work through a redundant abstract re-derivation to reach a conclusion already in hand.

**Required**: Discharge S8★ via the C1a appeal directly (it gives existence, uniqueness, and conditions (a)–(c)). If the single-run shape of the Insertion region is worth recording, reframe the M7/INS.chain-shift material as an explicit *supplementary characterization* of the canonical decomposition's shape, not as the discharge of S8★.

### Issue 2: API-level essay content in the append discussion

**ASN-0100, §The Operation's Inputs**: "The *append* operation Nelson lists as a separate convenience (APPEND) is the j = N case of INSERT — distinct in name only (a caller need not know N if a separate API offers append directly), identical in semantic effect."

**Problem**: The parenthetical "(a caller need not know N if a separate API offers append directly)" is API-surface commentary, not part of the abstract claim that append is the j = N case. It explains an implementation/caller convenience that the spec does not constrain.

**Required**: Drop the parenthetical; the surrounding sentence ("the j = N case... identical in semantic effect") makes the point without the API aside.

### Issue 3: Use-site inventory of inherited I3 frames

**ASN-0100, §Effect Three, "Identification with the foundation's post-insertion shift"**: "The companion frames are inherited likewise: I3-L (PostInsertionLeftFrame) gives the Left region (v < p preserved), I3-X (PostInsertionCrossSubspaceFrame) the cross-subspace frame, and I3-D (PostInsertionCrossDocumentFrame) the cross-document frame."

**Problem**: This enumerates which I3 frame underwrites which INSERT region — a use-site inventory of the I3 identification's downstream consumers rather than prose advancing the identification itself. The frame conditions are independently stated and proved in §The Operation: Formal Contract and re-discharged per-step in §Atomicity, so the inventory adds a third bookkeeping pass.

**Required**: Reduce to the substantive identification (INSERT's shift effect = I3 at S = s_C, with the Insertion gap filled rather than vacated) and let the frame discharges stand where they are proved, rather than cataloguing them here.

## OUT_OF_SCOPE

(none — the note stays within INSERT on the content subspace; COPY/DELETE/link-subspace/version material is correctly deferred to Open Questions and §Bounding the Scope.)

VERDICT: REVISE
