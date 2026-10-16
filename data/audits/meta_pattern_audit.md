# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s1** — 57 questions (52 single-answer, 5 multi-select). Random-guess baseline: **24.7%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| similar_twin_member | 36.5% | 61% | 31.9% |
| position_D | 29.9% | 84% | 29.0% |
| position_B | 29.7% | 84% | 28.9% |
| shortest_option | 26.4% | 100% | 26.4% |
| position_A | 25.7% | 82% | 25.5% |
| position_C | 25.6% | 83% | 25.4% |
| avoid_longest | 25.4% | 82% | 25.3% |
| stem_keyword_overlap | 21.1% | 41% | 23.2% |
| longest_option | 22.3% | 100% | 22.3% |
| odd_one_out | 15.2% | 100% | 15.2% |
| most_hedged | 0.0% | 11% | – |
| avoid_hedged | 42.0% | 11% | – |
| least_absolute | 18.5% | 19% | – |
| most_absolute | 29.8% | 19% | – |
| code_formatted_only | 15.3% | 21% | – |
| numeric_middle | 33.0% | 9% | – |
| largest_image_option | 28.6% | 14% | – |
| smallest_image_option | 30.4% | 14% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (9)

- `s1-q012` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 82 chars vs longest distractor 70, ratio 1.17) (in >=1 displayed pool variant)
- `s1-q015` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 70 chars vs longest distractor 69, ratio 1.01) (in >=1 displayed pool variant)
- `s1-q016` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 80 chars vs longest distractor 65, ratio 1.23) (in >=1 displayed pool variant)
- `s1-q020` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 93 chars vs longest distractor 81, ratio 1.15) (in >=1 displayed pool variant)
- `s1-q026` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 69 chars vs longest distractor 60, ratio 1.15) (in >=1 displayed pool variant)
- `s1-q035` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 85 chars vs longest distractor 79, ratio 1.08) (in >=1 displayed pool variant)
- `s1-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 71 chars vs longest distractor 70, ratio 1.01) (in >=1 displayed pool variant)
- `s1-q040` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 41 chars vs longest distractor 34, ratio 1.21) (in >=1 displayed pool variant)
- `s1-q048` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 91 chars vs longest distractor 83, ratio 1.10) (in >=1 displayed pool variant)
