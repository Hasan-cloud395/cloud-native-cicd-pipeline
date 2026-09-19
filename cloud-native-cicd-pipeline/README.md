# Cloud-Native CI/CD Pipeline

An end-to-end DevOps reference project: a small Flask microservice, containerized with
Docker, deployed to Kubernetes via Helm, provisioned on AWS with Terraform, configured
with Ansible, built/deployed through a GitHub Actions CI/CD pipeline, and monitored
with Prometheus/Grafana.

## Architecture

```
Developer push -> GitHub Actions (test -> build -> scan -> push image -> deploy)
                        |
                        v
              GitHub Container Registry (GHCR)
                        |
                        v
        Kubernetes cluster (Helm release, HPA, Ingress)
                        |
                        v
        Prometheus scrapes /metrics -> Grafana dashboards
```

Infrastructure (VPC, EKS cluster, ECR repo) is provisioned with Terraform.
Ansible is included for scenarios where you're running on plain EC2/VMs
instead of (or alongside) Kubernetes.

## Repository layout

```
app/                    Flask microservice, Dockerfile, unit tests
helm/myapp/             Helm chart (Deployment, Service, Ingress, HPA)
terraform/              AWS VPC + EKS + ECR provisioning
ansible/                Host configuration & container deployment (VM path)
monitoring/             kube-prometheus-stack values + ServiceMonitor
.github/workflows/      CI/CD pipeline (test -> build -> scan -> deploy)
```

## Pipeline stages

1. **Test** — installs dependencies and runs the pytest suite on every push/PR.
2. **Build & push** — builds a multi-stage Docker image and pushes it to
   GHCR, tagged with both `latest` and the commit SHA.
3. **Scan** — runs Trivy against the built image for CRITICAL/HIGH CVEs.
4. **Deploy** — runs `helm upgrade --install` against the target cluster and
   waits for rollout to succeed.

## Running locally

```bash
cd app
pip install -r requirements.txt
python app.py
# curl http://localhost:5000/health
```

## Building the image

```bash
docker build -t cloud-native-cicd-pipeline:local ./app
docker run -p 5000:5000 cloud-native-cicd-pipeline:local
```

## Provisioning infrastructure

```bash
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

## Deploying to Kubernetes

```bash
helm upgrade --install myapp ./helm/myapp \
  --set image.tag=<commit-sha> \
  --namespace production --create-namespace
```

## Required GitHub secrets

| Secret        | Purpose                                   |
|---------------|--------------------------------------------|
| `KUBE_CONFIG` | base64-encoded kubeconfig for the deploy job |

`GITHUB_TOKEN` for GHCR auth is provided automatically by GitHub Actions.

## Tech stack

Python (Flask) · Docker · Kubernetes · Helm · Terraform (AWS EKS/VPC/ECR) ·
Ansible · GitHub Actions · Trivy · Prometheus · Grafana

## License

MIT — see `LICENSE`.
