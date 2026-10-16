# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s3** — 67 questions (61 single-answer, 6 multi-select). Random-guess baseline: **23.9%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_A | 30.4% | 81% | 29.2% |
| position_D | 30.4% | 81% | 29.1% |
| position_C | 28.8% | 80% | 27.8% |
| position_B | 28.5% | 81% | 27.6% |
| avoid_hedged | 29.5% | 38% | 26.1% |
| similar_twin_member | 26.5% | 51% | 25.2% |
| most_absolute | 26.8% | 39% | 25.0% |
| avoid_longest | 23.9% | 74% | 23.9% |
| most_hedged | 21.4% | 38% | 23.0% |
| stem_keyword_overlap | 20.6% | 60% | 21.9% |
| longest_option | 21.6% | 100% | 21.6% |
| least_absolute | 15.9% | 39% | 20.8% |
| odd_one_out | 19.9% | 100% | 19.9% |
| shortest_option | 18.1% | 100% | 18.1% |
| code_formatted_only | 24.0% | 17% | – |
| numeric_middle | 42.0% | 14% | – |
| largest_image_option | 10.2% | 18% | – |
| smallest_image_option | 2.3% | 18% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (9)

- `s3-q016` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 65 chars vs longest distractor 54, ratio 1.20) (in >=1 displayed pool variant)
- `s3-q017` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 79, ratio 1.25) (in >=1 displayed pool variant)
- `s3-q024` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 44 chars vs longest distractor 42, ratio 1.05) (in >=1 displayed pool variant)
- `s3-q028` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 78 chars vs longest distractor 77, ratio 1.01) (in >=1 displayed pool variant)
- `s3-q030` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 99 chars vs longest distractor 96, ratio 1.03) (in >=1 displayed pool variant)
- `s3-q034` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 130 chars vs longest distractor 124, ratio 1.05) (in >=1 displayed pool variant)
- `s3-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 88 chars vs longest distractor 79, ratio 1.11) (in >=1 displayed pool variant)
- `s3-q039` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 95 chars vs longest distractor 77, ratio 1.23) (in >=1 displayed pool variant)
- `s3-q052` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 82 chars vs longest distractor 72, ratio 1.14) (in >=1 displayed pool variant)
