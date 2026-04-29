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