## What this is

The ownership/authority subsystem: the layer that decides *who may act on which addresses*. It binds the (authority-silent) tumbler address space of ASN-0034 to principals by prefix containment, turning "this address exists" into "this principal owns it."

## Design commitments

These are locked in for the whole system; downstream design cannot violate them.

- **Ownership is a theorem about addresses, not stored state.** The two-place predicate `owns(π, a)` is decided by comparing two tumblers (`pfx(π) ≼ a`) — no registry, table, or history consulted (O1). *Forced.* Consequence: there is no ownership table to keep consistent, migrate, replicate, or corrupt. Authorization-by-containment can be checked anywhere — at the edge, in any layer — without a round trip to authoritative state.

- **The only authoritative ownership state is the set of principal prefixes.** Domains, coverage, effective owner, provenance, and the delegation forest are all *derived* from this set (O2, O4, O6, NestingByDelegation). *Forced.* The state is small — one entry per principal, not per address.

- **Effective owner = longest-prefix match.** `ω(a)` selects the registered principal whose prefix matches `a` and is longest (the EffectiveOwner definition; O2). *Forced.* Exclusivity — exactly one owner — is a *consequence* of longest-match plus prefix-injectivity, not a separately stored fact. This is the one operation that consults state, and it is exactly the operation the udanax-green reference never had to build (it ran one account per session).

- **The registry is append-only with immutable values.** Principals are never removed (O12); prefixes never change (O13). *Forced.* No revocation, no in-place transfer, no mutation. This is what makes ownership a monotonic refinement rather than a rewrite.

- **Ownership only ever refines, and only via delegation.** `ω(a)` can change solely by a delegation introducing a *longer* matching prefix (O3); nothing else moves it, and it never gets shorter (monotonic-refinement corollary). *Forced.* Ownership history is tree growth, never edit.

- **The account tier is the floor of ownership** (`zeros(pfx(π)) ≤ 1`, O1a). *Forced* (by the bootstrap + delegation conditions). Allocation is uniform at every tier — anyone can fork sub-addresses — but *principals* exist only at node/account level. Below the account there is only "mine vs. not mine," never a finer owner. This bounds the registry's size and tier.

- **Delegation is irrevocable** (O8) and **the docuverse is a forest, not a tree** (O9). *Both forced* by monotonic refinement and prefix geometry respectively. A parent can never reclaim a delegated subdomain; ownership cannot cross a node boundary, so each node is an independent ownership root and the same human on two nodes is two unrelated principals.

- **Denial of a write you don't own is never an error — it is a fork** (O10). *Forced* as the only coherent response to immutability + exclusivity: you get a fresh address in *your* domain, one tier below your prefix; the original is untouched and its owner unchanged. There is deliberately no write-into-others'-content path.

- **The principal registry is a labeling of the baptismal registry.** Every prefix is itself a baptized address (PrefixBaptismCoupling); every delegation *is* a baptism (O18, O17b). *Forced.* You do not get a second, independent allocation mechanism for principals.

*Conventional, not forced:* which tumbler tier counts as "account" (inherited from ASN-0034/0040), the initial bootstrap set, and whether delegation events are recorded with delegator identity (see below — recomputable).

## What must be built

- **A principal registry** — the set of principals and their prefixes. Add (with prefix), test membership, enumerate, look up prefix. Append-only; never deletes or mutates; small; node/account tier only.
- **An ownership predicate** — given a prefix and an address, decide containment. Pure, total, decidable, stateless.
- **An effective-owner resolver** — given a baptized address, return the unique longest-matching principal. Total on baptized addresses (coverage guarantees a hit).
- **A delegation gate** — check the five conditions (ancestry; authorization = delegator is most-specific coverer; account-tier; top-down-order = nobody already extends the new prefix; fresh-valid) and, if satisfied, *atomically* baptize the new prefix and register the new principal. Reject otherwise. The only non-bootstrap entry for principals.
- **A subdivision-authority check (O5)** — confirm an allocator is the most-specific coverer of what it allocates.
- **A fork operation (O10)** — allocate a fresh address one tier below a principal's prefix, leaving the target untouched.
- **Bootstrap initialization (O14)** — seed an initial principal set that is nonempty, account-tier, injective, valid, pairwise non-nesting, and covers the initially-baptized addresses.

