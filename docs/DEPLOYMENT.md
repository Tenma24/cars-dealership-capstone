# Deployment guide

## Container images

From the repository root, build and push these images to a registry accessible to your IBM Cloud project:

```sh
docker build -t REGISTRY/cars-web:1 ./server
docker build -t REGISTRY/cars-database:1 ./server/database
docker build -t REGISTRY/cars-sentiment:1 ./server/djangoapp/microservices
docker push REGISTRY/cars-web:1
docker push REGISTRY/cars-database:1
docker push REGISTRY/cars-sentiment:1
```

Replace REGISTRY with your actual registry namespace. No deployment has been claimed solely on the basis of these configuration files.

## IBM Cloud Code Engine

Create/select your Code Engine project and configure registry access. Deploy the sentiment image on port **5050**, Node image on port **3030**, and web image on port **8000**. Code Engine injects PORT for the web process. Keep the service applications private/project-visible where possible.

Node needs `MONGODB_URL` for your managed MongoDB deployment and `SERVICE_TOKEN` from a secret. Never publish MongoDB without authentication. Flask needs no API key; VADER runs locally.

Web configuration:

| Variable | Value |
| --- | --- |
| DJANGO_DEBUG | 0 |
| DJANGO_SECRET_KEY | a long random secret |
| DJANGO_ALLOWED_HOSTS | exact deployed host, without scheme |
| CSRF_TRUSTED_ORIGINS | https://your-deployed-host |
| BACKEND_URL | private Node service URL |
| SENTIMENT_URL | private Flask service URL |
| SERVICE_TOKEN | same internal secret as Node |
| SQLITE_PATH | path to durable mounted SQLite storage |

Code Engine's writable container filesystem is ephemeral. **Do not claim durable users/sessions by leaving SQLite in the container layer.** For the course demonstration, a single-instance ephemeral environment can be used only with this limitation understood; accounts disappear on replacement/restart. For a durable deployment, use a compatible persistent storage setup or migrate Django to managed PostgreSQL. SQLite must remain a single-replica deployment; do not mount the same SQLite database into several app replicas. Kubernetes with a ReadWriteOnce PVC is supplied below as a durable single-instance alternative.

Create the admin using the hosting environment's supported job/exec workflow with the same database configuration. Do not embed an administrator password in an image or GitHub workflow. Verify registration, login and review persistence through the deployed hostname before collecting evidence.

After deployment, save the actual HTTPS URL in `evidence/deploymentURL`, then capture `deployed_landingpage.png`, `deployed_loggedin.png`, `deployed_dealer_detail.png`, and `deployed_add_review.png`. Include the logged-in username where required.

## Kubernetes

The sample `deploy/kubernetes.yaml` assumes images tagged as above, an ingress/TLS controller supplied by your cluster, a default StorageClass, and a pre-created `cars-secrets` Secret containing `DJANGO_SECRET_KEY`, `SERVICE_TOKEN`, and `MONGODB_URL`. MongoDB must be a managed authenticated service. Replace REGISTRY and the example hostname before applying. The manifest deploys one Django replica with a persistent SQLite volume and internal services for Node and Flask. Adjust the volume ownership init container to your cluster's security policy if required.

## Reference documentation

- https://cloud.ibm.com/docs/codeengine?topic=codeengine-application-workloads
- https://cloud.ibm.com/docs/codeengine?topic=codeengine-envvar
- https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
- https://docs.djangoproject.com/en/5.2/howto/csrf/
