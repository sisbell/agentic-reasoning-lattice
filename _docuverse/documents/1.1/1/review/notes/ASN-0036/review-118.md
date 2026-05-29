# Review of ASN-0036

This is a strong, rigorous ASN: weakest-precondition analysis is present (S0, S3), the worked example exercises conjunct (b) of S8 at a non-trivial run (`n=5`, verified at `k=3`), and edge cases (empty subspace, `m=1` necessity, depth-2 vs depth-≥3 contiguity) are handled. The REVISE items below are predominantly forward-reference accretion and restatement, as the `review-mode.anti-bloat` classifier directs.

## REVISE

### Issue 1: S1 says the same thing twice
**ASN-0036, The content store**: "S1 is a corollary of S0, stated separately for emphasis." and later "It is the domain conjunct of S0, restated for emphasis, and it specialises T8..."
**Problem**: Two paragraphs in the same property restate that S1 is the domain conjunct of S0 "for emphasis." The first sentence carries no information the second does not.
**Required**: Drop the first ("stated separately for emphasis") sentence; keep the single post-proof statement that fixes S1's scope against T8.

### Issue 2: S5 previews and forward-references its own proof
**ASN-0036, Sharing**: "Sharing defeats any finite bound in two independent ways: across documents... and within a single document..." followed by "The Proof below discharges both constructions, verifying S0–S3 for each."
**Problem**: The prose narrates the two-construction structure of the proof that immediately follows, and explicitly points forward to it. This is defensive scaffolding, not reasoning — the proof body already states and discharges both constructions.
**Required**: Delete the "two independent ways" preview and the "The Proof below discharges..." pointer. Let the proof speak.

### Issue 3: Definition Depends clauses end with redundant use-site inventories
**ASN-0036, subspace_I and subspace**: "The function depends only on S7b and S7c." / "The function depends only on `#v ≥ 1`."
**Problem**: Each trailing sentence restates the Depends list it sits inside. The Depends enumeration already records exactly what the function consumes; the summary adds nothing.
**Required**: Remove both trailing sentences.

### Issue 4: Text-subspace-only scoping is restated five-plus times
**ASN-0036, Arrangement contiguity**: the intro prose ("the architectural design constraint imposed by this ASN applies only to the text subspace; they are not claimed to hold for the link subspace S=2 or any other subspace. The formal contracts here are written for S=1.") repeats a caveat already encoded by each of D-CTG/D-MIN/D-CTG-depth/D-SEQ binding `S = 1` in their formal statements, and again echoed by "(bound to text subspace `S = 1`)" in every Properties-table row.
**Problem**: The same scoping fact appears in the section preamble, in four formal contracts, and in four table entries. The formal `S = 1` binding is sufficient; the surrounding prose is duplicative.
**Required**: State the text-subspace restriction once (in the section preamble) and let the formal `V_1(d)` binding carry it; drop the per-property and per-table prose echoes.

### Issue 5: S8-depth carries a forward-reference meta-sentence
**ASN-0036, S8-depth discussion**: "The corresponding depth-, prefix-, and subspace-preservation facts for shifts of both V-positions and I-addresses are established by ShiftPreservation and OrdShiftHom below."
**Problem**: This sentence advances no claim of the current section; it only announces that two later results exist. The later results cite their own preconditions where needed.
**Required**: Remove the sentence. Cross-reference at the point of use, not in advance.

### Issue 6: S9 restates its own (non-)content
**ASN-0036, The separation theorem**: "S9 is the directional reading of S0" / "S9 is the formal statement of Nelson's claim" and the table's "named directional reading of S0 (no formal content beyond S0)."
**Problem**: S9 correctly has no formal content beyond S0, but the section repeats this characterization three ways and then appends a four-item essay enumeration of downstream guarantees (link survivability, version reconstruction, transclusion integrity, origin traceability) that S9 itself does not establish.
**Required**: Keep the single corollary statement and the asymmetry observation; trim the guarantee enumeration to a one-line pointer or remove it, since none of it is derived here.

## OUT_OF_SCOPE

### Topic 1: Link-subspace (S=2) contiguity semantics
**Why out of scope**: The ASN correctly defers sparse/tombstone link-subspace contiguity to a future ASN and binds D-CTG/D-MIN/D-SEQ to `S = 1`. No coverage gap to flag — this is properly future territory.

### Topic 2: Per-operation preservation of D-CTG, D-MIN, S2
**Why out of scope**: Whether DELETE/INSERT/COPY/REARRANGE preserve the contiguity invariants is posed as Open Questions and matches the declared OUT OF SCOPE topic (operation-specific frame conditions). Correctly handled.

VERDICT: REVISE
