# Review of ASN-0100

## REVISE

### Issue 1: I3-coincide transfer/non-transfer bookkeeping has accreted into meta-prose with duplicated forward references
**ASN-0100, §Effect Three ("Identification with the foundation's post-insertion shift")**: "I3's preconditions (...) are met by INS.pre, so invoking I3 and inheriting its per-state lemmas is licensed... The transfer does not extend to I3's content-frame-dependent lemmas: ... The lemmas resting on I3-C — I3-S7 ... and the inherited proof premise of I3-S3 — therefore do not transfer; INSERT re-derives S3 (§Referential integrity) and S7 (§Post-state V-position well-formedness) independently against the grown content store."
**Problem**: This passage is largely transfer-bookkeeping: a defensive justification that the invocation "is licensed," plus an inventory of which foundation lemmas do/don't transfer, with forward pointers to two downstream sections. The same non-inheritance point is then restated at each pointer site (§Referential integrity: "not by inheriting I3-S3, whose proof premise rests on the content frame I3-C that INSERT violates; §Effect Three"; §Post-state V-position well-formedness: "inherited I3-VP ... inherited I3-VD ... inherited I3-fin"). Multiple paragraphs in different sections defer to and restate the same fact. This is the forward-reference accretion the anti-bloat classifier targets — the load-bearing content (Left ∪ Shifted-right coincide pointwise with M_{I3}; S3/S7 re-derived) survives a single sentence; the catalogue and the "is licensed" framing do not advance the proof.
**Required**: Collapse the non-transfer inventory to one sentence at the point of use (S3/S7 are re-derived, not inherited, because INSERT grows `dom(C)`), and remove the duplicate restatements at the downstream sites.

### Issue 2: Cross-document link-projection invariance is stated twice
**ASN-0100, §Cross-document independence**: "Cross-document independence extends to link projection: for any link `ℓ ∈ dom(L)` and any document `d' ≠ d`, `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)` — the projection of any link into `d'` depends only on `M(d')` and on `ℓ`'s coverage, both unchanged here."
**Problem**: This is the same claim, with the same justification, that INS.proj later derives rigorously for the `d' ≠ d` case ("π is the identity and N = ∅ ... LP4 ... composing across the finite step sequence ... yields `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`"). Two paragraphs say the same thing in different words; the earlier one is a preview that adds nothing the formal derivation lacks.
**Required**: Drop the preview in §Cross-document independence (or reduce to a cross-reference to INS.proj), keeping the single derivation.

### Issue 3: Forward-deferral inventory in the atomicity argument
**ASN-0100, §Atomicity and Canonical Order**: "The component-frame argument leaves three genuinely intermediate-specific obligations, discharged below: S4 at each K.α intermediate, L0's content conjunct per fresh address, and P6/P7 at the K.α/K.ρ commits."
**Problem**: This sentence is a "discharged below" use-site inventory — it names obligations only to point forward to where they are handled in the same section, without advancing the argument. The reader still has to read those discharges; the inventory is navigational meta-prose.
**Required**: Remove the inventory sentence; each obligation is already discharged in its own bullet immediately following.

## OUT_OF_SCOPE

### Topic 1: Insertion into the link subspace, COPY, DELETE/REARRANGE, version derivation, replication
**Why out of scope**: The ASN correctly bounds itself to content-subspace INSERT and lists these explicitly in §Bounding the Scope; they belong to other operation ASNs.

The mathematical core is sound: boundary cases (prepend/`j=0` forced clearance, append/`j=N`, empty document, cleared-subspace re-insertion, deep `m_C=3` off-prefix exclusion) are each verified against a concrete example; S2/S3★/D-CTG★/D-MIN★/D-SEQ★/S8★ are discharged per region with the I3 content-frame violation correctly handled by independent re-derivation; the wp analysis treats two non-trivial postconditions. The findings are accreted meta-prose around forward references, not correctness gaps.

VERDICT: REVISE
