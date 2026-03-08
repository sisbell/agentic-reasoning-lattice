module Foundation {
  import opened TumblerAlgebra

  // -------------------------------------------------------------------------
  // Type aliases
  // -------------------------------------------------------------------------

  // I-space address is a tumbler
  type IAddr = Tumbler

  // Abstract content value — decidable equality, compilable
  datatype Value = Value(raw: nat)

  // Document = its orgl I-address
  type DocId = IAddr

  // -------------------------------------------------------------------------
  // VPos — tagged ordinal in V-space
  // -------------------------------------------------------------------------

  datatype VPos = TextPos(ord: nat) | LinkPos(ord: nat)

  function Ord(q: VPos): nat {
    match q
    case TextPos(n) => n
    case LinkPos(n) => n
  }

  predicate IsTextPos(q: VPos) {
    q.TextPos?
  }

  predicate IsLinkPos(q: VPos) {
    q.LinkPos?
  }

  // Valid VPos: ordinal > 0 (1-indexed)
  predicate ValidVPos(q: VPos) {
    Ord(q) > 0
  }

  // Ordering within same subspace
  ghost predicate VPosLt(q1: VPos, q2: VPos) {
    (IsTextPos(q1) && IsTextPos(q2) && Ord(q1) < Ord(q2)) ||
    (IsLinkPos(q1) && IsLinkPos(q2) && Ord(q1) < Ord(q2))
  }

  ghost predicate VPosLe(q1: VPos, q2: VPos) {
    q1 == q2 || VPosLt(q1, q2)
  }

  // VPos arithmetic — shift within same subspace tag
  function VPosShiftAdd(q: VPos, n: nat): VPos {
    match q
    case TextPos(x) => TextPos(x + n)
    case LinkPos(x) => LinkPos(x + n)
  }

  function VPosShiftSub(q: VPos, n: nat): VPos
    requires Ord(q) >= n
  {
    match q
    case TextPos(x) => TextPos(x - n)
    case LinkPos(x) => LinkPos(x - n)
  }

  // -------------------------------------------------------------------------
  // State
  // -------------------------------------------------------------------------

  datatype State = State(
    iota: map<IAddr, Value>,
    docs: set<DocId>,
    vmap: map<DocId, map<VPos, IAddr>>
  )

  // -------------------------------------------------------------------------
  // Helpers
  // -------------------------------------------------------------------------

  // Allocated addresses = dom(iota)
  function Allocated(s: State): set<IAddr> {
    s.iota.Keys
  }

  // Text ordinals in document d
  function TextOrdinals(s: State, d: DocId): set<nat>
    requires d in s.vmap
  {
    set q | q in s.vmap[d] && IsTextPos(q) :: Ord(q)
  }

  // Link ordinals in document d
  function LinkOrdinals(s: State, d: DocId): set<nat>
    requires d in s.vmap
  {
    set q | q in s.vmap[d] && IsLinkPos(q) :: Ord(q)
  }

  // Count of text positions in document d
  function TextCount(s: State, d: DocId): nat
    requires d in s.vmap
  {
    |TextOrdinals(s, d)|
  }

  // Count of link positions in document d
  function LinkCount(s: State, d: DocId): nat
    requires d in s.vmap
  {
    |LinkOrdinals(s, d)|
  }

  // {1, ..., n}
  function RangeSet(n: nat): set<nat> {
    set i {:trigger i + 0} | 1 <= i <= n
  }

  // Next text position to allocate in document d
  function NextTextPos(s: State, d: DocId): VPos
    requires d in s.vmap
  {
    TextPos(TextCount(s, d) + 1)
  }

  // Next link position to allocate in document d
  function NextLinkPos(s: State, d: DocId): VPos
    requires d in s.vmap
  {
    LinkPos(LinkCount(s, d) + 1)
  }

  // Address a is visible in document d
  ghost predicate VisibleInDoc(a: IAddr, d: DocId, s: State)
    requires d in s.vmap
  {
    exists q :: q in s.vmap[d] && s.vmap[d][q] == a
  }

  // Address a is visible somewhere in the system
  ghost predicate VisibleInSystem(a: IAddr, s: State) {
    exists d :: d in s.docs && d in s.vmap && VisibleInDoc(a, d, s)
  }

  // -------------------------------------------------------------------------
  // Well-formedness predicates
  // -------------------------------------------------------------------------

  // J0 — V-space references only allocated content
  ghost predicate J0(s: State) {
    forall d :: d in s.docs && d in s.vmap ==>
      forall q :: q in s.vmap[d] ==> s.vmap[d][q] in Allocated(s)
  }

  // J1 — Text ordinals form {1, ..., k} per document
  ghost predicate J1(s: State) {
    forall d :: d in s.docs && d in s.vmap ==>
      TextOrdinals(s, d) == RangeSet(TextCount(s, d))
  }

  // J2 — Link ordinals form {1, ..., m} per document
  ghost predicate J2(s: State) {
    forall d :: d in s.docs && d in s.vmap ==>
      LinkOrdinals(s, d) == RangeSet(LinkCount(s, d))
  }

  // WellFormed — conjunction of structural invariants
  ghost predicate WellFormed(s: State) {
    // All documents are allocated addresses
    s.docs <= Allocated(s) &&
    // All documents have vmap entries
    (forall d :: d in s.docs ==> d in s.vmap) &&
    // All VPos entries are valid (ordinal > 0)
    (forall d :: d in s.docs ==>
      forall q :: q in s.vmap[d] ==> ValidVPos(q)) &&
    // Invariants
    J0(s) && J1(s) && J2(s)
  }
}
