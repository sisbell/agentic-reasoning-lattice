# Regional Review — ASN-0034/TumblerSub (cycle 3)

*2026-04-23 05:06*

### Transitive-scope justification in TumblerSub Depends
**Class**: OBSERVE
**ASN**: TumblerSub *Depends*, four entries:
> "NAT-closure ... Required in scope for the consumed contracts of TA-Pos, ActionPoint, Divergence, and ZPD, each of which cites `1 ∈ ℕ`, the additive identity `0 + n = n`, or closure under `+` in its body."
> "NAT-wellorder ... Required in scope for the consumed contracts of Divergence, ZPD, and ActionPoint..."
> "NAT-cancel ... Required in scope for the consumed T1 contract: T1's trichotomy discharge (Case (ii, ii)...) ..."
> "NAT-discrete ... Required in scope for the consumed T1 and ActionPoint contracts..."

**Issue**: Other Depends entries in TumblerSub describe *what the axiom supplies to this proof* (e.g., NAT-sub's conditional closure used at `aₖ − wₖ ∈ ℕ`; T3's forward direction used to derive `a ≠ w`). The four entries above do the opposite: they inventory which *other* consumed contracts would need the axiom in scope. TumblerSub's own body never invokes `1 ∈ ℕ`, `0 + n = n`, summand absorption, least-element, or the discrete successor — they are transitive-only citations. Listing transitive dependencies in Depends with use-site inventories across siblings is the essay/use-site-inventory pattern the review discipline flags, and it also inflates the TumblerSub Depends list with entries that are genuinely not Dependencies of the TumblerSub proof. A caller who has the consumed contracts (Divergence, ZPD, ActionPoint, T1) in scope already gets those axioms transitively via those contracts' own Depends; re-listing them here duplicates rather than informs. Not a correctness defect — the axioms are needed somewhere, just not at this site.

---

### Case 1 of T1 trichotomy: unstated equality-position range extension
**Class**: OBSERVE
**ASN**: T1 proof, Case 1:
> "The shared-position equalities now range over all `1 ≤ i ≤ m`, so `a = b` by T3."

**Issue**: The hypothesis entering Case 1 is "no divergence position exists", which gives `aᵢ = bᵢ` for all `i` with `1 ≤ i ≤ m ∧ i ≤ n` (shared positions) and rules out exhaustion-shape divergences. After deriving `m = n`, the text states "the shared-position equalities now range over all `1 ≤ i ≤ m`". The move from "shared positions" to "all `1 ≤ i ≤ m`" is trivial (once `m = n`, shared = full), but its mechanism — that `1 ≤ i ≤ m ∧ i ≤ n` collapses to `1 ≤ i ≤ m` under `m = n` — is left implicit at a step that invokes T3's universal-agreement precondition. Not a defect; a reader tracking T3's precondition has to fill in the substitution. Minor.

---

VERDICT: OBSERVE

## Result

Regional review converged after 3 cycles.

*Elapsed: 1709s*
