set -o errexit
set -o pipefail
set -o nounset

python -m flask db upgrade
gunicorn --bind 0.0.0.0:$PORT app:app