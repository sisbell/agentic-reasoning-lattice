Reviewing M3 against the six source notes, the M1/M2 interfaces, and the decomposition. I traced the load-bearing machinery end-to-end before judging: the frontier allocator's `next_in`/`decompose`/`namespace`, the level-aware `(parent, g)` keying (the ASN-0123 collision-avoidance gotcha), the `ω`-stability race argument behind the in-closure vs pre-read lock decisions, and each of the seven conflict resolutions. They hold up — I'll record the spot-checks that mattered, then the polish.

**Verification highlights (no defect found):**
- **Allocator typechecks and computes the right addresses.** `decompose`'s binary `g`-recovery (`g=1 ⟺ zeros(addr)==zeros(parent)`) is sound because M1's `inc(·,1)` adds no zero and `inc(·,2)` adds exactly one — verified for all six Allocate kinds (account/sub-account/document/version/content/link). `content_ns`/`link_ns`/`version_ns`/`document_ns` anchors match ASN-0093/0047 FirstEmission, and `decompose` recovers the identical `NsKey`, so **lock key ≡ frontier key by construction** as claimed. `shift(c1, m)` for subsequent emissions is safe (c1 is a full address with its ordinal in the last position, not a bare `doc·0·subspace` base).
- **Level-awareness is correct.** content `(b_C(d),1)`, link `(b_L(d),1)`, version `(d,1)` are three distinct anchors → three distinct keys; the "`(home_doc,g)` would conflate version with content" warning is apt and avoided.
- **`ω`-stability claim is correct, including the case I doubted.** A delegation that would refine `ω(d_src)`/`ω(account)` is blocked: the only longer account-tier coverer is the account itself, which is already allocated (so `(v)` freshness rejects it), and any finer covering prefix has `zeros≥2` (so `(iii)==1` rejects it). The stable pre-read therefore makes M5's branch-dependent VERSION lock buildable.
- **Conflict resolutions are factually grounded.** Verified B6 imposes no `p∈B` (conflict 5), `baptize([1],1)=[1,1]` mints a zeros=0 node (conflict 7), O15(iii) reads `≤1`, O10 admits a node-tier self-owned-account fork (conflict 6). The `==1` narrowing + node-mint suppression are necessary and sound (an un-narrowed delegate would register a principal at a frontier-encoded "node" never added to `nodes` — an `entity_level` inconsistency).
- **Interface fidelity.** Every M1 call (`checked_inc`/`inc`/`shift`/`parent`/`zeros`/`ordinal`/`validate`/`is_prefix`/`subspace`/classify) and M2 call (`transact`/`snapshot`/`Staging`/`WorldState`/`LockKey`/`Seq`/`TxnError`) is used as given; `transact` is never re-entered (mints are pure, `fork` opens no txn of its own).

**Revision list (sharpenings only):**

1. **`[SHARPENING]`** Reconcile the `Space` enum's home. M2's interface places the central tag enum "in the engine crate," but M3 (foundation, built before `W`) hardcodes `Space::Namespace/Principals/Nodes`. State explicitly that M3 *reserves three variants* in a central `Space` enum that lives at a layer foundation modules can reference (alongside `LockKey`), not in the engine crate above M3 — otherwise a literal reading of M2's wording implies an inverted dependency.

2. **`[SHARPENING]`** Spell out the two bodies left as prose: `Namespace<W>`'s struct definition (`{ kernel: Arc<Kernel<W>> }`) and `next_account_prefix` (`g = match parent.level() { Node => 2, Account => 1, _ => return None }; self.next_in(&NsKey{ parent: parent.tumbler().clone(), g }).ok()`). Both are inferable, but `next_account_prefix` is load-bearing for M10's no-guess-and-retry path and a detailed build-spec should pin it.

3. **`[SHARPENING]`** Resolve the duplication of `principals_lock_key`/`node_lock_key` between interface §A (declared as `M3State::` associated functions) and §1 (declared as free `fn`s). Pick one home (the associated functions delegating to the encoding) so a builder isn't unsure which is canonical.

4. **`[SHARPENING]`** Drop `Span` from the "All types Tumbler/Address/Level/Span/Nat are M1's" list — M3 uses no spans; carrying it implies an endset/extent responsibility M3 doesn't own.

5. **`[SHARPENING]`** State `delegate`'s condition-evaluation precedence (which typed `DelegateError` wins when several fail). Any order is correct, but pinning it makes the typed-rejection contract deterministic for M10 and for tests.

VERDICT: CONVERGED
