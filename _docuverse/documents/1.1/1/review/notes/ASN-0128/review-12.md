# Review of ASN-0128

The technical core of this note held up under checking. I verified I0a in both directions (including the recovery-of-coverage claim and the strictness witness), the I1a induction (including the K ~ R retraction-of-retraction case and born-nullified deposits), I6's wp in both directions (the born-nullified-miss necessity argument is correct: a deposit landing inactive cannot disturb the miss hypothesis), DR's discipline derivation (the distinctness-at-Θ / antichain-at-Θ' split is sound, and using the post-state to establish the state-independent tumbler fact ¬(a ≼ f) is legitimate), DR's hit-branch re-establishment of all four guarantees, the BH2 termination bound, BH4's age arithmetic (age ≥ 0 for resident tuples by L-ContiguousPrefix), and the coverage-irredundant-list lemma inside I1. The gate-first/dedup-second order, the validate-where-read asymmetry between I1 and the wrapper, and the sterilization-containment argument in S3 are all coherent. The findings below are accretion findings under the note's `review-mode.anti-bloat` classifier: the reasoning is right, but it is increasingly buried.

## REVISE

### Issue 1: I0 has grown a design-alternatives essay that restates its one point at least four times

**ASN-0128, Idem operational semantics, I0**: "A strictly finer criterion is therefore available — denoted-set equality … We reject it because it would deduplicate by presentation rather than by assertion — the active subset could then hold coverage-equal tuples that no membership test, no `Observe` pattern, and no retraction separates … The authorities draw the line in the same place … I0 restates that division of labor: the store keeps the first-committed decomposition exactly (L12), and sameness is computed over coverage at the surface."

**Problem**: The definition is complete after its first three sentences (criterion, decidability, the one-sentence ground). What follows restates assertion-vs-presentation repeatedly: "sameness for de-duplication is sameness of assertion," "deduplicate by presentation rather than by assertion," "the gate measures *form* … idem measures *content*," "sameness is computed over coverage at the surface." The withdrawal-multiplicity argument and the Gregory/Nelson division-of-labor paragraph each make the same point once more, and the paragraph carries three forward pointers ("the separating pair, I0a" twice, "bounded by the identity below"). A reader checking I1 against I0 must skip most of this block to find the criterion.

**Required**: Keep the criterion, the decidability citation, the one-sentence ground, a two-sentence rejection of denoted-set equality (with I0a as the strictness witness), and one attribution sentence. Cut the restatements and the duplicate forward pointers.

### Issue 2: RP's transfer clauses embed downstream-consumer inventories and document-design meta

**ASN-0128, The registration record, RP**: "Transfer then has three clauses, mirroring ASN-0126's own B1–B3 apparatus; later sections cite them by name." RP-a: "— the gate's verdicts, P4, P6, FrontierUnification, the projection bridge onto ASN-0086 (compose `π` after `ρ`), and the per-state ASN-0086 results ASN-0126's own B2 carries (R0a among them) —". RP-b: "RangeSterilization and the persistence lemmas R6a/R6c (as ASN-0126's B3 carries them) transfer this way, never by RP-a; transition invariants (P3 as a step property, L12/L12a as ASN-0126's B2 carries them) likewise transfer … ASN-0126 keeps exactly this separation — its B2 against its B3, scope restriction included — and RP preserves it."

**Problem**: These are use-site inventories inside a definition. Every later citation already names its route inline ("via ASN-0126's B2 and RP-a", "by RP-b's derivation projection"), so the inventories are redundant with the use sites — and the closing sentence ("ASN-0126 keeps exactly this separation … and RP preserves it") is prose about the document mirroring another document, not a claim about states or steps.

**Required**: State the three transfer clauses as rules (what kind of conclusion transfers, by what mechanism). Delete the lemma inventories and the two mirroring sentences; let use sites carry their own route citations, as they already do.

### Issue 3: the validate-where-read contrast is drawn twice, each side deferring to the other

**ASN-0128, I1 (home validation) and DR (preconditions)**: I1: "Validate-where-read is the implementation's discipline as well: Gregory's back end never validates a request's document argument as an unconditional entry check … (The retraction wrapper, by contrast, checks its P0 uniformly, hits included — DR, Standard registrations.)" DR: "Uniform P0, against I1's branch-local home validation for a general `Emit_K`, is the same validate-where-read principle: the wrapper's from-fill puts `subtree(d_retr)` into its I0 identity, so `d_retr` is read on both branches."

**Problem**: The same contrast in different words in two sections, with a cross-deferral in each direction. I1's parenthetical anticipates a deviation the reader hasn't met yet; DR re-derives the principle I1 already stated.

**Required**: Draw the contrast once, at the wrapper — that is where the deviation needs explaining, and the from-fill argument is the substantive half. I1 keeps the rule and the Gregory evidence and drops the parenthetical.

### Issue 4: the active-view escape hatch and the never-filtered surfaces are stated three times

**ASN-0128, Denotation and views / BH1 / example**: Views: "filtering is undone by asking the active view; nullification is undone by nothing (R6c), only resurfaced in the audit view." BH1: "A caller recovers an unfiltered enumeration by requesting the *active* view; the audit view is a strictly larger escape hatch — it additionally includes nullified tuples — and is not what filtering hides." Example: "The escape hatch is the *active* view, not the audit view: … while the audit view (which additionally resurfaces nullified tuples) is not the lens in play." Likewise "the audit view … is rewritten by nothing" (Views) against "raw `Observe_K` — both its hist (audit) and oper (active) selectors — never filters" (BH1); and the branch-verdict fact appears in both BH2's adoption line ("the verdicts are not decorative: a document carrying two active supersession claims is a branch, `tip = ⊥`") and S2 ("to ⊥ at a branch or a cycle (BH2's verdicts; the ⊥ cases are by design, per BH2's Effect)").

**Problem**: Same facts in different words across sections. The triplicated escape hatch is the clearest case: one definition, one restatement, one re-explanation inside an example that should only demonstrate.

**Required**: Pin each fact once — the view lattice and escape hatches in Denotation and views, the rewrite-scope formula in BH1, the branch verdict in BH2. The example and S2 cite without re-explaining.

### Issue 5: settlement and restoration claims are re-announced across sections

**ASN-0128, header / What this note commits / S3 / DR / I2**: Open Question 7's settlement is announced in the header paragraph ("The standard retraction registration additionally settles ASN-0126's Open Question 7 (sterilization containment) at the operation surface"), again in the commits bullet ("…and settling Open Question 7 — and, on surface-disciplined substrates, restoring the disciplined-domain wp simplification ASN-0126 had to abandon…"), and again opening S3's policy paragraph ("The shipped registration carries an operation-surface policy that settles ASN-0126's Open Question 7"). The wp-simplification restoration is stated in the commits bullet and again at DR's close ("…is restored one layer up as a guarantee of this operation surface"). I2 closes with a third advance copy of DR's result: "the standard retraction registration (Standard registrations) is what keeps substrate-mediated retraction from sterilizing slots in the first place."

**Problem**: Multiple paragraphs in different sections defer to or pre-announce the same downstream result. This is the canonical accretion pattern: each cycle's revision added one more pointer at DR/S3 rather than letting the result live where it is proved.

**Required**: Announce each settlement once, in the commits list. S3 and DR then prove their content without re-announcing it; I2's closing sentence is deleted (its sterilization caveat with the RangeSterilization citation stays — that is load-bearing).

### Issue 6: counterfactuals about cases the committed semantics already excludes

**ASN-0128, BH4 `retract_stale`**: "Were batch admission left to the constituents' own P0 checks alone, with no entry evaluation, an invalid `d_retr` would void the batch only absent interleaving — `K.λ_sh` frames `Σ.M`, but an interleaved K.σ step may allocate `d_retr` mid-batch, after which the remaining constituents are admitted while the earlier ones were rejected — a front-truncated batch, neither voided nor complete, retracting an arbitrary suffix of the stale set. Entry-evaluation forecloses the partial execution…"

**Problem**: The committed contract — P0 evaluated at batch entry, no constituent issued on failure — excludes the front-truncated batch outright; the paragraph then argues at length against a design the note does not adopt. The same paragraph also carries the redundancy "both layers check — and the per-call checks confirm the entry verdict" immediately after stating each layer's check. The same pattern appears in BH4's compatibility paragraph: the parenthetical "(The workaround under `idem = ⊤` — nullify the incumbent … is two calls with a window between them and a retraction tuple burned per renewal; requiring `idem = ⊥` buys one-call renewal instead.)" costs out a configuration R-C0 already fails at construction, and the lead sentence "BH4's row in R-C0 differs in kind from the other three" is framing about the constraint table rather than content of the behavior.

**Required**: `retract_stale` states the committed semantics in three sentences: entry P0 at the stale-set state, nothing issued on failure; per-constituent P0/P-tgt then admitted by domain monotonicity under any interleaving; already-retracted targets handled by the I0 case split (which is substantive — keep it). BH4 keeps the derivation of `idem = ⊥` from what age must measure (that is the constraint's content) and drops the workaround costing and the differs-in-kind framing.

## OUT_OF_SCOPE

### Topic 1: The serializing authority in I4
**Why out of scope**: I4 correctly notes that `→_sh` inherits a sequential interleaved model and posits "a serializing authority orders the two calls before either becomes a step" — but the authority's obligations (atomicity of the dedup-check-then-step pair, ordering guarantees across homes) are unspecified. A concurrent operational semantics is new machinery for a successor, not an error here; I4's per-interleaving analysis is complete on the sequential model it declares.

### Topic 2: Caller-facing error algebra
**Why out of scope**: Rejection is uniformly "no step, no address" (S3 fixes this; Open Question 3 correctly notes the error semantics are not open). Whether callers can distinguish rejection causes — gate failure vs. invalid `d` vs. P-tgt failure — and what the surface operations' full return signatures are is API territory for a successor note, not a gap in the state semantics committed here.

### Topic 3: Cross-home ordinal time
**Why out of scope**: BH4 pins age as home-relative and proves the state holds no cross-home denominator, with single-document homing as the protocol-level workaround. A cross-home ordinal reference (any global-order construction) would be a real state extension, exactly parallel to the substrate clock the note explicitly declines; it belongs to whatever future note takes that on.

VERDICT: REVISE
