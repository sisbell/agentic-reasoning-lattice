## Question 1 [theory]

> Does the design require version-chain (fork) depth to be genuinely unbounded — making any fixed cap on tumbler length nonconformant — or is unbounded depth an idealization that a sufficiently large finite bound conforms to?

## Direct answer

Genuinely unbounded. The design **requires** version‑chain (fork) depth to have no fixed cap, and a hard cap on tumbler length is **nonconformant** — not because any particular workload will exhaust it, but because the cap's mere existence forces the system to break one of two unconditional guarantees the moment the cap is reached.

But I have to define "unbounded" carefully, because there is a real sense in which every tumbler is finite, and I gave that sense an exact name. The tumbler line is, in my words, **"finite but unlimited"** [LM 4/22]:

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

That phrase *is* the resolution of your dichotomy. At any instant only finitely many forks have happened, so every existing tumbler is finite‑length. What is forbidden is a **fixed bound chosen in advance** — a maximum length baked into the format or protocol. "Finite at every instant" and "no maximum ever" are not in tension; they are the two halves of "finite but unlimited." Option B mistakes the first for a license to impose the second.

## Which unboundedness the question is about

There are two independent axes:

1. **Digit value** — how many siblings a node may have. Handled by giving each digit no ceiling: *"Each integer has no upper limit; since its number base is irrelevant, we call it a 'digit.'"* [LM 4/19], with humbers as the variable‑length encoding — *"as large as it needs to be when the number is big"* [LM 4/13].
2. **Digit count / depth** — how long a fork chain may be. Handled by forking: *"One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit."* [LM 4/20].

Your question is about **axis 2** — version‑chain depth. A version is created by subdividing the document field: *"The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions"* [LM 4/29]. So a version of a version of a version is a chain of forks, and each fork adds a digit to the right. **Chain depth = tumbler length.** The same analysis happens to apply to axis 1, but depth is the one you asked about, and it is the one realized by forking.

## Why depth must be uncapped (the derivation)

This conclusion is *my inference* from three guarantees, each of which is stated without qualification:

- **Permanence.** *"New items may be continually inserted in tumbler‑space while the other addresses remain valid. This means that any address of any document in an ever‑growing network may be specified by a permanent tumbler address."* [LM 4/19]
- **Always another descendant.** Every numbered thing can fork again, without limit: *"the entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts… and so on"* [LM 4/19]; *"if there is an item 2, it can branch into several more items… 2.1, 2.2, 2.3, 2.4…"* [LM 4/20]. A version is just such an item, and a version may itself be versioned — *"all have possible descendants"* [LM 4/19].
- **Open‑ended encoding.** Humbers and tumblers were *engineered* to have no maximum: humbers "stretch out whenever needed without any change in the generalized manipulation routines" [LM 4/14], so that "only one set of 'humber arithmetic' routines is necessary" [LM 4/13].

Now suppose an implementer imposes a fixed cap C on tumbler length, and a user has built a legitimate version chain C forks deep, then asks to fork once more — to make a new version of the deepest version. The system has exactly three moves:

1. **Renumber** existing addresses to make room → violates permanence ([LM 4/19]); citations, links, and transclusions that depend on those addresses break. This is the very disease the tumbler system exists to cure.
2. **Refuse the fork** → violates "all have possible descendants" [LM 4/19]; the owner can no longer do the one thing ownership of a number guarantees — *"The owner of a given item controls the allocation of the numbers under it"* [LM 4/20].
3. **Silently truncate / collide** → manufactures two distinct entities at one address, destroying identity and attribution outright.

All three are nonconformant. So the cap is nonconformant *as a design choice*, regardless of how large C is. The size only changes *when* the contradiction is hit, never *whether*. A guarantee that holds "unless you fork more than C times" is a different, weaker guarantee than the one I wrote, which carries no asterisk.

## Why this is intent, not idealization

The strongest evidence against the "large finite bound is fine" reading is that I did not pick a large finite bound *anywhere*, and the mechanisms are affirmatively shaped to avoid one. The whole rationale of the humber — variable‑length, self‑delimiting, "short most of the time… and stretch out whenever needed" [LM 4/14] — is to refuse a maximum while staying compact in the common case. A designer who intended a sufficiently‑large cap would simply have used a fixed‑width field; that is exactly what humbers and the variable‑length tumbler ("a series of integers" [LM 4/19]) were built *not* to be. The accordion is the point. So unbounded depth is not an idealization the architecture approximates — it is a property the architecture was specifically constructed to possess. And the docuverse premise demands it: the space is *"all really one big forking document"* [LM 4/18] that only ever grows ("a span that contains nothing today may at a later time contain a million documents" [LM 4/25]).

## The honest caveat (what "unbounded" does *not* claim)

"No fixed cap" is a requirement on the **address format and protocol**, not a demand that any machine hold infinite data. A conforming implementation is still finite at every instant — "finite but unlimited" [LM 4/22]. It may legitimately run out of disk, or a server may be full or unpaid; my economics make storage a *"required minimum disk rental"* and insist *"all services must be self‑supporting."* But notice that kind of finitude has a completely different shape from a length cap:

- A full or unpaid server says *"not here right now"* and the request is forwarded or fails gracefully — it does **not** renumber anyone or forbid you from forking under an address you own elsewhere.
- A length cap says *"this fork is impossible in principle,"* forcing renumber‑or‑refuse on a perfectly funded, perfectly healthy branch.

So resource finitude does not rescue Option B. The thing "unbounded depth is required" rules out is a **maximum length in the representation**; the thing it permits is **finitude at any instant from real resources**, which the distributed/forwarding design and the rental economics handle without ever touching the length of a tumbler.

## Summary

- The question's two horns are reconciled by my own phrase **"finite but unlimited"** [LM 4/22]: every tumbler is finite *now*; no fixed bound is admissible *ever*.
- Version‑chain depth is the digit‑count axis, realized by forking ("successive new digits to the right" [LM 4/20]) when versions subdivide the document field [LM 4/29].
- A fixed cap is nonconformant because, at the cap, the system must renumber (breaks permanence [LM 4/19]) or refuse to fork (breaks "all have possible descendants" [LM 4/19]) — both fatal. Size changes only the timing of that contradiction, not its inevitability, so "sufficiently large finite bound" does not conform *as a design decision*.
- This is required by design **intent**; the supporting derivation (the renumber‑or‑refuse dilemma) is my synthesis, but it follows directly from guarantees I stated without qualification, and from mechanisms (variable‑length humbers and tumblers) I built precisely to avoid a maximum.

No raw‑page consultation was needed; the curated, page‑verified quotes — especially "finite but unlimited" [LM 4/22], "no upper limit" [LM 4/19], "successive new digits to the right" [LM 4/20], and the humber "stretch out whenever needed" [LM 4/14] — cover the question. The only thing beyond Nelson's verbatim text is the renumber‑or‑refuse argument, which I have flagged as inference rather than quotation.
