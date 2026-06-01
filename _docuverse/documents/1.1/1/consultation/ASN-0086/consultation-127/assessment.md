# Channel Assignment — ASN-0086 review-127

**Date:** 2026-06-01 00:15

## Issue 1: WP Case 1 justifies retaining PC twice in identical terms
Reason: Pure editorial deduplication — consolidating three restatements of the same "PC is layer-supplied, hence retained though non-weakest" claim into one. No design intent or implementation evidence is required; the fix operates entirely on text already present in the ASN.

## Issue 2: R0 proof states its per-address scope caveat twice, with a defensive non-use inventory
Reason: Editorial consolidation of a scope caveat and removal of a defensive non-use inventory, both already justified by the proof's own structure. The four-lemma list and its replacement are derivable from the ASN's existing argument; no external channel needed.

## Issue 3: "Arrangement modification is out of scope" paragraph re-establishes → completeness already stated
Reason: Editorial deduplication — the M2-derivation content stays, the duplicated completeness claim is removed. Both the kept and dropped content are already in the ASN; the fix requires no design intent or implementation evidence.

## Issue 4: Properties-Introduced table embeds full derivation chains, duplicating the proofs
Reason: Editorial reduction of table entries to statement-plus-headline-dependency, with the derivation prose already living in the body proofs. Nothing external is needed since the table merely mirrors content the ASN already proves.
