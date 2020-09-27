
# Setup

## Create secret 

```
# replace accordingly
U=$(echo -n '<user>' | base64)
P=$(echo -n '<password>' | base64)

echo "
apiVersion: v1
kind: Secret
metadata:
  name: tower-secret
data:
  T_USER: ${U}
  T_PASS: ${P}
" | kubectl apply --filename=-
```

## Build container using s2i

`./build.sh`

* Requires s2i - https://github.com/openshift/source-to-image 

## Create Knative Service

```
kn service create sinktower --image=markito/sink2tower:v1 --env ENDPOINT="https://ansible.rhdemo.io/api/v2/job_templates/193/launch/"  --env-from secret:tower-secret
```

## Setup AWS SQS Event Source that sinks to the Knative Service
