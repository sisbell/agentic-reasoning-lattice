## Question 16 [evidence]

> When `select()` returns multiple ready connections, does the loop ever interleave reads from one player's request with execution of another's, or is each `xanadu()` call dispatched only after a complete request is assembled — i.e., can a partial request stall mid-operation?

## KB Synthesis

Each `xanadu()` call is dispatched only after the relevant FD was marked ready by `select()`, but whether that guarantees a *complete* request is available is what matters — and the KB answers part of this.

**What the KB confirms**

[INV-ATOMICITY] (Finding 0042) documents the call chain inside `xanadu()`:

```
getrequest → requestfns[request] → sendresultoutput → tfree
```

All four steps — including request parsing via `getrequest` — happen *inside* a single `xanadu(&task)` invocation, before control returns to `select()`. [INV-SEQUENTIAL-DISPATCH] (Finding 0042) confirms that once the loop picks an FD and calls `xanadu()`, no other connection is served until `xanadu()` returns.

**The gap the KB does not cover**

The KB does not document whether `getrequest` performs a single non-blocking read or loops blocking until it has assembled a complete request. This matters:

- If `getrequest` issues a single `read()` and the `select()` guarantee (at least one byte ready) is all it relies on, a multi-segment TCP delivery could leave `getrequest` blocking inside `xanadu()` waiting for the rest of the frame — which would stall all other connections for the duration of that network delay.
- If `getrequest` reads only what `select()` has indicated is available and returns an error on a partial frame, the protocol would need a retry mechanism — but the KB records no such mechanism.

**Best-supported inference**

Given that the system uses Unix socket I/O over `select()` and is described as single-threaded with run-to-completion dispatch, the most consistent reading of [INV-ATOMICITY] is that `getrequest` *does* block until the full request arrives. That means a slow or misbehaving frontend that sends a request in fragments would stall the entire daemon — other connections see no progress until `getrequest` returns and `xanadu()` completes.

There is no interleaving of reads across connections (the sequential loop prevents that), but a partial request *does* stall mid-`xanadu()`, blocking all others for as long as `getrequest` waits for the remaining bytes. The KB does not document a mechanism that would allow the loop to time out, yield, or serve another connection while a request is being assembled.

---

## Code Exploration

I have everything needed to give a complete, cited answer.

---

## Answer

**Short answer: yes, a partial request can stall the entire server mid-operation.** There is no complete-request assembly gate before `xanadu()` is called, and every argument byte is read lazily from a blocking `getc()` inside the request handler itself.

---

### The event loop (`bed.c`)

```c
/* bed.c:110-141 */
inputfds2 = inputfds;
if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
else {
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            user = fdtoplayer[i];           // bed.c:120
            task.inp = player[user].inp;    // bed.c:121
            task.outp = player[user].outp;
            task.account = player[user].account;
            ...
            xanadu(&task);                  // bed.c:128
            ...
        }
    }
}
```

`select()` fires when **any** data is available on a socket — it makes no guarantee that a complete request has arrived. The `for` loop then iterates fd-numbers 0 to `nfds` and calls `xanadu()` for each ready fd **in-order**. `xanadu()` must return before the loop can advance to the next fd.

---

### What `xanadu()` does (`bed.c:153-172`)

```c
int xanadu(typetask *taskptr)
{
    typerequest request;
    logstuff = FALSE;
    if (setjmp(frontendeof)) {
        dobertexit(user);
        player[user].wantsout = TRUE;
    } else if (getrequest(taskptr, &request)) {   // bed.c:161
        (*requestfns[request])(taskptr);           // bed.c:162 — handler reads its own args
        sendresultoutput(taskptr);
        if (request == QUIT) player[user].wantsout = TRUE;
    }
    tfree(taskptr);
    ...
}
```

`getrequest()` reads **only the request opcode** (the integer before the `~`). It does not buffer or pre-read arguments. The dispatch at `bed.c:162` happens after only that opcode is confirmed.

---

### How `getrequest()` reads (`get2fe.c:297-322`)

```c
bool getrequest(typetask *taskptr, typerequest *requestptr)
{
    taskptr->charinbuff = FALSE;
    num = 0; flag = FALSE;
    while (c = pullc(taskptr)) {        // get2fe.c:313 — read one byte at a time
        if (!isdigit(c)) break;
        num = num * 10 + c - '0';
        flag = TRUE;
    }
    *requestptr = num;
    return (flag && (c == WORDELIM || c == '\n') && validrequest(...));
}
```

And `pullc()` (`get2fe.c:39-67`):

```c
char pullc(typetask *taskptr)
{
    if (taskptr->charinbuff) { ... return charbuff; }
    else {
        temp = getc(taskptr->inp);      // get2fe.c:47 — BLOCKING syscall
        if (temp == EOF) { frontenddied(); }
        ...
        return (temp);
    }
}
```

`getc()` is a blocking C library call on a `FILE*` created via `fdopen(s, "r")` at `socketbe.c:96`. If no bytes have arrived, this call **blocks the process** — not a timeout, not a signal, a full synchronous block.

---

### Where the stall happens

The handlers in `fns.c` call their own `get*` routines to parse arguments **after** dispatch:

```c
/* fns.c:41-43 (copy handler) */
if (
   getcopy(taskptr, &docisa, &vsa, &localspecset)   // reads args from socket
&& docopy(taskptr, &docisa, &vsa, localspecset))    // then executes
    putcopy(taskptr);
```

Every `getcopy`, `getspecset`, `gettumbler`, `gettext`, etc., internally calls `pullc()` → `getc()` on `taskptr->inp`. If the argument bytes haven't arrived yet, `getc()` blocks at that point.

The stall location depends on how far the client has sent:

| Client has sent | Server blocks at |
|---|---|
| Nothing yet | `pullc()` inside `getrequest()` (`get2fe.c:313`) |
| Opcode `0~` but no args | `pullc()` inside the first `get*` call in the handler |
| Part of an argument | `pullc()` mid-argument parse |

In all cases, the `xanadu()` call in the `bed.c:128` loop **has not returned**, so the `for` loop cannot advance to the next ready fd. Other players with complete requests sitting in their socket buffers — already marked ready by `select()` — wait.

---

### No interleaving, but also no protection

The design is strictly **one-request-at-a-time**: there is no interleaving of reads from different connections, because there is only one thread and the outer loop is blocked inside `xanadu()`. What you get instead is the opposite problem: a single stalled connection locks out everyone else.

The `setjmp`/`longjmp` at `bed.c:158-160` only triggers on `EOF` (connection close), not on a slow/partial writer. A client that sends `0~` (INSERT opcode) and then stops writing holds the server indefinitely.

The 2-second `select()` timeout (`bed.c:74`) only controls how long the server waits for *any* player to have data before cycling through `new_players()` and `leave()`. Once inside `xanadu()`, there is no timeout on any individual read.

---

### Summary

- **`xanadu()` is dispatched after only the opcode is confirmed**, not after a complete request is assembled (`bed.c:161-162`, `get2fe.c:297-322`).
- **Argument reads happen lazily inside the handler**, via blocking `getc()` calls (`get2fe.c:47`).
- **A partial request stalls the server**: if a client sends a partial message, the server blocks in `pullc()` → `getc()` inside `xanadu()`, and the outer `for` loop in `bed.c:118` cannot advance to serve other connections.
- **There is no interleaving**: reads from one player's request and another player's execution cannot overlap — the server is single-threaded and processes one connection at a time — but this is not a feature, it's a consequence of the same blocking design that enables the stall.
