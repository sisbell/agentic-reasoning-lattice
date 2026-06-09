# Review of ASN-0116

I checked the operation decomposition, the I3-family citations, the composite-validity argument, the invariant discharges, and the worked example. The arrangement reasoning is genuinely careful: the gapped-arrangement-plus-block-fill construction, the block-disjointness attribution (which positions are withheld by I3-V vs. I3-CS), the K.μ⁻/K.μ⁺ realization of the shift, and the RAN range identity all check out. The cross-ASN citations are all to foundation ASNs (no standard-7 violation), and no out-of-scope operation claims are defined. I found one substantive gap.

## REVISE

### Issue 1: PROV (the provenance coupling) is never verified against the concrete scenario
**ASN-0116, "A worked insertion"**: The worked example ("Insert `XY` (`n = 2`) at `p = q_3`") traces I-ALLOC, IP0, I-SHIFT, I-LEFT, I-NEW, IP1, I-DOM, IP4, IP5, IP6, and the three boundary cases — but never traces `R'` and never checks J0, J1★, or J1'★ against the scenario. The reading "yields `a_1, a_2, X, Y, a_3, a_4, a_5`" stops at content; provenance is absent.

**Problem**: PROV (InsertionProvenance) is one of the note's headline claims — the introduction states the operation "carries an obligation to grow `R` in lockstep with allocation," and PROV discharges the mandatory coupling constraints. Review standard 6 requires key postconditions to be verified against a specific scenario. The *most* subtle part of PROV is exactly the asymmetry J1'★ enforces: INSERT must record `A_new = {[d.0.s_C.7], [d.0.s_C.8]}` but must **not** record the range-old shifted-suffix addresses `a_3, a_4, a_5`, even though those addresses now sit at *new* V-positions `q_5, q_6, q_7`. A position-based reader's natural error is to record them. This non-obvious behavior is precisely what a concrete example must pin down, and it is the one place the example is silent.

**Required**: Extend the `XY`-at-`q_3` example to exhibit `R' = R ∪ {([d.0.s_C.7], d), ([d.0.s_C.8], d)}` and check (i) J0 — both fresh addresses appear in `M'(d)` at `q_3, q_4`; (ii) J1★ — the range-new addresses `A_new` carry records; (iii) J1'★ — `a_3, a_4, a_5`, range-old despite occupying new slots `q_5, q_6, q_7`, get **no** new record. A line confirming P7a at the post-state for one prior address would also close the loop.

## OUT_OF_SCOPE

### Topic 1: Provenance under transclusion-based placement
The fourth Open Question (content placed by transclusion of an address whose provenance already names a different origin) is correctly deferred — it belongs to the COPY/transclusion reframing (ASN-0118), not to native INSERT, where creation and placement coincide.

VERDICT: REVISE
