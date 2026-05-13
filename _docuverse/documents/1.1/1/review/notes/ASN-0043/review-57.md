# Review of ASN-0043

## REVISE

### Issue 1: Chain-start premise for `home(a) = d` not formally captured

**ASN-0043, Home and Ownership**: "The equality `home(a) = d` for the creating document `d` is structural: by L1c, the T10a-conforming allocator chain producing `a` starts from `d` and proceeded entirely by `inc` steps that preserve positions 1..#d."

**ASN-0043, L11b proof**: "By L1c on `Σ`, the existing link `a` was produced by a T10a-conforming allocator chain emanating from `home(a)`'s link subspace; `a` was the frontier of that allocator at the moment of its own allocation event."

**Problem**: L1c's formal statement says only that link allocation operates within T10a (sibling via `inc(·, 0)`, child-spawning via `inc(·, k')` with `k' ∈ {1, 2}`). It does NOT formally state that the chain producing a particular link `a` starts at, or emanates from, `home(a)`. L1a is similarly restricted to membership: `home(a) ∈ dom(Σ.M)`. The chain-prefix-preservation argument requires the chain to reach `home(a)` at some intermediate stage with all subsequent steps at length > `#home(a)` — only then are positions 1..#home(a) preserved through to `a`. This premise is not formally entailed by L1a + L1c.

The Home and Ownership section also asserts a general consequence: "For links `a₁, a₂` allocated under distinct documents `d₁ ≠ d₂`, chain-prefix-preservation gives `home(a₁) = d₁` and `home(a₂) = d₂`." This depends on the same unstated premise — the general claim that `home(a)` IS the document that allocated `a` (not merely some allocated document containing `a`'s prefix) cannot be derived from the formal invariants alone.

The L9 proof avoids this gap because it explicitly constructs the chain to start at `d'`, so chain-prefix-preservation applies locally. But the Home and Ownership section's general claim needs the global premise.

**Required**: Strengthen L1c (or add a clause to L1a) to formally state the chain-start condition — for example, "for every `a ∈ dom(Σ.L)`, the T10a-conforming allocator chain producing `a` is produced from `home(a)` by a finite sequence of `inc(·, k')` steps whose first step has length ≤ #home(a) and whose subsequent steps operate at length > #home(a)." With this, chain-prefix-preservation follows rigorously rather than from prose intuition.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
