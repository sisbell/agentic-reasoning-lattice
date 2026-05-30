# Review of ASN-0042

## REVISE

### Issue 1: Covering-chain lemma carries a use-site inventory instead of advancing the lemma
**ASN-0042, Ownership Domains (after the Covering-chain lemma proof)**: "The lemma admits an immediate specialization: when `p = pfx(π₁)`, `q = pfx(π₂)`, and `x = a` for some `a ∈ Σ.B`, any two principals covering `a` have nested prefixes; the same specialization applies with a principal's prefix `pfx(π')` in place of the address."
**Problem**: This paragraph pre-enumerates downstream instantiations (the principal/principal and principal/address specializations used later in O2 Step 2, O7(a), O8, O10) without advancing the lemma's content. The general statement `(A x, p, q : p ≼ x ∧ q ≼ x ⟹ p ≼ q ∨ q ≼ p)` already covers every use; each call site instantiates it directly and visibly does so. This is the "definition's introduction enumerates downstream consumers" pattern.
**Required**: Delete the specialization paragraph. Let the use sites instantiate the lemma.

### Issue 2: O7(c) proof re-opens conditions it has just discharged
**ASN-0042, O7 postcondition (c) proof**: After establishing "Conditions (i)…(ii)…hold…satisfying condition (ii)", the proof continues: "Condition (ii) requires re-checking at later states `Σ'' ⪰ Σ'`, and condition (vii) (freshness) must be checked at the prospective delegation state in all cases… *Condition (ii):* if `π'` has itself already delegated some `p* ⪯ p''`… *Condition (vii):* if `p''` has already been baptized…"
**Problem**: The Formal Contract for (c) already encodes the conditional cleanly ("satisfiable… at every state at which O15 conditions (ii), (vi), (vii) hold for `p''`"; "(vii)… is *not* asserted at `Σ'` for arbitrary `p''`"). The proof body then imagines two later-state failure scenarios (π' already sub-delegated `p*`; `p''` already a namespace) that pertain to states *after* `Σ'` and are exactly what the conditional phrasing already excludes from the `Σ'`-claim. This is reviser drift — content imagining cases the carrier's own conditional handles.
**Required**: State once, at `Σ'`, that (ii) and (vi) are discharged and (vii) is left as a per-state obligation; drop the imagined `p*`/namespace failure cases (they belong to the conditional wording, not the proof of satisfiability at `Σ'`).

### Issue 3: Trust-boundary claim stated twice in identical force
**ASN-0042, Principal Identity section**: "The binding `session.account = pfx(π)` is an axiom of the session, not a theorem derivable within O1–O10… the ownership properties are independent of which mechanism is chosen."
**ASN-0042, Summary of the Model**: "Principal identity (the binding of a session to a tumbler prefix) is exogenous to this model: the ownership properties O1–O10 hold for any identity-binding mechanism the system chooses."
**Problem**: The same proposition is asserted in full in two sections. The Summary line and the Principal Identity section's core claim are the same thing in different words.
**Required**: Keep one. The Summary pointer suffices; trim the Principal Identity section to its single non-redundant observation (that `validaccount` returns TRUE, locating enforcement outside the model) or remove the duplicate sentence from one location.

### Issue 4: Triplicated boilerplate across the three Delegation preservation paragraphs
**ASN-0042, Delegation section** (O1a, T4, O1b preservation paragraphs): each closes with the verbatim-templated "…The base case for the induction is O14's Nth clause…; non-delegation transitions preserve [X] trivially, since O15 admits no new principal and O13 fixes existing prefixes. By induction on the reachability sequence, [X] holds in every reachable state."
**Problem**: The induction scaffold (base = O14 clause, step = O13/O15 for non-delegation, conclude by reachability induction) is identical across all three and repeated word-for-word. A reader must skip past the same machinery three times to reach the per-invariant content.
**Required**: State the shared reachability-induction scaffold once, then give only the invariant-specific discharge (condition (iv) for O1a, condition (v) for T4, the length-contradiction for O1b).

## OUT_OF_SCOPE

None. The ASN's Scope and Open Questions sections already partition future territory (ownership transfer, overlap enforcement, cross-node federation, delegation-history recording) correctly.

VERDICT: REVISE
