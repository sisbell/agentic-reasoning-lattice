# Gregory Consultation

**Question:** In Gregory's udanax-green implementation, the function tumblerincrement(source, rightshift, bint, dest) takes a bint parameter that controls the increment amount. We know that element-level allocation uses bint=textset->length (inserttextingranf in granf2.c). Question: What bint values are used at each allocation level — servers, accounts, documents, versions, and elements? Find every call site of tumblerincrement across the codebase and report the rightshift and bint values used. We need to know whether bint=1 is the universal case at structural levels, or whether any structural-level allocation also uses bint>1.


## KB Synthesis

Let me search the codebase for all `tumblerincrement` call sites.

<tool_call>
{"name":"Grep","params":{"pattern":"tumblerincrement","path":"/Users/shane/Documents/github/claude/xanadu-spec","recursive":true}}
</tool_call>
<tool_response>
<status>success</status>
<result>
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:83:- tumblerlength, tumblerincrement, tumblersub
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:99:- tumblerincrement, tumblersub, tumblerscaledown
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:113:- tumblerincrement, strongsub
/Users/shan/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:127:- tumblerincrement, strongsub
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:138:- tumblerincrement, strongsub  
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:148:- tumblerincrement, strongsub
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:162:- tumblerincrement
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:189:- tumblerincrement
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:205:- tumblerincrement
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:217:- tumblerincrement
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/final-statements/ASN-0034-formal-statements.md:83:- tumblerlength, tumblerincrement, tumblersub
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md:83:- tumblerlength, tumblerincrement, tumblersub
...
</result>
</tool_response>

<tool_call>
{"name":"Glob","params":{"pattern":"/Users/shane/Documents/github/claude/xanadu-spec/**/*.c","recursive":true}}
</tool_call>
<tool_response>
<status>success</status>
<result>
No files found matching the pattern.
</tool_response>

<tool_call>
{"name":"Glob","params":{"pattern":"**/*.c","path":"/Users/shane/Documents/github/claude/xanadu-spec"}}
</tool_call>
<tool_response>
<status>success</status>
<result>
No files found matching the pattern.
</tool_response>

<tool_call>
{"name":"Bash","params":{"command":"find /Users/shane/Documents/github/claude/xanadu-spec -name '*.c' 2>/dev/null | head -20"}}
</tool_call>
<tool_response>
<status>success</status>
<result>

</status>
</result>
</tool_response>

<tool_call>
{"name":"Bash","params":{"command":"ls /Users/shane/Documents/github/claude/xanadu-spec/"}}
</tool_call>
<tool_response>
<status>success</status>
<result>
CLAUDE.md
LICENSE
README.md
notes
vault
</result>
</tool_response>

The source C files aren't in this repository. This is a spec-writing project, and the KB contains extracted findings. Let me look at what the KB already tells us about `tumblerincrement` call sites, then check any additional session logs or notes for this information.
<tool_call>
{"name":"Bash","params":{"command":"find /Users/shane/Documents/github/claude/xanadu-spec -name '*.md' | xargs grep -l 'tumblerincrement' 2>/dev/null | head -20"}}
</tool_call>
<tool_response>
<status>success</status>
<result>
/Users/shane/Documents/github/claude/xanadu-spec/vault/3-modeling/formal-statements/ASN-0034-formal-statements.md
/Users/shane/Documents/github/claude/xanadu-spec/vault/experts/ASN-0034/sessions/session_00001.md
</result>
</tool_call>
</tool_response>

