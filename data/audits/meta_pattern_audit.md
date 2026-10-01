# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s3** — 63 questions (57 single-answer, 6 multi-select). Random-guess baseline: **23.9%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_B | 31.0% | 79% | 29.5% |
| position_A | 30.9% | 80% | 29.5% |
| position_D | 30.8% | 80% | 29.4% |
| position_C | 29.0% | 79% | 27.9% |
| avoid_hedged | 30.1% | 41% | 26.5% |
| similar_twin_member | 29.0% | 48% | 26.4% |
| most_absolute | 27.5% | 42% | 25.4% |
| avoid_longest | 23.9% | 79% | 23.9% |
| most_hedged | 21.2% | 41% | 22.8% |
| stem_keyword_overlap | 21.3% | 65% | 22.2% |
| longest_option | 21.4% | 100% | 21.4% |
| least_absolute | 15.8% | 42% | 20.5% |
| odd_one_out | 19.7% | 100% | 19.7% |
| shortest_option | 17.5% | 100% | 17.5% |
| code_formatted_only | 24.0% | 18% | – |
| numeric_middle | 42.0% | 16% | – |
| largest_image_option | 23.4% | 14% | – |
| smallest_image_option | 6.2% | 14% | – |

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
