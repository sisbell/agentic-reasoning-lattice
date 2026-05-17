// ASN-0034: T5 — ContiguousSubtrees
// If two tumblers a and c share a common prefix p, then every tumbler b
// lying between them in the lexicographic order also shares that prefix.
// Subtrees under a prefix occupy a contiguous interval on the tumbler line.
include "./CarrierSetDefinition.dfy"
include "./PrefixRelation.dfy"
include "./LexicographicOrder.dfy"
include "./NatStrictTotalOrder.dfy"

module ContiguousSubtrees {
  import opened CarrierSetDefinition
  import opened PrefixRelation
  import opened LexicographicOrder
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  ghost predicate TumblerLessOrEqual(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
  {
    a == b || LexicographicOrder.LexicographicOrder(a, b)
  }

  // Length bound: when a ≤ b ≤ c with both a and c extending p, then b's
  // length is at least |p|. Suppose not: then any T1 witness for a < b lies
  // strictly below |p|, forcing b to diverge from c on a shared-prefix
  // position — contradicting b ≤ c.
  lemma PrefixLengthBound(p: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(p) && InT(a) && InT(b) && InT(c)
    requires Length(p) >= 1
    requires PrefixOf(p, a)
    requires PrefixOf(p, c)
    requires TumblerLessOrEqual(a, b)
    requires TumblerLessOrEqual(b, c)
    ensures Length(p) <= Length(b)
  {
    if Length(b) < Length(p) {
      // a == b ruled out: Length(a) >= Length(p) > Length(b).
      assert a != b;
      assert LexicographicOrder.LexicographicOrder(a, b);

      var k :| 1 <= k
            && (forall i :: 1 <= i < k ==>
                  i <= Length(a) && i <= Length(b) &&
                  Component(a, i) == Component(b, i))
            && ((k <= Length(a) && k <= Length(b) &&
                 Less(Component(a, k), Component(b, k)))
                || (k == Length(a) + 1 && k <= Length(b)));

      // Case (ii) of a < b is impossible: Length(a) + 1 ≤ Length(b) < Length(p)
      // contradicts Length(a) ≥ Length(p).
      assert k <= Length(a) && k <= Length(b) &&
             Less(Component(a, k), Component(b, k));

      // k ≤ Length(b) < Length(p), so k is in the shared-prefix region with c.
      assert k <= Length(p);
      assert Component(a, k) == Component(p, k);
      assert Component(c, k) == Component(p, k);
      // Component(b, k) > Component(a, k) == Component(c, k).

      // Now b ≤ c forces a contradiction.
      if b == c {
        // Length(b) == Length(c) ≥ Length(p) > Length(b).
        assert false;
      } else {
        assert LexicographicOrder.LexicographicOrder(b, c);
        var k' :| 1 <= k'
              && (forall i :: 1 <= i < k' ==>
                    i <= Length(b) && i <= Length(c) &&
                    Component(b, i) == Component(c, i))
              && ((k' <= Length(b) && k' <= Length(c) &&
                   Less(Component(b, k'), Component(c, k')))
                  || (k' == Length(b) + 1 && k' <= Length(c)));

        if k' == Length(b) + 1 && k' <= Length(c) {
          // b is a prefix of c on positions 1..Length(b); k ≤ Length(b)
          // forces Component(b, k) == Component(c, k), contradicting >.
          assert k <= Length(b);
          assert Component(b, k) == Component(c, k);
          Irreflexive(Component(b, k));
          assert false;
        } else {
          assert k' <= Length(b) && k' <= Length(c) &&
                 Less(Component(b, k'), Component(c, k'));
          if k' < k {
            // Agreement before k' from both witnesses + shared prefix gives
            // Component(b, k') == Component(c, k'), contradicting <.
            assert Component(a, k') == Component(b, k');
            assert k' <= Length(p);
            assert Component(a, k') == Component(p, k');
            assert Component(c, k') == Component(p, k');
            assert Component(b, k') == Component(c, k');
            Irreflexive(Component(b, k'));
            assert false;
          } else if k' == k {
            // Less(b[k], c[k]) but a < b case gave Component(b, k) > Component(c, k).
            Asymmetric(Component(b, k), Component(c, k));
            assert false;
          } else {
            // k' > k: agreement before k' gives Component(b, k) == Component(c, k).
            assert Component(b, k) == Component(c, k);
            Irreflexive(Component(b, k));
            assert false;
          }
        }
      }
    }
  }

  // If a ≤ b ≤ c and both a and c agree with the same n-prefix, then b
  // agrees with that prefix on those positions too. The mismatch position,
  // combined with the LessThan witnesses, would land in the agreement region
  // of one of the witnesses and contradict prefix equality.
  lemma SandwichedPrefix(a: Tumbler, b: Tumbler, c: Tumbler, n: nat)
    requires InT(a) && InT(b) && InT(c)
    requires n <= Length(a) && n <= Length(b) && n <= Length(c)
    requires forall i :: 1 <= i <= n ==> Component(a, i) == Component(c, i)
    requires TumblerLessOrEqual(a, b)
    requires TumblerLessOrEqual(b, c)
    ensures forall i :: 1 <= i <= n ==> Component(b, i) == Component(a, i)
  {
    forall j | 1 <= j <= n
      ensures Component(b, j) == Component(a, j)
    {
      SandwichedAtPosition(a, b, c, n, j);
    }
  }

  // Pointwise version: b agrees with a at one shared-prefix position.
  lemma SandwichedAtPosition(a: Tumbler, b: Tumbler, c: Tumbler, n: nat, j: nat)
    requires InT(a) && InT(b) && InT(c)
    requires n <= Length(a) && n <= Length(b) && n <= Length(c)
    requires 1 <= j <= n
    requires forall i :: 1 <= i <= n ==> Component(a, i) == Component(c, i)
    requires TumblerLessOrEqual(a, b)
    requires TumblerLessOrEqual(b, c)
    ensures Component(b, j) == Component(a, j)
  {
    if a == b {
      // b inherits a's components.
    } else if b == c {
      assert Component(b, j) == Component(c, j) == Component(a, j);
    } else {
      assert LexicographicOrder.LexicographicOrder(a, b);
      assert LexicographicOrder.LexicographicOrder(b, c);

      var ka :| 1 <= ka
            && (forall i :: 1 <= i < ka ==>
                  i <= Length(a) && i <= Length(b) &&
                  Component(a, i) == Component(b, i))
            && ((ka <= Length(a) && ka <= Length(b) &&
                 Less(Component(a, ka), Component(b, ka)))
                || (ka == Length(a) + 1 && ka <= Length(b)));

      if ka == Length(a) + 1 && ka <= Length(b) {
        // a is a "case-(ii) prefix" of b on positions 1..Length(a) ≥ n.
        assert j <= n <= Length(a);
        assert j < ka;
        assert Component(a, j) == Component(b, j);
      } else {
        assert ka <= Length(a) && ka <= Length(b) &&
               Less(Component(a, ka), Component(b, ka));

        if ka > j {
          assert Component(a, j) == Component(b, j);
        } else {
          // ka ≤ j ≤ n; derive Component(b, ka) > Component(c, ka).
          assert ka <= n;
          assert Component(a, ka) == Component(c, ka);
          // Component(b, ka) > Component(a, ka) == Component(c, ka).

          var kb :| 1 <= kb
                && (forall i :: 1 <= i < kb ==>
                      i <= Length(b) && i <= Length(c) &&
                      Component(b, i) == Component(c, i))
                && ((kb <= Length(b) && kb <= Length(c) &&
                     Less(Component(b, kb), Component(c, kb)))
                    || (kb == Length(b) + 1 && kb <= Length(c)));

          if kb == Length(b) + 1 && kb <= Length(c) {
            // b is a "case-(ii) prefix" of c, so b[ka] == c[ka].
            assert ka <= Length(b);
            assert ka < kb;
            assert Component(b, ka) == Component(c, ka);
            Irreflexive(Component(b, ka));
            assert false;
          } else {
            assert kb <= Length(b) && kb <= Length(c) &&
                   Less(Component(b, kb), Component(c, kb));

            if kb < ka {
              // a, b agree before ka, so a[kb] == b[kb].
              // a, c agree on 1..n; kb < ka ≤ n, so a[kb] == c[kb].
              assert Component(a, kb) == Component(b, kb);
              assert kb <= n;
              assert Component(a, kb) == Component(c, kb);
              assert Component(b, kb) == Component(c, kb);
              Irreflexive(Component(b, kb));
              assert false;
            } else if kb == ka {
              // Less(b[ka], c[ka]) but b[ka] > c[ka].
              Asymmetric(Component(b, ka), Component(c, ka));
              assert false;
            } else {
              // kb > ka: b, c agree before kb, so b[ka] == c[ka].
              assert Component(b, ka) == Component(c, ka);
              Irreflexive(Component(b, ka));
              assert false;
            }
          }
        }
      }
    }
  }

  // T5 — ContiguousSubtrees.
  lemma ContiguousSubtrees(p: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(p) && InT(a) && InT(b) && InT(c)
    requires Length(p) >= 1
    requires PrefixOf(p, a)
    requires PrefixOf(p, c)
    requires TumblerLessOrEqual(a, b)
    requires TumblerLessOrEqual(b, c)
    ensures PrefixOf(p, b)
  {
    PrefixLengthBound(p, a, b, c);
    var n := Length(p);
    // a and c both extend p, so they agree on positions 1..n.
    assert forall i :: 1 <= i <= n ==> Component(a, i) == Component(p, i);
    assert forall i :: 1 <= i <= n ==> Component(c, i) == Component(p, i);
    SandwichedPrefix(a, b, c, n);
  }
}
