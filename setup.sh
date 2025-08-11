#!/usr/bin/env bash
set -e

# تفعيل بيئة افتراضية
python -m venv .venv
source .venv/bin/activate

# تحديث pip
pip install --upgrade pip

# تثبيت المكتبات من requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "✅ Environment setup complete!"
