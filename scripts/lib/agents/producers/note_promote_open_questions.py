"""Note-promote-open-questions producer — promote ASN open-questions
into new inquiry ASNs.

Operator-gated pure producer. One fire = read the source ASN's "Open
Questions" section, ask the LLM which questions warrant their own
ASN, create a substrate-citizen inquiry doc per promoted item, and
save a `promotion.open-questions` classified audit report.

Caste: pure producer (one-shot identity grant). The LLM plays the
scout role here (decides which items earn new identity); the
operator is the trigger ("scan ASN-N now"). This makes promote
architecturally distinct from extract/absorb/clone, where the
operator plays the scout. Per agent-castes.md the choreography is
still Scout → Producer.

Identity grants per fire:

  - `inquiry` classifier on each new inquiry doc
  - `promotion.open-questions` classifier on the audit report
  - `provenance.derivation(source_note → report)`
  - `provenance.derivation(report → each new inquiry)`

Operator workflow:

  python scripts/promote-open-questions.py 34
"""

from __future__ import annotations

import sys
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.agents.producers._promote_helpers import (
    create_inquiry_doc, load_existing_inquiries, load_existing_promotion,
    next_asn_number, parse_promoted, save_promotion_report,
)
from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session
from lib.shared.common import find_asn, log_usage, read_file
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import LATTICE, prompt_path


PROMOTE_TEMPLATE = prompt_path("discovery/promotion/promote-open-questions.md")


class NotePromoteOpenQuestionsAgent(Agent):
    """One promote-open-questions per fire — pure producer (operator-gated)."""

    role: ClassVar[str] = "note-promote-open-questions"

    def __init__(self, *, model: str = "opus", effort: str = "max"):
        self.model = model
        self.effort = effort

    def run(self, session: Session, note_addr: Address) -> AgentResult:
        note_rel = session.get_path_for_addr(note_addr)
        if note_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        import re
        m = re.search(r"ASN-(\d{4})", note_rel)
        if m is None:
            return AgentResult(success=False, detail="unparseable-note-path")
        asn_num = int(m.group(1))
        asn_path, asn_label = find_asn(str(asn_num))
        if asn_path is None:
            return AgentResult(success=False, detail="find_asn-failed")

        template = read_file(PROMOTE_TEMPLATE)
        if not template:
            return AgentResult(success=False, detail="prompt-template-missing")

        inquiries_text = load_existing_inquiries(session)
        existing_promotion = load_existing_promotion(asn_num, "open-questions")

        prompt = (
            template
            .replace("{{asn_content}}", asn_path.read_text())
            .replace("{{inquiries}}", inquiries_text)
            .replace("{{existing_promotion}}", existing_promotion or "(none)")
        )

        print(f"  [PROMOTE] {asn_label} — open questions", file=sys.stderr)
        print(f"  Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

        result = invoke_claude(prompt, model=self.model, effort=self.effort)
        if not result.text:
            return AgentResult(success=False, detail="llm-no-output")
        log_usage("promote-open-questions", result.elapsed, asn=asn_num)

        promoted = parse_promoted(result.text)
        promoted_addrs = []
        if promoted:
            print(
                f"\n  {len(promoted)} new ASN(s) promoted:", file=sys.stderr,
            )
            cur_num = next_asn_number(session)
            for item in promoted:
                if "title" not in item or "question" not in item:
                    print(f"  [SKIP] Incomplete item: {item}", file=sys.stderr)
                    continue
                area = item.get("area", "")
                print(
                    f"    ASN-{cur_num:04d}: {item['title']} [{area}]",
                    file=sys.stderr,
                )
                addr = create_inquiry_doc(
                    session, cur_num, item["title"], item["question"],
                    area, asn_num,
                    nelson=item.get("nelson", 10),
                    gregory=item.get("gregory", 10),
                )
                promoted_addrs.append(addr)
                cur_num += 1
        else:
            print(f"\n  No new ASNs promoted from {asn_label}", file=sys.stderr)

        source_note_addr = session.get_addr_for_path(
            str(asn_path.relative_to(LATTICE)),
        )
        save_promotion_report(
            session, asn_num, "open-questions", result.text,
            source_note_addr=source_note_addr,
            promoted_inquiry_addrs=promoted_addrs,
        )

        return AgentResult(
            success=True,
            detail=f"asn={asn_label} promoted={len(promoted_addrs)}",
        )
