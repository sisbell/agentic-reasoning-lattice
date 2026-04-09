include "LinkStore.dfy"

// L11b — NonInjectivity
module NonInjectivity {
  import opened LinkStore
  import opened TumblerAlgebra

  // Fresh address: for any finite set, a tumbler outside it exists.
  // Constructs Tumbler([m]) for some m not in S.
  lemma FreshAddress(S: set<Tumbler>, n: nat)
    ensures exists m: nat :: m >= n && Tumbler([m]) !in S
    decreases |S|
  {
    if Tumbler([n]) !in S {
    } else {
      FreshAddress(S - {Tumbler([n])}, n + 1);
    }
  }

  // DIVERGENCE: The ASN quantifies over states satisfying L0–L14 and requires
  // the extended state Σ' to also satisfy L0–L14. This model captures the
  // structural core: a fresh address exists (by unboundedness of T) and can
  // carry the same link value. Invariant preservation would require modeling
  // the full L0–L14 suite and T9 forward allocation.
  lemma NonInjectivity(store: Store, a: Tumbler)
    requires a in store
    ensures exists a': Tumbler, store': Store ::
      a' != a &&
      a' in store' &&
      store'[a'] == store[a] &&
      (forall x :: x in store ==> x in store' && store'[x] == store[x])
  {
    FreshAddress(store.Keys, 0);
    var m :| m >= 0 && Tumbler([m]) !in store.Keys;
    var a' := Tumbler([m]);
    var store' := store[a' := store[a]];
    assert a' != a;
    assert a' in store';
    assert store'[a'] == store[a];
    assert forall x :: x in store ==> x in store' && store'[x] == store[x];
  }
}
