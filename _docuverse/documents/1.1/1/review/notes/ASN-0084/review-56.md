# Review of ASN-0084

## REVISE

### Issue 1: Inline "not-done-here" disclaimers duplicate the Open Questions
**ASN-0084, R-SP and CanonicalRunDecomposition**: R-SP opens "This lemma establishes sufficiency only (the ⇐ direction)... It does not characterize the weakest precondition." Open Question 5 then asks "What is the weakest precondition for REARRANGE_K to establish the post-state invariant suite Q...". Likewise CanonicalRunDecomposition states "No postcondition of this ASN requires the operational *exhaustive-Merge process*... or its confluence," and Open Question 6 asks "By what operational process is the S8-unique maximal (canonical) run partition recovered... and is that process confluent...".
**Problem**: This is the "explains what is NOT needed" / deferral pattern. Each lemma carries a defensive paragraph announcing the absence of a result, and the same absence is then correctly registered as an Open Question. The disclaimer advances no reasoning the Open Question doesn't already carry.
**Required**: Drop the inline disclaimers; let the Open Questions be the sole home for the deferred work. R-SP need only state the implication direction it proves; CanonicalRunDecomposition need only name the foundation's maximal partition.

### Issue 2: Width-positivity is derived twice
**ASN-0084, "Width-ordinal identities" (under RegionPartition) and "Width positivity" (under Consequences of R-PRE)**: the first reads "Hence ord(c_{i+1}) ≥ ord(c_i) + 1 > ord(c_i)... each width is therefore a well-defined positive natural number (≥ 1)"; the second re-derives "Step 1... reduces CS2's strict tumbler ordering c_i < c_{i+1} to ord(c_i) < ord(c_{i+1}), so ord(c_{i+1}) − ord(c_i) ≥ 1 by the truncated subtraction".
**Problem**: Two paragraphs in different sections establish the same fact (each region width ≥ 1 from CS2 via the singleton identification) in different words.
**Required**: Derive width ≥ 1 once and cite it from the other site. Keep the distinct content (the width-as-ordinal-difference formula; the width-as-V-position-count step) but not the duplicated ≥ 1 argument.

### Issue 3: R-BLK Scope note is a use-site inventory deferring to R-NS
**ASN-0084, R-BLK "Scope note on non-S runs"**: "the substantive verification — V-extent confinement... post-state S8-cons consistency... and pairwise disjointness from subspace-S runs... — is recorded once in R-NS and not repeated. The Phase clauses below state explicitly where this dispatch fires."
**Problem**: The note inventories where R-NS will be cited and then Phases 1–3 each re-cite R-NS(NS-π)/R-NS(NS-run) anyway. The inventory is meta-prose about the document's own cross-references; it does not advance the run-transformation argument. This is the "definition/section enumerates where its dependency fires" pattern.
**Required**: Delete the Scope note. The per-Phase citations to R-NS already carry the dispatch at the point of use.

### Issue 4: Verbatim verification boilerplate repeated across the five worked examples
**ASN-0084, the five "Worked Example" sections**: the R-RI verification sentence "Since ran(M(d)) ⊆ dom(C) by S3 of the pre-state and C' = C, ran(M'(d)) ⊆ dom(C'). ✓" appears verbatim in all five; the R-PRE CS1–CS4 restatement and the "Width positivity... (consequence) ✓" line are likewise mechanically repeated.
**Problem**: The examples themselves earn their place (each traces a distinct μ sub-case — forward, fixed, backward — plus the empty-exterior boundary). But the R-RI/R-PRE scaffolding is identical text that re-proves nothing example-specific; it is filler the precise reader skips.
**Required**: Keep one full R-RI/R-PRE trace; in the remaining examples reduce these to "R-RI, R-PRE: as in the first example (only the values differ)." Retain only the example-specific computations (M'(d) values, π, displacement, run decomposition).

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: Already correctly logged as Open Questions; generalizing the cut count and characterizing closure under composition is new territory, not a defect in the 3/4-cut treatment.

META: The ASN defines a genuine state operation (REARRANGE) with abstract preconditions, postconditions, and an invariant-preservation audit — it specifies system guarantees, not implementation mechanics, so it has not drifted.

VERDICT: REVISE
