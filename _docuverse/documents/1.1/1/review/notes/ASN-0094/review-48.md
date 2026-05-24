# Review of ASN-0094

After working through the proofs, lemmas, and worked examples carefully against the foundation, I find this ASN comprehensive and rigorous. The stratification is acyclic and explicit. Key verifications:

**Stratification check.** Sh0–Sh1 induct independently against the empty-baseline; Sh2–Sh3 consume Sh0–Sh1 as state-indexed lemmas for `slot_addrs(·)` well-formedness only (not in their inductive hypotheses); LinkAddressNotPrefixOfEmit is independent; EffectiveWpSimplification consumes Sh1, Sh3, and the Lemma; Sh4 consumes Sh0–Sh3 and the Lemma. No cycle.

**LinkAddressNotPrefixOfEmit proof.** Case I (same-home) closes via Uniform link sub-allocator chain length + T10a.7 + T3. Case II splits on length: II.A collapses to T3 + L1a directly; II.B's NAT-card additivity + T4a/T4b/T4c positional analysis derives the home-equality contradiction. The structural observation that K.λ-emitted addresses force `#w ≤ 1` is honest about the proof's `#w ≥ 2` generality being exhibited counterfactually.

**Sh4 Case D.** Step D.0's discharge of `addr(τ_new) ∉ nullified(Σ')` via the Lemma at both self- and cross-witnesses is sound. The structural bound `|leaving| ≤ 1` from R0a + R1 + PrefixSpanCoverage correctly pins the simultaneous step to at most `+1, −1`. The subset-closure derivation from `A_R^{Σ'} ⊆ A_R^Σ ∪ {τ_new}` is properly unpacked.

**EffectiveWpSimplification.** Step 1's discharge of `NoCraftedSpanReachesD` via Sh1+Sh3 at K:=R (replacing implicit Sh-conf-at-past-emission+R2+monotonicity bridge) is the right shape. Step 2's case-split on K's ~-class with Lemma at the new emission's G-slot under `K ~ R` closes cleanly. The conditional-on-substrate-reach scoping correctly handles the Sh-conf-rejected sub-regime.

**NullifyActiveSubsetCompatibility.** Both cases (clause iii admit + clause ii suppress) deliver active-subset content. The audit-slice multiplicity loss is properly recorded as a deliberate set-semantics commitment, not a hidden semantic shift.

**Worked examples.** Comment, Coverage+SHCD, Resolution standalone, Tuple-Classifier, Provenance, Attributed Retraction, FDD, and Sh4 suppression walkthroughs exercise canonical-form, cardinality, target-domain, single-home, Sh4-suppression, FDD-suppression, and routing rejection paths. Reject case AR3 properly distinguishes partition mismatch from unallocated-target.

**Appendix.** NAT-card and NAT-sub derivations from listed NAT axioms + (Peano-rec) + (Peano-zero-least) are sound; successor injectivity → right-identity → successor-distributivity → ℕ-commutativity → ℕ-associativity chain checks.

**Sh5(b) audit table.** Per-row symbol classification against categories (i)–(iv) with (v)/(vi) carve-outs is consistent. K_is_fresh rejection at `mtime` is the correct META falsifiability demonstration.

The framework's commitments (Emit_K routing, Sh4/FDD/SHCD contracts, empty-baseline, framework-wide `subspace_I(·) = E(·).1` identification) are explicit and properly scoped. The Open Questions properly tag refinements vs scope boundaries.

VERDICT: CONVERGED
