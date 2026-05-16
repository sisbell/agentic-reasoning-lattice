## Question 1 [evidence]

> Does the udanax-green allocator support reaching every structurally-valid link address under a document seed (zeros=3, E₁=s_L, T4-valid), regardless of prior allocations in that document's link subtree, or are some structurally-valid addresses permanently unreachable once nearby allocators have committed?

## KB Synthesis

## Link Address Reachability in the udanax-green Allocator

The answer is **yes, every structurally-valid link address under a document seed is reachable — but only if no address in that subtree has been advanced beyond the target by a prior allocation**.

### The allocation mechanism

From [SS-ADDRESS-ALLOC] / Finding 0065, link I-address allocation works as follows:

1. `upperbound` = `docISA.0.3.x` (one element-field past the link subspace)
2. `findpreviousisagr` returns the maximum existing address below that bound
3. If none exists: allocate at `docISA.0.2.1` (first link)
4. Otherwise: `tumblerincrement(max, 0, 1)` → `max + 0.1` (increment by 1 at the last significant digit)

This produces a strictly sequential series: `docISA.0.2.1`, `docISA.0.2.2`, `docISA.0.2.3`, …

### Why no structurally-valid address is skipped

The increment-by-1 mechanism (`rightshift=0` in `tumblerincrement`) guarantees there are no gaps under normal sequential operation. Every N ∈ {1, 2, 3, …} is reached in order before N+1 is allocated [INV-MONOTONIC]. The upper-bound search is also scoped: it cannot cross into element-field 3 or beyond, so no out-of-subtree allocation can pollute the link counter [Finding 0065, [PRE-ADDRESS-ALLOC]].

### The irreversibility caveat

[INV-NO-IADDR-REUSE] establishes that allocated addresses persist permanently in the granfilade (which is append-only, [FC-GRANF-ON-DELETE]). Since `findpreviousisagr` always returns the **current maximum** in the subtree, any address that exists in the link range — even a deleted one — sets the floor for future allocation. If some non-standard path had placed address `docISA.0.2.10` in the granfilade before addresses 2–9 were allocated, those would be permanently unreachable because subsequent calls would increment from 10 onward. [INV-MONOTONIC], [INV-NO-IADDR-REUSE].

Under well-formed sequential operation this cannot happen: each allocation is exactly `prev_max + 1`. The containment-check fix (Bug 0013, [PRE-ADDRESS-ALLOC]) closes the cross-boundary pollution path that could otherwise advance the subtree maximum illegitimately.

### Summary

Under the invariants the system actually enforces:

| Condition | Reachable? |
|-----------|-----------|
| Normal sequential MAKELINK calls | All addresses `docISA.0.2.N` for N≥1, in order |
| After K MAKELINKs, address K+1 | Yes — always the next allocation |
| Address M < K after K allocations | No — monotonic, no reuse [INV-NO-IADDR-REUSE] |
| Cross-subtree pollution (pre-fix) | Could skip addresses (Bug 0013) |

Every structurally-valid link address is reachable from a clean subtree. The allocator commits addresses one-at-a-time from the bottom up, so no prior commitment makes a higher address unreachable — it only prevents lower addresses from being revisited.