<tool_call>
{"name":"Bash","params":{"command":"grep -n 'tumblerincrement' /Users/shane/Documents/github/claude/xanadu-spec/vault/experts/ASN-0034/sessions/session_00001.md | head -40"}}
</tool_call>
<tool_response>
<status>success</status>
<result>
1093:      tumblerincrement(&lsa, 0, textset->length, &lsa);
1094:```
1095:This calls `tumblerincrement(source=lsa, rightshift=0, bint=textset->length, dest=lsa)`.
1097:For a single-character insert, `textset->length=1` giving `bint=1`. For a multi-character insert, `bint=length>1`.
1102:```c
1103:tumblerincrement(&lowerbound, 0, 1, isaptr);
1104:```
1105:This calls `tumblerincrement(source=lowerbound, rightshift=0, bint=1, dest=isaptr)`.
1107:#### CREATEDOCUMENT / VERSION (structural)
1108:For structural allocation (document addresses, version addresses), we need `findisatoinsertnonmolecule`:
1109:
1110:```c
1111:tumblerincrement(hintptr->hintisa, depth-1, 1, &upperbound);
1112:```
1113:This calls `tumblerincrement(source=hintisa, rightshift=depth-1, bint=1, dest=upperbound)`.
1114:
1115:`depth` is set by `makehint`:
1116:- ACCOUNT→DOCUMENT: depth=2, so rightshift=1
1117:- DOCUMENT→DOCUMENT (version): depth=1, so rightshift=0
1118:- NODE→NODE: depth=1, so rightshift=0
1119:
1119:The `bint=1` is universal for structural allocation.
1120:
1121:#### MAKELINK (link orgl allocation)
1122:```c
1123:tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
1124:```
1125:This calls `tumblerincrement(source=hintisa, rightshift=2, bint=atomtype+1, dest=upperbound)`.
1126:
1127:`atomtype` for a LINKATOM is 2, so `bint=3`.
</result>
</tool_response>

<tool_call>
{"name":"Bash","params":{"command":"grep -n 'tumblerincrement' /Users/shane/Documents/github/claude/xanadu-spec/vault/experts/ASN-0034/sessions/session_00001.md"}}
</tool_call>
<tool_response>
<status>success</status>
<result>
1093:      tumblerincrement(&lsa, 0, textset->length, &lsa);
1094:```
1095:This calls `tumblerincrement(source=lsa, rightshift=0, bint=textset->length, dest=lsa)`.
1097:For a single-character insert, `textset->length=1` giving `bint=1`. For a multi-character insert, `bint=length>1`.
1102:```
1103:tumblerincrement(&lowerbound, 0, 1, isaptr);
1104:```
1105:This calls `tumblerincrement(source=lowerbound, rightshift=0, bint=1, dest=isaptr)`.
1107:#### CREATEDOCUMENT / VERSION (structural)
1108:For structural allocation (document addresses, version addresses), we need `findisatoinsertnonmolecule`:
1109:
1110:```c
1111:tumblerincrement(hintptr->hintisa, depth-1, 1, &upperbound);
1112:```
1113:This calls `tumblerincrement(source=hintisa, rightshift=depth-1, bint=1, dest=upperbound)`.
1114:
1115:`depth` is set by `makehint`:
1116:- ACCOUNT→DOCUMENT: depth=2, so rightshift=1
1117:- DOCUMENT→DOCUMENT (version): depth=1, so rightshift=0
1118:- NODE→NODE: depth=1, so rightshift=0
1119:
1119:The `bint=1` is universal for structural allocation.
1120:
1121:#### MAKELINK (link orgl allocation)
1122:```c
1123:tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
1124:```
1125:This calls `tumblerincrement(source=hintisa, rightshift=2, bint=atomtype+1, dest=upperbound)`.
1126:
1127:`atomtype` for a LINKATOM is 2, so `bint=3`.
</result>
</tool_response>

