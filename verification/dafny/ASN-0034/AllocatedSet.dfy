// ASN-0034: AllocatedSet — LEMMA (definition)
// Defines the allocation state model (State, Activated, DomState, Allocated)
// and proves: persistence of activation, domain inclusion, initial-segment
// structure, frame condition, and forward-ordering transfer.
include "./AllocatorDiscipline.dfy"
include "./LexicographicOrder.dfy"
include "./EnumerationInjectivity.dfy"
include "./CarrierSetDefinition.dfy"

module AllocatedSet {
  import opened AllocatorDiscipline
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened LexicographicOrder
  import opened EnumerationInjectivity

  // State: pair (activated-allocator set, sibling-count map).
  // count is defined exactly on act; every activated allocator conforms.
  datatype State = State(act: set<Allocator>, count: map<Allocator, nat>)

  ghost predicate ValidState(s: State) {
    (forall a :: (a in s.act) <==> (a in s.count)) &&
    (forall a :: a in s.act ==> AllocatorDiscipline.AllocatorDiscipline(a))
  }

  // activated(A, s) — projection of the act component.
  ghost predicate Activated(a: Allocator, s: State) {
    a in s.act
  }

  // domₛ(A) as a sequence: {SiblingAt(A,0), …, SiblingAt(A,count[A])}.
  ghost function DomStateSeq(a: Allocator, s: State): seq<Tumbler>
    requires Activated(a, s) && a in s.count
  {
    seq(s.count[a] + 1, i => if 0 <= i then SiblingAt(a, i as nat) else BaseAddress(a))
  }

  // domₛ(A) as a set: initial segment when activated, ∅ otherwise.
  ghost function DomState(a: Allocator, s: State): set<Tumbler>
    requires ValidState(s)
  {
    if !Activated(a, s) then {}
    else set t | t in DomStateSeq(a, s)
  }

  // ⋃ { domₛ(A) : A ∈ act } — union over a finite set of activated allocators.
  ghost function UnionDomState(act: set<Allocator>, s: State): set<Tumbler>
    requires ValidState(s)
    requires forall a :: a in act ==> Activated(a, s)
    decreases act
  {
    if act == {} then {}
    else
      var a :| a in act;
      DomState(a, s) + UnionDomState(act - {a}, s)
  }

  // allocated(s) = ⋃ { domₛ(A) : activated(A, s) }
  ghost function Allocated(s: State): set<Tumbler>
    requires ValidState(s)
  {
    UnionDomState(s.act, s)
  }

  // --- Transition shapes ---

  // T1: sibling increment of A ∈ Act(s) — extends A's count by 1.
  ghost predicate T1Step(s: State, s': State, a: Allocator)
    requires ValidState(s)
  {
    Activated(a, s) &&
    s'.act == s.act &&
    s'.count == s.count[a := s.count[a] + 1]
  }

  // T2: child spawn of A ∉ Act(s) — activates A with count 0.
  ghost predicate T2Step(s: State, s': State, a: Allocator)
    requires ValidState(s)
  {
    !Activated(a, s) &&
    AllocatorDiscipline.AllocatorDiscipline(a) &&
    (match a
       case RootAllocator(_) => false
       case ChildAllocator(p, sp, k) =>
         Activated(p, s) &&
         sp in DomState(p, s) &&
         (k == 1 || k == 2)) &&
    s'.act == s.act + {a} &&
    s'.count == s.count[a := 0]
  }

  // T3: non-allocating — state is unchanged.
  ghost predicate T3Step(s: State, s': State) {
    s'.act == s.act && s'.count == s.count
  }

  // --- Postconditions ---

  // Persistence of activation: Act(s) ⊆ Act(s') for every admissible step.
  lemma PersistenceOfActivation(s: State, s': State, b: Allocator)
    requires ValidState(s)
    requires Activated(b, s)
    requires (exists a :: T1Step(s, s', a)) || (exists a :: T2Step(s, s', a)) || T3Step(s, s')
    ensures Activated(b, s')
  { }

  // No spontaneous activation: a non-spawn step cannot activate b.
  lemma NoSpontaneousActivation(s: State, s': State, b: Allocator)
    requires ValidState(s)
    requires !Activated(b, s)
    requires (exists a :: T1Step(s, s', a)) ||
             (exists a :: T2Step(s, s', a) && a != b) ||
             T3Step(s, s')
    ensures !Activated(b, s')
  {
    if exists a :: T2Step(s, s', a) && a != b {
      var a :| T2Step(s, s', a) && a != b;
    }
  }

  // Domain inclusion: every element of domₛ(A) lies in dom(A).
  lemma DomStateIncluded(a: Allocator, s: State, t: Tumbler)
    requires ValidState(s)
    requires Activated(a, s)
    requires t in DomState(a, s)
    ensures InDomain(t, a)
  {
    var ds := DomStateSeq(a, s);
    assert t in ds;
    var i :| 0 <= i < |ds| && ds[i] == t;
    assert ds[i] == SiblingAt(a, i);
  }

  // Initial-segment structure: index i ≤ count[a] contributes SiblingAt(a,i).
  lemma DomStateElementAt(a: Allocator, s: State, i: nat)
    requires ValidState(s)
    requires Activated(a, s)
    requires i <= s.count[a]
    ensures SiblingAt(a, i) in DomState(a, s)
  {
    assert DomStateSeq(a, s)[i] == SiblingAt(a, i);
  }

  // Frame: T3 steps preserve Allocated(s).
  lemma FrameCondition(s: State, s': State)
    requires ValidState(s)
    requires T3Step(s, s')
    ensures ValidState(s') && Allocated(s) == Allocated(s')
  { }

  // Transfer of T9: co-realized addresses at i < j are lexicographically ordered.
  lemma ForwardAllocationTransfer(a: Allocator, s: State, i: nat, j: nat)
    requires ValidState(s)
    requires Activated(a, s)
    requires i < j && j <= s.count[a]
    ensures InT(SiblingAt(a, i)) && InT(SiblingAt(a, j))
    ensures LexicographicOrder.LexicographicOrder(SiblingAt(a, i), SiblingAt(a, j))
  {
    assert AllocatorDiscipline.AllocatorDiscipline(a);
    StrictMonotonicity(a, i, j);
  }
}
