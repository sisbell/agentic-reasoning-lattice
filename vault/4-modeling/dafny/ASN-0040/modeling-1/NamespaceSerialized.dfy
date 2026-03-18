include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module NamespaceSerialized {
  import opened TumblerAlgebra

  // B4 — NamespaceSerialized
  // (A β₁, β₂ : ns(β₁) = ns(β₂) : commit(β₁) ≺ read(β₂) ∨ commit(β₂) ≺ read(β₁))

  // Namespace of a baptism: the (parent, depth) pair
  datatype Namespace = Namespace(parent: Tumbler, depth: nat)

  // A baptism event records its namespace and the registry snapshots
  // at read time and after commit.
  datatype BaptismEvent = BaptismEvent(
    ns: Namespace,
    readRegistry: set<Tumbler>,
    commitRegistry: set<Tumbler>
  )

  // DIVERGENCE: The ASN uses temporal precedence (≺) over concurrent events.
  // The sequential functional model has no concurrency primitive. We capture
  // temporal precedence as registry set inclusion: commit(β₁) ≺ read(β₂)
  // iff β₁.commitRegistry ⊆ β₂.readRegistry — the observable consequence
  // of one operation completing before another begins.

  ghost predicate CommitPrecedesRead(e1: BaptismEvent, e2: BaptismEvent) {
    e1.commitRegistry <= e2.readRegistry
  }

  // B4 — precondition on baptize: all baptism pairs in the same
  // namespace are temporally serialized.
  ghost predicate Serialized(trace: seq<BaptismEvent>) {
    forall i, j ::
      (0 <= i < |trace| && 0 <= j < |trace| && i != j
       && trace[i].ns == trace[j].ns)
      ==>
      (CommitPrecedesRead(trace[i], trace[j])
       || CommitPrecedesRead(trace[j], trace[i]))
  }

  // Incremental form: the new event is serialized with all prior
  // same-namespace events. This is the requires clause on baptize.
  ghost predicate NamespaceSerialized(
    trace: seq<BaptismEvent>,
    current: BaptismEvent
  ) {
    forall i :: (0 <= i < |trace| && trace[i].ns == current.ns) ==>
      CommitPrecedesRead(trace[i], current)
  }

  // The incremental form preserves the full trace property.
  lemma SerializedExtension(trace: seq<BaptismEvent>, current: BaptismEvent)
    requires Serialized(trace)
    requires NamespaceSerialized(trace, current)
    ensures Serialized(trace + [current])
  { }
}
