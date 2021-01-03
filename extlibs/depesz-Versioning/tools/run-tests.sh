#!/usr/bin/env bash

# Unofficial Bash Strict Mode
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'
# End of Unofficial Bash Strict Mode

this_script="$( readlink -f "${BASH_SOURCE[0]}" )"
script_dir="$( dirname "${this_script}" )"
top_dir="$( dirname "${script_dir}" )"

cd "${top_dir}"

pg_prove t/*sql