## Implementation approaches

The unifying move (Lampson: cache answers and use *hints* rather than authoritative duplicate state) is that **the only thing you must persist authoritatively is the set of principal prefixes; everything else is recomputable.**

**Principal registry — where the authoritative state lives.**
- *Option A — label the baptism journal.* Since every prefix is already a baptized address, mark the baptism records that are delegations/bootstrap (carrying the delegator id if you want it) and treat the in-memory principal set as an *index recovered by replay*. This is exactly this repo's substrate pattern (`links.jsonl` journal → `paths.json` registry, rebuilt by replay) and matches udanax-green, where account creation inserts the prefix into the granfilade *in the same operation* (`insertseq`) — there is no separate registry.
- *Option B — a separate principal table* plus reverse index for queries. Duplicates state; risks divergence.

Pick **A.** The delegation/bootstrap events *are* the log; the principal set is a derived, losable hint. A separate authoritative table is precisely the shape that produces the ownership-divergence trap (looser/duplicated authority state). Going further: the *delegation forest itself* (who delegated to whom) is recomputable from the prefix set alone — the parent of any principal is the most-specific covering principal (NestingByDelegation), and refinement is monotonic, so structural position determines parentage. So you need not record delegator identity at all — it is a hint. *What you give up:* this recompute-the-parent shortcut breaks the moment ownership transfer is introduced (an open question), because effective owner could then diverge from structural position. Be explicit that the simplification holds only while refinement stays monotonic.

**Effective-owner resolver — longest-prefix match.** This is the classic IP-routing FIB problem.
- *Linear scan* over the prefix set, keeping the longest match: O(|Π|), no extra structure. Since Π is small and per-node, this is often enough; Green was effectively O(1) with one account.
- *Radix/PATRICIA trie* keyed on tumbler components: longest match is one root-to-leaf walk, and the trie nests exactly as domains nest. The principled choice when |Π| or query rate grows.
- *Cache the answer* per address (`address → owner`) as a hint. By monotonic refinement a stale entry can only ever be a *prefix-ancestor* of the true owner, never wrong in the other direction — so a miss is cheap and safe to recheck. Textbook recomputable hint.

Default to **scan**; upgrade to the **trie** only when it earns its keep; add the **cache** if ω is hot. Do **not** reach for the granfilade/enfilade machinery here — that earns its keep on content spans, not on a node/account-tier set this small. On the Rust/`im` target, hold the prefix set (or trie) as a **persistent, structurally-shared map**: each delegation yields a cheap new immutable version, which gives you `ω_Σ` at any historical Σ for free by retaining old roots — directly serving the spec's state-relativized functions (each reachable Σ is just a retained snapshot).

**Delegation gate.** Reuse the resolver for condition (ii) (is the delegator the longest match of the proposed prefix?); condition (iv) is a subtree-emptiness query (no principal under the new prefix) — O(1)-ish in a trie, O(|Π|) in a scan; (i)/(iii) are pure address arithmetic; (v)'s freshness consults the baptismal registry. **Atomicity is the crux:** baptizing the prefix and registering the principal must be one indivisible step. Use the journal: write a *single* record that is both the baptism and the principal-tag — one append, recovered atomically — rather than a two-phase "baptize then register" that can half-fail. Make the journal append the serialization point (as the repo's substrate does), which also enforces O15's "≤ 1 new principal per transition" for free. **A real constraint to honor:** the allocator produces only the next contiguous sibling or the canonical first child (O17c; verified in Green), so you cannot delegate account `#5` while `#1–4` are unbaptized — either restrict delegation to the next free slot (Green-faithful) or baptize the intermediates first (as the spec's worked example does for `[1,0,2,3]`).

**Subdivision-authority (O5) and fork (O10).** If a session is bound to one principal and may only name *its own* prefix as the allocation hint, then O5 holds **by construction** — you are the most-specific coverer of your own fresh slots — and no per-allocation authorization check is needed. This is precisely Green's model: allocation is ownership-blind, anchored at the session's own account, advancing unilaterally past delegated siblings. The fork is then the *same* "find ceiling, climb one step" allocator applied to your own subtree (`next(Σ.B, pfx(π), 2)`), and the ownership layer does *only* the allocation — the content-sharing half (inclusion/transclusion) belongs to the content/link layer. Keep them separate (do one thing well); Green's fork-of-another's-document is one allocation call placing the new address under the requesting account, with content wired separately.

