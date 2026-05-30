# Channel Assignment — ASN-0042 review-98

**Date:** 2026-05-30 02:32

## Issue 1: `odom`-rename justification is notation meta-prose
Reason: Pure editorial trim — collapsing the rationale to the bare definition `odom(π) = {a ∈ T : pfx(π) ≼ a}` requires nothing beyond the ASN's own text. No design intent or implementation evidence is at stake.

## Issue 2: Forward-reference inventory framing on derived facts
Reason: Dropping the "named once for reuse" / "cited at use sites below" framing while keeping the fact and its proof is internal copy-editing; the derived facts (BootstrapContainment, Freshness-(v)) are already fully stated in the ASN.

## Issue 3: Delegation condition (v) re-derived in five places
Reason: Consolidating the "(v) ⟹ T4 ∧ freshness" derivation into the Freshness-(v) lemma and citing it elsewhere is deduplication of content already present; the B6-sufficiency chain is internal to the ASN and ASN-0040, which it already cites.

## Issue 4: Duplicated implementation corroboration
Reason: The reviewer asserts the four `findpreviousisagr`/`findisatoinsertgr` mentions are paraphrases of one already-grounded fact; anchoring it once and referencing it relocates existing Gregory-sourced evidence without needing new evidence.

## Issue 5: "Honest summary" hedge reads as relocated prior-finding content
Reason: The axiom/derived split is already given by the Properties table's Status column; cutting the self-correcting narration and stating the sets once is purely internal restructuring.

## Issue 6: Imprecise zero-count justification in O10(c)
Reason: The correction is a tumbler-algebra fact — sibling-advance `inc(·,0)` preserves zeros (B5a) while field-opening `inc(·,2)` introduces the separator — all derivable from ASN-0034/0040 semantics already cited in the ASN, so no design-intent or code evidence is required.
