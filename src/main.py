from evaluator import evaluate_transcript

with open("transcripts/lesson1.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

result, response = evaluate_transcript(transcript)

print(result)