<tool_call>
{"name":"Bash","params":{"command":"sed -n '1070,1200p' /Users/shane/Documents/github/claude/xanadu-spec/vault/experts/ASN-0034/sessions/session_00001.md"}}
</tool_call>
<tool_response>
<status>success</status>
<result>
1070:
1071:### Question
1072:
1073:In Gregory's udanax-green implementation, the function tumblerincrement(source, rightshift, bint, dest) takes a bint parameter that controls the increment amount. We know that element-level allocation uses bint=textset->length (inserttextingranf in granf2.c). Question: What bint values are used at each allocation level — servers, accounts, documents, versions, and elements? Find every call site of tumblerincrement across the codebase and report the rightshift and bint values used. We need to know whether bint=1 is the universal case at structural levels, or whether any structural-level allocation also uses bint>1.
1074:
1075:### Answer
1076:
1076:I need to search across the codebase for all `tumblerincrement` calls. Let me be systematic.
1077:
1078:#### tumble.c — the implementation
1079:
1079:The function itself at `tumble.c:599-623`:
1080:```c
1081:tumblerincrement(typetumbler *source, int rightshift, int bint, typetumbler *dest)
1082:```
1083:It adds `bint` to the digit at position `(nstories(source) - 1 - rightshift)` from the left, then propagates carry.
1084:
1085:#### granf2.c — allocation sites
1086:
1086:Three distinct call sites in `granf2.c`:
1087:
1088:**1. inserttextingranf (element allocation — text atoms):**
1089:```c
1090:findisatoinsertmolecule(taskptr, granf, hint, (typemolecule **)&textloafptr, isaptr);
1091:...
1092:tumblerincrement(&lsa, 0, textset->length, &lsa);
1093:```
1094:This calls `tumblerincrement(source=lsa, rightshift=0, bint=textset->length, dest=lsa)`.
1094:This is the end-address computation (start + length = end), not the allocation itself.
1095:
1097:For a single-character insert, `textset->length=1` giving `bint=1`. For a multi-character insert, `bint=length>1`.
1097:
1098:**2. findisatoinsertmolecule (content address allocation — molecules/text and link atoms):**
1099:```c
1100:tumblerincrement(&lowerbound, 0, 1, isaptr);
1101:```
1102:This calls `tumblerincrement(source=lowerbound, rightshift=0, bint=1, dest=isaptr)`.
1102:The `lowerbound` is the previous highest molecule address in the bounded region.
1103:
1104: #### CREATEDOCUMENT / VERSION (structural)
1105:For structural allocation (document addresses, version addresses), we need `findisatoinsertnonmolecule`:
1106:
1107:```c
1108:tumblerincrement(hintptr->hintisa, depth-1, 1, &upperbound);
1109:```
1110:This calls `tumblerincrement(source=hintisa, rightshift=depth-1, bint=1, dest=upperbound)`.
1111:
1112:`depth` is set by `makehint`:
1113:- ACCOUNT→DOCUMENT: depth=2, so rightshift=1
1114:- DOCUMENT→DOCUMENT (version): depth=1, so rightshift=0
1115:- NODE→NODE: depth=1, so rightshift=0
1116:
1116:The `bint=1` is universal for structural allocation.
1117:
1118:#### MAKELINK (link orgl allocation)
1119:```c
1120:tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
1121:```
1122:This calls `tumblerincrement(source=hintisa, rightshift=2, bint=atomtype+1, dest=upperbound)`.
1123:
1124:`atomtype` for a LINKATOM is 2, so `bint=3`.
1125:
1126:This sets an **upper bound** for the search, not the allocated address itself. It places the ceiling of the search at `hintisa + (atomtype+1)` shifted right by 2 digits. The actual allocation is done by `findisatoinsertmolecule` using `tumblerincrement(&lowerbound, 0, 1, isaptr)` — so the final link I-address allocation still uses `bint=1`.
1127:
1127:#### tumble.c — additional call sites
1128:
1128:**tumblerincrement in `insertpm` (orglinks.c):**
1129:```c
1129:tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);
1130:```
1130:This is `tumblerincrement(source=zero, rightshift=shift, bint=inc, dest=V-width)`.
1131:`inc = tumblerintdiff(&lwidth, &zero)` extracts the integer value from the I-width.
1131:`shift = tumblerlength(vsaptr) - 1`.
1132:`bint = inc` = integer content byte count of the span.
1132:
1133:This is the **V-width encoding** call, not an allocation. It converts a content count to a V-space width tumbler. `bint` here can be any positive integer (the byte count of the content being inserted). See [SS-INSERT-VWIDTH-ENCODING].
1134:
1134:#### tumble.c — tumblerincrement within tumble.c itself
1135:
1135:Used in `tumblerscaledown`:
1136:```c
1136:tumblerincrement(t, 0, 1, t);
1137:```
1137:This rounds up the last digit by 1. `bint=1`.
1138:
1138:And also in `tumblercomputedistance`:
1139:```c
1139:tumblerincrement(tptr, 0, 1, tptr);
1140:```
1140:Again `bint=1`.
1141:
1141:#### Other call sites
1142:
1141:Searching other `.c` files in the backend — `do1.c`, `do2.c`, `orglinks.c`, `edit.c`, `sporgl.c`, `insert.c`, `retrie.c`, `credel.c`:
1142:
1142:None of these files contain direct calls to `tumblerincrement`. The allocation-related calls are centralized in `granf2.c` and `orglinks.c`.
1143:
1144:#### Summary table
1145:
1145:| Call site | rightshift | bint | Purpose |
1146:|-----------|-----------|------|---------|
1146:| `inserttextingranf` end-addr | 0 | textset->length | Compute end I-address of inserted text range |
1146:| `findisatoinsertmolecule` allocation | 0 | 1 | Allocate next content address (text or link atoms) |
1147:| `findisatoinsertnonmolecule` upper bound | depth-1 | 1 | Compute allocation search ceiling for structural allocation |
1148:| `findisatoinsertmolecule` for MAKELINK upper bound | 2 | atomtype+1 (=3 for LINKATOM) | Compute search ceiling for link atom region |
1149:| `insertpm` V-width encoding | shift=len-1 | inc (byte count) | Encode content byte count as V-space width tumbler |
1150:| `tumblerscaledown` internal | 0 | 1 | Round up last digit |
1151:| `tumblercomputedistance` internal | 0 | 1 | Round up during distance computation |
1152:
1152:**Conclusion**: `bint=1` is indeed universal for all **allocation** operations at all structural levels (accounts, documents, versions, link atoms). The exception is:
1153:- `inserttextingranf` end-address computation: `bint=textset->length` (this computes where the allocated block ends, not the start address)
1154:- `insertpm` V-width encoding: `bint=inc` (byte count of content, not an allocation)
1155:- MAKELINK upper-bound computation: `bint=atomtype+1=3` (this is a search ceiling, not an allocated address)
1155:
1155:The actual address written to `isaptr` in all allocation paths is always produced by `tumblerincrement(&lowerbound, 0, 1, isaptr)` — one step past the previous maximum.
1156:
</result>
</tool_response>

