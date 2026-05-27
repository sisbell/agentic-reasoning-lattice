## Question 5 [evidence]

> Does udanax-green's two-phase (knife + classify-walk) protocol execute as one atomic transition, or does it sequence through observable intermediate states that correspond to existing K.μ⁻ / K.μ~ kinds?

## KB Synthesis

## Two-Phase DELETE: Atomic Transition or Observable Intermediate?

The KB gives a clear answer at two levels.

### External Observability: Strictly Atomic

[INV-ATOMICITY] (Finding 0042) is definitive: the `bed.c` event loop processes each FEBE operation via run-to-completion scheduling. `xanadu(&task)` executes the entire DELETE — both phases — before returning to `select()`. No other FEBE operation can interleave. From every external observer's perspective, DELETE is a single atomic transition with no visible intermediate.

[INV-SEQUENTIAL-DISPATCH] (Finding 0042) reinforces this: even when multiple frontends have pending requests, they are served sequentially.

---

### Internal Sequencing: Two Genuine Intermediate States

Despite external atomicity, the implementation does sequence through real, distinct POOM tree states:

**State 0 — Pre-cut:** Initial POOM. Some crums may straddle the deletion boundaries [delete_start, delete_end).

**State 1 — Post-knife, pre-delete:** `makecutsbackuptohere()` has run. [PRE-DELETE Finding 0075] establishes the invariant characterizing this state:

> `whereoncrum(blade, crum) ∈ {ONMYLEFTBORDER, ONMYRIGHTBORDER}` for every blade-crum pair — meaning no crum straddles a deletion boundary.

The formal predicate on State 1 is: `∀ crum ∈ POOM : crum.reach ≤ delete_start ∨ crum.grasp ≥ delete_end ∨ (crum.grasp ≥ delete_start ∧ crum.reach ≤ delete_end)`. All crums are now *aligned* with the deletion interval. Content still exists; no V-positions have been modified. The POOM has *more* crums than State 0 (boundary crums were split by `slicecbcpm`).

[INV-NO-ZERO-WIDTH-CRUM] (Finding 0075) holds throughout: `slicecbcpm` only fires on `THRUME` positions, so both resulting half-crums have strictly positive width.

**State 2 — Post-classify-walk:** `deletend()`'s case analysis has run:
- **Case 1 crums** (within deletion range): `disown` + `subtreefree` — removed from tree [ST-DELETE Finding 0058, 0064]
- **Case 2 crums** (after deletion): `tumblersub` applied to V-displacement via `strongsub` [ST-DELETE Finding 0053, 0055]
- **Case 0 crums** (before deletion): untouched

[FC-SUBSPACE] (Finding 0055) notes an important asymmetry in State 2: the `strongsub` exponent guard incidentally preserves cross-subspace crums (links at 2.x are immune to text-range deletion shifts), while [FC-SUBSPACE Finding 0054] shows INSERT's subspace isolation is *deliberate* via a second knife blade. Two different mechanisms, one emergent frame condition.

[ST-DELETE Finding 0057] documents what is NOT in State 2: the spanfilade is unchanged throughout both phases — no `deletespanf` function exists, so spanf permanently diverges from POOM post-deletion.

---

### Regarding K.μ⁻ / K.μ~

These labels do not appear in the KB. I cannot map them to specific kinds from the KB's evidence. What I can say is:

- State 1 (post-knife) is a formally characterizable intermediate kind: the POOM satisfies a *boundary-alignment predicate* not present before Phase 1 and not present after Phase 2 (because Phase 2 removes those aligned crums entirely).
- State 2 is the final kind matching the canonical post-DELETE postconditions in [ST-DELETE].

If K.μ⁻ and K.μ~ refer to "knife-applied" and "knife-removed" kinds in a formal enfilade theory, State 1 and State 2 respectively are the natural referents. But that mapping requires external specification of what those labels mean — it is not answerable from the KB alone.

---

## Code Exploration

I now have everything I need to give a precise, source-cited answer. Let me write it.

---

## Does the Knife + Classify-Walk Execute as One Atomic Transition?

**Short answer:** The two phases execute as a single atomic transition from every FEBE-protocol-observable vantage point. Intermediate states do exist in memory between phases, but they cannot be observed by any FEBE command because the single-threaded event loop prevents interleaving. Crucially, no intermediate state corresponds to a distinct `cenftype` (node kind) — the only kinds in the code are `GRAN`, `SPAN`, and `POOM`, and none of them change during either phase.

---

### 1. The Event Loop Establishes the Atomicity Boundary

`bed.c:153-168` — `xanadu()`:

```c
} else if (getrequest(taskptr, &request)) {
    (*requestfns[request])(taskptr);   // dispatches ONE full command
    sendresultoutput(taskptr);         // sends result only after it completes
```

And the outer event loop at `bed.c:111`: `select(nfds+1, &inputfds2, 0, 0, &timeout)` only fires after `xanadu()` returns. There is no preemption, no threading, no coroutines. One FEBE command runs to completion before the next `select()` can dispatch another. Any intermediate state inside a command handler is categorically invisible to any other FEBE participant.

---

### 2. The Phases Are Sequential C Lines Within One Function — Not Separate Transactions

All three mutating operations contain both phases inside a single function body with no return between them:

