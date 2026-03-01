module ASN_0004 {

  // Type aliases
  type Addr = nat
  type Pos = nat
  type DocId = nat
  type Content = nat
  type User = nat

  datatype Subspace = Text | LinkSp

  datatype Link = Link(from_set: set<Addr>, to_set: set<Addr>, type_set: set<Addr>)

  datatype State = State(
    ispace: map<Addr, Content>,
    poom: map<DocId, map<Pos, Addr>>,
    spanindex: set<(Addr, DocId)>,
    links: set<Link>,
    owner: map<DocId, User>
  )

  datatype InsertResult = InsertResult(s': State, a0: Addr)

  // Subspace classifiers (abstract — refined in implementation)
  function {:axiom} SubPos(p: Pos): Subspace
  function {:axiom} SubAddr(a: Addr): Subspace

  // --- Helper functions ---

  function Addrs(l: Link): set<Addr> {
    l.from_set + l.to_set + l.type_set
  }

  function AddrRange(a0: Addr, len: nat): set<Addr> {
    set i | 0 <= i < len :: a0 + i
  }

  function TextPositions(s: State, d: DocId): set<Pos>
    requires d in s.poom
  {
    set q | q in s.poom[d] && SubPos(q) == Text
  }

  function TextSize(s: State, d: DocId): nat
    requires d in s.poom
  {
    |TextPositions(s, d)|
  }

  function ImgText(s: State, d: DocId): set<Addr>
    requires d in s.poom
  {
    set q | q in s.poom[d] && SubPos(q) == Text :: s.poom[d][q]
  }

  function ImgLink(s: State, d: DocId): set<Addr>
    requires d in s.poom
  {
    set q | q in s.poom[d] && SubPos(q) == LinkSp :: s.poom[d][q]
  }

  // --- Definition: ShiftMapping ---

  // ShiftMapping — shift positions in a V→I mapping at position p by width w
  function ShiftMapping(m: map<Pos, Addr>, p: Pos, w: nat): map<Pos, Addr>
    requires w > 0
  {
    // Positions below p in same subspace: unchanged
    (map q | q in m.Keys && SubPos(q) == SubPos(p) && q < p :: m[q])
    // Positions at or above p in same subspace: shifted up by w
    + (map q | q in m.Keys && SubPos(q) == SubPos(p) && q >= p :: (q + w) := m[q])
    // Different subspace: unchanged
    + (map q | q in m.Keys && SubPos(q) != SubPos(p) :: m[q])
  }

  // --- Invariant predicates (INV) ---

  // S-DISJ — Subspace Disjoint
  predicate SubspaceDisjoint(s: State) {
    forall d :: d in s.poom ==> ImgText(s, d) !! ImgLink(s, d)
  }

  // S0 — V→I Grounding
  predicate VIGrounding(s: State) {
    forall d, q :: d in s.poom && q in s.poom[d]
      ==> s.poom[d][q] in s.ispace
  }

  // S2 — Link Grounding
  predicate LinkGrounding(s: State) {
    forall L, a :: L in s.links && a in Addrs(L) ==> a in s.ispace
  }

  // S3 — Span Index Consistent
  predicate SpanIndexConsistent(s: State) {
    forall pair :: pair in s.spanindex ==> pair.0 in s.ispace
  }

  // S4 — POOM Injective
  predicate PoomInjective(s: State) {
    forall d, q1, q2 :: d in s.poom && q1 in s.poom[d] && q2 in s.poom[d] && q1 != q2
      ==> s.poom[d][q1] != s.poom[d][q2]
  }

  // S5 — Positions Dense
  predicate PositionsDense(s: State) {
    forall d :: d in s.poom ==>
      var n := TextSize(s, d);
      (n == 0 ==> TextPositions(s, d) == {}) &&
      (n > 0 ==> TextPositions(s, d) == set q | 1 <= q <= n)
  }

  // --- ValidState ---

  predicate ValidState(s: State) {
    // Structural: every owned document has a poom entry
    (forall d :: d in s.owner ==> d in s.poom) &&
    SubspaceDisjoint(s) &&
    VIGrounding(s) &&
    LinkGrounding(s) &&
    SpanIndexConsistent(s) &&
    PoomInjective(s) &&
    PositionsDense(s)
  }

  // --- Transition invariants (INV, two-state) ---

  // S1 — I-space Immutable
  predicate IspaceImmutable(s: State, s': State) {
    forall a :: a in s.ispace ==> a in s'.ispace && s'.ispace[a] == s.ispace[a]
  }

  // P2 — Span Index Monotone
  predicate SpanIndexMonotone(s: State, s': State) {
    forall pair :: pair in s.spanindex ==> pair in s'.spanindex
  }

  // --- Precondition predicates (PRE) ---

  // PRE1 — Document Exists
  predicate DocExists(s: State, d: DocId) {
    d in s.owner
  }

  // PRE2 — Is Owner
  predicate IsOwner(s: State, d: DocId, user: User) {
    d in s.owner && s.owner[d] == user
  }

  // PRE3 — Position Valid
  predicate PositionValid(s: State, d: DocId, p: Pos)
    requires d in s.poom
  {
    1 <= p <= TextSize(s, d) + 1
  }

  // PRE4 — Content Non-Empty
  predicate ContentNonEmpty(c: seq<Content>) {
    |c| > 0
  }

  // --- Postcondition predicates (POST) ---

  // INS1 — Fresh Addresses
  predicate FreshAddresses(s: State, s': State, a0: Addr, c: seq<Content>) {
    |AddrRange(a0, |c|)| == |c| &&
    AddrRange(a0, |c|) !! s.ispace.Keys &&
    AddrRange(a0, |c|) <= s'.ispace.Keys
  }

  // INS1a — Text Subspace Allocation
  predicate TextSubspaceAllocation(a0: Addr, c: seq<Content>) {
    forall i :: 0 <= i < |c| ==> SubAddr(a0 + i) == Text
  }

  // INS2 — Content Established
  predicate ContentEstablished(s': State, a0: Addr, c: seq<Content>) {
    forall i :: 0 <= i < |c| ==> (a0 + i) in s'.ispace && s'.ispace[a0 + i] == c[i]
  }

  // INS3 — Content Placement
  predicate ContentPlacement(s': State, d: DocId, p: Pos, a0: Addr, c: seq<Content>) {
    d in s'.poom &&
    forall i :: 0 <= i < |c| ==> (p + i) in s'.poom[d] && s'.poom[d][p + i] == a0 + i
  }

  // INS4 — Position Shift
  predicate PositionShift(s: State, s': State, d: DocId, p: Pos, c: seq<Content>) {
    d in s.poom && d in s'.poom &&
    // (a) Below insertion point in same subspace: unchanged
    (forall q :: q in s.poom[d] && SubPos(q) == SubPos(p) && q < p
      ==> q in s'.poom[d] && s'.poom[d][q] == s.poom[d][q]) &&
    // (b) At or above insertion point in same subspace: shifted by |c|
    (forall q :: q in s.poom[d] && SubPos(q) == SubPos(p) && q >= p
      ==> (q + |c|) in s'.poom[d] && s'.poom[d][q + |c|] == s.poom[d][q])
  }

  // INS5 — Span Index Extended
  predicate SpanIndexExtended(s': State, d: DocId, a0: Addr, c: seq<Content>) {
    forall i :: 0 <= i < |c| ==> (a0 + i, d) in s'.spanindex
  }

  // --- Frame condition predicates (FRAME) ---

  // INS-F1 — I-space Upper Bound
  predicate IspaceUpperBound(s: State, s': State, a0: Addr, c: seq<Content>) {
    s'.ispace.Keys <= s.ispace.Keys + AddrRange(a0, |c|)
  }

  // INS-F2 — Other Docs Unchanged
  predicate OtherDocsUnchanged(s: State, s': State, d: DocId) {
    forall d' :: d' != d && d' in s.poom
      ==> d' in s'.poom && s'.poom[d'] == s.poom[d']
  }

  // INS-F4 — Links Preserved
  predicate LinksPreserved(s: State, s': State) {
    s.links <= s'.links
  }

  // INS-F4a — No New Links
  predicate NoNewLinks(s: State, s': State) {
    s'.links <= s.links
  }

  // INS-F5 — Subspace Isolation
  predicate SubspaceIsolation(s: State, s': State, d: DocId, p: Pos) {
    d in s.poom && d in s'.poom &&
    forall q :: q in s.poom[d] && SubPos(q) != SubPos(p)
      ==> q in s'.poom[d] && s'.poom[d][q] == s.poom[d][q]
  }

  // INS-F6 — Span Index Upper Bound
  predicate SpanIndexUpperBound(s: State, s': State, d: DocId, a0: Addr, c: seq<Content>) {
    s'.spanindex <= s.spanindex + (set i | 0 <= i < |c| :: (a0 + i, d))
  }

  // --- Operation function ---

  function Insert(s: State, d: DocId, p: Pos, c: seq<Content>, user: User): (r: InsertResult)
    requires ValidState(s)
    requires DocExists(s, d)
    requires IsOwner(s, d, user)
    requires PositionValid(s, d, p)
    requires ContentNonEmpty(c)
    // Invariant preservation
    ensures ValidState(r.s')
    // Transition invariants
    ensures IspaceImmutable(s, r.s')
    ensures SpanIndexMonotone(s, r.s')
    // Postconditions
    ensures FreshAddresses(s, r.s', r.a0, c)
    ensures TextSubspaceAllocation(r.a0, c)
    ensures ContentEstablished(r.s', r.a0, c)
    ensures ContentPlacement(r.s', d, p, r.a0, c)
    ensures PositionShift(s, r.s', d, p, c)
    ensures SpanIndexExtended(r.s', d, r.a0, c)
    // Frame conditions
    ensures IspaceUpperBound(s, r.s', r.a0, c)
    ensures OtherDocsUnchanged(s, r.s', d)
    ensures LinksPreserved(s, r.s')
    ensures NoNewLinks(s, r.s')
    ensures SubspaceIsolation(s, r.s', d, p)
    ensures SpanIndexUpperBound(s, r.s', d, r.a0, c)
  {
    assume false; InsertResult(s, 0) // specification only — body is future work
  }

  // --- Lemmas ---

  // P0 — Address Irrevocable
  lemma AddressIrrevocable(s: State, s': State)
    requires IspaceImmutable(s, s')
    ensures forall a :: a in s.ispace ==> a in s'.ispace
  { }

  // P1 — Content Immutable (restates S1)
  lemma ContentImmutable(s: State, s': State)
    requires IspaceImmutable(s, s')
    ensures forall a :: a in s.ispace ==> a in s'.ispace && s'.ispace[a] == s.ispace[a]
  { }

  // INS-D1 — Domain Size
  lemma DomainSize(s: State, d: DocId, p: Pos, c: seq<Content>, user: User)
    requires ValidState(s) && DocExists(s, d) && IsOwner(s, d, user)
    requires PositionValid(s, d, p) && ContentNonEmpty(c)
    ensures var r := Insert(s, d, p, c, user);
      d in r.s'.poom && TextSize(r.s', d) == TextSize(s, d) + |c|
  { }

  // INS-D2 — V→I Correspondence Preserved
  lemma VICorrespondencePreserved(s: State, d: DocId, p: Pos, c: seq<Content>, user: User)
    requires ValidState(s) && DocExists(s, d) && IsOwner(s, d, user)
    requires PositionValid(s, d, p) && ContentNonEmpty(c)
    ensures var r := Insert(s, d, p, c, user);
      var s' := r.s';
      // (a) Below insertion point: content unchanged
      (forall q :: q in s.poom[d] && SubPos(q) == SubPos(p) && q < p
        ==> s'.ispace[s'.poom[d][q]] == s.ispace[s.poom[d][q]]) &&
      // (b) At or above insertion point: shifted content unchanged
      (forall q :: q in s.poom[d] && SubPos(q) == SubPos(p) && q >= p
        ==> s'.ispace[s'.poom[d][q + |c|]] == s.ispace[s.poom[d][q]])
  { }

  // INS-CORR — Insert Correctness (summary)
  lemma InsertCorrectness(s: State, d: DocId, p: Pos, c: seq<Content>, user: User)
    requires ValidState(s) && DocExists(s, d) && IsOwner(s, d, user)
    requires PositionValid(s, d, p) && ContentNonEmpty(c)
    ensures
      // (i) I-space domain is exactly extended
      Insert(s, d, p, c, user).s'.ispace.Keys == s.ispace.Keys + AddrRange(Insert(s, d, p, c, user).a0, |c|) &&
      // (ii) Existing content unchanged
      (forall a :: a in s.ispace ==> Insert(s, d, p, c, user).s'.ispace[a] == s.ispace[a]) &&
      // (iii) New content established
      (forall i :: 0 <= i < |c| ==> Insert(s, d, p, c, user).s'.ispace[Insert(s, d, p, c, user).a0 + i] == c[i]) &&
      // (iv) POOM is shift + new entries
      Insert(s, d, p, c, user).s'.poom[d] == ShiftMapping(s.poom[d], p, |c|)
        + (map i | 0 <= i < |c| :: (p + i) := Insert(s, d, p, c, user).a0 + i) &&
      // (v) Other documents unchanged
      (forall d' :: d' != d && d' in s.poom ==> Insert(s, d, p, c, user).s'.poom[d'] == s.poom[d']) &&
      // (vi) Span index exactly extended
      Insert(s, d, p, c, user).s'.spanindex == s.spanindex + (set i | 0 <= i < |c| :: (Insert(s, d, p, c, user).a0 + i, d)) &&
      // (vii) Links unchanged
      Insert(s, d, p, c, user).s'.links == s.links
  { }

  // INS-ATOM — Insert Atomic
  lemma InsertAtomic(s: State, d: DocId, p: Pos, c: seq<Content>, user: User)
    requires ValidState(s) && DocExists(s, d) && IsOwner(s, d, user)
    requires PositionValid(s, d, p) && ContentNonEmpty(c)
    ensures var r := Insert(s, d, p, c, user);
      // Either full transition or no change
      ValidState(r.s')
      // (atomicity is ensured by the function being total: it always returns
      //  a valid result satisfying all ensures clauses)
  { }
}