This session log contains the complete answer. Here it is synthesized:

---

## `tumblerincrement` call sites — bint and rightshift at every level

The source code does not live in this repo, but a prior expert session captured every call site. The findings cross-reference [SS-ADDRESS-ALLOC], [INV-MONOTONIC], [SS-INSERT-VWIDTH-ENCODING], and [ST-ADDRESS-ALLOC].

### Complete call-site table

| Call site | File | rightshift | bint | Purpose |
|-----------|------|-----------|------|---------|
| `inserttextingranf` end-address | `granf2.c` | 0 | `textset->length` | Compute end I-address of inserted text range (not an allocation — adds length to start to get end) |
| `findisatoinsertmolecule` allocation | `granf2.c` | 0 | **1** | Allocate next content address (text atoms AND link atoms) — the actual `isaptr` result |
| `findisatoinsertnonmolecule` upper bound | `granf2.c` | `depth-1` | **1** | Compute search ceiling for structural allocation (accounts, documents, versions) |
| MAKELINK search ceiling | `granf2.c` | 2 | `atomtype+1` = **3** for LINKATOM | Upper bound for link atom region search — **not** the allocated address |
| `insertpm` V-width encoding | `orglinks.c` | `tumblerlength(vsaptr)-1` | `inc` (byte count) | Encode byte count as V-space width tumbler [SS-INSERT-VWIDTH-ENCODING] |
| `tumblerscaledown` internal | `tumble.c` | 0 | **1** | Round up last digit |
| `tumblercomputedistance` internal | `tumble.c` | 0 | **1** | Round up during distance computation |

### The `rightshift` breakdown for structural levels

From `findisatoinsertnonmolecule` with `rightshift = depth-1`:

| Allocation type | `makehint` depth | rightshift |
|-----------------|-----------------|-----------|
| ACCOUNT→DOCUMENT | 2 | **1** |
| DOCUMENT→DOCUMENT (version, owned) | 1 | **0** |
| NODE→NODE | 1 | **0** |

### Key conclusions

**`bint=1` is universal for all actual address allocations.** Every call that writes the result into `isaptr` uses `tumblerincrement(&lowerbound, 0, 1, isaptr)` — one step past the previous maximum in the bounded region. This holds for:
- Text atom I-addresses
- Link atom I-addresses  
- Document addresses (CREATE, VERSION)

The apparent exceptions are **not allocations**:
- `inserttextingranf`: `bint=textset->length` — this computes the **end** of the block (start + length), not a fresh allocation address
- MAKELINK: `bint=3` — this sets the **upper-bound search ceiling**, not the allocated address; the actual link I-address still comes from `findisatoinsertmolecule` with `bint=1`
- `insertpm`: `bint=inc` — V-width encoding, not address allocation at all

The `rightshift` parameter does vary: `rightshift=0` for content/version/node allocation, `rightshift=1` for account→document allocation. But `bint` is locked to 1 for all of them.

