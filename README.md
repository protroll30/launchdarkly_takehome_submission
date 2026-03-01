# launchdarkly_takehome_submission

Minimal Flask app that uses LaunchDarkly flags to switch between simple and complex (popularity vs diversity) recommendation algorithms.

Setup: pip install -r requirements.txt, copy .env.example to .env, set LD_SDK_KEY (Test env SDK key from LaunchDarkly).

Run: python app.py, open http://127.0.0.1:5000.

Flags to create in LaunchDarkly (Test env). Key must match exactly.
    - use-complex-recs: boolean, default Off. When on, uses complex recs.
    - recomm_algo_experiment: string (key uses underscores), two variations
        - For the app to choose the diversity algorithm, the variation Value sent by LaunchDarkly must be 'diversity' or 'div' 
        (case-insensitive). Any other value uses the popularity algorithm.

Targeting: Context includes key (user_key from form) and user_type (standard/power). Rules in LD can be added (ex: "when user_type = power, serve div"). With that rule, User type: power gets diversity; standard gets the default (e.g. popularity).

Testing: Toggle use-complex-recs On/Off; change default or rules for recomm_algo_experiment to see Algorithm: simple vs complex (popularity) vs complex (diversity).

