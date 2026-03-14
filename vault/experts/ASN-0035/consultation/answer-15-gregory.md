## Question 15 [gregory]

> Can a single backend process serve multiple node addresses simultaneously, or is there a strict one-process-per-node invariant enforced somewhere in the event loop (`bed.c`)?

## KB Synthesis

The KB does not document a one-process-per-node invariant, and the architecture described implies a single process serves arbitrary node addresses.

**What the KB says about the event loop**

[SS-SESSION-STATE] (Finding 0022) establishes that `bed.c` manages up to `MAX_PLAYERS = 25` concurrent connections via a `player[]` array and `select()`. Each session has its own **per-session account context** (`wheretoputit`), but all sessions share the same global enfilades. Nothing in the session model constrains which part of the address hierarchy a session can operate in.

[INV-SEQUENTIAL-DISPATCH] (Finding 0042) confirms that `bed.c:118-128` iterates over all ready file descriptors sequentially with no filtering by node:

> The event loop processes each FEBE operation atomically via run-to-completion scheduling...any serialization order produces correct results.

[FC-SESSION-ACCOUNT-ISOLATION] confirms that `account(1.1.0.1)` in session A and `account(1.1.0.2)` in session B are independent — two sessions operating under distinct accounts (and thus distinct node subtrees) coexist in the same process without interference.

[INV-GLOBAL-ADDRESS-UNIQUENESS] (Finding 0022) explicitly validates this: multiple sessions on the same account produce distinct sequential document addresses, and by implication, multiple sessions on different accounts (different nodes) also coexist correctly under one daemon.

**What the KB does not say**

There is no finding documenting a constraint of the form `bed.c` binds to one node address, rejects connections from other node subtrees, or enforces a node-scoped connection check. The address hierarchy ([SS-ADDRESS-SPACE], [SS-TUMBLER-CONTAINMENT]) is a purely logical naming convention over a flat granfilade — it carries no process-affinity semantics.

**Conclusion**

A single backend process serves multiple node addresses simultaneously. The `bed.c` event loop is address-agnostic: it dispatches operations from all sessions regardless of their current account, and the account context is a per-session variable that sessions set independently. No node-per-process invariant exists in the implementation or is implied by any KB entry.

---

## Code Exploration

---

## Answer: A Single Process Explicitly Serves Multiple Node Addresses

The architecture is **not** one-process-per-node. A single backend process is designed to serve multiple simultaneous frontend connections — each potentially with a different account/node address.

---

### 1. The Comment Says It All

`bed.c:10`:
```c
/*
    bed.d	- multi-user backend main
*/
```

This is a multi-user backend from the start. No ambiguity in intent.

---

### 2. `select()`-Based Multiplexing Over All Active Connections

`bed.c:103-142` runs the main event loop:

```c
for (;;) {
    if (n_players < 1) {
        diskflush();
        new_players(player, &n_players, TRUE, &task);  /* wait for fe */
    }
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];             /* bed.c:120 */
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;  /* bed.c:123 */
                ...
                xanadu(&task);
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

`select()` polls **all** connected frontend file descriptors simultaneously. For every ready FD in a single loop iteration, `user = fdtoplayer[i]` switches context and dispatches `xanadu()`. Multiple connections are tracked and served within one process.

---

### 3. The Player Array: Each Entry Has Its Own Account Tumbler

`players.h:13-21`:
```c
typedef struct _player {
    char    *name;
    INT     userid;
    INT     wantsout;
    INT     socket;
    FILE    *inp;
    FILE    *outp;
    tumbler account;    /* xanadu host and account tumbler */
} PLAYER;
```

`socketbe.c:37-38`:
```c
#define MAX_PLAYERS     25
PLAYER player[MAX_PLAYERS];
```

Each connected player carries its own `account` tumbler — its Xanadu node+account address. Up to **25 concurrent connections** are supported before the backend starts refusing (`socketbe.c:85-88`):

```c
if ( *n_playersp >= MAX_PLAYERS ) {
    fprintf(stderr,"TOOMANY frontends: won't log another one\n");
    close(s);
}
```

---

### 4. FD-to-Player Mapping

`socketbe.c:34`:
```c
INT fdtoplayer[32];
```

When `new_players()` accepts a new connection (`socketbe.c:118-121`):

```c
fdtoplayer[s] = *n_playersp;
inputfds |= (1<<s);
nfds = max(s, nfds);
(*n_playersp)++;
```

Each accepted socket FD maps to a player slot. The `inputfds` bitmask accumulates all active FDs. The `select()` bitmask is an `INT` (32-bit), imposing a hard ceiling of **32 file descriptors** regardless of `MAX_PLAYERS`.

---

### 5. Per-Connection Document Access Control in `bert.c`

There is no global "current node" state. The bert (open-document) table is scoped by **connection index**:

`bert.c:52`:
```c
int checkforopen(tumbler *tp, int type, int connection)
```

`bert.c:128`:
```c
int addtoopen(tumbler *tp, int connection, int created, int type)
```

`bert.c:63-79` walks the `berttable[]` hash chain and compares `bert->connection == connection` for every open-state check. Connection 0 and connection 3 have completely independent open sets on the same document. In `fns.c:396`:

```c
doopen(taskptr, &t, &newt, type, mode, user)
```

`user` — the global connection index set in `bed.c:120` — is passed as `connection` throughout.

`isthisusersdocument()` in `socketbe.c:197-201` compares the requested document's account against the *current player's* account tumbler:

```c
int isthisusersdocument(tumbler *tp) {
    return tumbleraccounteq(tp, &(player[user].account));
}
```

This means ownership checks are per-connection, not global. Two players with different account tumblers (different node addresses) are independently authorized.

---

### 6. Account (Node) Setup Is Per-Connection

`fns.c:364-373` — the `XACCOUNT` request (request code 34) sets the node address for a specific connected player:

```c
void xaccount(typetask *taskptr)
{
    if (getxaccount(taskptr, &(player[user].account))) {
        putxaccount(taskptr);
    } else {
        putrequestfailed(taskptr);
    }
}
```

This writes the incoming account tumbler directly into `player[user].account`, where `user` is the current connection index. Each connection independently negotiates its own node identity.

---

### 7. Serialization: Multi-Connection, But Single-Threaded

The global `int user` at `bed.c:28`:

```c
int user = 0;		/* Global current user ID */
```

is set before each `xanadu()` call (`bed.c:120`) and used by all downstream code to index `player[]`. This means requests are **serialized** — only one request is in flight at a time — but connections are **multiplexed**: the `select()` loop cycles through all ready FDs in a single pass. There is no I/O blocking on one connection while another waits.

---

### Summary Table

| Constraint | Value | Source |
|---|---|---|
| Max simultaneous connections | 25 | `socketbe.c:28` `MAX_PLAYERS` |
| FD bitmask ceiling | 32 | `socketbe.c:34` `fdtoplayer[32]`, `INT` select mask |
| Per-connection state | `player[user].account`, bert connection index | `players.h:20`, `bert.c:66` |
| Request execution | Serialized (single-threaded, cooperative) | `bed.c:120-128` global `user` |
| One-process-per-node invariant | **None** | — |

**Conclusion:** A single backend process can and does serve multiple node addresses simultaneously, up to a hard limit of 25 connections (or 32 FD slots, whichever binds first). Each connection independently negotiates its account/node tumbler via `XACCOUNT`. The bert access-control layer scopes all document-open state by connection index. There is no architectural enforcement of one-process-per-node anywhere in `bed.c`, `socketbe.c`, or `bert.c`.
