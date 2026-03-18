include "LinkStore.dfy"

// L9 — TypeGhostPermission
module TypeGhostPermission {
  import opened TumblerAlgebra
  import TumblerAddition
  import LinkStore

  // --- Freshness machinery ---

  // Find a natural number >= k not in finite set S
  function FreshNatAbove(S: set<nat>, k: nat): nat
    ensures FreshNatAbove(S, k) >= k
    ensures FreshNatAbove(S, k) !in S
    decreases S
  {
    if k !in S then k
    else FreshNatAbove(S - {k}, k + 1)
  }

  // Project first-component values of single-component tumblers
  function SingleComponents(S: set<Tumbler>): set<nat> {
    set t | t in S && |t.components| == 1 :: t.components[0]
  }

  // A single-component tumbler whose value is not in the projection is fresh
  lemma SingleComponentFresh(S: set<Tumbler>, n: nat)
    requires n !in SingleComponents(S)
    ensures Tumbler([n]) !in S
  {
    if Tumbler([n]) in S {
      assert n in SingleComponents(S);
    }
  }

  // --- L9 ---

  // Ghost types are permitted: for any finite store domains, there exists
  // a well-formed link whose type endset covers an address outside both domains.
  //
  // The witness constructs a link (∅, ∅, {(g, [1])}) at a fresh address a,
  // where g is a fresh single-component tumbler outside domL ∪ domC.
  // Since g ∈ coverage({(g, [1])}) and g ∉ domC ∪ (domL ∪ {a}), the type
  // endset references a "ghost" address.
  lemma TypeGhostPermission(domL: set<Tumbler>, domC: set<Tumbler>)
    ensures exists a: Tumbler, link: LinkStore.Link, sp: LinkStore.Span ::
      a !in domL &&
      LinkStore.WellFormedLink(link) &&
      sp in link.typ &&
      LinkStore.WellFormedSpan(sp) &&
      LessThan(sp.start, TumblerAdd(sp.start, sp.length)) &&
      sp.start !in domC && sp.start !in (domL + {a})
  {
    var proj := SingleComponents(domL + domC);
    var na := FreshNatAbove(proj, 1);
    var ng := FreshNatAbove(proj, na + 1);
    var a := Tumbler([na]);
    var g := Tumbler([ng]);

    SingleComponentFresh(domL + domC, na);
    SingleComponentFresh(domL + domC, ng);

    var disp := Tumbler([1]);
    var sp := LinkStore.Span(g, disp);
    var link := LinkStore.Link({}, {}, {sp});

    // WellFormedSpan: PositiveTumbler([1]) with ActionPoint 0 < 1 = |g|
    assert disp.components[0] == 1;

    // g < g ⊕ disp: at position 0, ng < ng + 1
    LessThanIntro(g, TumblerAdd(g, disp), 0);
  }
}