**`deletend()` — `edit.c:44–75`:**
```c
makecutsnd (fullcrumptr, &knives);                              // line 44 — knife phase
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);// line 45 — find LCA
prologuend ((typecorecrum*)father, &foffset, &fgrasp, NULL);    // line 46 — classify-walk setup
for (ptr = findleftson(father); ptr; ptr = next) {             // line 47 — classify-walk loop
    switch (deletecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1: disown(...); subtreefree(...); break;             // line 59-60 — delete
      case 2: tumblersub(&ptr->cdsp...);                        // line 63 — adjust displacement
    }
}
setwispupwards(father, 1);   // line 74
recombine(father);           // line 75
```

**`rearrangend()` — `edit.c:110–141`:** same pattern, knife at line 110, classify-walk at lines 112–136.

**`makegappm()` — `insertnd.c:148–171`:** knife at line 148, classify-walk at lines 151–169.

No function returns between the two phases. All state between phases is held in stack-local variables (`knives`, `father`, `foffset`, `fgrasp`).

---

### 3. The Knife Phase Does Create a Real (But Invisible) Intermediate State

`makecutsnd()` at `ndcuts.c:15-31` calls `makecutsdownnd()` → `makecutsbackuptohere()`. For bottom-level crums that fall exactly on a knife boundary (return value `THRUME` from `whereoncrum()`), `slicecbcpm()` is called at `ndcuts.c:84`.

`slicecbcpm()` at `ndcuts.c:373-450`:
- Creates a new bottom crum (`ndcuts.c:80`)
- Computes the new widths for both halves (`ndcuts.c:438-445`)
- Calls `adopt(new, RIGHTBRO, ptr)` at `ndcuts.c:448`

After `makecutsnd()` returns and before the classify-walk loop starts (i.e., after `edit.c:44` and before `edit.c:47`), the tree is in a state where:

- All THRUME crums have been split — no node straddles a knife boundary anymore
- The children of `father` have NOT yet had their spatial positions (`.cdsp`) adjusted for the pending deletion/rearrangement

This is a real intermediate memory state. If you could freeze execution between those two source lines and run a retrieval, you would get an answer that hasn't yet applied the pending delete or shift. But because of the event loop (§1), no FEBE command can be dispatched at this point.

There is also a K.μ~ variant: during the classify-walk loop itself (`edit.c:47-73`), some children have been processed (deleted or adjusted) and others have not. This partial state exists for the duration of the loop.

---

### 4. `cenftype` Never Changes During Either Phase — No K.μ⁻/K.μ~ Kinds Exist in the Type System

The word "kind" in `cenftype` (`GRAN`, `SPAN`, `POOM`) is never touched during a knife or classify-walk. The only place `cenftype` is assigned is in `adopt()` at `genf.c:438`:

```c
new->cenftype = old->cenftype; /* make crum know what kind it is */
```

This assignment:
1. Fires exactly once per node — when it's adopted into the tree
2. Copies the kind from the node's future sibling/parent
3. Happens **before** any structural pointer linkage (which runs at `genf.c:503–519`)

So when `slicecbcpm()` creates a new bottom crum and calls `adopt(new, RIGHTBRO, ptr)` at `ndcuts.c:448`, the new node already has `cenftype` set to the same value as `ptr`. It is never unclassified, never in a "pending reclassification" kind.

The classify-walk classification (`deletecutsectionnd`, etc.) is **spatial classification** — which interval-between-blades a node falls in. It returns integers (0, 1, 2, 3) representing position relative to knife cuts (`edit.c:191–248`). This drives structural mutations (disown, `cdsp` adjust), but it doesn't write any type field. The word "classify" in "classify-walk" does not refer to `cenftype` at all.

---

### 5. The POOM Insert Case: A Composed Two-Phase Protocol

`insertnd.c:51-61` reveals an additional layering for POOM:

```c
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);  // full knife+classify-walk for gap creation
    setwispupwards(fullcrumptr, 0);
    doinsertnd(fullcrumptr, origin, width, infoptr, index);  // actual content insertion
    setwispupwards(fullcrumptr, 1);
    break;
```

`makegappm()` is itself a complete knife+classify-walk unit (lines 148–171 of `insertnd.c`), and it returns before `doinsertnd()` is called. After `makegappm()` returns and before `doinsertnd()` runs, the POOM tree has an open gap (a region in V-space with no content). This is a structurally sound but content-incomplete state. A retrieval against the gap address would return nothing. This state is also not FEBE-observable (same event-loop argument), but it is the closest thing in the code to a defined intermediate state between two operations.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Are the two phases within one call stack? | Yes | `edit.c:44–75`, `insertnd.c:148–171` — no return between phases |
| Can any FEBE command observe the intermediate state? | No | `bed.c:111,162-163` — `select()` only fires after `xanadu()` returns |
| Does the intermediate state correspond to a distinct `cenftype`? | No | `genf.c:438` — `cenftype` is set once at `adopt()`, never during knife or classify-walk |
| Do K.μ⁻/K.μ~ correspond to distinct kind values in the code? | No | The only `cenftype` values are `GRAN`, `SPAN`, `POOM`; no intermediate type exists |
| Is the intermediate state real in memory? | Yes | After `edit.c:44`, nodes are split; before `edit.c:47`, no displacements have been adjusted |
| Does the classify-walk change node kinds? | No | It classifies spatial position relative to blades; returns section integers, not `cenftype` values |

The protocol executes as **one atomic FEBE transition** and **sequences through real intermediate memory states** between the two phases — but those states carry no distinct `cenftype` and are invisible to any protocol observer. K.μ⁻ and K.μ~ name real states in the execution trace, but they are not kinds in the code's type system.
