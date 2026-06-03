# Review of ASN-0071

## REVISE

### Issue 1: PC-RANGE proof omits the equal-depth (#v = #u) sub-case — the primary case

**ASN-0071, *Resolution* (Positions of depth #v ≥ #u)**: "for `u ≤ v`, T1 case (i) at `#u` gives `u ≤ v ⟺ u_{#u} ≤ v_{#u}` (when `v_{#u} = u_{#u}`, `u` is a prefix of the deeper `v`, so `u < v` ... — still `u ≤ v`); for `v < r` ... (equality `v_{#u} = r_{#u}` makes `r` a proper prefix of the deeper `v`, so `r < v`, excluded)."

**Problem**: The split is "#v ≥ #u" vs "#v < #u," but inside "#v ≥ #u" both parentheticals silently assume the *strictly deeper* sub-case (#v > #u): "the deeper v," "u < v," "r < v." The equal-depth sub-case #v = #u is never shown, yet for the boundary component values it behaves differently:
- `u ≤ v` direction, `v_{#u} = u_{#u}`, `#v = #u`: then `v = u`, so `u ≤ v` holds by *equality*, not by "`u < v`."
- `v < r` direction, `v_{#u} = r_{#u}`, `#v = #u`: then `v = r`, excluded because the reach is an *exclusive* upper bound — not because "`r < v`" (which is false here; `v = r`).

This is not a corner case. By S8-depth every content-subspace `v ∈ dom(M(d_s))` has `#v = m_C`, so when the anchor matches the source depth (`#u = m_C` — exactly the well-formed `ContentReference` case the ASN says it generalizes), *every* captured position has `#v = #u`. The proof narrates only the sub-case that does not occur in the principal scenario and skips the one that does.

**Required**: Treat #v = #u and #v > #u as explicit sub-cases. For #v = #u, justify `u ≤ v` via `v_{#u} = u_{#u} ⟹ v = u` and exclude `v_{#u} = r_{#u} ⟹ v = r ∉ ⟦σ⟧` by the exclusive reach — not by "r < v."

### Issue 2: "What we do not specify" (ii) and (iii) are out-of-scope deferrals, not non-specifications

**ASN-0071, *What we do not specify***: "(ii) *Replica freshness.* ... replica-divergent views in a distributed deployment are out of scope. (iii) *Access-control filtering.* ... the visibility policy ... is a separate layer ... out of scope."

**Problem**: Both items point at layers the project Scope already declares out of scope (replication/BEBE; link/visibility policy). A paragraph whose content is "topic X is a separate layer, out of scope" advances no reasoning about FINDDOCSCONTAINING — it is meta-prose deferring to a downstream/adjacent location. Item (i) *Order* is legitimate (it states what the operation does *not* promise about its own result); (ii) and (iii) are not about this operation's result at all.

**Required**: Remove (ii) and (iii), or fold the single load-bearing point (find is evaluated at one state `Σ`) into the *Currency* section where it already lives.

### Issue 3: vspec relaxation paragraph is a use-site inventory plus defensive design rationale

**ASN-0071, *The query***: "A vspec is deliberately ASN-0058's `ContentReference (d_s, σ)` with two of its three well-formedness conditions dropped. ASN-0058 requires (i) ... (ii) ... (iii) ...; a well-formed `ContentReference` further demands ... A vspec keeps only (ii) and drops (i) and (iii) — and the coverage demand — *because search must tolerate exactly the cases those conditions forbid*. A query is posed against a source whose arrangement the requester does not control or fully know ..."

**Problem**: The paragraph re-enumerates a foundation definition's clauses at the use site, then justifies the design choice in prose ("because search must tolerate exactly the cases those conditions forbid," "the requester does not control or fully know"). The operative content is one line: a vspec retains only T12 on `ℓ`. The surrounding inventory and motivation are accretion of the kind the anti-bloat classifier targets.

**Required**: State the vspec preconditions directly (as the bullet list already does) and drop the comparative re-derivation of ASN-0058's conditions. If a contrast with `ContentReference` is needed, one clause suffices.

### Issue 4: duplicated reachability deferrals

**ASN-0071, *A worked scenario***: "*Reachability.* The thirteen steps are the standard allocate–place–record ... composites of ASN-0047 ... so `Σ` is reachable" and later "These two steps form another standard transcluding composite of ASN-0047, so `Σ⁺` is reachable."

**Problem**: Two paragraphs in the same section make the same deferral ("standard composite of ASN-0047 ⟹ reachable") in different words.

**Required**: State the reachability justification once and reference it, or merge the two into a single closing remark covering all fifteen steps.

## OUT_OF_SCOPE

### Topic 1: relationship between current-state result and the historical relation R
The first Open Question (how `find`'s current result relates to ASN-0047's permanent `R`) is genuinely a future ASN — the *Currency* section correctly establishes that `find` reads only `E_doc` and `M`, and bounding completeness against historical containment is new territory.

### Topic 2: rejection vs silent filtering of unresolvable positions
The second Open Question (when the system must reject rather than F-FILT) is a policy concern for a future operation-error ASN, not a defect here.

VERDICT: REVISE
