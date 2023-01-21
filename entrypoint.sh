#!/usr/bin/env sh
set -e
action=$1
shift

help () {
  echo "
  Backend Available Commands
    help                     : show this help
    runserver                : start a local development server
    test [args...]           : run pytest args with coverage report if no args run full test suite
  "
}

run_server () {
  exec "uvicorn" "main:app" "--app-dir" "/user/home" "--host" "0.0.0.0" "--port" "8000"
}

case ${action} in
help)
  help
  exit 0
  ;;
runserver)
  run_server
  ;;
test)
  exec "pytest" "--cov-report" "html" "--cov-report" "xml" "--cov-report" "term" "--cov=app" "--cov-config=.coveragerc" "${@}"
  ;;
*)
  echo "Unknown action: \"${action}\"."
  help
  ;;
esac

exec "${action}" "$@"
