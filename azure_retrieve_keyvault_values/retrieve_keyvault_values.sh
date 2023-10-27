#!/bin/bash

KEYVAULT_NAME=$1

secret_names=$(az keyvault secret list --vault-name "$KEYVAULT_NAME" --query "[].name" --output tsv)

for secret_name in $secret_names; do
    secret_name=$(echo "$secret_name" | tr -d '[:space:]')

    secret_value=$( az keyvault secret show --vault-name "$KEYVAULT_NAME" --name "$secret_name" --query 'value' --output tsv )

    echo "Secret: $secret_name - Value: $secret_value"
done