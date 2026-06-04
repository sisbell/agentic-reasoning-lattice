## Question 1 [evidence]

> In the collapse case, are the elementary steps K.μ⁻ and K.μ⁺ each independently valid (their own preconditions met), with the non-trivial-net-effect clause (ii) borne solely by the named composite K.μ~ and not by the elementary steps?

## KB Synthesis

The notation K.μ⁻, K.μ⁺, K.μ~, and "non-trivial-net-effect clause (ii)" do not appear in the KB. This is a question about a formal specification framework layered on top of the implementation findings — the KB documents implementation behavior, preconditions, state transitions, frame conditions, and invariants, but does not contain any composite-step decomposition schema using that notation or any named clause structure governing net-effect preconditions for collapse cases.

This question is not answerable from the KB.

---

## Code Exploration

I now have everything needed. Here is my complete answer.

---

## Answer: Collapse Case — Precondition Independence and Non-Trivial-Net-Effect

**The short answer is yes.** K.μ⁻ and K.μ⁺ each satisfy their own preconditions independently in the collapse case, and the non-trivial-net-effect clause (condition ii) is carried exclusively by the composite K.μ~ — implemented as the `modified`-flag gate in `recombinend()` — and is not enforced by either elementary step.

---

### The Collapse Mechanism in the Code

In udanax-green, the "collapse" of two adjacent sibling nodes is the post-operation step performed by `eatbrossubtreend()` [recombine.c:205–233], called from `takeovernephewsnd()` [recombine.c:165–203] inside `recombinend()` [recombine.c:104–131]. The composite K.μ~ maps to this path.

The entry gate for `recombinend()` is at line 112:

```c
if (father->height < 2  || !father->modified)
    return(0);
```

`!father->modified` is the non-trivial-net-effect check. It prevents the collapse machinery from even running unless something actually changed. This is the sole location where condition (ii) is enforced.

---

### K.μ⁻: The Delete Step

`deletend()` [edit.c:31–76] is the shrink/removal elementary step.

Its only precondition is addressability: `prologuend()` at line 39 establishes `[grasp, reach)` from the full-crum's current state. No precondition checks whether the deletion range actually overlaps anything. `deletecutsectionnd()` [edit.c:235–248] classifies each child crum as:

- **case 0** — unaffected (no-op on that crum)
- **case 1** — falls entirely in range (disown + free)
- **case 2** — partially in range (subtract width)
- **case −1** — error

A result of case 0 for every child crum is perfectly valid — `deletend()` completes normally, then calls `setwispupwards(father,1)` [edit.c:74] and `recombine(father)` [edit.c:75]. If nothing changed, `setwisp()` propagates no width change and `ivemodified()` does not set `modified = TRUE`, so the collapse gate at recombine.c:112 returns immediately. The delete step is structurally valid even as a no-op.

---

### K.μ⁺: The Insert Step

`insertnd()` [insertnd.c:15–111] is the grow/insertion elementary step.

Its precondition — the **only** one — is:

```c
if (iszerotumbler (&width->dsas[index]))
    gerror ("zero width in insertnd\n");
```
[insertnd.c:48–49]

That check is repeated inside `doinsertnd()` [insertnd.c:189–190] and `insertmorend()` [insertnd.c:227–228]. Width ≠ 0 is the entire precondition. Nothing else is required for the step to be "valid."

For POOM, `makegappm()` [insertnd.c:124–172] is called first. At lines 140–143 it can short-circuit:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

This `return(0)` is a no-op gap step — not a precondition failure. The insert step at line 57 (`doinsertnd()`) still runs afterwards. The step remains valid.

`insertcbcnd()` [insertnd.c:242–275] either extends an existing crum [lines 250–258] or creates a new one [lines 260–274]. Either way, `setwispupwards()` is called [lines 253, 271], and if the wisp actually changed, `ivemodified()` eventually fires, setting `modified = TRUE` up the tree. If no wisp changed, the collapse gate stays closed.

---

### Where Non-Trivial-Net-Effect Lives

`ivemodified()` [genf.c:522–544] sets the `modified` flag:

```c
ptr->modified = TRUE;   /* genf.c:539 */
```

It is called by the elementary steps only when a structural change actually occurs (a crum is disowned, a width changes, a new crum is adopted). It is never called as a precondition check — it is a *consequence* of change.

The composite K.μ~ check is at `recombinend()` [recombine.c:112]:

```c
if (father->height < 2  || !father->modified)
    return(0);
```

Only when `modified` is TRUE does the algorithm proceed to sort siblings, run `ishouldbother()` [recombine.c:150–163], and call `eatbrossubtreend()` [recombine.c:205–233] to perform the actual collapse. `ishouldbother()` performs an additional capacity check — but that too operates at the composite level, not on either elementary step individually.

---

### Summary

| Property | K.μ⁻ (`deletend`) | K.μ⁺ (`insertnd`) | K.μ~ (`recombinend` + `eatbrossubtreend`) |
|---|---|---|---|
| Own precondition | Addressable range [edit.c:39] | Non-zero width [insertnd.c:48–49] | `modified == TRUE` [recombine.c:112] |
| Can be a no-op? | Yes (all crums case 0) | Yes (makegappm short-circuits, no wisp change) | N/A — does not fire if no-op |
| Non-trivial-net-effect enforced here? | No | No | Yes, exclusively |

Each elementary step checks only its own structural precondition, which can be satisfied even when the step changes nothing. Condition (ii) — that the composite operation produce a non-trivial net change — is borne solely by the `!father->modified` gate at [recombine.c:112], which guards the composite K.μ~. Neither elementary step independently enforces it.
