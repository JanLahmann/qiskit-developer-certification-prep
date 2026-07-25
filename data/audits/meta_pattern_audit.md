# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s3** — 44 questions (38 single-answer, 6 multi-select). Random-guess baseline: **23.7%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_A | 34.8% | 76% | 32.1% |
| position_B | 34.7% | 76% | 32.0% |
| position_C | 31.6% | 75% | 29.6% |
| position_D | 31.5% | 75% | 29.5% |
| similar_twin_member | 38.2% | 28% | 27.7% |
| avoid_hedged | 29.6% | 59% | 27.2% |
| most_absolute | 25.9% | 60% | 25.0% |
| stem_keyword_overlap | 24.8% | 88% | 24.6% |
| code_formatted_only | 24.0% | 27% | 23.8% |
| longest_option | 23.7% | 100% | 23.7% |
| avoid_longest | 23.1% | 98% | 23.1% |
| most_hedged | 22.1% | 59% | 22.8% |
| least_absolute | 16.5% | 60% | 19.4% |
| odd_one_out | 18.0% | 100% | 18.0% |
| shortest_option | 14.0% | 100% | 14.0% |
| numeric_middle | 39.7% | 15% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (9)

- `s3-q016` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 65 chars vs longest distractor 54, ratio 1.20) (in >=1 displayed pool variant)
- `s3-q017` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 79, ratio 1.25) (in >=1 displayed pool variant)
- `s3-q017` (predict-output) — **stem_echo_tell** [medium]: correct option echoes stem vocabulary (overlap 4 vs best distractor 2) (in >=1 displayed pool variant)
- `s3-q024` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 44 chars vs longest distractor 42, ratio 1.05) (in >=1 displayed pool variant)
- `s3-q028` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 78 chars vs longest distractor 77, ratio 1.01) (in >=1 displayed pool variant)
- `s3-q030` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 96, ratio 1.03) (in >=1 displayed pool variant)
- `s3-q034` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 130 chars vs longest distractor 124, ratio 1.05) (in >=1 displayed pool variant)
- `s3-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 88 chars vs longest distractor 79, ratio 1.11) (in >=1 displayed pool variant)
- `s3-q039` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 95 chars vs longest distractor 77, ratio 1.23) (in >=1 displayed pool variant)
- `s3-q052` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 82 chars vs longest distractor 72, ratio 1.14) (in >=1 displayed pool variant)
- `s3-q052` (predict-output) — **stem_echo_tell** [medium]: correct option echoes stem vocabulary (overlap 5 vs best distractor 2) (in >=1 displayed pool variant)
