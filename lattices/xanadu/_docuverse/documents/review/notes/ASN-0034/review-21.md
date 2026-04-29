# Review of ASN-0034

The proofs are correct throughout — every case analysis is complete, every verification checks out, no hand-waving. The issues are mechanical: the dependency graph has missing and spurious entries, and several name fields diverge from the body's labels.

## REVISE

### Issue 1: TA3 and TA3-strict have no follows_from in the dependency graph
**ASN-0034, Verification of TA3**: The proof of TA3 (weak order preservation under subtraction) is a substantial multi-page case analysis that explicitly uses T1 (ordering cases throughout), TumblerSub (constructive definition for all cases), TA6 (Case 0: "every zero tumbler is less than every positive tumbler"), and T3 (equality conclusions). The dependency graph lists no `follows_from` entries for either TA3 or TA3-strict. TA3-strict's proof inherits TA3's full case structure ("Only Cases 1–3 apply, all of which produce strict inequality") and therefore depends on the same properties.
**Problem**: Undeclared dependencies on T1, TumblerSub, TA6, T3 for TA3. Undeclared dependencies for TA3-strict (at minimum the same set). This is inconsistent with how comparable properties are tracked — TA1 (introduced, with verification) has `follows_from: TA0`; T5 (introduced, with proof) has `follows_from: T1`.
**Required**: Add `follows_from` entries. For TA3: T1, TumblerSub, TA6, T3. For TA3-strict: at minimum the same, since it relies on TA3's case analysis.

### Issue 2: Three individual dependency graph corrections
**ASN-0034, dependency graph**:

(a) **T7 — spurious dependency on T1.** The graph lists `follows_from: T1, T3, T4`. The body says T7 is "a corollary of T3 (canonical representation) and T4 (hierarchical parsing)." T1 is mentioned *after* T7 and explicitly labeled: "The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2)... This is a consequence, not an assumption." The property table confirms: "corollary of T3, T4." Remove T1 from T7's `follows_from`.

(b) **D0 — undeclared dependency on Divergence.** D0 states: "the divergence k of a and b satisfies k ≤ #a." This directly references the Divergence definition without listing it in `follows_from`. D1 correctly includes Divergence. Add Divergence to D0's `follows_from`.

(c) **TA-assoc — undeclared dependency on TumblerAdd.** The proof explicitly expands TumblerAdd's component formulas for all three cases ("both sides produce aᵢ for i < k_b... bᵢ for k_b < i < k_c... cᵢ beyond"). The graph has no `follows_from` at all. Add TumblerAdd to TA-assoc's `follows_from`.

**Required**: Apply all three corrections.

### Issue 3: TA7a name mismatch in dependency graph
**ASN-0034, dependency graph**: The graph entry for TA7a has `name: "Ordinal-only shift arithmetic"`. The body labels it **"TA7a (Subspace closure)."** These are genuinely different names describing different aspects — "Subspace closure" names the guarantee (arithmetic stays in the subspace); "Ordinal-only shift arithmetic" names the mechanism (use ordinals, not full positions).
**Problem**: Downstream references will cite "Subspace closure" or "TA7a". A graph entry with a different name obscures the connection.
**Required**: Change the graph's name field to "Subspace closure" to match the body.

### Issue 4: GlobalUniqueness property table missing T10a
**ASN-0034, Properties Introduced table**: The table entry reads "theorem from T9, T10, T3, T4, TA5." The proof explicitly invokes T10a in Case 4: "By T10a, the parent allocator uses `inc(·, 0)` for all its sibling allocations." The dependency graph correctly includes T10a.
**Problem**: The property table is inconsistent with both the proof text and the dependency graph.
**Required**: Change the property table entry to "theorem from T3, T4, T9, T10, T10a, TA5".

### Issue 5: Systematic name mismatches between body labels and dependency graph
**ASN-0034, dependency graph**: Multiple graph entries use the property table's Statement column or a paraphrase rather than the body's parenthetical label. Examples:

| Label | Body name | Graph name |
|-------|-----------|------------|
| T0(a) | Unbounded component values | Every component value of a tumbler is unbounded |
| T5 | Contiguous subtrees | The set of tumblers sharing a prefix forms a contiguous interval under T1 |
| TA-strict | Strict increase | Adding a positive displacement strictly advances |
| TA1 | Order preservation under addition | Addition preserves the total order (weak) |
| TA-assoc | AdditionAssociative | Addition is associative where both compositions are defined |
| TA5 | Hierarchical increment | Hierarchical increment inc(t, k) produces t' > t |

Other entries (T1, T3, T4, TA-LC, TA-MTO, TS1–TS5, etc.) correctly match the body's parenthetical. The inconsistency suggests the extraction used different sources for different properties.
**Problem**: The `name` field should match the body's canonical label so that graph entries are unambiguously identifiable.
**Required**: Align all graph name fields with the body's parenthetical labels.

## OUT_OF_SCOPE

None. The ASN stays within its stated scope of tumbler algebra. It does not stray into I-space/V-space semantics, operation frame conditions, enfilade internals, or document lifecycle.

VERDICT: REVISE
