I reviewed M3 against M1/M2 (as given) and the six source notes (ASN-0040/0093/0047/0042/0103/0123). I worked the load-bearing checks concretely rather than trusting the prose; summarizing what I verified before listing improvements.

## What holds up (the load-bearing checks)

- **Every M1/M2 call typechecks against the given interfaces.** `checked_inc(&Address,usize)→Result<Address,GateViolation>`, `shift(&Tumbler,&Nat)`, `parent(&Address)`, `zeros/ordinal(&Tumbler)`, `validate(Tumbler)`, `Tumbler::new/get/len`, and the M2 `transact`/`snapshot`/`Staging`/`push` seam are all used as specified. The `HasM3` read-accessor + `W::Record: From<M3Rec>` write-mirror is a legitimate sub-state composition over M2's `WorldState` — no invented upstream API.
- **The `(parent,g)` frontier keying is correct and is the real ASN-0123 fix.** I traced decompose/`namespace` for content `(b_C(d),1)`, link `(b_L(d),1)`, version `(d,1)`, document `(account,2)`, account `(N,2)`, sub-account `(account,1)`, and nested versions/version-content. The `g = (zeros(addr)==zeros(parent)) ? 1 : 2` recovery round-trips against `next_in`'s mint for every chain, and a Document-classified version vs. document resolve to *different* frontiers — so document↔version separation falls out of the key, at both mint and `is_allocated`/`entity_level` query time. No two of the chains under one document share an `NsKey`.
- **`next_in`'s `shift(c1, m)` is sound.** `c1=checked_inc(parent,g)` always carries ordinal 1 in its last position; `shift` adds `m` at `#v` (last component), giving `c_{m+1}` with no carry and no text→link mis-shift — exactly the "full element position, not a bare base" case M1's `shift` contract permits.
- **Lock key ≡ frontier key, by one code path.** `*_lock_key = ns_lock_key(*_ns(..))` and the mint advances `next_in(*_ns(..))` through the same `*_ns` helper + injective length-delimited encoding; the staged `Allocate` decomposes back to the same `NsKey`. The "don't lean on v1's global lock" argument is genuinely discharged.
- **M5 cross-owner VERSION pre-read is sound.** I checked the ω(d_src)-stability claim independently: no account-tier (`zeros≤1`) prefix of a `zeros=2` document can sit strictly between its account and itself, and a sub-account never prefixes the document — so no concurrent `delegate` can lengthen the coverer. M5 can therefore pick the branch-dependent lock before the closure. This was the one place a cycle/contradiction could hide; it doesn't.
- **delegate's in-closure gate is the correct fix** for the pre-snapshot race, and is faithful to M2 (keys held across `base()`-read + commit). The §6 narrowing (iii) `≤1→==1` and §7 suppression of `baptize(node,1)` are a **genuine** ASN-0042/0040-vs-ASN-0047 conflict (I confirmed `baptize([1],1)=[1,1]` is a zeros=0 node mint), resolved soundly and stated, not papered over. The §6 node-tier-O10 drop is a stated, coherent model choice with a covering path (delegation) and an open-decision flag.
- **No false claim about a note or upstream**, no dropped invariant (B0/B1/B2/B3/B7/B8/B9/B10, P1/P3/P6/P8, O1/O2/O8/O9/O15/O17c, V0/VD all mapped), no neighbor overreach (lazy `M(d)=∅`, no M4/M7 reads), and the registered-empty-vs-unallocated seam to M5/M6/M8 is exposed via `is_registered_document`/`is_allocated` exactly as the decomposition assigns.

I could not find a material defect: a competent Rust engineer can build this module, correctly, from this document.

## Revision list (all sharpening)

1. **[SHARPENING]** Expand `mint_document` / `mint_version` / `mint_link` to explicit bodies. They're given only as a "pattern delta to `mint_content`" (precondition + `*_ns`). Everything needed is present and derivable, but spelling out the three two-line bodies (e.g. `mint_document`: `if self.entity_level(account)!=Some(Level::Account){return Err(NotAnAccount)}; let a=self.next_in(&document_ns(account)).map_err(Gate)?; Ok((a.clone(),Allocate{addr:a.tumbler().clone()}))`) removes the one place the builder must reconstruct rather than read.

2. **[SHARPENING]** Make the `delegate` condition-(ii) table entry Option-faithful. `effective_owner(new_prefix).id = delegator` calls `.id` on an `Option<Principal>`; render it `effective_owner(new_prefix).map_or(false, |p| p.id == delegator)` → `NotAuthorized` (the `None` arm is reachable only if checked before (i), but stating it removes the ambiguity).

3. **[SHARPENING]** Pin the top-down (iv) range-scan bounds. "OrdMap range scan" leaves the builder to derive that `new_prefix`'s strict descendants form the contiguous lex interval `(Excluded(new_prefix), Excluded(inc(new_prefix,0)))`; state it, since the correctness of (iv) depends on that interval being exactly the principals nested under `new_prefix`.

4. **[SHARPENING]** Note (or defensively enforce) why `apply`'s `frontiers.insert(.., n)` overwrite is safe. It relies on per-namespace ordinals being monotone and M2 replaying in `Seq` order; a one-line invariant note (or a `max` on the existing value) documents why the overwrite never regresses a frontier.

5. **[SHARPENING]** Fix `principal_tier_prefixes`' return lifetime. The `move` closure borrows `a`, so `impl Iterator<Item=Tumbler> + '_` is ambiguous with `&self` present; tie it to `a` (`fn …<'a>(&self, a: &'a Address) -> impl Iterator<Item=Tumbler> + 'a`).

6. **[SHARPENING]** Reconcile `PrincipalId(pub u64)` with the prose's "opaque." Either keep it opaque (and note `u64` is the recommended default width) or drop the "opaque" framing; as written the type is concrete while the text and the Open-decisions section call it opaque.

VERDICT: CONVERGED
