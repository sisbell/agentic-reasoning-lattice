# Review of ASN-0086

## REVISE

### Issue 1: Nullify scope covers subtree, not single tuple
**ASN-0086, Definition — Nullify**: "Nullify(Σ, a) ≡ Emit_R(Σ, ∅, {(a, δ(1, #a))})"

**Problem**: By PrefixSpanCoverage, coverage of the to-span is `{t : a ≼ t}` — the entire subtree of a. The definition of `nullified(Σ)` then includes every `A_rel^Σ` address with a as prefix, not just a itself. L1c permits link addresses that are proper prefix-extensions of other link addresses (spawn-under-link via `inc(a, 1)` is T10a-conforming, preserves T4, gives a child link with `zeros = 3`, `#E ≥ 3`, `subspace_I = s_L`). The substrate-permitted scenario `a, a.x ∈ dom(Σ.L)` makes `Nullify(a)` retract both. The text describes Nullify as targeting "a", suggesting single-tuple intent.

More generally, `Emit_R` accepts arbitrary to-spans, so users can craft retractions with arbitrary scope — e.g., `Emit_R(Σ, ∅, {(d, δ(1, #d))})` would retract every link with home = d, since `nullified` filters to `A_rel` and link addresses have d as prefix.

**Required**: Either (a) prove that Emit_K-only emission discipline produces a "flat" `dom(Σ.L)` with no prefix-nesting among link addresses (the R0 construction does produce flat layouts, but the ASN doesn't establish this as an invariant), or (b) adjust Nullify's span to truly isolate a (which is impossible via TumblerAdd — see below), or (c) explicitly document the subtree/scope semantics and acknowledge that Nullify is a subtree retraction, not a single-tuple one. Note that no span via TumblerAdd can isolate a single tumbler (since `a.0` cannot be reached from a via `⊕`), so option (b) requires a different primitive than spans-as-defined.

### Issue 2: R0 chain-witness vs. substrate-emission gap
**ASN-0086, R0 proof Step 2 Case A**: "(ii) Sibling sweep inc(·, 0) within A_d, advancing from A_d's base d.0.1... to d.0.s_L... applied s_L − 1 times..."

**Problem**: The proof treats the L1c chain as a conformance witness ("L1c asserts the existence of a conforming chain to a, not the re-issuance of every spawn that chain traverses"), implying the substrate can transition directly to Σ' depositing only at a. But neither ASN-0043 nor ASN-0086 specifies the substrate's emission primitive. If the primitive is "advance allocator + emit at frontier" (the natural T10a interpretation), then Case A's chain requires emitting at each intermediate address. Sub-case "if A_d has not yet emitted any address under Σ" creates A_d via spawn (d, 2), depositing at d.0.1 (subspace s_C); the sibling sweep through positions 1..s_L − 1 deposits at additional content-subspace addresses. These would side-effect Σ.C, contradicting Emit_K's stated frame `Σ'.C = Σ.C`.

If allocation is decoupled from deposit (so addresses can be "spawned but unfilled"), this should be made explicit and the persistence guarantees of unfilled addresses argued. If they are coupled, R0's construction needs intermediate-emission accounting.

**Required**: Specify the substrate's emission primitive — either by axiom (e.g., "the substrate admits emit-at-arbitrary-L1c-conforming-address as a primitive") or by reconciling R0's chain with whatever primitive ASN-0043 implicitly assumes. Without this, R0 stands on an unstated substrate assumption.

### Issue 3: Emit_K frame condition asserted, not derived
**ASN-0086, Definition — Emit_K**: "All other components of Σ are held in frame: Σ'.C = Σ.C and Σ'.M = Σ.M."

**Problem**: The frame is asserted as part of the operation's definition but not derived from R0. R0's proof Step 4 says "Σ.C and Σ.M unchanged" but doesn't justify — the justification depends on resolution of Issue 2. If Case A side-effects content emissions, Σ'.C ≠ Σ.C, and the asserted frame is false.

**Required**: Once Issue 2 is resolved, derive the frame conditions explicitly. Alternatively, state Emit_K's frame as a definitional commitment of the substrate (independent of R0's proof) — but then R0's role is to show such a transition exists in →, not to construct it via T10a chains.

### Issue 4: R6b justification conflates with R6a
**ASN-0086, R6b proof**: "Direct from the Definition of nullified(Σ): the existential quantifier ranges over L_R^Σ, not A_R^Σ. We do not iterate; once retracted, always retracted."

