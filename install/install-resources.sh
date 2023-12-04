#!/bin/bash

# Check if the command-line argument is provided
if [[ $# -eq 0 ]] ; then
  echo "Error: Please provide the environment as a command-line argument: 'dev','prep' or 'prod'"
  exit 1
else
  echo "Usage: $1 <environment>"
  ENV="$1"
fi

# Get the absolute path of the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Navigate to the root folder
ROOT_DIR="$SCRIPT_DIR/.."
cd "$ROOT_DIR" || exit

# Source the .env file
if [ -f .env ]; then
  source .env
else
  echo "Error: .env file not found in the root folder."
  exit 1
fi


export TF_VAR_google_project_id="$ENV-$GCP_PROJECT_ID"
export TF_VAR_google_bucket_name="$BUCKET_NAME"
export TF_VAR_google_bucket_name_processed="$BUCKET_NAME-processed"

cd ./install/modules
terraform init
terraform apply -auto-approve
