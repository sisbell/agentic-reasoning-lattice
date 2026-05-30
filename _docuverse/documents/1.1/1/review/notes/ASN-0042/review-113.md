# Review of ASN-0042

## REVISE

### Issue 1: The O1a/T4/O1b invariance induction is proved twice
**ASN-0042, *The Account-Level Boundary* and *Delegation***: The Account-Level Boundary section gives "O1a is a reachable-state invariant, proved by induction... *Non-delegation step:* O15 admits no new principal and O13 (PrefixImmutability) fixes existing prefixes, so the bound carries unchanged. *Delegation step:* the sole new principal `π'` satisfies `zeros(pfx(π')) ≤ 1` by condition (iii)...". The Delegation section then restates the identical structure: "T4 and O1b are reachable-state invariants proved by the same induction... non-delegation transitions preserve it trivially, since O15 admits no new principal and O13 (PrefixImmutability) fixes existing prefixes".
**Problem**: Two paragraphs in different sections run the same induction skeleton ("O15 admits no new principal, O13 fixes prefixes, condition (iii)/clause of O14 for the base") for the same three invariants. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Prove O1a, O1b, and T4 reachable-state invariance once (they share base case O14 and the same delegation/non-delegation step) and cite that single derivation from both sites.

### Issue 2: O7(c) hedges over future states the postcondition does not quantify over
**ASN-0042, O7 postcondition (c)**: "This discharge rests on `Π_{Σ'} ∖ Π_Σ = {π'}`, which holds only at `Σ'`: at any later prospective delegation state `Σ''` where `π'` has itself sub-delegated some `p''' ≺ p''`, that sub-delegate is the most-specific cover of `p''`, so `π'` no longer satisfies condition (ii) for `p''` there." and "Postcondition (c) thus asserts the *right*... it does not assert an absolute right to an arbitrary strict descendant `p''`, nor a right against subsequent sub-delegations or namespace baptisms by `π'` itself."
**Problem**: Postcondition (c) is scoped to the right available at entry state `Σ'` (and its Formal-Contract restatement already says "at the prospective delegation state"). The paragraph then imagines later states `Σ''`, walks through how the right erodes, and appends a defensive "does not assert" disclaimer. This is reviser drift — narrating cases outside the claim's scope plus a defensive justification in a structural slot.
**Required**: State condition (ii)/(iv)/(v) discharge for `π'`-as-delegator at `Σ'` and stop. The per-state caveat is already carried by condition (v)'s next-reachability requirement; delete the `Σ''` walkthrough and the "does not assert" disclaimer.

### Issue 3: O8 proof appends a case-walk the postcondition excludes
**ASN-0042, O8 proof**: "Note that the proof makes no claim about *who* the effective owner is — only that it is not `π`. The effective owner may be `π'` itself, or it may be a sub-delegate `π''` introduced by `π'` with `pfx(π') ≺ pfx(π'')`. In the latter case, `ω_{Σ'}(a) = π''` for `a ∈ odom(π'')`..."
**Problem**: O8's postcondition is exactly `ω_{Σ'}(a) ≠ π`. The proof body already establishes it via the strict length gap. This trailing paragraph re-litigates who the owner *is* — a question the claim deliberately does not ask — and re-applies the same argument to a hypothetical `π''`. Meta-prose that does not advance the proven negative.
**Required**: Remove; the postcondition and its three-line longest-match argument suffice.

### Issue 4: `pfx` introduction pre-states and forward-references O1b, which then restates it
**ASN-0042, *Ownership as a Structural Predicate***: "The mapping `pfx` is injective — distinct principals have distinct prefixes (formalized as O1b below)." Immediately after the `pfx` Formal Contract: "**O1b (PrefixInjectivity).** `(A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`".
**Problem**: The injectivity fact is asserted in prose, forward-pointed to O1b, and then O1b restates it verbatim within a few lines. The properties table further notes "injectivity O1b... are derived invariants, not part of this axiom." Three touches of one fact.
**Required**: Drop the prose assertion and the "(formalized as O1b below)" pointer; let O1b carry it. (Note also that O1b is presented here as a flat statement but the table and Delegation section treat it as a *derived reachable-state invariant* — pick one framing.)

### Issue 5: `ω_Σ(a)` definition prose forward-points instead of advancing the definition
**ASN-0042, `ω_Σ(a)` (EffectiveOwner)**: "This is a partial definition until we show that the right-hand side picks out exactly one principal in every reachable state. That is the content of O2."
**Problem**: A definition's body ending in "that is the content of [downstream claim]" is a pointer, not definitional content. The well-definedness is precisely what O2 proves on the next lines; the sentence only announces it.
**Required**: Delete the two sentences; the partiality is evident from `ω_Σ : Σ.B → Π_Σ` and O2 follows immediately.

### Issue 6: Field-decomposition reasoning re-derived inline in O9 (and elsewhere)
**ASN-0042, O9 proof, Case 2**: "By T4b (UniqueParse), T4a (SyntacticEquivalence), and T4's positive-component constraint, the prefix has the form `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ`... the first zero of `a` is at position `α + 1`. Hence `N(a) = [a₁, ..., aₐ] = ..."
**Problem**: FieldStructure (in *The Account-Level Boundary*) already establishes uniquely where node/user separators fall and that segments are non-empty; AccountPrefix re-walks it; O6's forward direction re-walks it; O9 Case 2 walks it a fourth time. The repeated "first zero at position α+1, so N(a)=..." derivation is the same mechanical scan each time.
**Required**: Cite FieldStructure for the separator-position/field-extraction facts and apply them, rather than reconstructing the zero-scan inside each ownership proof.

## OUT_OF_SCOPE

### Topic 1: Divergence of structural provenance (O6) from effective ownership (O2) under transfer
The corollary `pfx(ω(a)) ≼ acct(a)` notes provenance and authority "coincide... under the system as specified." If transfer is later admitted they diverge. This is correctly deferred to the first Open Question; no action needed in this ASN.

META: not applicable — the note defines ownership state (`Π`, `pfx`, `Σ.B`-coupling), operations on it (delegation, fork), and reachable-state invariants (O1a–O18) at the abstract level any conforming implementation must satisfy; it has not drifted into implementation mechanics despite heavy Gregory corroboration.

VERDICT: REVISE
