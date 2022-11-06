#!/bin/bash

set -ex

# -- https://docs.microsoft.com/en-us/cli/azure/iot/hub/module-twin?view=azure-cli-latest#az-iot-hub-module-twin-update

setup_prod () {
    # https://docs.microsoft.com/en-us/cli/azure/manage-azure-subscriptions-azure-cli
    az account set --subscription 'SmartCityProd'
    az account show --output table

}


IOT_HUB=Ora-ioth
DEV=E98FD595-6758-4A9D-9640-6C97DDCEA663

# setup_prod

# az iot hub device-identity list  -n ${IOT_HUB} | jq  '.[].deviceId'
# (https://docs.microsoft.com/en-us/cli/azure/iot/hub/module-identity?view=azure-cli-latest#az-iot-hub-module-identity-show)
# az iot hub module-identity show -n ${IOT_HUB} --device-id ${DEV} -m ModulePower
deploy () {
    DID=d_henry_test_v2
    DID=$1
    # https://docs.microsoft.com/en-us/azure/iot-edge/how-to-deploy-cli-at-scale?view=iotedge-2020-11
    # https://docs.microsoft.com/en-us/cli/azure/iot/edge/deployment?view=azure-cli-latest#az-iot-edge-deployment-create

    # az iot edge deployment list  -n Ora-ioth |jq '.[].id'

    CONF=/home/henry/g_nv/ds/azure/EdgeSolutionDeepStream5.1/config/deployment.arm64v8.json
    CONF=/home/henry/buspas/x_EdgeSolution/config/deployment.x.arm64v8.json
    CONF=/home/henry/g_nv/ds/azure/TSolution/config/deployment.arm64v8.json
    az iot edge deployment create -d $DID -n ${IOT_HUB} --content ${CONF} --labels '{"name":"henry", "device":"19"}' \
        --target-condition "tags.info.name='buspas19' and tags.info.version='henry'" --priority 11
    exit 0;
}
rm_deploy () {
    DID=$1
    az iot edge deployment delete -d $DID -n ${IOT_HUB} 
}

rm_deploy ds51_v1;
#rm_deploy d_henry_test_v2;
deploy ds51_v1


az iot hub module-twin  show -n ${IOT_HUB} --device-id ${DEV} -m ModulePower  #| jq '.properties.desired["telemetry-interval"]'
az iot hub module-twin  show -n ${IOT_HUB} --device-id ${DEV} -m ModuleDisplay  #| jq '.properties.desired["telemetry-interval"]'


# az iot hub module-identity show -n Zeno-ioth --device-id EdgeDevice19 -m ModulePower


# az iot hub module-twin show -n Zeno-ioth --device-id EdgeDevice19 -m ModuleDisplay   | jq '.properties.desired["telemetry-interval"]'
# az iot hub module-twin update -n Zeno-ioth --device-id EdgeDevice19 -m ModuleDisplay --desired '{"power_control": { "low":{"action_setting" : {"on":false} } }}'

#set modulePower
# az iot hub module-twin update -n Zeno-ioth --device-id EdgeDevice19 -m ModulePower --desired '{ "telemetry-interval":10 , "cloudtelemetry-interval": 10}'



