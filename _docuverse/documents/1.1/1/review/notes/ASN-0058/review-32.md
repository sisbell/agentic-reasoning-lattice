# Review of ASN-0058

## REVISE

### Issue 1: M7f elides the B3 case-split that distinguishes merge from split

**ASN-0058, M7f (MergeFrame):** "Verification. Analogous to M6f: the merged block occupies exactly V(β₁) ∪ V(β₂) and maps each position to the same I-address as before."

**Problem:** The "analogous to M6f" gloss does not cover B3's non-trivial structure for the merged block. M6f's B3 was direct — each split piece maps its V-positions to the same I-addresses as β did, no index translation required. M7f's B3 requires a case-split: positions v₁ + k for 0 ≤ k < n₁ map via β₁, but for n₁ ≤ k < n₁ + n₂, v₁ + k must be re-expressed as v₂ + (k − n₁) via M-aux + V-adjacency before β₂'s B3 applies, and the resulting I-address a₂ + (k − n₁) must be re-expressed as a₁ + k via M-aux + I-adjacency. This case-split appears explicitly in C1a's later restatement (under "B3 specifically") but is missing at M7f's site of definition. The asymmetry between M6f and M7f is precisely what "analogous" obscures.

**Required:** At M7f, write out the B3 case-split with explicit M-aux applications for both V-position translation (v₁ + k = v₂ + (k − n₁)) and I-address translation (a₁ + k = a₂ + (k − n₁)). Promote C1a's existing case-split to M7f's own verification.

### Issue 2: M16's citation of M0 for n₁ ≥ 1 is misdirected

**ASN-0058, M16 (CrossOriginMergeImpossibility) proof:** "M0 (WidthCoupling) gives n₁ ≥ 1."

**Problem:** M0's content is `|V(β)| = |I(β)| = n` — a cardinality identity, not a positivity claim. The fact n ≥ 1 comes from the mapping block definition, which fixes "n ∈ ℕ with n ≥ 1 — the width." M0 uses n ≥ 1 (it's needed for the singleton V(β) = {v} case at n = 1) but does not introduce it. The same misdirection appears in M7-cov ("n₁ ≥ 1 by M0").

**Required:** Cite the mapping block definition for n₁ ≥ 1, not M0.

### Issue 3: "Trivial partition corollary" mislabels a multi-step argument

**ASN-0058, properties table for M12a:** "with the trivial partition corollary, the set of maximal runs partitions dom(f) and is uniquely determined by f"

**Problem:** The body's "Partition corollary" is anything but trivial — it requires the explicit right-extension and left-extension phases, with M-aux index translation, condition-1/condition-3 preservation arguments at each step, and a termination argument leaning on S8-fin. Calling it "trivial" in the summary table contradicts the proof's actual length. A reader scanning the table would expect a one-liner; the body delivers a substantial construction.

**Required:** Drop "trivial" — the corollary is straightforward in structure but not trivial. Either "via the partition corollary" or "via the extension argument" is honest.

VERDICT: REVISE
