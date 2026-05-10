"""Note-promote-out-of-scope producer — promote review OUT_OF_SCOPE
items into new inquiry ASNs.

Operator-gated pure producer. One fire = collect OUT_OF_SCOPE
sections from all reviews of a source ASN, ask the LLM which items
warrant their own ASN, create substrate-citizen inquiry docs per
promoted item, and save a `promotion.out-of-scope` classified audit
report.

Caste: pure producer. The LLM plays the scout role (decides which
items earn new identity); the operator triggers the scan. Mirrors
NotePromoteOpenQuestionsAgent in shape; differs only in input
collection (review files vs note body) and prompt template.

Identity grants per fire:

  - `inquiry` classifier on each new inquiry doc
  - `promotion.out-of-scope` classifier on the audit report
  - `provenance.derivation(source_note → report)`
  - `provenance.derivation(report → each new inquiry)`

Operator workflow:

  python scripts/promote-out-of-scope.py 34
"""

from __future__ import annotations

import re
import sys
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.agents.producers._promote_helpers import (
    create_inquiry_doc, load_existing_inquiries, load_existing_promotion,
    next_asn_number, parse_promoted, save_promotion_report,
)
from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session
from lib.lattice.labels import extract_label_digits, format_label
from lib.shared.common import find_asn, log_usage, read_file
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import LATTICE, REVIEWS_DIR, prompt_path
from lib.shared.prompts import read_prompt


PROMOTE_TEMPLATE = prompt_path("agents/producers/note_promote_out_of_scope.md")


def _collect_out_of_scope(asn_label: str) -> str:
    """Collect OUT_OF_SCOPE sections from all reviews for an ASN.

    Returns formatted text with source labels, or "(none)" if empty.
    """
    review_dir = REVIEWS_DIR / asn_label
    if not review_dir.exists():
        return "(none)"

    parts = []
    for review_path in sorted(review_dir.glob("review-*.md")):
        text = review_path.read_text()
        m = re.search(r'## OUT_OF_SCOPE\b(.*?)(?=\n## |\Z)', text, re.DOTALL)
        if m:
            section = m.group(1).strip()
            if section:
                parts.append(f"### From {review_path.name}\n\n{section}")

    return "\n\n---\n\n".join(parts) if parts else "(none)"


class NotePromoteOutOfScopeAgent(Agent):
    """One promote-out-of-scope per fire — pure producer (operator-gated)."""

    role: ClassVar[str] = "note-promote-out-of-scope"

    def __init__(self, *, model: str = "opus", effort: str = "max"):
        self.model = model
        self.effort = effort

    def run(self, session: Session, note_addr: Address) -> AgentResult:
        note_rel = session.get_path_for_addr(note_addr)
        if note_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        digits = extract_label_digits(note_rel)
        if digits is None:
            return AgentResult(success=False, detail="unparseable-note-path")
        asn_num = int(digits)
        asn_path, asn_label = find_asn(str(asn_num))
        if asn_path is None:
            return AgentResult(success=False, detail="find_asn-failed")

        defer_items = _collect_out_of_scope(asn_label)
        if defer_items == "(none)":
            print(
                f"  No OUT_OF_SCOPE items found in reviews for {asn_label}",
                file=sys.stderr,
            )
            return AgentResult(success=True, detail="no-deferrals")

        template = read_prompt(PROMOTE_TEMPLATE)
        if not template:
            return AgentResult(success=False, detail="prompt-template-missing")

        inquiries_text = load_existing_inquiries(session)
        existing_promotion = load_existing_promotion(asn_num, "out-of-scope")

        prompt = (
            template
            .replace("{{defer_items}}", defer_items)
            .replace("{{inquiries}}", inquiries_text)
            .replace("{{existing_promotion}}", existing_promotion or "(none)")
        )

        print(f"  [PROMOTE] {asn_label} — out-of-scope", file=sys.stderr)
        print(f"  Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

        result = invoke_claude(prompt, model=self.model, effort=self.effort)
        if not result.text:
            return AgentResult(success=False, detail="llm-no-output")
        log_usage("promote-out-of-scope", result.elapsed, asn=asn_num)

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
                    f"    {format_label(cur_num)}: {item['title']} [{area}]",
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
            session, asn_num, "out-of-scope", result.text,
            source_note_addr=source_note_addr,
            promoted_inquiry_addrs=promoted_addrs,
        )

        return AgentResult(
            success=True,
            detail=f"asn={asn_label} promoted={len(promoted_addrs)}",
        )
