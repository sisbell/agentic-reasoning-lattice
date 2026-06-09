# Review of ASN-0126

## REVISE

### Issue 1: The reachable-state conformance guarantee is asserted but absent from the property list

**ASN-0126, Single-source**: "induction over `→_sh`-steps gives that within such a substrate `dom(Σ.L)` carries only conforming tuples and there is no off-gate path into the link store."

**Problem**: This state-level invariant — *every tuple stored at any reachable state conforms to its registered shape* — is the guarantee an app actually relies on, yet it is stated only in passing prose. The formal property that should carry it, P4, is explicitly single-step and "records the gate's *enablement* half only." No P1–P6 states the closure ("for every `→_sh*`-reachable Σ and every `a ∈ dom(Σ.L)`, `Sh-conf` holds for `Σ.L(a)` under its registered type"). A consumer must reconstruct the induction (P4 + `Σ_init.L = ∅`) themselves.

**Required**: Raise the reachable-state conformance invariant to an explicit property with its (short) inductive derivation, rather than leaving the headline guarantee in narrative.

### Issue 2: The attribution-via-home-document point is stated three times

**ASN-0126, Single-source**:
- "What is *not* lost is attribution: a retraction's responsible party rides on its home document `d_retr`, independent of the from-set, so even `F = ∅` is still an attributed operation."
- "for the case ASN-0086 wrote as `F = ∅`, the canonical fill is the home document's own unit-depth span … a legitimate case-specific use of the slot that designates the party the retraction issues from, not a derivation assertion."
- "what changes is only the from-slot, which moves from the inexpressible `∅` to a one-span attribution — the app's source, or canonically the home document."

**Problem**: Three sentences in one section assert the same fact (attribution rides on `d_retr`, the home-document span is the canonical fill). The reader re-reads the same claim twice to confirm nothing new was added.

**Required**: State the F=∅ → `|F|=1` re-expression and its attribution rationale once.

### Issue 3: "Binary is weaker than unit-depth discipline" is explained twice at length

**ASN-0126, Single-source** ("Binary registration does **not** by itself entail ASN-0086's UnitDepthRetractionDiscipline … `→_sh` does **not** guarantee R-Scope's single-tuple-scope result …") and **The shape-gated emit** ("*Disciplined-domain simplification (conditional).* … a general `→_sh`-reachable state may carry an `L_R` tuple with a non-unit Binary range to-span, so the third conjunct's vacuity cannot be imported there").

**Problem**: Both paragraphs *explain* the same structural fact — a non-unit Binary G escapes unit-depth, so the discipline must be a separate operational commitment. The worked "born nullified" example then *demonstrates* it (legitimately). Having the fact explained twice before the demonstration is redundant.

**Required**: State the fact once (Single-source), reference it where the wp simplification needs it, and let the worked example demonstrate.

### Issue 4: "Domain-discharge ordering" is explained twice

**ASN-0126, The shape-gated emit**: "These are read left-to-right under the **domain-discharge ordering**: (0) and (i) jointly discharge the domain condition for (ii) … arity-3 and registration must both hold before (ii) carries a truth value."

**ASN-0126, wp derivation**: "The conjunction is read left-to-right under the domain-discharge ordering: `K registered` precedes and licenses `Sh-conf`."

**Problem**: The second occurrence re-explains a reading convention already fully established a few paragraphs earlier. A back-reference suffices.

**Required**: Drop the re-explanation; cite the ordering by name only.

### Issue 5: Projection-bridge paragraph carries defensive meta-prose

**ASN-0126, The shape-gated emit**: "All reachability in this note is with respect to `→_sh`, and the projection bridge is what licenses importing those `→`-domain results." and "Under this definition P4 holds *by construction* of `K.λ_sh`, not as a derived property of the unmodified ASN-0086 relation."

**Problem**: These sentences justify the *approach* (why the bridge is allowed, how P4 is obtained) rather than advancing the bridge's content. The load-bearing claims — `a_emit(π(Σ),d)=a_emit(Σ,d)`, transfer of R0/L-ContiguousPrefix/PrefixSpanCoverage — are already stated. The reader skips past the rationale to reach them.

**Required**: Remove the self-justifying sentences; keep the two concrete consequences.

### Issue 6: "Properties established" re-derives rather than indexes

**ASN-0126, Properties established, P5**: the entry re-argues definedness and state-independence ("Registration status is itself state-independent: by P1 … so K is registered at Σ iff registered at Σ' …") already fully established in *Registry permanence*.

**Problem**: A summary list should point to derivations (as P1–P3 mostly do with "*Derived* (…)"), not restate them. P5's body duplicates the Registry-permanence argument verbatim in substance.

**Required**: Compress P5 (and any similarly expanded entry) to the statement plus a derivation pointer.

### Issue 7: Open-question item 4 contains essay content in a structural slot

**ASN-0126, Open questions, item 4**: "Nelson names no retraction type and treats his standard set as provisional, so by his design R currently falls on the app-defined side while remaining a candidate for standardization-by-convention."

**Problem**: The open-questions list enumerates deferred decisions; this sentence is a historical-rationale aside on Nelson's design, not a question. It is meta-prose lodged in a slot meant for crisp pointers.

**Required**: State the open question (does the substrate ship pre-registered types?) and drop the Nelson exposition or move it to evidence prose.

## OUT_OF_SCOPE

### Topic 1: Idem semantics
The `idem` field is registered and frozen (P3) but no operation reads it; its meaning is correctly deferred (Open questions #1). Not an error here.

### Topic 2: Multi-source (|F|>1) and arity > 3
The note states the |F|=1, N=3 narrowing explicitly and routes broader needs to ASN-0086's ungated `→`. Loosening these belongs to a successor note (Open questions #6).

VERDICT: REVISE
