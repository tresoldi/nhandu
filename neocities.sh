#!/bin/bash
set -e

# Hardcoded defaults (optional - leave empty to require -u/-p flags)
USER=""
PASS=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Show usage information
show_usage() {
  cat <<EOF
Usage: $0 [-u USER] [-p PASS] [-h] COMMAND [ARGS...]

Options:
  -u USER    Override default username
  -p PASS    Override default password (WARNING: visible in process list)
  -h         Show this help message

Commands:
  upload FILE1 [FILE2 ...]         Upload one or more files (remote names match local basenames)
  delete FILE1 [FILE2 ...]         Delete one or more files
  list [PATH]                      List files (optionally in PATH)
  info [SITENAME]                  Get site info (yours if no sitename provided)

Examples:
  $0 upload local.html                    # Uploads as local.html
  $0 upload file1.html file2.html         # Uploads both files
  $0 upload *.html                        # Uploads all HTML files in current directory
  $0 -u myuser -p mypass delete img1.jpg img2.jpg
  $0 list
  $0 list /images
  $0 info youpi

Security Note:
  Passwords passed via -p flag are visible in process list (ps).
  For automation, consider modifying this script to use environment variables.
EOF
}

# Parse options
while getopts "u:p:h" opt; do
  case $opt in
    u) USER="$OPTARG";;
    p) PASS="$OPTARG";;
    h) show_usage; exit 0;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1;;
  esac
done
shift $((OPTIND-1))

# Check if command provided
if [ $# -eq 0 ]; then
  echo -e "${RED}Error: No command specified${NC}" >&2
  echo
  show_usage
  exit 1
fi

COMMAND="$1"
shift

# Helper function to check if credentials are provided
require_auth() {
  if [ -z "$USER" ] || [ -z "$PASS" ]; then
    echo -e "${RED}Error: This command requires authentication${NC}" >&2
    echo "Please provide credentials via -u and -p flags, or hardcode them in the script." >&2
    exit 1
  fi
}

# Command implementations

cmd_upload() {
  require_auth

  if [ $# -eq 0 ]; then
    echo -e "${RED}Error: upload requires at least one FILE argument${NC}" >&2
    exit 1
  fi

  # Loop through all provided files
  for local_file in "$@"; do
    if [ ! -f "$local_file" ]; then
      echo -e "${RED}Error: File '$local_file' does not exist${NC}" >&2
      continue
    fi

    local remote_name="$(basename "$local_file")"
    echo "Uploading '$local_file' as '$remote_name'..."
    curl -u "$USER:$PASS" -F "$remote_name=@$local_file" "https://neocities.org/api/upload"
    echo
  done
}

cmd_delete() {
  require_auth

  if [ $# -eq 0 ]; then
    echo -e "${RED}Error: delete requires at least one FILE argument${NC}" >&2
    exit 1
  fi

  echo "Deleting files: $*"

  # Build curl command with multiple -d arguments
  local curl_args=()
  for file in "$@"; do
    curl_args+=(-d "filenames[]=$file")
  done

  curl -u "$USER:$PASS" "${curl_args[@]}" "https://neocities.org/api/delete"
  echo
}

cmd_list() {
  require_auth

  local path="${1:-}"

  if [ -n "$path" ]; then
    echo "Listing files in '$path'..."
    curl -u "$USER:$PASS" "https://neocities.org/api/list?path=$path"
  else
    echo "Listing all files..."
    curl -u "$USER:$PASS" "https://neocities.org/api/list"
  fi
  echo
}

cmd_info() {
  local sitename="${1:-}"

  if [ -n "$sitename" ]; then
    # Public info doesn't require auth
    echo "Getting info for site '$sitename'..."
    curl "https://neocities.org/api/info?sitename=$sitename"
  else
    # Getting your own site info requires auth
    require_auth
    echo "Getting info for your site..."
    curl -u "$USER:$PASS" "https://neocities.org/api/info"
  fi
  echo
}

# Command dispatcher
case "$COMMAND" in
  upload) cmd_upload "$@";;
  delete) cmd_delete "$@";;
  list)   cmd_list "$@";;
  info)   cmd_info "$@";;
  *)
    echo -e "${RED}Error: Unknown command '$COMMAND'${NC}" >&2
    echo
    show_usage
    exit 1
    ;;
esac
