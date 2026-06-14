# Review of ASN-0134

This is a careful, genuinely deep note, and most of its hard machinery holds up under scrutiny. The frontier lemmas (H0–H2) are proved by complete case analysis including the cross-subspace and first-emission boundaries; the G1 confluence argument is the standard adjacent-transposition argument applied correctly; the W3 distinction between *collision* (rejection) and *hole* (never produced) is exactly right; the §7 addresses are arithmetically consistent; and the §8 verdict-soundness banking argument and its two strictness witnesses check out line by line. The two-level step/operation seam (G1 step-level confluence vs. the operation-level order-dependence families) is honestly drawn. The findings below are where the rigor lapses.

## REVISE

### Issue 1: The K.σ registration conflict is assumed away, not eliminated — `register-before-allocate` is named but `register-vs-register` is dropped

**ASN-0134, §4 / §9 MIC / SAFE(c)**: "Its two preconditions — *document-address freshness* (distinct agents propose distinct `d`) and the *register-before-allocate* dependency... are assumed from the entity-allocation layer." → "registration needs no clause of its own — `K.σ` is scoped out of the conflict analysis (§4)." → SAFE(c): "(document registration `K.σ` is scoped out, §4)".

**Problem**: The note commits `𝔼` to "ASN-0093's allocation model carried up through ASN-0086/0126/0128" (§1), whose document-registration step is ASN-0093's `K.σ`, with precondition `d ∉ dom(M) ∧ T4-valid(d) ∧ zeros(d) = 2`. That precondition does **not** give cross-agent address freshness: two agents proposing the *same* fresh `d` against a shared pre-state both satisfy `d ∉ dom(M)`, both pass, the first commits, and the second now finds `d ∈ dom(M)` and is rejected (A1). This is a same-target conflict *structurally isomorphic to H2* — and the note never models it.

The deferral to "the entity-allocation layer" relocates the conflict rather than discharging it. Document addresses are emitted by an account's document sub-allocator (`A_doc` in the foundation vocabulary); two concurrent same-account document creations read one frontier and collide on one address by the *identical* H2 argument. So "distinct agents propose distinct `d`" is not a free hypothesis at any layer — it is a per-home (per-account) serialization obligation, the H2/clause-2 analog one level up.

This has three concrete consequences the note overstates:
1. **H3 and the G1-lift are conditional on an unmet hypothesis.** The lift's confluence enumerates "registration/registration of distinct targets (by H3)" as the only registration/registration transposition. Two *same-target* registrations are not `≺`-incomparable-and-commuting — only one commits — so the lift's confluence holds only *under* freshness, which the substrate does not supply.
2. **MIC is not the "minimal complete" contract it claims.** "registration needs no clause of its own" is false: document allocation needs the same per-home serialization as clause 2. MIC omits it.
3. **The honest classification is a third order-dependence family.** A same-target registration race is, like the §4 target-residence race, an order-dependent *rejection* (consistent, but order-dependent in *which* agent's `K.σ` is realized vs. rejected). The note isolates the target-residence race meticulously but silently drops its registration twin.

**Required**: Either (a) add a registration/document-allocation serialization clause to MIC (the H2 analog at the account/document-sub-allocator level), making `K.σ` an *instance* of the per-home discipline rather than an exemption; or (b) state explicitly that document-address freshness is an **undischarged** hypothesis whose realization requires that same per-home serialization, and that absent it concurrent same-target registrations are an order-dependent rejection like the target-residence race. Do not present registration as conflict-free.

### Issue 2: V2's "weakest sufficient condition" mis-scopes `Q`-affecting steps for a cross-type join — nullifications are omitted

**ASN-0134, §8 (V2 discussion)**: "For a cross-type join the constituents are active-view reads `Observe_{K_i}`, and a type-`K_i` tuple may be homed anywhere, so the excluded steps are *type-scoped* — ranging across all homes carrying `Q`'s types."

**Problem**: This contradicts the note's own definition of `Q`-affecting: "a writer step to be **`Q`-affecting**... when it changes the value of some constituent `c_i` whose read has not yet been taken." For a cross-type quiescence verdict, `c_i = Observe_{K_i}(oper) = A_{K_i} = L_{K_i} ∖ nullified`. A **nullification** — an `Emit_R` deposited at the *retractor's* home `d_retr` — that covers an active `K_i` tuple grows `nullified`, shrinks `A_{K_i}`, and is therefore `Q`-affecting by the stated definition. But `d_retr` need not be "a home carrying `Q`'s types"; it can be any home at all. (The §8 trace's own `Q`-affecting step *is* a nullify — it merely happens to be co-homed with its target there, masking the general case.)

So the characterization "ranging across all homes carrying `Q`'s types" undercounts: a reader who builds the exclusion from it would fail to exclude an unsoundness-causing nullify homed at a non-`Q`-type home, and the supposedly-sufficient condition would not in fact be sufficient. The note presents the middle condition as "the weakest *sufficient* condition this note establishes," so this is not cosmetic — a downstream layer relying on the weaker condition rather than clause 6 inherits the gap. (The clause-6 *conclusion* — the one-index construction is global — is unaffected, since it excludes *all* writer steps and so catches nullifies a fortiori.)

**Required**: State the cross-type join's `Q`-affecting scope as "any step changing some not-yet-read `A_{K_i}` — both `K_i`-emits *and* nullifications (R-emits whose to-coverage hits an active `K_i` tuple), the latter homed at arbitrary retractor homes," rather than "homes carrying `Q`'s types."

### Issue 3: Anti-bloat — meta-prose around A0 and a forward use-site inventory in the intro

**ASN-0134, §1 (A0)**: "Its force is entirely negative and entirely decisive... Every consequence below is a cash-out of A0."
**ASN-0134, intro**: "We ground each guarantee in Nelson's design intent as it arises: that every change leaves the store in *canonical order* with nothing uncanonical in between (A6), that overwrite-free permanent addressing puts monotonicity beyond any schedule's reach (W0), and that an honest verdict is taken against *one cross-section* of the store... (V0)." and "The very corpus this note belongs to was produced by a runner driving many workers against one store."

**Problem**: The A0 sentences describe the claim's *importance and role* ("entirely decisive," "Every consequence below is a cash-out") rather than its content — the actual reasoning is the adjacent "a half-applied step is not a state of `𝔼`, so it is not nameable." The intro sentence is a forward use-site inventory tagging downstream claims `(A6)/(W0)/(V0)` whose Nelson-intent content is restated at those claims; and the "very corpus" sentence is self-referential essay content. These are precisely the patterns the anti-bloat classifier targets — prose the precise reader skips past to reach the claim.

**Required**: Cut the role/importance framing and the use-site tags; keep A0's substantive negative-force reasoning and state each Nelson intent once, where it is used.

## OUT_OF_SCOPE

The note's Open Questions and "What this note does not cover" appropriately defer the cross-server consistency model (OQ6), the optimistic-primitive realizations of clauses 2/6/7 (OQ1–3), batch-reader-atomicity (OQ4), and static sub-allocator partitioning (OQ7). These are correctly future territory; I am not asking for them. (Note that OQ7 weakens clause 2 *downward* and does not cover Issue 1, which is an over-claim in the present text, not missing future coverage.)

META: The note defines a contract (MIC) any faithful implementation must satisfy, stated abstractly and mechanism-free, plus the execution-model guarantees that derive it — this is a consistency/isolation specification, not drifted into implementation mechanics.

VERDICT: REVISE
