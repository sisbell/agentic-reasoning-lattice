## Question 2 [theory]

> Does Nelson's design treat the act of delegating a sub-account at slot `k` under prefix `p` as itself baptizing `p.0.k` into the address registry, such that no delegated sub-account prefix can exist outside the high-water-mark range of its parent's child stream?

# Delegation, Baptism, and the High-Water Mark

## Two distinct claims to evaluate

Your question bundles two propositions. I'll answer each from the design intent perspective.

## 1. Is delegation itself the act of baptism?

**Yes — in my design, delegating a sub-account and baptizing its number are the same act.** There is no separate "registration" step between "I gave you slot k" and "k now exists in the address registry."

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

The act of *designating* is the act of *baptizing*. They are not two operations.

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Allocation = baptism. There is no separate registry that must be updated after the parent allocates.

## 2. Caution about the `p.0.k` notation

Your question's address form `p.0.k` deserves scrutiny. In my design the digit `0` is a **major field divider**, not a sub-account separator:

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

Sub-accounts *within* the User field fork by appending digits, not by inserting a `0`:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

So if `p` is an account prefix and `k` is a delegated sub-account, the baptized address is **`p.k`**, not `p.0.k`. The `0` belongs only at the Server→User, User→Document, or Document→Element transitions.

If your formalization treats the child-stream entry as `p.0.k`, that is a misreading of the field-separator convention — the same error I would expect to see flagged elsewhere in your project. (Your own memory notes a recurring "subspace identifier" misreading of `0`.)

## 3. The high-water-mark range — design intent vs. implementation property

**My design describes successive allocation but does not explicitly mandate a high-water-mark invariant.**

What I say:

> "Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

The word "successive" is suggestive but not formally constraining. I describe the *typical pattern* of allocation, not a *prohibition* on skipping slots or allocating non-monotonically.

What follows from my stated intent:

- The owner of `p` has **exclusive control** over allocation under `p` [LM 4/20]
- New addresses are **inserted while existing addresses remain valid** [LM 4/19]
- No central authority coordinates this — "Whoever owns a specific node... may in turn designate" [LM 4/17]

What does **not** follow explicitly from my stated intent:

- That allocations must be contiguous (no gaps)
- That allocations must be strictly increasing (no reuse below a maximum)
- That a child cannot exist whose slot exceeds some recorded "high-water mark"

The high-water-mark property is a **reasonable formalization** of my "successive" language — it captures the natural meaning of monotonic delegation — but it is an inference, not a verbatim guarantee. Treat it as an implementation/formalization decision consistent with my text, not as a design mandate I explicitly issued.

## 4. What I *do* guarantee about delegated prefixes

- They are owned exclusively by the delegatee
- The parent's act of allocation makes them valid addresses immediately
- They form a subtree under `p` that maps to a contiguous range on the tumbler line — because of depth-first ordering [LM 4/25]:

> "A span may be visualized as a zone hanging down from the tumbler line—what is called in computer parlance a depth-first spanning tree." [LM 4/25]

That last point is the closest I come to your high-water-mark claim: every delegated prefix sits within the subtree of `p`, and that subtree is a contiguous tumbler-span. But this is about **subtree containment**, not about ordering of slot allocation within `p`'s child stream.

## Summary

| Claim | My design intent |
|---|---|
| Delegation = baptism | **Yes**, verbatim. Allocation is baptism. [LM 4/17, 4/20] |
| Address form is `p.0.k` | **No** — sub-accounts fork as `p.k`. `0` is a field separator. [LM 4/26, 4/28] |
| Delegated prefixes lie within `p`'s subtree | **Yes**, by depth-first ordering. [LM 4/25] |
| Slots must respect a high-water-mark | **Not explicitly stated.** "Successive" allocation is described but monotonicity is not formally required. |

The high-water-mark invariant is a fair formalization, but if you cite it as my intent, you are extrapolating — and you should say so. The thing I *did* commit to is exclusive ownership of allocation under `p`, not a particular discipline for ordering slots within the child stream.
