from pathlib import Path

from evaluator import evaluate_transcript

BASE_DIR = Path(__file__).resolve().parent.parent

TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "run_log.txt"

# Approximate Gemini pricing (update if needed)
INPUT_COST_PER_MILLION = 0.30
OUTPUT_COST_PER_MILLION = 2.50

# Clear previous log
LOG_FILE.write_text("", encoding="utf-8")

for transcript_file in TRANSCRIPTS_DIR.glob("*.txt"):

    print(f"Processing {transcript_file.name}...")

    try:
        transcript = transcript_file.read_text(encoding="utf-8")

        evaluation, response = evaluate_transcript(transcript)

        output_file = OUTPUT_DIR / f"{transcript_file.stem}.json"

        output_file.write_text(
            evaluation.model_dump_json(indent=4),
            encoding="utf-8"
        )

        usage = response.usage_metadata

        prompt_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        total_tokens = usage.total_token_count

        estimated_cost = (
            (prompt_tokens / 1_000_000) * INPUT_COST_PER_MILLION
            +
            (output_tokens / 1_000_000) * OUTPUT_COST_PER_MILLION
        )

        with LOG_FILE.open("a", encoding="utf-8") as log:

            log.write(f"Transcript : {transcript_file.name}\n")
            log.write("Status     : SUCCESS\n")
            log.write(f"Prompt Tokens : {prompt_tokens}\n")
            log.write(f"Output Tokens : {output_tokens}\n")
            log.write(f"Total Tokens  : {total_tokens}\n")
            log.write(f"Estimated Cost: ${estimated_cost:.6f}\n")
            log.write("-" * 50 + "\n")

        print(f"Saved {output_file.name}")

    except Exception as e:

        with LOG_FILE.open("a", encoding="utf-8") as log:

            log.write(f"Transcript : {transcript_file.name}\n")
            log.write("Status     : FAILED\n")
            log.write(f"Error      : {e}\n")
            log.write("-" * 50 + "\n")

        print(f"Failed: {transcript_file.name}")