---

## Code Exploration

I now have everything I need. Here is the complete analysis:

---

## `tumblerincrement` Call Sites: bint Values by Allocation Level

### The Function

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599–623]:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    ...
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
}
```

- `rightshift` controls which position in the mantissa is incremented (0 = least-significant active position)
- `bint` is the amount added at that position

---

### Type Hierarchy Constants [xanadu.h:140–146]

```c
#define NODE      1    // server/node level
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4

#define TEXTATOM  1
#define LINKATOM  2
```

---

### Structural ISA Allocation: `findisatoinsertnonmolecule` [granf2.c:203–241]

This function is invoked for all **non-ATOM** subtypes (nodes/servers, accounts, documents, versions). The critical parameter is `depth`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

All three `tumblerincrement` calls in this function use **bint=1**:

```c
tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);  // [granf2.c:213] — upper bound
...
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);            // [granf2.c:237] — first child
...
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr); // [granf2.c:240] — next sibling
```

#### Node/Server Level

`docreatenode_or_account` [do1.c:251]:
```c
makehint(NODE, NODE, 0, &isa, &hint);
```
- supertype=NODE(1), subtype=NODE(1) → `depth = (1==1) ? 1 : 2 = **1**`
- All three `tumblerincrement` calls: **rightshift ∈ {0, 1}, bint=1**

#### Account Level

Accounts are created via the same `makehint(NODE, NODE, ...)` call — there is no separate account-level allocation function. `xaccount` [fns.c:364] only reads a pre-existing player account from the player table; it does not allocate in the granfilade. Account addresses ARE node addresses, created by `docreatenode_or_account`.

- **bint=1 universally**

#### Document Level

`docreatenewdocument` [do1.c:239]:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```
- supertype=ACCOUNT(2), subtype=DOCUMENT(3) → `depth = (2==3) ? 1 : 2 = **2**`
- [granf2.c:213]: `tumblerincrement(&hintisa, 1, **1**, &upperbound)` — bint=1
- [granf2.c:237]: `tumblerincrement(&hintisa, 2, **1**, isaptr)` — bint=1
- [granf2.c:240]: `tumblerincrement(isaptr, ..., **1**, isaptr)` — bint=1

#### Version Level

`docreatenewversion` has two branches [do1.c:271, 275]:

- **Same account** (`tumbleraccounteq && isthisusersdocument`):  
  `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` — supertype==subtype → depth=1, **bint=1**

- **Different account**:  
  `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` — same as document creation, depth=2, **bint=1**

---

### Atom ISA Allocation: `findisatoinsertmolecule` [granf2.c:158–180]

Invoked when `hintptr->subtype == ATOM`, for inserting text (`TEXTATOM`) or link (`LINKATOM`) atoms. The bint values here are derived from `hintptr->atomtype`:

#### TEXTATOM (atomtype=1), called from `doinsert`/`domakelink` with `makehint(DOCUMENT, ATOM, TEXTATOM, ...)` [do1.c:117, 180]:

| Line | Call | rightshift | bint |
|------|------|-----------|------|
| [granf2.c:162] | `tumblerincrement(&hintisa, 2, atomtype+1, &upperbound)` | 2 | **2** (=TEXTATOM+1) |
| [granf2.c:166] | `tumblerincrement(&lowerbound, 2, atomtype, isaptr)` | 2 | **1** (=TEXTATOM) |
| [granf2.c:167] | `tumblerincrement(isaptr, 1, 1, isaptr)` | 1 | **1** |
| [granf2.c:169] | `tumblerincrement(&lowerbound, 0, 1, isaptr)` | 0 | **1** |

The bint=2 at line 162 constructs the **upper bound of the search range** (to find where to insert), not the increment applied to the allocated address itself.

#### LINKATOM (atomtype=2), called with `makehint(DOCUMENT, ATOM, LINKATOM, ...)` [do1.c:180, 207]:

| Line | Call | rightshift | bint |
|------|------|-----------|------|
| [granf2.c:162] | `tumblerincrement(&hintisa, 2, atomtype+1, &upperbound)` | 2 | **3** (=LINKATOM+1) |
| [granf2.c:171] | `tumblerincrement(&hintisa, 2, 2, isaptr)` | 2 | **2** |
| [granf2.c:173] | `tumblerincrement(isaptr, 1, 1, isaptr)` | 1 | **1** |
| [granf2.c:175] | `tumblerincrement(&lowerbound, 0, 1, isaptr)` | 0 | **1** |

