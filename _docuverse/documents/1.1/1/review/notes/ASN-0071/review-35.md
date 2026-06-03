# Review of ASN-0071

The operation is defined cleanly as a pure function of state, the PC (prefix confinement) proof is genuinely worked through rather than asserted, and the worked scenario discharges each precondition step-by-step and exercises the boundary cases (empty query, infinite-reach span filtered to one position, multi-block dedup, cross-depth subtree capture, interior-action-point rejection). I found no correctness defect in the math. The findings below are all of the accretion/meta-prose kind the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Circular, misleading forward reference in the PC argument
**ASN-0071, *The query***: "This is the relaxed analogue of ASN-0058's C0a, proven here directly from the vspec preconditions. **The argument is the position-1 reasoning of the Resolution section, run at every prefix position rather than just position 1**: for any j with 1 ≤ j < #u..."
**Problem**: The sentence defers the argument *downstream* to the Resolution section, then immediately gives the full argument inline. Meanwhile the Resolution section's subspace-confinement step cites "PC's position-1 instance (**proven in *The query***)." The dependency runs query → resolution, so the forward pointer is backwards and circular: the Resolution section contains no independent position-1 reasoning to defer to. A reader chasing the pointer finds only a citation back to here.
**Required**: Delete "is the position-1 reasoning of the Resolution section, run at every prefix position rather than just position 1." The argument stands on its own where it is; state it as "the argument runs at every prefix position 1 ≤ j < #u."

### Issue 2: The wp-defined derivation is given twice in different words
**ASN-0071, *Resolution*** and **the operation***: Resolution says the expression "`⟦σ⟧ ∩ dom(Σ.M(d_s))` is ill-formed when `d_s ∉ Σ.E_doc`. The subset claim is therefore gated on the same well-definedness precondition we state for `find` below — `wp-defined`..." Then *The operation* re-derives it: "`iaddrs(Q)(Σ)` consults `Σ.M(d_s)`... and `dom(Σ.M) = Σ.E_doc` (M1, ASN-0047). The expression `⟦σ⟧ ∩ dom(Σ.M(d_s))` is therefore meaningful only when `d_s ∈ Σ.E_doc`."
**Problem**: The same `dom(Σ.M) = E_doc ⟹ d_s ∈ E_doc` argument is presented in full in two sections. The Resolution version even forward-points to the operation version ("we state for `find` below"), which is the deferral-to-downstream pattern.
**Required**: State the precondition and its M1-based justification once (in *The operation*, where `find`'s domain is defined) and reference it from Resolution in one clause, not a parallel re-derivation.

### Issue 3: The subset claim is restated with the same caveat across three sites
**ASN-0071, *Resolution* / *The operation* / claims table**: "`iaddrs(Q)(Σ) ⊆ dom(Σ.C)` ... is read with `Σ` explicit on both sides — the right-hand side is the input state's content store, not a fixed set." The "state-dependent / Σ explicit on both sides" qualification recurs in Resolution (twice), in *The operation*, and in the F-iaddrs Basis cell.
**Problem**: The same hedge ("both sides state-dependent at Σ") is repeated nearly verbatim. The reader must re-read identical caveats.
**Required**: Prove and qualify the subset claim once in Resolution; let the table cell cite it without re-explaining the state-dependence.

### Issue 4: The vspec definition enumerates a downstream consumer
**ASN-0071, *The query***: "**What it retains — the single fact the Resolution section's resolve-equivalence needs** — is subspace confinement, recovered from `actionPoint(ℓ) = #u` and `#u ≥ 2`."
**Problem**: The definition's introduction names a downstream consumer ("the fact the Resolution section's resolve-equivalence needs") instead of advancing the definition's meaning. The relevant content — vspec retains subspace confinement — survives without the use-site inventory.
**Required**: Drop the "the single fact the Resolution section's resolve-equivalence needs" clause; state directly that the vspec retains subspace confinement.

### Issue 5: Essay content and a duplicated recovery claim
**ASN-0071, *What we do not specify* and *Discovery through sharing***: "These omissions are deliberate. They distinguish what FINDDOCSCONTAINING fundamentally is from what specific deployments may add around it. Each is properly the subject of a separate specification." Separately, the home/transcluding recovery ("`origin(a)` names `a`'s home... comparing it against each `d ∈ find(Q)` recovers the relationship") appears both in *Discovery through sharing* and as the worked-scenario "Home/transcluding recovery" bullet.
**Problem**: The first is essayistic framing that advances no reasoning. The second states the recovery mechanism twice (general claim + scenario instance is fine, but both spell out the full `d = origin(a)` ⟺ home vs transclude rule).
**Required**: Cut the "These omissions are deliberate..." sentence. Keep the recovery rule's general statement in *Discovery* and reduce the scenario bullet to the concrete instantiation (`origin(a₁) = d_A` home; `d_B`, `d_D` transclude) without re-deriving the rule.

## OUT_OF_SCOPE

### Topic 1: Historical containment, replica consistency, visibility filtering
**Why out of scope**: The ASN correctly defers these to the Open Questions and *What we do not specify* sections; they are separate operations/specifications, not gaps in `find`'s definition. No action needed beyond the prose trims in Issue 5.

VERDICT: REVISE
