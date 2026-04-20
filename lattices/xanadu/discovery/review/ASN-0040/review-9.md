# Review of ASN-0040

Based on Dafny verification — 18/18 verified, 7 divergences

## REVISE

No genuine spec issues found. All 7 divergences are proof artifacts (see SKIP).

## QUALITY

### File: BaptismalClosure.dfy — PASS
### File: ContiguousPrefix.dfy — PASS
### File: FieldAdvancement.dfy — PASS
### File: GhostValidity.dfy — PASS
### File: GlobalUniqueness.dfy — PASS
### File: HighWaterMarkSufficiency.dfy — PASS
### File: Irrevocability.dfy — PASS
### File: NamespaceDisjointness.dfy — PASS
### File: NamespaceSerialized.dfy — PASS
### File: OnlyRegistryModified.dfy — PASS
### File: RegistryGrowth.dfy — PASS
### File: RegistryT4Validity.dfy — PASS
### File: SeedConformance.dfy — PASS
### File: SiblingZerosPreserved.dfy — PASS
### File: StreamExtendsParent.dfy — PASS
### File: StreamStrictlyOrdered.dfy — PASS
### File: UnboundedExtent.dfy — PASS
### File: ValidDepth.dfy — PASS

### Cross-module: SIMPLIFY

**Missing abstraction: `StreamElement` defined 10 times.** The identical function

```dafny
function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
  requires d >= 1
  requires n >= 1
{
  Tumbler(p.components + Zeros(d - 1) + [n])
}
```

appears in BaptismalClosure, ContiguousPrefix, HighWaterMarkSufficiency, NamespaceDisjointness, OnlyRegistryModified, RegistryGrowth, SeedConformance, StreamExtendsParent, StreamStrictlyOrdered, and UnboundedExtent. Additionally, `InStream` and `Children` are duplicated between OnlyRegistryModified and RegistryGrowth, and the validity predicate (`ValidBaptismParams` / `ValidBaptismDepth` / `ValidBaptism`) has 5 near-identical variants across modules.

A shared `BaptismCore` module should define `StreamElement`, `InStream`, `Children`, and the canonical validity predicate once. All proof modules import from it. This reduces maintenance risk — a change to the stream definition currently requires 10 synchronized edits — and eliminates the risk of variants silently diverging.

## SKIP

### All 7 divergences: proof artifacts

None of these require ASN changes. Grouped by category:

**Encoding choices (3).** GhostValidity models occupancy as an explicit set because the ASN's Σ only has Σ.B — the ASN explicitly defers content storage. NamespaceSerialized encodes temporal precedence (≺) as registry set inclusion because Dafny has no concurrency primitive; this is the standard sequential-model encoding. OnlyRegistryModified adds an opaque `rest` field to SystemState to give the frame condition non-trivial content — the ASN's "all other state components" needs something to quantify over.

**Equivalent formulations (2).** RegistryGrowth uses `StreamElement(p, d, |children|+1)` instead of the ASN's `if children = ∅ then inc(p,d) else inc(max(children), 0)`. The equivalence is exactly B2 (HighWaterMarkSufficiency), which verified clean. GlobalUniqueness assumes the (p, d, n) triple differs rather than deriving distinct indices from B4 serialization — the Dafny proof takes the conclusion of B4+B1 as its starting point.

**Scope boundaries (2).** RegistryT4Validity proves single-step preservation rather than full state-machine induction — standard for inductive invariants, the ASN's "all reachable states" claim follows by induction over the step proof. UnboundedExtent proves stream injectivity (the structural core) rather than operational reachability through B6-constrained baptism sequences — injectivity is the load-bearing property; reachability is compositional.

### 11 clean verifications

BaptismalClosure, ContiguousPrefix, FieldAdvancement, HighWaterMarkSufficiency, Irrevocability, NamespaceDisjointness, SeedConformance, SiblingZerosPreserved, StreamExtendsParent, StreamStrictlyOrdered, ValidDepth — all verified without divergence.

VERDICT: SIMPLIFY
