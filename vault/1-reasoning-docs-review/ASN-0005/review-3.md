# Review of ASN-0005

## REVISE

### Issue 1: DEL7 conflates global and per-document discoverability; false contiguity claim

**ASN-0005, "Ghost links and partial resolution"**: "The link's discoverability state for a given endset is determined by how many documents' POOMs currently reference addresses in A"

**Problem**: DEL7 defines live/partial/ghost with existential quantification over all documents — these are global states. But DEL8's `resolve(L, endset, d)` takes a specific document. The bridge paragraph then claims: "A live endset resolves to a single contiguous V-span set." Under DEL7's global definition, a "live" endset has every address mapped by *some* document, but resolving through any particular document may yield empty or partial results (document A maps to a₁, document B maps to a₂, resolving through either gives incomplete coverage). The claim is false as stated.

Even granting a per-document interpretation, "single contiguous" is unproven. After editing operations, I-addresses from an endset can occupy non-contiguous V-positions in a document. Nothing in the specification guarantees that endset addresses remain contiguously arranged.

The concrete example compounds the confusion: "L is now a ghost link relative to d" uses a per-document concept that DEL7 never defines. DEL7's ghost means no document anywhere maps to the endset — a much stronger condition than "this particular document doesn't."

**Required**: (1) Define discoverability per-document: `live_in(L, endset, d)` iff `resolve_addrs(L, endset, d) ≠ ∅`, with live/partial/ghost as the per-document classification that DEL8 actually computes. (2) Derive the global classification from the per-document ones. (3) Drop the contiguity claim or state the additional conditions under which it holds. (4) Use the per-document terminology consistently in the concrete example.

### Issue 2: "Three permanence commitments" but four listed

**ASN-0005, "The permanence context"**: "The system makes three permanence commitments that constrain every operation"

**Problem**: Four properties follow (P0, P1, P2, P3). The subsequent sentence correctly says "These four properties." The opening count is wrong.

**Required**: Change "three" to "four."

### Issue 3: Variable shadowing in wp analysis

**ASN-0005, "Weakest precondition: span-index forward inclusion"**: `wp(DELETE(d, p, w), R) = (A d', a : (E p : poom(d').p = a) ⟹ (a, d') ∈ spanindex)`

**Problem**: The bound variable `p` in `(E p : poom(d').p = a)` shadows the DELETE parameter `p` from `DELETE(d, p, w)`. Both appear in scope simultaneously. The postcondition R introduced the same shadowing: `(A d', a : (E p : poom'(d').p = a) ⟹ ...)`. Dijkstra's convention gives bound variables local scope, so the formula is technically unambiguous, but a reader tracing the substitution must distinguish which `p` is the deletion start position and which ranges over all positions.

**Required**: Rename the bound variable throughout the wp section (e.g., `q`): `(E q : poom(d').q = a)`.

### Issue 4: POOM entry positional correspondence unstated

**ASN-0005, "I-dimension invariance in surviving entries"**: "Let the entry map V-range [v₁, v₂) to I-range [i₁, i₂)"

**Problem**: The three partial-overlap cases compute I-displacements by positional offset — head removal uses `i₁ + k` where `k = (p ⊕ w) − v₁` is a V-offset. This requires that within a single POOM entry, V-position `v₁ + k` maps to I-address `i₁ + k` (a 1:1 order-preserving correspondence) and that `v₂ − v₁ = i₂ − i₁` (equal widths). This is the span model and is consistent with the vocabulary's definition ("contiguous range... specified by a start tumbler and length"), but it is never explicitly stated as a structural property of POOM entries. All three split formulas depend on it.

**Required**: State as a premise: within a single POOM entry mapping V-range `[v₁, v₂)` to I-range `[i₁, i₂)`, the correspondence is positional (`v₁ + k ↦ i₁ + k` for `0 ≤ k < v₂ − v₁`) and `v₂ − v₁ = i₂ − i₁`. One line; grounds the entire split analysis.

## OUT_OF_SCOPE

### Topic 1: Concurrent DELETE atomicity
**Why out of scope**: The ASN correctly identifies this in its open questions. Concurrency semantics require their own treatment — defining observable intermediate states, linearizability conditions, and interaction with cross-document isolation.

### Topic 2: POOM fragmentation bounds
**Why out of scope**: The ASN correctly notes that middle splits increase entry count and asks whether unbounded growth is permissible. This is a system-level resource management question that applies to all operations producing splits, not DELETE alone.

### Topic 3: Link subspace concrete trace
**Why out of scope**: DEL1a is specified and the inline scenario ("after deleting the link at position 2.2, the link at 2.3 remains at 2.3") verifies the key claim. A full formal trace parallel to the text-subspace example would strengthen confidence but is a completeness improvement, not a correction.

VERDICT: REVISE
