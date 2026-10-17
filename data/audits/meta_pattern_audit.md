# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s4** — 55 questions (50 single-answer, 5 multi-select). Random-guess baseline: **23.3%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_C | 30.4% | 79% | 28.9% |
| position_A | 29.9% | 80% | 28.6% |
| shortest_option | 28.5% | 100% | 28.5% |
| position_B | 27.9% | 79% | 26.9% |
| similar_twin_member | 33.5% | 28% | 26.2% |
| avoid_longest | 25.7% | 92% | 25.5% |
| position_D | 25.4% | 79% | 24.9% |
| most_absolute | 26.4% | 49% | 24.8% |
| avoid_hedged | 24.0% | 38% | 23.5% |
| most_hedged | 20.8% | 38% | 22.4% |
| stem_keyword_overlap | 21.7% | 91% | 21.9% |
| least_absolute | 16.8% | 49% | 20.1% |
| longest_option | 18.9% | 100% | 18.9% |
| odd_one_out | 12.5% | 100% | 12.5% |
| code_formatted_only | 21.7% | 22% | – |
| numeric_middle | 19.9% | 14% | – |
| largest_image_option | 12.5% | 4% | – |
| smallest_image_option | 25.0% | 4% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (10)

- `s4-q012` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 161 chars vs longest distractor 144, ratio 1.12) (in >=1 displayed pool variant)
- `s4-q015` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 91 chars vs longest distractor 89, ratio 1.02) (in >=1 displayed pool variant)
- `s4-q019` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 55 chars vs longest distractor 54, ratio 1.02) (in >=1 displayed pool variant)
- `s4-q027` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 81 chars vs longest distractor 74, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q032` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 108 chars vs longest distractor 99, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q040` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 71 chars vs longest distractor 65, ratio 1.09) (in >=1 displayed pool variant)
- `s4-q042` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 74 chars vs longest distractor 66, ratio 1.12) (in >=1 displayed pool variant)
- `s4-q053` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 37 chars vs longest distractor 35, ratio 1.06) (in >=1 displayed pool variant)
- `s4-q054` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 96 chars vs longest distractor 93, ratio 1.03) (in >=1 displayed pool variant)
- `s4-q058` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 87 chars vs longest distractor 83, ratio 1.05) (in >=1 displayed pool variant)
