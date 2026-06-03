# Review of ASN-0069

## REVISE

### Issue 1: Dependency Audit's justification for the V2 re-derivation is factually wrong

**ASN-0069, §"Dependency Audit"**: "The one local re-derivation — `d_src ≼ d_new` in the structural-ancestry argument, which J4 (ASN-0047) also supplies directly — is retained only because its length-identity by-product feeds V11a."

**Problem**: V11a does not consume the structural-ancestry section's length by-product. V11a's own derivation re-derives the length identity from scratch: "(i) *Length identity.* `#dⁱ_new = #d_src + i` ... *Step*: ... by V1 `dⁱ⁺¹_new = inc(dⁱ_new, 1)`; TA5(d) at `k = 1` gives `#dⁱ⁺¹_new = #dⁱ_new + 1`." Moreover, the scenarios differ: V11a's chain steps are all *first* forks (`k = 1`, length `#d_src + i`), while the structural-ancestry section's nested length induction concerns the *subsequent-fork* (`k = 0`) case yielding length `#d_src + 1` — a value V11a never references. So the stated reason for retaining a re-derivation of something J4 supplies directly is inaccurate, and the re-derivation is redundant.

**Required**: Either source `d_src ≼ d_new` from J4 (ASN-0047) directly and delete the structural-ancestry re-derivation (V11a is self-contained on length), or correct the Dependency Audit to state the re-derivation's actual purpose. The current justification is a use-site inventory that misnames its consumer.

### Issue 2: V8b is near-tautological and padded with out-of-scope speculation

**ASN-0069, §"Structural Correspondence", V8b**: "Any subsequent loss of correspondence at a position of `F` requires an edit or deletion to one side — both out of scope for this ASN — so within the fork transition vocabulary `F` remains the full witness set; the V8 correspondence is total over `F` and is bounded above by `F` for definitional reasons (`Corr_g` restricted to fork-time positions cannot exceed the fork-time set)."

**Problem**: V8b defines `F := V_{s_C}(d_op)|_{Σ'}` — the fork-time witness set — and then claims V8 correspondence is "total over `F`" (this is just V8 restated) and "bounded above by `F` for definitional reasons" (trivially true: a set restricted to itself cannot exceed itself). The remaining content reasons about subsequent edits/deletions that the ASN explicitly excludes — reviser drift imagining cases the fork transition vocabulary does not contain. V8b adds nothing over V8.

**Required**: Delete V8b, or replace it with a non-tautological claim that advances reasoning beyond V8. If the intent is "fork-time is the maximal correspondence," state that as a consequence without the out-of-scope edit narrative.

### Issue 3: V11 "Anchoring at Σ" speculates about out-of-scope edits to `d_src`

**ASN-0069, §"Composability", V11 "Anchoring at Σ"**: "Modifications M-targeted at `d_src` between fork steps are admissible (they change `d_src`'s current arrangement without altering its `Σ`-state values, which is what V11's conclusion references)."

**Problem**: This sentence imagines arrangement edits to `d_src` (an editing operation, out of scope) to justify the choice of anchoring point. The anchoring decision is adequately motivated by the preceding sentence (the premise scopes preservation to immediate sources, leaving `d_src` unconstrained after step 1). The parenthetical's appeal to out-of-scope modifications is meta-prose that does not advance the proof.

**Required**: Remove the speculative sentence; the anchoring rationale stands without invoking out-of-scope edit operations.

## OUT_OF_SCOPE

### Topic 1: Snapshot vs. living fork, version-space coherence, fork discoverability
**Why out of scope**: The Open Questions correctly defer these to future ASNs. They concern operations and structures (editing propagation, version DAG presentation, descendant enumeration) beyond CREATENEWVERSION's state-transition contract.

VERDICT: REVISE
