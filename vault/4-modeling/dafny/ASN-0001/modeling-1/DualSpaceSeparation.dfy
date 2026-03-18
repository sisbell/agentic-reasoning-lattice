include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module DualSpaceSeparation {

  import opened TumblerAlgebra

  // T11 — DualSpaceSeparation (INV, predicate(State, State))
  // transition; architectural
  //
  // Permanence (T8, T9, T10) applies exclusively to I-space.
  // Editing shifts (INSERT/DELETE via +/-) apply exclusively to V-space.
  // No editing operation shifts an I-space address.
  // No operation claims permanence for a V-space position.

  type ContentId = nat

  // V-space entry: subspace identifier and ordinal within that subspace
  datatype VEntry = VEntry(subspace: nat, ordinal: nat)

  // Combined state: I-space (permanent addresses) and V-space (mutable positions)
  datatype DualState = DualState(
    ispace: map<Tumbler, ContentId>,
    vspace: map<ContentId, VEntry>
  )

  // T11: Across any editing transition, I-space is invariant.
  // The asymmetry is the property: I-space has a preservation constraint;
  // V-space has none (no permanence claimed).
  ghost predicate DualSpaceSeparation(s: DualState, s': DualState) {
    forall a :: a in s.ispace ==>
      a in s'.ispace && s'.ispace[a] == s.ispace[a]
  }

  // Editing operations act only on V-space, passing I-space through unchanged

  function EditInsert(s: DualState, sub: nat, p: nat, n: nat): DualState
    requires n > 0
  {
    DualState(
      s.ispace,
      map id | id in s.vspace ::
        if s.vspace[id].subspace == sub && s.vspace[id].ordinal >= p
        then VEntry(sub, s.vspace[id].ordinal + n)
        else s.vspace[id]
    )
  }

  function EditDelete(s: DualState, sub: nat, p: nat, n: nat): DualState
    requires n > 0
    requires forall id ::
               (id in s.vspace && s.vspace[id].subspace == sub
                && s.vspace[id].ordinal > p) ==>
               s.vspace[id].ordinal >= p + n
  {
    DualState(
      s.ispace,
      map id | id in s.vspace ::
        if s.vspace[id].subspace == sub && s.vspace[id].ordinal >= p + n
        then VEntry(sub, s.vspace[id].ordinal - n)
        else s.vspace[id]
    )
  }

  // T11 holds for Insert: editing preserves I-space
  lemma InsertSeparation(s: DualState, sub: nat, p: nat, n: nat)
    requires n > 0
    ensures DualSpaceSeparation(s, EditInsert(s, sub, p, n))
  { }

  // T11 holds for Delete: editing preserves I-space
  lemma DeleteSeparation(s: DualState, sub: nat, p: nat, n: nat)
    requires n > 0
    requires forall id ::
               (id in s.vspace && s.vspace[id].subspace == sub
                && s.vspace[id].ordinal > p) ==>
               s.vspace[id].ordinal >= p + n
    ensures DualSpaceSeparation(s, EditDelete(s, sub, p, n))
  { }

  // Compositionality: sequential edits preserve the invariant
  lemma Transitive(s: DualState, s': DualState, s'': DualState)
    requires DualSpaceSeparation(s, s')
    requires DualSpaceSeparation(s', s'')
    ensures DualSpaceSeparation(s, s'')
  { }
}
