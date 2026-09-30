from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / 'models'
EXPERT_DIR = MODEL_DIR / 'experts'
BASE = 'https://raw.githubusercontent.com/UdithKumar-tech/Meghova/aisha-ml/ML/'
FILES = {
    'regime_classifier.pkl': BASE + 'regime_classifier.pkl',
    'regime_label_encoder.pkl': BASE + 'regime_label_encoder.pkl',
    'experts/active_expert.pkl': BASE + 'experts/active_expert.pkl',
    'experts/break_expert.pkl': BASE + 'experts/break_expert.pkl',
    'experts/normal_expert.pkl': BASE + 'experts/normal_expert.pkl',
    'experts/depression_expert.pkl': BASE + 'experts/depression_expert.pkl',
    'experts/coastal_orographic_expert.pkl': BASE + 'experts/coastal_orographic_expert.pkl',
}

for rel, url in FILES.items():
    dest = MODEL_DIR / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f'Downloading {rel} ...')
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)
    print(f'  saved {dest} ({dest.stat().st_size} bytes)')

print('\nAll Meghova model files downloaded.')
