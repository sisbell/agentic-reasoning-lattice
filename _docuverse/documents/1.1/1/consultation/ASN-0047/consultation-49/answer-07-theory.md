## Question 7 [theory]

> Does the design admit node-allocation roots other than the bootstrap n₀ (i.e., is there a designed "protocol-determined ancestor" distinct from the single bootstrap root that baptism/forking descends from)?

# No: One Tree, One Root

My design has a single rooted tree. There is no protocol-determined ancestor distinct from the bootstrap. All node-allocation descends from one origin.

## The explicit statement

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

This is categorical. *All* servers descend from it. Not "most"; not "by convention"; not "unless otherwise designated." The redundancy is deliberate — the leading `1` is the bootstrap, and it lets `1` alone mean "the entire docuverse."

## Why one root, not several

The forking principle requires a single origin:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "So the docuverse is all really one big forking document." [LM 4/18]

The whole point of baptism is that **whoever owns a number controls the subnumbers below it** [LM 4/17]. For this to work without a central authority adjudicating disputes, there must be exactly one root from which all ownership descends. Two roots would mean two unrelated authorities — and then `1.x` and (say) `2.x` would name independent tumbler-spaces that could never be unified, never compared arithmetically, never spanned by a single address.

## What this rules out

- No "second root" for, say, an alternate jurisdiction, an off-network archive, or a parallel federation
- No protocol-level mechanism for grafting a foreign tree into the docuverse at any point other than as a descendant of an existing owned node
- No way to allocate a node-address whose ancestry does not trace back to `1`

## What it does *not* rule out

The single-root requirement is about *allocation*, not about *physical infrastructure*:

- Servers are physically distributed; vendors operate independently; BEBE federates them — but every server's address still descends from `1`
- A vendor can spin off sub-servers under its own owned node (forking)
- Ghost elements exist at addresses where nothing is stored [LM 4/23], but those addresses are still under the same root

The architecture is: one logical tree, many physical machines.

## Bottom line

If you're considering introducing a second protocol-determined ancestor, you're departing from my design. The single bootstrap root is load-bearing — it is what makes "the entire docuverse" expressible as `1`, what makes tumbler arithmetic closed, and what makes baptism a self-coordinating allocation scheme without a central registry.
