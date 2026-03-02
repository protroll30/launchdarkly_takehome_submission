# launchdarkly_takehome_submission

Minimal Flask app that uses LaunchDarkly flags to switch between simple and complex (popularity vs diversity) recommendation algorithms.

---

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and set your LaunchDarkly **Test** environment SDK key:
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and set `LD_SDK_KEY` to the SDK key provided in the submission email.

---

## Run

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## Flags to create in LaunchDarkly (Test env)

Flag keys must match exactly.

- **use-complex-recs** (boolean)
  - Default: Off.
  - When On, the app uses the complex recommendation path; when Off, it uses the simple algorithm.

- **recomm_algo_experiment** (string; key uses underscores)
  - Two variations (e.g. pop and div).
  - For the app to use the **diversity** algorithm, the variation value sent by LaunchDarkly must be `diversity` or `div` (case-insensitive). Any other value uses the **popularity** algorithm.

---

## Targeting

Context sent to LaunchDarkly includes:

- **key** — from the form’s User Key field
- **user_type** — from the form’s User Type dropdown (`standard` or `power`)

You can add rules in LaunchDarkly (e.g. when **user_type** is one of **power**, serve **div**). With that rule, User type **power** gets the diversity algorithm; **standard** gets the default (e.g. popularity).

---

## Testing

- Toggle **use-complex-recs** On/Off to see **Algorithm: simple** vs **complex (popularity)** or **complex (diversity)**.
- Change the default or add rules for **recomm_algo_experiment** to switch between popularity and diversity when the complex path is On.
- Submit the form with User type **standard** vs **power** to verify targeting (if you added the power rule above).
