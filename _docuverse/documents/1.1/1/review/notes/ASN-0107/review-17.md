# Review of ASN-0107

## REVISE

### Issue 1: A1 conflates the two anchorings under one conditional header
**ASN-0107, A1 (FreshContentNeutrality)**: "leaves the count unchanged *for a request whose parts denote unchanged content*. For the existence count the neutrality is *unconditional* ..."
**Problem**: The claim's lead conditions neutrality on "a request whose parts denote unchanged content," then immediately asserts existence-count neutrality is "unconditional." For existence anchoring `Q` is a fixed permanent address set — there is no "content change" notion for it to be conditioned on — so the qualifier in the header applies only to the discovery reading, yet it is stated as the claim's blanket precondition. A reader cannot tell which anchoring the header governs.
**Required**: Split A1 into its existence half (unconditional, a corollary of E3) and its discovery half (conditioned on the no-incoming-links premise), rather than pinning both under a single conditional sentence whose condition is meaningful for only one of them.

### Issue 2: Reconciliation recap paragraph does not advance reasoning
**ASN-0107, "Two Anchorings"**: "The two anchorings reconcile Nelson's design with the implementation evidence. ... An implementation that resolves the query through a document's mapping realises D1–D2; one that queries fixed addresses realises E1–E4."
**Problem**: This paragraph restates what E1–E4 and D1–D2 already establish and maps each to "an implementation" — a use-site recap, not a step in the argument. It is meta-prose the precise reader must read past.
**Required**: Delete, or compress to the one load-bearing sentence (the anchorings agree exactly when queried content is unedited between readings), which is the only part not already carried by the claims.

### Issue 3: A2 defensive aside imagines a move the definition already excludes
**ASN-0107, A2**: "The maximally-permissive `Q₂ = Q₃ = T` form belongs to *existence* anchoring ... under discovery anchoring every part is resolved through `d_new`'s arrangement ... and is therefore a finite image set, never the whole space `T`. The discovery analogue *widens* the query rather than unconstraining it ..."
**Problem**: Discovery anchoring's `Qᵢ(Σ)` is *by definition* a forward image set; no caller can supply `T` under it. The paragraph rebuts a reader error the resolution definition structurally forecloses — reviser drift that swells A2 to a full paragraph around a one-line distinction (existential discoverability vs conjunctive `sat`).
**Required**: Keep the discoverability-vs-`sat` slot distinction (genuine content); drop the prose that explains why `T` cannot be passed under discovery.

### Issue 4: Reordering necessity/sufficiency stated twice
**ASN-0107, D2 reordering clause** and **"A Worked Instance" reordering paragraph**: both state that setwise-fixity of `Wᵢ` is sufficient but not necessary, the counterexample being a reorder within a shared-image class.
**Problem**: The same necessary/sufficient point is argued abstractly in D2 and then re-argued in the worked example ("Setwise fixity ... would suffice ... but is not necessary — had `v₁` and `v₂` shared a single I-address ..."). Two passages in different sections carrying the same content.
**Required**: Let D2 carry the principle and let the worked example merely *exhibit* a falling count; remove the example's re-derivation of the sufficiency/necessity claim.

### Issue 5: Implementation mechanics in an abstract-guarantee slot
**ASN-0107, P1**: "any enumeration realising `match` must collapse multi-span matches per link, so that the returned integer is the set cardinality and not a multiset tally."
**Problem**: "any enumeration realising `match`" is implementation guidance about how a backend walks its indices. The abstract guarantee is P1 itself (`[sat] ∈ {0,1}`); the enumeration obligation is a derived implementation note, not part of the invariant.
**Required**: Drop the enumeration sentence or move it out of the claim body — the cardinality guarantee already discharges the set-vs-multiset decision abstractly.

## OUT_OF_SCOPE

(none — the note correctly defers retrieval of the matched links to FINDLINKS/ASN-0099 and does not stray into pagination, MAKELINK, FOLLOWLINK, or BEBE.)

VERDICT: REVISE
