from pathlib import Path

from evaluator import evaluate_transcript

BASE_DIR = Path(__file__).resolve().parent.parent

TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

for transcript_file in TRANSCRIPTS_DIR.glob("*.txt"):

    print(f"Processing {transcript_file.name}...")

    transcript = transcript_file.read_text(encoding="utf-8")

    evaluation, response = evaluate_transcript(transcript)

    output_file = OUTPUT_DIR / f"{transcript_file.stem}.json"

    output_file.write_text(
        evaluation.model_dump_json(indent=4),
        encoding="utf-8"
    )

    print(f"Saved {output_file.name}")