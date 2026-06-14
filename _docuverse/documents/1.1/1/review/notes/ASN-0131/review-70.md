# Review of ASN-0131

The mathematics here is sound and unusually thorough: RE-ADDR, RE-RET (both directions), RE-CWP, RE-UDIST, and the two-obstruction intersection analysis (RE-UDIST-∩) all check out, the worked instance genuinely exercises every distinctive postcondition, and the e₃ field-agreement disjointness argument is rigorous. The wp (RE-CWP) is non-trivial and correctly derived. My findings are precision and anti-bloat refinements, not correctness gaps — but the note carries the `review-mode.anti-bloat` classifier, and the patterns below are squarely what that asks me to surface.

## REVISE

### Issue 1: The "higher-arity retraction links are immaterial to `nullified`" fact is restated three times, twice in one paragraph

**ASN-0131, "The unit of the answer"** — the standing-assumption paragraph says it once parenthetically:

> "(ASN-0086 does admit *higher-arity* retraction-typed links into `dom(Σ.L)` by ordinary `K.λ`; these never enter `L_R`, and — as we use below — never enter `nullified`.)"

and again three sentences later:

> "...higher-arity retraction-typed links, absent from `L_R`, are immaterial to it."

and a third time in **"Fresh emissions and the addressable population"**:

> "Higher-arity retraction-typed links, admitted to `dom(Σ'.L)` but absent from `L_R`, never bear on it."

(plus an echo in the RE-ADDR claim row: "scoped to the retraction slice `L_R` (all that `nullified` consults)").

**Problem**: This is the "two paragraphs say the same thing in different words" pattern, compressed to two sentences in a single paragraph. The reader must re-parse the same disclaimer at each occurrence to confirm nothing new is being said.

**Required**: State it once, at the point where it matters (RE-ADDR, where arity-independence is actually used), and delete the within-paragraph duplication in the standing-assumption block.

### Issue 2: Addressability infrastructure is front-loaded into the answer-definition section, declared "throughout," and carries a use-site lemma inventory

**ASN-0131, "The unit of the answer"**: the standing-assumption paragraph and the `Σ.L`-evolution-bridge paragraph land *before* RE-DEF, and the bridge enumerates its downstream consumers:

> "any `∀`-quantified ASN-0086 `→*`-reachable `Σ.L`-lemma — R0a/FlatLinkDomain and R-Scope among them — carries to every ASN-0047-reachable state."

The standing assumption is introduced as adopted "throughout":

> "We adopt throughout, as a **standing assumption**, ASN-0086's *relational-layer discipline commitment*..."

**Problem**: Two issues compound. (a) The dependency is over-scoped: RE-DEF, the touch semantics, RE-SND/RE-CMP, RE-UDIST, RE-UDIST-∩, RE-SEL, RE-TRANS, RE-IDENT, and RE-CWP are all independent of the discipline commitment and the bridge — `nullified(Σ)` is a function of `Σ.L` whether or not retractions go through `Nullify`. Only RE-ADDR, RE-RET, and the fresh-emission case of RE-EDIT consume them. "Throughout" tells the reader the whole note is conditional on a usage discipline, when the core query semantics are unconditional. (b) The bridge is dense reconciliation machinery placed pages before its first use, and the "via the `Σ.L`-evolution bridge" reminders recur at each citation — the enumerated lemma inventory is the "definition's introduction enumerates downstream consumers" pattern.

**Required**: Relocate the standing-assumption + bridge block to RE-ADDR (its first consumer), scope the dependency explicitly to RE-ADDR/RE-RET/fresh-emission-stability, and drop the "R0a/FlatLinkDomain and R-Scope among them" inventory (cite each lemma where used instead).

### Issue 3: `R` is overloaded despite the stated reservation

**ASN-0131, "Fresh emissions and the addressable population"**:

> "writing `Θ` for ASN-0086's designated retraction type, whose own symbol `R` this note reserves for other uses."

**Problem**: The reservation is not honored. `R` still appears in the *retraction* sense throughout — the slice `L_R` (`L_R^Σ`, "the `L_R`-growing step," "the retraction slice `L_R`") and the operation `Emit_R` in RE-RET's `Nullify(Σ, d_retr, ℓ) ≡ Emit_R(...)` — while RE-CWP simultaneously uses `R` for the K.μ⁻ *retention set* ("the retention set `R`", `M(d) ↾ R`). So `R` denotes both retraction-slice content and retained arrangement positions, the very collision the Θ-renaming announced it would avoid. Within RE-RET, the type slot is written `Θ` in `Σ'.L(b) = (∅, {(ℓ, δ(1, #ℓ))}, Θ)` but `Emit_R` two clauses earlier, so one section carries both `Emit_R` (R = retraction type) and `Θ` (= retraction type) for the same object.

**Required**: Either complete the renaming (use `Emit_Θ`, and keep `L_R` only as the inherited ASN-0086 symbol with an explicit note that its subscript is the retraction type `Θ`), or rename the K.μ⁻ retention set to a non-`R` symbol — and either way drop the misleading claim that `R` "is reserved for other uses."

## OUT_OF_SCOPE

The Open Questions correctly defer the genuinely-future topics rather than smuggling them into this ASN: OQ5 (anchoring in a non-co-resident link store) routes to the BEBE/replication layer; OQ3 (rendered V-position answers) and OQ7 (link-subspace regions, `W ⊆ s_L`) are clean future ASNs; OQ6 (type-slot match against content) is carried as a flagged hypothesis, not silently assumed. None of these is an in-this-ASN error mislabeled as future work. The note also correctly cites ASN-0127's image/discovery machinery (F-IMG, F-V, D-CWP, the existence-vs-discovery taxonomy) rather than rebuilding it.

VERDICT: REVISE
