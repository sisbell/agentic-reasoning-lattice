# Channel Assignment — ASN-0094 review-25

**Date:** 2026-05-20 04:54

## Issue 1: Sh4 Case D — "τ_new joins A_R^{Σ'}" is asserted but never justified explicitly
Reason: Fix is derivable from the ASN's own content — add explicit steps citing Lemma — RetractionTargetNotOnChain (established earlier in the document) at τ_new's G-slot witness and each prior R-tuple's G-slot witness. Uses only machinery already proved in this ASN.

## Issue 2: Origin vs home terminology in RetractionTargetNotOnChain
Reason: Fix is derivable from ASN-0086 (which defines both `origin(·)` and `home(·)` and establishes their relationship). The fix is either to cite the identification from ASN-0086 or use one term consistently — both options are textual revisions against the existing spec.

## Issue 3: Worked example baseline is stronger than framework's empty-baseline
Reason: Pure notational fix — either rename the walkthrough's starting state symbol or clarify it as a post-Σ_init state reached via K.σ-steps. Internal to this ASN's prose.

## Issue 4: The "L1c via T10a.4" derivation in RetractionTargetNotOnChain Case II is unexplained
Reason: Fix is derivable from ASN-0043 (L1c) and ASN-0034 (T10a.4, T4) — expand the citation chain or find a more direct citation. Pure textual revision against already-established upstream lemmas.

## Issue 5: Resolution catalog row's "primary consumption" framing obscures base templates
Reason: Pure rewording of the catalog row to clarify that Sh5(b)-generated base templates are first-class; "primary consumption" documents the dominant pattern, not a constraint. Internal editorial fix.

## Issue 6: Sh4 universal-scope clarification is repeated verbatim in Sh4 Case D and FDD preservation
Reason: Pure editorial — replace the second occurrence with a citation to the first. Internal.

## Issue 7: Sh5(b) catalog audit table's "failed-check illustration" placement
Reason: Pure presentational restructuring — add a rejected row to the table or move the callout. Internal.

## Issue 8: Pre-emission candidate-set computation as a workaround is mentioned but not specified
Reason: Framework-internal design choice — either surface `C_K(F, G, Σ)` and `C_fd(F, Σ)` (already defined inside the contracts) as standalone layer-callable queries, or remove the sentence. Both options are derivable from the framework's existing structure.

## Issue 9: AllocatedAddressAntichain Step 3.1 contradiction argument is verbose
Reason: Pure editorial tightening of the prose; the underlying argument is unchanged. Internal.
