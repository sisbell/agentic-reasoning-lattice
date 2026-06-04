# Review of ASN-0100

This is an unusually thorough note; the invariant coverage in §Verifying the Invariants is close to exhaustive and the worked-example projection trace checks out. My findings are concentrated in two areas: one conceptual issue with how composite atomicity is framed, and several instances of the forward-reference / meta-prose accretion this note is flagged for.

## REVISE

### Issue 1: Composite atomicity is framed as an environmental precondition, but ValidComposite★ already supplies it — the residue is implementation mechanics

**ASN-0100, §The Operation: Formal Contract → Environmental Assumptions**: "No elementary transition of any other composite interleaves between INSERT's elementaries that touches the resources INSERT depends on. … single-threaded serialisation, per-document locking restricted to d's text-subspace arrangement and content sub-allocator chain A_C(d), or any other mechanism preventing inter-composite elementary interleaving…"

**Problem**: ValidComposite★ (ASN-0047) defines a valid composite as a *contiguous* finite transition sequence `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'`. At the abstract level the transitions are totally ordered and a composite's steps are contiguous, so no foreign transition interleaves between INSERT's elementaries — "composite-level atomicity" is definitional, not an extra environmental property the substrate must supply. The determinacy of Σ' from the pre-state therefore follows from INSERT *being* a valid composite. The K.α side-effect dependency the ASN worries about (the chain index `m_d` advancing mid-composite) cannot arise within a single valid composite. What remains is genuinely an *implementation* concern (multiple threads realizing the sequential model), and the enumeration of locking strategies is implementation mechanics below this ASN's abstraction level. The system guarantee is "INSERT is a valid composite, hence Σ' is determined"; concurrency control is an out-of-scope implementation obligation.

**Required**: Replace the extended Environmental Assumptions treatment (and the matching INS.atomicity prose and Open-Question Q1 framing) with a brief statement that INSERT's steps form a contiguous valid composite, so Σ' is determined by the contract; note in one sentence that an implementation must realize the sequential model, without enumerating lock strategies.

### Issue 2: I3-* lemmas cited as "discharged also by" are imprecise and redundant with the ASN's own re-derivations

**ASN-0100, §Arrangement functionality / §Referential integrity / §Post-state V-position well-formedness**: e.g. "discharged also by I3-S3 (ASN-0082)", "I3-S2 (PostInsertionFunctionality; ASN-0082) discharges functionality on the regions it covers", "cf. I3-VP", "cf. I3-VD", "cf. I3-fin".

**Problem**: ASN-0082's I3-VP/I3-VD/I3-fin/I3-S2/I3-S3 quantify over *all* of `dom(M'(d))` for ASN-0082's shift-only post-state, whose range and content store differ from INSERT's M'(d) (INSERT adds Insertion positions and extends dom(C)). The note itself flags that the whole-post-state frames I3-C and I3-S7 fail here. I3-S3's shift-only justification reaches `ran(M'(d)) ⊆ dom(C')` via `dom(C') = dom(C)` (I3-C) — exactly the frame that fails. The ASN re-derives S2, S3★, S8a, S8-depth, S8-fin itself (correctly, using P0's `dom(C) ⊆ dom(C')`), making the "discharged also by I3-X" citations both imprecise (they require silently reinterpreting the lemma's quantifier domain to "the regions it covers") and redundant.

**Required**: Either drop the I3-* discharge citations and rely on the in-section re-derivations, or state explicitly that only the shift-image clause of I3 transfers and that the cited I3-* invariant lemmas are re-derived here because their ASN-0082 justifications depend on the failing shift-only frame.

### Issue 3: Use-site inventory embedded in the S8a derivation

**ASN-0100, §Post-state V-position well-formedness (S8a bullet)**: "This `shift(p, k)` argument is independent of whether the Left and Shifted-right regions are non-empty, so it serves as the single derivation of Insertion-region S8a that the empty-case walkthrough and the §Atomicity step-3 verification both invoke."

**Problem**: This sentence advances no reasoning about S8a; it enumerates downstream consumers of the derivation — a flagged accretion pattern. The derivation stands on its own; the bookkeeping is noise the reader must skip.

**Required**: Delete the sentence. If the empty-case and §Atomicity passages need the result, they cite it without the source needing to announce its consumers.

### Issue 4: Multiple sections defer to the same "I3 scope note"

**ASN-0100, §Effect Three and §Post-state V-position well-formedness**: the standalone "Scope of ASN-0082's I3 against INSERT's post-state" paragraph, plus repeated back-pointers "cf. the I3 scope note above" and "per the I3 scope note above" appearing in the S7/I3-S7 discussion and elsewhere.

**Problem**: Several sections defer to one downstream/upstream location to explain which I3 frames fail — a flagged "multiple paragraphs defer to the same location" pattern. With Issue 2 resolved (re-derive, don't cite), most of this scope-management prose becomes unnecessary.

**Required**: Fold the single load-bearing fact (only I3's shift clause transfers; I3-C/I3-S7 fail) into the one place it is used and remove the repeated deferrals.

### Issue 5: The m_C depth-fixing explanation is repeated four times

**ASN-0100**: the "first insertion fixes m_C = m … S8-depth is a per-state invariant under ValidComposite★" content appears in §The Operation's Inputs, in §Sequential text-subspace structure (empty case), in the empty-document worked example, and in the INS.inv.depth claim row.

**Problem**: The same fact, reworded across four locations — a flagged "two paragraphs say the same thing in different words" pattern, here multiplied.

**Required**: State the depth-fixing behaviour once (the precondition section is the natural home) and reference it elsewhere without re-explaining.

### Issue 6: The first K.α "forced ordering" bullet is essay-length rationale in a structural slot

**ASN-0100, §Atomicity and Canonical Order** (first K.α-induced forced-ordering bullet): a full paragraph re-explaining via "side-effect dependency through dom(C)," including a counterfactual ("Were the firings reordered…").

**Problem**: The operative point — K.α's subsequent-emission predicate consults dom(C), so the (k+1)-th firing depends on the k-th firing's commit — is one sentence. The surrounding counterfactual and re-explanation is rationale essay content padding a structural list item.

**Required**: Reduce to the single dependency statement; drop the counterfactual and the "not from definitional precedence" digression.

## OUT_OF_SCOPE

### Topic 1: Minimum substrate machinery for composite atomicity (Open Question Q1)
**Why out of scope**: This is a real future question, but as noted in Issue 1 the abstract guarantee is already supplied by ValidComposite★; the locking-machinery question is an implementation-substrate concern for a different note, not a gap in this ASN's abstract contract.

### Topic 2: Link-subspace insertion, COPY, version derivation
**Why out of scope**: Correctly bounded by §Bounding the Scope. The §INSERT vs. COPY corollaries and INS.identity.version stay within INSERT's own allocation/identity behaviour and do not specify COPY or version mechanics, so they are in-scope framings rather than drift.

VERDICT: REVISE