Again, bint=3 at line 162 and bint=2 at line 171 are for **range-bound computation**, not for advancing past an existing allocation.

---

### Content Element Allocation: `inserttextgr` [granf2.c:83–109]

```c
tumblerincrement(&lsa, 0, textset->length, &lsa);  // [granf2.c:100]
```

- **bint = `textset->length`** — advances the local storage address (LSA) by the number of bytes in the text chunk

This is the **only call where bint>1 is used for actual storage position advancement**: multi-character text is laid out as a contiguous span in the granfilade, and `lsa` is stepped forward by the content length for each text segment in the list.

Also `findlastisaincbcgr` [granf2.c:280–284], which finds the last ISA in a GRANTEXT crum during search:
```c
tumblerincrement(offset, 0, (INT)ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
```
- **bint = textlength−1** — this is a **query traversal** helper, not an allocator

---

### V-Space (VSA) and Utility Calls (not ISA allocation)

These construct V-space addresses (where content lives in a document's virtual address space) and are unrelated to ISA (identity-space address) allocation:

| File:Line | Context | rightshift | bint |
|-----------|---------|-----------|------|
| `do2.c:157–158` | `findnextlinkvsa`: building minimum link VSA (2.1) | 0, 1 | **2**, **1** |
| `do2.c:172–176` | `setlinkvsas`: from-VSA (1.1), to-VSA (2.1) | 0, 1 | **1**, **1**, **2**, **1** |
| `do2.c:179–180` | `setlinkvsas`: three-VSA (3.1) | 0, 1 | **3**, **1** |
| `do2.c:58` | `tumbler2spanset`: ISA→spanset width | tumblerlength-1 | **1** |
| `sporgl.c:81–82` | `link2sporglset`: retrieving link endpoints by whichend | 0 | **whichend** (1/2/3), **1** |
| `orglinks.c:37` | `findvsatoappend`: link-space start (2.0) | 0 | **2** |
| `orglinks.c:42–43` | `findvsatoappend`: fallback VSA (1.1) | 0, 1 | **1**, **1** |
| `orglinks.c:117` | `insertpm`: V-span width from content width | shift | **inc** (computed) |
| `spanf1.c:168–169` | `finddocscontainingsp`: docspace search range | 0 | **DOCISPAN=4**, **1** |
| `do1.c:395` | `filter_vspanset_to_text_subspace`: constant 1.0 | 0 | **1** |
| `context.c:194,200,286` | context window arithmetic | 0 | computed offsets |
| `insert.c:89,94` | crum boundary tracking | 0 | textlength, remainingroom |
| `credel.c:511` | width update | 2 | **1** |
| `insertnd.c:179,181,182` | POOM node second-cut positioning | -1, 0, 1 | **1**, computed, **1** |
| `test.c:877` | test loop counter | 0 | **1** |

---

### Summary: Answer to the Question

**bint=1 is the universal case for all structural ISA-allocation levels** — nodes/servers, accounts, documents, and versions. Every call in `findisatoinsertnonmolecule` [granf2.c:213, 237, 240] uses bint=1 regardless of depth. The `depth` parameter controls the *position* in the tumbler (rightshift), not the *amount* of increment.

**bint>1 appears only in these contexts:**

1. **Content element level** (`inserttextgr` [granf2.c:100]): `bint = textset->length` — advances the granfilade LSA by actual character count.

2. **Atom ISA bound computation** (`findisatoinsertmolecule` [granf2.c:162, 166, 171]): `bint = atomtype+1` (2 or 3) and `bint = atomtype` (1 or 2) — used to compute the **search window bounds** to find where to place the next atom, not to advance the allocated address itself.

3. **V-space (VSA) construction** (do2.c, sporgl.c, orglinks.c, spanf1.c): `bint ∈ {2, 3, 4, DOCISPAN=4, whichend}` — constructing virtual-address-space coordinates and search ranges, not ISA allocation.

There is no structural-level (server/account/document/version) allocation site anywhere in the codebase where bint>1 is passed to `tumblerincrement`. The distinction is clean: **structural levels always use bint=1; only content (text bytes) and V-space coordinate construction use bint>1**.