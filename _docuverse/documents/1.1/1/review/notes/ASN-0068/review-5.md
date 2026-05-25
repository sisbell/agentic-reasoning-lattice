# Review of ASN-0068

## REVISE

### Issue 1: Iterated predecessor notation `v − j` not formally extended

**ASN-0068, CV-MAX existence proof**: The construction `R := (v_a − j, v_b − j, j + n_R)` and surrounding arithmetic use `v − j` for the j-th iterated V-predecessor.

**Problem**: The parenthetical in the maximality definition only formally defines "valid V-predecessor of `v` at depth `m`" — the `j = 1` case. Iterated `v − j` for `j ≥ 1` (and the degenerate `v − 0`) is used in the existence proof construction without formal extension. A reader must infer that `v − j` means the unique `v'` of depth `m` with `v' + j = v`, that `v − 0 = v`, and that existence requires `v_m ≥ j + 1`.

**Required**: Formally extend `v − j` as the unique `v'` of depth `m` with `v' + j = v`, with `v − 0 := v` and the inverse property `(v − j) + j = v` made explicit. State the existence condition (`v_m ≥ j + 1` for the depth-m case under D-SEQ★).

### Issue 2: Predecessor-arithmetic step not cited

**ASN-0068, CV-MAX existence proof (right-maximality check)**: The identity `((v_a − j) + (j + n_R), (v_b − j) + (j + n_R)) = (v_a + n_R, v_b + n_R)` is asserted.

**Problem**: This identity rests on (a) the predecessor inverse property `(v − j) + j = v` and (b) shift-addition associativity supplied by M-aux (ASN-0058) — `(v + c) + j = v + (c + j)`. Neither is cited. The same gap appears in the symmetric `v_a − j − 1` claim of the left-maximality check. The contrast with the carefully cited "OrdinalShift's last-component formula (ASN-0034) together with T3 (ASN-0034)" elsewhere in the proof is conspicuous; this step deserves the same treatment.

**Required**: Cite M-aux (ASN-0058) and the predecessor inverse at the arithmetic step. The chain is `(v − j) + (j + n_R) = ((v − j) + j) + n_R` (M-aux) `= v + n_R` (predecessor inverse).

### Issue 3: Validity of R as a correspondence run not explicitly verified

**ASN-0068, CV-MAX existence proof**: "The triple `R := (v_a − j, v_b − j, j + n_R)` is then a correspondence run containing `(v_a, v_b)` at offset `k = j`..."

**Problem**: R's validity as a correspondence run requires conditions (i)–(iii) to hold at every offset `0 ≤ k < j + n_R`. The proof asserts R is a run and proceeds directly to "We verify maximality" without stitching the walks together. The verification is straightforward but skipped: offsets `0, …, j − 1` are covered by the left walk at distance `j − k`; offsets `j, …, j + n_R − 1` reduce to the right walk via `(v_a − j) + k = v_a + (k − j)`.

**Required**: Add a one-paragraph verification splitting the offset range `[0, j + n_R)` into the two regions and identifying which walk supplies the conditions in each. Without this, the proof obligation that R is well-formed is unmet — only maximality of R is established.

## OUT_OF_SCOPE

None — the Open Questions section already enumerates the natural future-ASN topics (concurrent comparison, multi-document composition, version-history walks, replication consistency, sub-allocator boundary semantics).

META: not applicable — the ASN stays squarely within specification territory (state, operation signature, structural invariants, derived consequences).

VERDICT: REVISE
