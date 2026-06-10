# Review of ASN-0114

I checked each claim's proof, the worked example, and the foundation references. The mathematics is sound: F0's wp is correctly the definedness condition; F1's two inclusions are the two failure modes; F2's `|R| ≥ 2` follows from span convexity (S0) applied to a disconnected coverage, with the quantifier over *all* F1-satisfying `R` handled correctly; F5's single-step→multi-step lift via LP13 is explicit and correct; F7's empty/invalid routing is forced by F0 + F1 + the two collapses, leaving `⟨⟩ ≠ ⊥` as its irreducible (hence primary) content. The worked example checks out arithmetically (`a₃ ⊕ δ(2,8) = a₅`; the gap witness `a₅ ∉ coverage(e₁)`; the `F`-restriction via LP-Fin Corollary). References are to foundation ASNs only (0034, 0043, 0053, 0093, 0098), and the `coverage`-on-span-sets extension is explicitly bridged, not reinvented. No drift into implementation mechanics — F3/F6 deliberately bind coverage and leave representation free, and the resolution-to-V-positions boundary is correctly excluded.

One issue, raised under the active anti-bloat classifier.

## REVISE

### Issue 1: The corollary-source inventory is stated verbatim in two places

**ASN-0114, "The selector and its domain" (roadmap closing the *Status of the result* discussion) and "Synthesis"**:

Roadmap: "...the remaining properties F2, F3, F5, F6, and F8 emerge alongside them as corollaries (F2, F3, F6 from F1; F5 from F1 and link immutability; F8 from F0 and F1)."

Synthesis: "...with F2, F3, F5, F6, and F8 following as corollaries (F2, F3, F6 from F1; F5 from F1 and link immutability; F8 from F0 and F1)."

**Problem**: The parenthetical derivation inventory `(F2, F3, F6 from F1; F5 from F1 and link immutability; F8 from F0 and F1)` is identical in both locations, and the surrounding "primary commitments — F1, F4, F7 / corollaries" framing is near-identical. This is the "two paragraphs say the same thing" / front-loaded use-site-inventory pattern the classifier flags. The roadmap instance is the weaker of the two: it enumerates each corollary's source *before any of those derivations have been shown*, so it is a forward-reference inventory the reader cannot yet verify; the synthesis instance is a legitimate recap because it follows the derivations. (The claims table is a third statement, but a reference table is conventional and not at issue.)

**Required**: State the source-by-source inventory once. Trim the roadmap sentence to the bare orientation it needs — name the F1/F4/F7 primary split and that the rest are corollaries — and let the synthesis carry the full `(... from F1; ... from F0)` inventory after the derivations exist. Or invert. Either way, do not repeat the parenthetical verbatim.

## OUT_OF_SCOPE

(none — the note correctly defers endset-to-V-position resolution, wire-encoding of `⟨⟩`/`⊥`, and multi-document coverage reporting to its Open Questions and the scope list, without admitting claims about them.)

VERDICT: REVISE
