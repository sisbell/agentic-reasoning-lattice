-- ASN-0034 T10a.3 LengthSeparation
-- Child allocator outputs have strictly greater length than parent sibling
-- outputs. Length separation is additive across nesting levels.

open util/integer

sig Tumbler {
  len: Int
} {
  len > 0
}

sig Allocator {
  sibLen: Int,
  outputs: set Tumbler,
  children: set Allocator,
  spawnK: Int,
  depth: Int
}

-- T10a.1: all outputs of an allocator have its sibling length
fact UniformLength {
  all a: Allocator, t: a.outputs | t.len = a.sibLen
}

fact PositiveSibLen {
  all a: Allocator | a.sibLen > 0
}

-- Tree structure: no cycles, single parent
fact TreeStructure {
  no a: Allocator | a in a.^children
  all a: Allocator | lone (children.a)
}

-- Root: no parent implies depth 0 and spawnK 0
fact RootConstraints {
  all a: Allocator | (no children.a) implies (a.depth = 0 and a.spawnK = 0)
}

-- Child: k' > 0, sibLen = parent.sibLen + k', depth = parent.depth + 1
fact ChildConstraints {
  all parent: Allocator, child: parent.children {
    child.spawnK > 0
    child.sibLen = plus[parent.sibLen, child.spawnK]
    child.depth = plus[parent.depth, 1]
  }
}

-- Postcondition: child outputs strictly longer than parent outputs
assert ChildOutputsLonger {
  all parent: Allocator, child: parent.children |
    child.sibLen > parent.sibLen
}

-- Postcondition: no child output equals any parent sibling (T3: different lengths => distinct)
assert NoChildParentCollision {
  all parent: Allocator, child: parent.children |
    no (parent.outputs & child.outputs)
}

-- Postcondition: descendant d levels deep has output length >= ancestor.sibLen + d
assert DepthAdditivity {
  all anc: Allocator, desc: anc.^children |
    desc.sibLen >= plus[anc.sibLen, minus[desc.depth, anc.depth]]
}

-- Postcondition: along any ancestor-descendant lineage, outputs never collide
assert LineageNoCollision {
  all anc: Allocator, desc: anc.^children |
    no (anc.outputs & desc.outputs)
}

-- Non-vacuity: parent with child, both producing outputs
run NonVacuity {
  some parent, child: Allocator |
    child in parent.children and
    some parent.outputs and
    some child.outputs
} for 5 but 6 Int

check ChildOutputsLonger for 5 but 6 Int
check NoChildParentCollision for 5 but 6 Int
check DepthAdditivity for 5 but 6 Int
check LineageNoCollision for 5 but 6 Int
