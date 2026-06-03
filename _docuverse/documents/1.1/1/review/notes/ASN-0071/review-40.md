# Review of ASN-0071

## REVISE

### Issue 1: "What this verifies" is a use-site inventory wrapped in meta-prose
**ASN-0071, *A worked scenario* ("What this verifies")**: "Each named property is established by the trace line cited; the labels bind property to evidence without re-deriving."
**Problem**: This subsection is an index that re-states, for each abstract label (F-SHARE, F-DIST, F-PART, …), which earlier trace line demonstrates it. The framing sentence describes what the bullets do rather than advancing any claim — exactly the use-site-inventory accretion the anti-bloat classifier targets. The genuinely new content (F-CUR's contraction remark, home/transcluding recovery) is buried among bullets that merely re-point at lines already in the trace.
**Required**: Drop the framing sentence and the bullets that only re-cite an already-labelled trace line. Keep only the bullets that add reasoning not present at the trace site (e.g., F-CUR's "would drop d_B even though R persists").

### Issue 2: Basis-column legend explains table format rather than reasoning
**ASN-0071, *Claims Introduced*** (paragraph preceding the table): "The Basis column records how each claim relates to the definitions F-iaddrs and F-find. *Definition* indicates…; *direct from F-X* indicates…; *Derived* indicates…"
**Problem**: This paragraph documents the meaning of the table's own column vocabulary. It is format glossary, not argument — meta-prose in a structural slot.
**Required**: Remove the paragraph; the terms "Definition / direct from F-X / Derived" are self-explanatory in context, and any necessary distinction can live in a one-clause footnote.

### Issue 3: Worked scenario re-discharges ASN-0047 coupling instead of exercising the operation
**ASN-0071, *A worked scenario* ("Composite structure")**: "The thirteen steps group into four valid composites … we confirm the coupling at each boundary" (and the fifth composite for `d_E`).
**Problem**: The per-composite discharge of J0, J1★, J1'★ verifies that the *construction* is a valid ASN-0047 composite sequence — it audits ASN-0047's machinery, not any FINDDOCSCONTAINING claim. No `find`/`iaddrs` property depends on it; the find-property verification (F-SHARE, F-SOUND, F-PART, multi-block resolve, subtree capture, interior-action-point rejection) is carried entirely by the **Find** and **Resolution** steps. Reciting the coupling discharge across five composites is the kind of cross-cycle accretion the anti-bloat mode flags.
**Required**: Replace the composite-by-composite coupling discharge with a single sentence asserting the state is reached by standard allocate–place–record composites of ASN-0047 (so its invariants hold), and keep the scenario's prose on what `find` returns.

## OUT_OF_SCOPE

(none — the Open Questions section already routes historical-`R` reconciliation, replica completeness, visibility filtering, and contraction invariants to future ASNs appropriately.)

VERDICT: REVISE
