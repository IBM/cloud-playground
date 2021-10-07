# Copyright (c) 2021 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash

set -ex

# Env Vars:
# COS: Cloud Object Storage instance name to use
PROJECT_NAME=$(ibmcloud ce project current | awk -F: '/Name/{ print $2 }' | sed -e 's/^[[:space:]]*//' -e "s/[[:space:]]*$//")
PROJECT_REGION=$(ibmcloud ce project current | awk -F: '/^Region/{ print $2 }' | sed -e 's/^[[:space:]]*//' -e "s/[[:space:]]*$//")
POLICY_ID=""
PROJECT_ID=$(ibmcloud ce project get --name ${PROJECT_NAME} | awk '/^ID/{ print $2 }')
BUCKET=${PROJECT_NAME}-${PROJECT_ID}

if [ -z "${COS}" ]; then
    COS_NAME="${PROJECT_NAME}-cos"
else
    COS_NAME="${COS}"
fi

COS_API_KEY="${COS_NAME}-key"
IAM_API_KEY="${PROJECT_NAME}-iam-key"
COS_SERVICE_ID="${COS_NAME}-service-id"
COS_SUB="${COS_NAME}-sub"
COS_KEY_SECRET="${COS_NAME}-secret"
IAM_KEY_SECRET="${PROJECT_NAME}-iam-secret"
COS_CONFIG_CM="${COS_NAME}-config"
BACKEND_URL_CM="${PROJECT_NAME}-backend-url"

# Create a COS instance unless one has been specified for use
if [[ -z "$COS" ]]; then
    CMD_STATUS=$(ibmcloud resource service-instance ${COS_NAME} > /tmp/cmd_output 2>&1)
    if [ ${CMD_STATUS} -ne 0 ]; then
        ibmcloud resource service-instance-create ${COS_NAME} cloud-object-storage lite global
        ibmcloud resource service-instance ${COS_NAME} > /tmp/cmd_output 2>&1
    else
        echo "${COS_NAME} already created"
    fi
    CID=$(cat /tmp/cmd_output | awk '/^ID/{ print $2 }')
else
    CMD_STATUS=$(ibmcloud resource service-instance ${COS_NAME} > /tmp/cmd_output 2>&1)
    if [ ${CMD_STATUS} -ne 0 ]; then
        echo "${COS_NAME} service not found"
        exit 1
    else
        echo "${COS_NAME} already created"
        CID=$(cat /tmp/cmd_output | awk '/^ID/{ print $2 }')
    fi
fi

# Set the COS config to use this instance
ibmcloud cos config crn --crn $CID --force
ibmcloud cos config auth --method IAM

# Create IAM authorization policy so we can receive notifications from COS
POLICY_ID=$(ibmcloud iam authorization-policy-create codeengine \
 cloud-object-storage "Notifications Manager" \
 --source-service-instance-name ${PROJECT_NAME} \
 --target-service-instance-id ${CID} | awk '/^Authorization/{ print $3 }')
echo "${POLICY_ID}" > /tmp/${PROJECT_NAME}.policyid

# Create our buckets
ibmcloud cos bucket-create --bucket ${BUCKET} \
  --ibm-service-instance-id $CID \
  --region $PROJECT_REGION

# Create a configmap
COS_REGION=$(ibmcloud cos config list | awk '/Default Region/{ print $3 }')
ibmcloud ce cm create -n ${COS_CONFIG_CM} \
  --from-literal COS_BUCKET=${BUCKET} \
  --from-literal COS_ENDPOINT=https://s3.${COS_REGION}.cloud-object-storage.appdomain.cloud \
  --from-literal COS_INSTANCE_ID=${CID} \
  --from-literal IAM_ENDPOINT=https://iam.cloud.ibm.com/identity/token

# Create a service ID to use when accessing COS and an API key for that ID
ibmcloud iam service-id-create ${COS_SERVICE_ID} > /tmp/cmd_output 
SERVICE_ID=$(cat /tmp/cmd_output | awk '/^ID/{ print $2 }')
ibmcloud iam service-policy-create ${SERVICE_ID} \
  --service-name cloud-object-storage \
  --service-instance ${CID} --roles Writer

# Store the COS-API key in a secret
TMP_FILE="/tmp/.tmpkey"
ibmcloud iam service-api-key-create ${COS_API_KEY} ${SERVICE_ID} \
  | awk '/API Key/{ print $3 }' > ${TMP_FILE}
ibmcloud ce secret create -n ${COS_KEY_SECRET} --from-file APIKEY=${TMP_FILE}
rm -f ${TMP_FILE}

# Store the CLOUD-API key in a secret
ibmcloud iam api-key-create ${IAM_API_KEY} -d ${IAM_API_KEY} --file ${TMP_FILE} -q
ibmcloud ce secret create -n ${IAM_KEY_SECRET} --from-literal APIKEY=$(cat ${TMP_FILE} | jq -r .apikey)
rm -f ${TMP_FILE}

# Setup the COS Event Source
ibmcloud ce sub cos create -n ${COS_SUB} -destination ${JOB_NAME} --destination-type job --event-type write --prefix job_ -b ${BUCKET}

#Create required config maps for frontend application
BACKEND_URL=$(ibmcloud ce app get -n ${BACKEND_NAME} | grep "URL:" | head -n 1 | awk '{print $2}')
ibmcloud ce cm create -n ${BACKEND_URL_CM} --from-literal API_URL=${BACKEND_URL}
ibmcloud ce app update -n ${FRONTEND_NAME} --env-from-configmap ${BACKEND_URL_CM}

#Create required config maps for backend application
ibmcloud ce app update -n ${BACKEND_NAME} --env-from-secret ${COS_KEY_SECRET} \
    --env-from-configmap ${COS_CONFIG_CM}

#Create required config maps for backend application
ibmcloud ce job update -n ${JOB_NAME} --env-from-secret ${COS_KEY_SECRET} \
    --env-from-secret ${IAM_KEY_SECRET} \
    --env-from-configmap ${COS_CONFIG_CM}
