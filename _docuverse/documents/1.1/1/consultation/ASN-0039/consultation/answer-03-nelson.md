## Question 3 [nelson]

> Can a position be baptized but never used — and if so, must the system distinguish between "registered but empty" and "never registered"?

### Nelson's Answer

Yes. Nelson explicitly names these "ghost elements." The key passage (4/23):

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links."

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

The word "element" here means "stored entity" — not the fourth tumbler field. Nelson has just stated that only content bytes and links are stored. Servers, accounts, and documents occupy positions on the tumbler line but have no stored representation. They ARE the ghost elements — positions that are present in the address structure but have nothing stored for them. The accompanying diagram (4/23) confirms this: server and user boxes are marked with diagonal lines indicating ghost status.

A ghost element is "virtually present in tumbler-space, since links may be made to them which embrace all the contents below them" (4/23). You can link to a server or account even though nothing is stored for it. The position is real; the stored representation is absent.

Nelson's model has no third state. The docuverse is "the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage" (4/23). A position is either conceptually assigned (baptized) or not. Whether content is stored there is a separate question. Ghost elements are baptized, addressable, linkable — but empty.
