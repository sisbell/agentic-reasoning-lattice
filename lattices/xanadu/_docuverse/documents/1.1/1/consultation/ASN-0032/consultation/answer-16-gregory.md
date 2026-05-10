## Question 16 [gregory]

> The `TRUE||!homeset` override in `sporglset2linkset` makes find_links search globally rather than scoped to a home document set — was global link discovery the original design intent, with the home-document filtering being dead code, or was scoped discovery intended but never completed?

## KB Synthesis

The `TRUE||!homeset` override is almost certainly a debugging artifact from an incomplete feature — scoped discovery was intended but never completed.

The evidence from the KB makes this clear on multiple levels:

**The code structure signals a bug, not design.** `if (TRUE||!homeset)` is a classic C debugging pattern for disabling a condition without deleting it. The semantically coherent original was `if (!homeset)`: "if no home set is provided, substitute the default permissive range." Prepending `TRUE||` disables the real condition while preserving it intact for later re-enabling. The hardcoded width of 100 was the fallback default, not an intentional "search everything" constant [EC-FIND-LINKS-GLOBAL].

**The caller faithfully passes the parameter through.** `findlinksfromtothreesp()` in `spanf1.c:56-103` accepts and passes `orglrange` to `sporglset2linkset`. If global search were the design intent, there would be no reason for the orgl range parameter to exist at the call site at all [PRE-FIND-LINKS / Finding 0069].

**Global content-identity-based discovery was the *primary* design — the orgl filter was a *secondary* scoping mechanism.** The entire link architecture is built around I-address intersection as the discovery mechanism [SS-LINK-ENDPOINT], [INV-LINK-GLOBAL-VISIBILITY], [INT-LINK-TRANSCLUSION]. The home document is for link *allocation* (where the link orgl lives) [SS-LINK-HOME-DOCUMENT], not for restricting discovery. The orgl-range filter in find_links was an additional opt-in restriction on top of content-identity search — it let you ask "among all links discoverable by content identity, return only those allocated under this document." That's a useful query but orthogonal to the core design.

**The `homedocids` filter being broken is consistent with known incompleteness.** The broken `homedocids` filter [EC-HOMEDOCIDS-FILTER-BROKEN] and the `TRUE||` override are related symptoms: orgl-range scoping was specified in the interface but the implementation was never finished or was disabled mid-development.

Bottom line: global content-identity-based discovery is the authentic design intent — that's what the whole I-address architecture is for. The orgl range filter was a planned extension to allow scoped queries, but it got disabled (`TRUE||`) at some point and was never re-enabled. The current global behavior is a consequence of that incomplete implementation, not the original vision.

---

## Code Exploration

Now I have all the evidence needed. Here is the complete answer:

---

## `TRUE||!homeset` in `sporglset2linkset`: Dead Code or Incomplete Feature?

**The answer is definitively: scoped link discovery was the original design intent. The `TRUE||` override is an in-progress development hack that was never removed, rendering an implemented protocol parameter permanently inert.**

---

### The Override

`sporgl.c:222–237`:
```c
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
    typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;

    *linksetptr = NULL;
    if (TRUE||!homeset) {                          // always true
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;       // hardcoded range
        nullhomeset.next = NULL;
        homeset = &nullhomeset;                    // discard caller's value
    }
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```

The condition `TRUE||!homeset` is a C idiom meaning *"I've decided to always take this branch for now."* It silently discards whatever homeset the caller computed and substitutes a hardcoded one. The else branch — use the caller's scope — is permanently dead.

---

### Evidence That Scoped Discovery Was The Design Intent

**1. The protocol actually reads and decodes a homeset from the client.**

`get1.c:121`:
```c
prompt (taskptr, "home documents\n");
if (!getspanset (taskptr, homesetptr, ISPANID))
    return (FALSE);
```

`get1fe.c:108–112` (FEBE binary protocol version):
```c
return (
   getspecset (taskptr, fromvspecsetptr)
&& getspecset (taskptr, tovspecsetptr)
&& getspecset (taskptr, threevspecsetptr)
&& getspanset (taskptr, homesetptr, ISPANID) && kluge());
```

