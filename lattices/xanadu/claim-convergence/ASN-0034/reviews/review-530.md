# Regional Review — ASN-0034/T4c (cycle 1)

*2026-04-24 12:56*

### `#t ≥ 1` described as "local unpacking" but is directly a T0 axiom clause
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: T4a setup: "T0 declares every `t ∈ T` to be a nonempty finite sequence over ℕ; a nonempty sequence has at least one component, so by the definition of length `#t ≥ 1` — this is a local unpacking performed here, not a postcondition cited from T0". T4b setup repeats the identical passage. T4a Depends (T0 entry): "… from which T4a locally unpacks `#t ≥ 1` (the length of a nonempty sequence is at least 1)". T4b Depends (T0 entry) likewise.
**Issue**: T0's Formal Contract Axiom list explicitly contains the clause `(A a ∈ T :: 1 ≤ #a)` with the parenthetical gloss "nonemptiness — each tumbler has at least one component". So `#t ≥ 1` *is* a first-class contract item of T0, available by direct citation. The T4a/T4b passage constructs a pseudo-derivation route (via "nonempty finite sequence" + "definition of length") and then defensively declares it "not a postcondition cited from T0" — which mischaracterises T0's contract and creates the impression that the bound requires derivation machinery it does not. The word "postcondition" is additionally off-register for T0, which is a carrier declaration with an Axiom slot rather than Postconditions.
**What needs resolving**: Either cite T0's axiom clause `(A a ∈ T :: 1 ≤ #a)` directly where `#t ≥ 1` is used in T4a and T4b, and update the corresponding Depends entries to reflect direct citation; or, if there is a reason to route through the narrative "nonempty finite sequence" framing, remove the false disclaimer that the fact is "not a postcondition cited from T0" and state accurately how the axiom clause connects to the usage.

### T4b Postconditions duplicates the Definition slot rather than exporting proved facts
**Class**: OBSERVE
**ASN**: T4b. Definition slot states: `dom(N)` = T4-valid subset; `dom(U) = {t ∈ dom(N) : zeros(t) ≥ 1}`; `dom(D) = {t ∈ dom(N) : zeros(t) ≥ 2}`; `dom(E) = {t ∈ dom(N) : zeros(t) = 3}`; per-`k` value assignments; "Outside the stated domains, the respective projections are not assigned values." Postconditions slot then restates: `dom(N)` is the T4-valid subset; `dom(U) ⊆ dom(N)` picks out `zeros(t) ≥ 1`; `dom(D) ⊆ dom(N)` picks out `zeros(t) ≥ 2`; `dom(E) ⊆ dom(N)` picks out `zeros(t) = 3`; the per-`k` presence pattern; "Outside the T4-valid subdomain, none of the projections is assigned a value".
**Issue**: The Postconditions slot should export what the Derivation *establishes about* the Definition (well-definedness, uniqueness, image contained in the all-`ℕ⁺`-component subset, field absence encoded by partiality). Instead it re-emits the domain structure and presence pattern verbatim, so a reader consulting the Postconditions slot to find the discharged guarantees has to match them against near-identical Definition text to locate what is new. Slot hygiene sibling to prior findings at T4 ("field separator" stipulation in the Axiom slot) and T4c (defining biconditionals sitting in Postconditions).

### T4c injectivity derives `0 < 1` from NAT-addcompat when NAT-closure posits it directly
**Class**: OBSERVE
**ASN**: T4c *Injectivity*: "NAT-addcompat's strict successor inequality `n < n + 1`, instantiated at `n ∈ {0, 1, 2}`, gives `0 < 1`, `1 < 2`, and `2 < 3`". Depends (NAT-addcompat entry): "supplies the strict successor inequality `n < n + 1`, instantiated at `n ∈ {0, 1, 2}` to obtain the base links `0 < 1`, `1 < 2`, `2 < 3`".
**Issue**: NAT-closure's Axiom list contains the clause `0 < 1` directly (labelled "distinctness of the two named constants"), so `0 < 1` is available by straight citation of an already-declared dependency. Routing `0 < 1` through NAT-addcompat's successor inequality at `n = 0` — which additionally needs NAT-closure's left-identity `0 + 1 = 1` to reduce `0 < 0 + 1` to `0 < 1`, a step the injectivity prose does not walk — takes a longer path for a fact NAT-closure axiomatises. NAT-addcompat is still needed for `1 < 2` and `2 < 3`, so this is not a Depends-list trim; it is a citation-choice observation that the first chain-link can come from NAT-closure's already-declared `0 < 1` without invoking a successor-identity step.

VERDICT: REVISE