**Problem**: "Once retracted, always retracted" states R6a (temporal persistence across state transitions), not R6b (logical non-iteration within a single state). R6b's content is distinct: even if the retracting tuple b is itself nullified by some later c ∈ L_R, the predicate at a only checks `b ∈ L_R`, not `b ∈ A_R`, so a remains nullified. This is a consequence of how nullified is defined (over L_R, not A_R) — the persistence claim is separately given by R6a.

**Required**: Reframe the justification to focus on logical depth. A concrete illustration would help: emit b nullifying a, then emit c targeting b; show that even though `b ∈ nullified(Σ')`, a is still nullified because the predicate evaluates `b ∈ L_R^Σ`, which is true and persistent regardless of b's own active-subset status.

### Issue 5: R0 dependency table incomplete
**ASN-0086, Properties Introduced table**: "R0 | LEMMA | TupleAddressFreshness — ...(= L1 + L1a + L1b + L1c + L3 + L0 + L-fin from ASN-0043; T0(a) + T0(b) + T10a axiom + T10a.6 + T10a.7 from ASN-0034; S7d from ASN-0036)"

**Problem**: The proof additionally invokes T10a.2 (in the worked example), T10a.4 (T4 preservation under discipline, used for T4-validity of a), T10a.8 (uniform sibling zero count, in Case B), TA5 (inc rules, throughout), TA5a (T4 preservation through inc, in Case A and B), S3 (ASN-0036, in the L14a check), and the Setup hypothesis. The dependency table understates the proof's footprint.

**Required**: Complete the dependency listing.

### Issue 6: R7 framing implicitly excludes Observe
**ASN-0086, R6c consequences (d) and R7**: "All visible relational-layer operations reduce to `Emit_K`."

**Problem**: Observe is a relational-layer operation but doesn't reduce to Emit_K — it leaves Σ unchanged. The claim is true only for state-transforming operations.

**Required**: Rephrase as "all visible *state-transforming* relational-layer operations reduce to Emit_K." R7's own statement gets this right; the framing in the surrounding prose (and R6c consequence (d)) doesn't.

### Issue 7: Setup hypothesis usage not consistently annotated
**ASN-0086, Setup hypothesis**: "We additionally assume globally `s_C`-resident content."

**Problem**: R4's proof explicitly invokes Setup. R0 Step 4's L14a verification implicitly uses it ("by the setup hypothesis, every such address is s_C-resident"). Other claims may also depend on it (e.g., the construction's freshness argument in Case A relies on subspace separation, which depends on `s_C ≠ s_L` plus s_C-residence). The note should distinguish global properties (under Setup) from sliced properties (which would hold without Setup, scoped to dom(Σ.C)|_{s_C}).

**Required**: Annotate each R-claim and operation with whether it requires the global Setup hypothesis or works under L14's native scoped form. The "Open Questions" hint at this with "future work admits s_L-resident content" but doesn't trace the implications through R0–R7.

### Issue 8: L14a verification in R0 Step 4 has implicit prior-state reliance
**ASN-0086, R0 Step 4, L14a check**: "Therefore dom(Σ'.L) ∩ ran(Σ'.M) = (dom(Σ.L) ∪ {a}) ∩ ran(Σ.M) = ∅, preserving L14a."

**Problem**: The argument shows `{a} ∩ ran(Σ.M) = ∅` by subspace separation. The reduction to `(dom(Σ.L) ∪ {a}) ∩ ran(Σ.M) = ∅` requires `dom(Σ.L) ∩ ran(Σ.M) = ∅`, which is L14a *at the prior state*. This prior-state reliance should be stated explicitly (it's a preservation lemma, not a fresh derivation).

**Required**: State that the disjointness for `dom(Σ.L)` is inherited from L14a at Σ, and the proof's contribution is the disjointness for `{a}`.

## OUT_OF_SCOPE

### Topic 1: Document-parameterized emission
**Why out of scope**: Emit_K doesn't accept a document parameter; the user gets whichever document the substrate's implementation picks. The ASN is at the abstract substrate layer; document-targeting is an implementation concern.

### Topic 2: Higher-arity active-subset semantics
**Why out of scope**: Explicitly punted to open questions; the standard-triple restriction is stated up front.

### Topic 3: Multi-document worked example
**Why out of scope**: The single-document example exercises R3, R6a, R6c. Multi-document scenarios would test cross-document references but aren't needed to verify the introduced properties.

### Topic 4: Concurrency / atomicity of Emit and Observe
**Why out of scope**: Already in open questions.

VERDICT: REVISE