**Recovery.** Registry = replay of the tagged journal. Snapshot the in-memory set/trie periodically as a checkpoint; recover from latest checkpoint + journal tail. Because the registry is a hint, a lost or corrupt checkpoint is non-fatal — rebuild from the log.

## Guarantees to uphold

Almost everything is a theorem of an append-only, immutable-prefix registry; the active-enforcement surface is small and worth isolating.

- **Permanence / no-expiry, monotonic refinement, irrevocability, node-locality, provenance** — *by construction.* They follow from append-only + immutable prefixes + longest-match + prefix geometry. The guarantee for permanence and irrevocability is literally the *absence* of a removal/revocation path; for node-locality it is that delegation's ancestry condition preserves the leading node component, so a prefix can never migrate across nodes.
- **Uniqueness of effective owner** — *a theorem, but conditional on active enforcement of prefix-injectivity.* Uniqueness (O2) is automatic *if* delegation enforces freshness/authorization so no two principals share a prefix. Enforce (v) and (ii); uniqueness then needs no runtime check.
- **Account-floor** — *actively enforced* at the delegation gate (reject `zeros(pfx(π')) ≥ 2`).
- **Coverage / no orphans** — *actively enforced* at two points: bootstrap must cover initial addresses, and allocation must be by a covering principal. Collapses to "by construction" if sessions may only allocate under their own prefix.
- **Longest-match resolution itself** — *the one thing you must actively build*, and the note's final open question. **Binary containment against a single account is not enough.** A node operator's prefix contains every address under its node, including delegated accounts; using containment where the contract requires `ω` makes the node operator appear to own delegated subdomains — the exact divergence the spec's longest-match selection exists to prevent. `owns()` (containment) is correctly two-valued and may hold for several principals at once; only `ω()` (longest match) arbitrates. Conflating them reproduces the bug.

## How it fits

- **Leans on the tumbler algebra (ASN-0034)** for the address space, the prefix relation `≼`, canonical representation, field/hierarchical parsing, total order, and contiguous-subtree structure. Ownership adds *meaning*, never addresses.
- **Leans on baptism (ASN-0040)** for the baptismal registry, the `next`/`hwm` allocator, monotone irrevocable allocation, and T4-validity of every allocated address. Every prefix is a baptized address; every delegation restricts to a baptism step on the registry component (O17b).
- **Hands to** the content/operations layer (what you may *do* with an owned address — read, write, version) and the link/transclusion layer (the content half of a fork). The note is explicit that content effects live outside its state Σ: ownership says *who may*, content says *what happens*.
- **Is consumed by** the session/access layer, which binds a session to a principal and is where `owns()` (cheap, stateless, pushed to the edge) and `ω()` (centralized resolver) are actually invoked.

Within the stack it sits *above* address allocation and *below* content operations: the authority layer.

## Decisions for the builder

- **Session↔principal binding — the biggest fork.** One principal per session (Green) collapses O5 and makes the resolver mostly unnecessary (you check `owns` against your own prefix); multi-principal sessions require real longest-match and active subdivision-authority checks. Decide this first — it sizes almost everything else.
- **Where authoritative state lives:** tag the baptism journal (recommended) vs. a separate delegation log vs. recompute-all-from-prefixes.
- **Whether to record delegator identity** or recompute the parent via most-specific-cover (recompute suffices while transfer is absent).
- **Resolver structure and caching:** scan vs. radix trie vs. cached/persistent map — sized to expected |Π|, query rate, and whether you want historical `ω_Σ` snapshots.
- **Delegate-prefix policy:** next-available-slot (Green-faithful, O17c) vs. baptize-intermediates to reach a chosen prefix.
- **Concurrency / serialization point:** Green serialized via a single-threaded loop, making baptize+register trivially atomic and "≤ 1 principal per transition" automatic. A concurrent build must choose a serialization point — the journal append is the natural one, consistent with this repo's substrate.
- **Bootstrap configuration:** the initial principal set and prefixes (single node operator vs. multi-node seed).
