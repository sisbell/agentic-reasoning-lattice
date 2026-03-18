-- T9-ForwardAllocation.als
-- Each allocator controls a prefix and allocates sequentially within it.
-- Property: addresses from the same allocator are strictly increasing.

open util/ordering[Time]

sig Time {}

sig Tumbler {
    pre: one Int,
    suf: one Int
} {
    pre >= 0
    suf >= 0
}

-- Tumblers are identified by their components
fact TumblerIdentity {
    all disj t1, t2: Tumbler | not (t1.pre = t2.pre and t1.suf = t2.suf)
}

-- Strict tumbler ordering (lexicographic on prefix then suffix)
pred tumblerLt[a, b: Tumbler] {
    a.pre < b.pre
    or (a.pre = b.pre and a.suf < b.suf)
}

sig Allocator {
    ownedPrefix: one Int,
    history: Time -> lone Tumbler
} {
    ownedPrefix >= 0
}

-- Each allocator has a unique prefix
fact UniquePrefix {
    all disj a1, a2: Allocator | a1.ownedPrefix != a2.ownedPrefix
}

-- Allocated tumblers carry the allocator's prefix
fact SharedPrefix {
    all a: Allocator, t: Time |
        some a.history[t] implies a.history[t].pre = a.ownedPrefix
}

-- Sequential allocation: suffix strictly increases with time
fact SequentialAllocation {
    all a: Allocator, t1, t2: Time |
        (some a.history[t1] and some a.history[t2] and lt[t1, t2])
            implies a.history[t1].suf < a.history[t2].suf
}

-- No tumbler allocated by two different allocators
fact DisjointAllocation {
    all disj a1, a2: Allocator, t1, t2: Time |
        (some a1.history[t1] and some a2.history[t2])
            implies a1.history[t1] != a2.history[t2]
}

-- T9: Forward Allocation
assert ForwardAllocation {
    all a: Allocator, t1, t2: Time |
        (some a.history[t1] and some a.history[t2] and lt[t1, t2])
            implies tumblerLt[a.history[t1], a.history[t2]]
}

check ForwardAllocation for 5 but exactly 2 Allocator, exactly 3 Time, 4 Int

-- Non-vacuity: some allocator makes at least two allocations
run NonVacuity {
    some a: Allocator, disj t1, t2: Time |
        some a.history[t1] and some a.history[t2]
} for 5 but exactly 2 Allocator, exactly 3 Time, 4 Int
