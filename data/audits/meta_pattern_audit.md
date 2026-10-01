# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s7** — 35 questions (32 single-answer, 3 multi-select). Random-guess baseline: **23.9%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_C | 33.5% | 75% | 31.1% |
| similar_twin_member | 34.8% | 65% | 31.0% |
| position_A | 29.2% | 75% | 27.9% |
| position_B | 29.0% | 75% | 27.8% |
| position_D | 29.0% | 76% | 27.8% |
| avoid_longest | 25.7% | 96% | 25.6% |
| stem_keyword_overlap | 24.5% | 88% | 24.5% |
| shortest_option | 23.5% | 100% | 23.5% |
| longest_option | 19.2% | 100% | 19.2% |
| odd_one_out | 6.4% | 100% | 6.4% |
| most_hedged | 0.0% | 6% | – |
| avoid_hedged | 27.8% | 6% | – |
| least_absolute | 7.1% | 9% | – |
| most_absolute | 46.4% | 9% | – |
| code_formatted_only | 38.1% | 6% | – |
| numeric_middle | 39.9% | 18% | – |
| largest_image_option | – | 0% | – |
| smallest_image_option | – | 0% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (7)

- `s7-q015` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 59 chars vs longest distractor 52, ratio 1.13) (in >=1 displayed pool variant)
- `s7-q020` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 55 chars vs longest distractor 50, ratio 1.10) (in >=1 displayed pool variant)
- `s7-q023` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 72 chars vs longest distractor 62, ratio 1.16) (in >=1 displayed pool variant)
- `s7-q024` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 79 chars vs longest distractor 68, ratio 1.16) (in >=1 displayed pool variant)
- `s7-q028` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 107 chars vs longest distractor 97, ratio 1.10) (in >=1 displayed pool variant)
- `s7-q036` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 39 chars vs longest distractor 37, ratio 1.05) (in >=1 displayed pool variant)
- `s7-q044` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 26 chars vs longest distractor 23, ratio 1.13) (in >=1 displayed pool variant)