This is not vestigial naming — it is actual protocol wire parsing. The client sends a homeset; the server reads and decodes it. Building a full round-trip for a parameter you intend to unconditionally ignore would be design nonsense.

**2. The prompt text "home documents\n" (`get1.c:121`) is user-facing design intent.**

It names the semantic concept explicitly: the user submits a set of home documents to scope the search.

**3. Three FEBE handlers exist with three different behaviors, showing an edit in-flight.**

`fns.c:196–201` — `findlinksfromtothree`:
```c
getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
    (typeispan*)NULL/*homeset*/, &linkset))
```
Homeset is fetched then **explicitly NULLed**, with a comment preserving the original expression. The developer changed this one.

`fns.c:211–213` — `findnumoflinksfromtothree`:
```c
getfindnumoflinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindnumoflinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
    homeset, &numberoflinks))
```
Passes homeset directly — **not updated**.

`fns.c:228–230` — `findnextnlinksfromtothree`:
```c
getfindnextnlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset,
    &homeset, &lastlink, &n)
&& dofindnextnlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
    homeset, &lastlink, &nextlinkset, &n))
```
Also passes homeset directly — **not updated**.

If the design was "always global," all three handlers would have been updated. They weren't. The `TRUE||` in `sporglset2linkset` makes the inconsistency moot, but it exposes the incomplete edit clearly.

**4. `kluge()` in `get1fe.c:198–202` is chained after homeset parsing and does nothing.**

```c
bool kluge(void)
{
/*  fclose (reallog);
    reallog = fopen("xueditlog","a");
*/  return (TRUE);
}
```

This function — explicitly named `kluge` — was inserted after homeset parsing in the FEBE path. Its body is entirely commented out; it always returns TRUE. It was a placeholder for work that was never completed.

**5. `TRUE||` is the canonical C hack for "always do this branch for now."**

In finished code, you either delete the else branch or restructure the condition. `TRUE||expr` preserves the else branch (making future restoration obvious) while ensuring it never executes. It reads as a temporary bypass left in place. Its companion — `/*TRUE||*/` in `insertnd.c:70` — shows the same pattern was used elsewhere and later removed, confirming this is a known development practice in this codebase.

---

### What the Hardcoded Substitute Actually Does

When the override fires, `nullhomeset` has:
- `stream = 0` (tumbler zero — no offset)
- `width.mantissa[0] = 100`

This is **not** the entire address space — it is a fixed range of 100 tumbler units from origin. In `sporglset2linksetinrange:257–259`:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler (&orglrange->width, 0, &range.width);
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

The ORGL search range becomes `[spantype, spantype + 100)` in the organizational dimension. Since link endpoint type slots are small integers (LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN), a width of 100 is broad enough to cover all of them. It works as a "good enough" substitute for a real home-document bound — which is exactly the behavior expected from a development workaround.

---

### Conclusion

The `TRUE||!homeset` override is **unfinished implementation, not intentional design**. The scoped link discovery feature was:

1. **Designed** — with a named concept ("home documents") and protocol field
2. **Plumbed** — the parameter travels the full call chain from wire parsing through four function layers to `sporglset2linkset`
3. **Partially implemented** — the `sporglset2linksetinrange` function accepts and uses `orglrange` when non-NULL (`sporgl.c:256–262`); the downstream logic exists
4. **Bypassed** — via `TRUE||!homeset`, which was inserted when the scoping logic was not ready or known to be broken, substituting a hardcoded approximation
5. **Never completed** — the edit to NULL out homeset in `fns.c` was done for one of three handlers; the `kluge()` placeholder was never filled in; the `TRUE||` was never removed

The home-document filtering parameter is not dead code in the sense of having never meant anything — it meant exactly what its name says, was part of a real design, and was built into the protocol. What is dead is the execution path that would have honored it.
