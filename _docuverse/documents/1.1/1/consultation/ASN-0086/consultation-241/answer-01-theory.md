## Question 1 [theory]

> Was retraction intended to apply only to already-existing, owned addresses, or does a baptize-and-retract-in-one-atomic-step (target owned at commit) fall within the "only the owner may withdraw" intent?

## Short answer

Nelson's "only the owner may withdraw" is a statement about **authority** (ownership at the moment of the act), not about **how long** that ownership has existed. A baptize-and-retract-in-one-atomic-step where the target is owned at commit satisfies the authority requirement, and — critically — raises none of the concerns that Nelson's *protective* constraint on retraction was designed to address. So it falls within the intent. But note up front: Nelson never discusses atomic operations, retraction as a primitive, or this sequencing question, so the conclusion below is an interpretation built from his principles, not an explicit ruling.

## Two distinct constraints in Nelson's model

Nelson's writing on withdrawal collapses two separate ideas that this question forces apart:

**1. The authority constraint (who may act):**

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." (2/29)

This is purely about authority. The right attaches to *ownership*, and ownership is established by baptism:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

Nothing here conditions the withdrawal right on the *age* of the ownership. If you baptize an address under your account, you own it the instant it exists. At commit, the authority test ("are you the owner of the target?") is satisfied.

**2. The protective constraint (when withdrawal is restricted):**

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." (2/43)

This is the *only* place Nelson restricts an owner's withdrawal — and it is explicitly scoped to **published** material with **dependents** ("other readers and users will come to depend on its accessibility"). The rationale is dependency, not ownership timing.

## Why the atomic case falls within intent

The protective constraint does not bite on a freshly-baptized target, for two reasons grounded in the sources:

- **Private documents are freely withdrawable.** Publication is a deliberate, "solemn event"; documents are private by default. For private documents, the session-model and publishing material make withdrawal free and instant — "privashing" lets an owner "retain the right to withdraw it at any time," and a private document "may be read and linked-to only by the owner and his or her associates" (2/42). A baptized-then-immediately-retracted address was never published, so the "stay published" rule never engages.

- **No dependents can exist.** The thing the rule protects is the reliance of *others* who have linked to or read the material. A target created and retracted in one atomic step has had no window in which others could form that reliance — no in-links, no readers. The harm the rule guards against is structurally impossible.

So in the atomic case both tests resolve cleanly: authority is present (you own it at commit), and the dependency-protection that would otherwise gate withdrawal has nothing to protect.

## The relevance of ghost elements

There's a subtlety worth surfacing. Baptized addresses can be referenced before content exists:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

This means a *third party* could, in principle, have linked to a ghost address before your atomic operation. If such an in-link existed at commit, you'd be in a different situation — closer to the "others depend on it" scenario, even though you never published. Nelson does not resolve this; it sits in the gap between "ghost elements are linkable" (4/23) and "stay published applies to dependents" (2/43). For a genuinely atomic baptize-and-retract with no intervening window, this edge case cannot arise, but it marks the boundary of where the answer stays clean.

## What is not covered by Nelson

NEED_RAW: I can reason about intent, but Nelson does not explicitly address any of the following, and I found nothing in the curated material on them:
- "Retraction" as a named primitive operation (Nelson has *modification* and *withdrawal-by-due-process*, not a retract verb)
- Atomicity / transactional commit semantics
- The specific sequencing of baptism relative to withdrawal

If you want to confirm there is no treatment of operation atomicity or a retract-style command, the FEBE protocol pages (4/61–4/79) are where it would appear — but the operations summary above lists only 17 commands (INSERT, DELETE, COPY, etc.) with no retract/withdraw primitive, which itself suggests withdrawal was conceived as a policy/contractual act (2/43) rather than a low-level operation.

## Bottom line

The "only the owner may withdraw" intent is an authority rule keyed to ownership-at-the-moment-of-acting, and Nelson's *one* restriction on owner withdrawal is scoped to published material with real dependents. A baptize-and-retract atomic step with the target owned at commit satisfies the authority rule and escapes the protective rule entirely (private, no dependents). It therefore falls within the intent — with the single caveat that a pre-existing third-party ghost-link to the target would push it toward the dependency-protected case Nelson did not fully resolve.
