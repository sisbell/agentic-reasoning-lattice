"""Maxwell 1867 theory channel — flat-corpus consultation plugin."""

import sys
from pathlib import Path

# Reach up from channels/<name>/consultations/ to workspace root, then scripts/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.consult_patterns import flat_corpus

HERE = Path(__file__).parent
CHANNEL = HERE.parent

generate_questions, consult = flat_corpus(
    resources_dir=CHANNEL / "resources",
    answer_prompt=HERE / "answer.md",
    gen_questions_prompt=HERE / "generate-questions.md",
    role_label="theory",
    channel_name="maxwell-1867",
)
