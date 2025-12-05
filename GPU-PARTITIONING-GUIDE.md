# NVIDIA A30 GPU Partitioning Demo for Nutanix Kubernetes

## Overview

This demo showcases **GPU Multi-Instance GPU (MIG) partitioning** on 2x NVIDIA A30 GPUs in a Nutanix Kubernetes environment. It demonstrates how to maximize GPU utilization, enable multi-tenancy, and provide workload isolation for AI/ML workloads.

## Customer Environment

- **Hardware**: 2x NVIDIA A30 GPUs (24GB VRAM each)
- **Platform**: Nutanix AHV with Kubernetes (Karbon/Upstream)
- **Storage**: Nutanix Files for persistent model storage
- **Networking**: Ingress controller for external access

## What is MIG (Multi-Instance GPU)?

NVIDIA MIG technology allows a single A30 GPU to be partitioned into multiple isolated GPU instances, each with:
- Dedicated GPU compute resources
- Isolated memory bandwidth
- Separate fault domains
- QoS guarantees

### A30 MIG Profiles

| Profile | GPU Memory | Compute | Max Instances | Use Case |
|---------|------------|---------|---------------|----------|
| 1g.6gb  | 6 GB       | 1/4 GPU | 4 per A30     | Development, CI/CD, Edge |
| 2g.12gb | 12 GB      | 1/2 GPU | 2 per A30     | Staging, Medium Models |
| Full GPU| 24 GB      | Full GPU| 1 per A30     | Production, Large Models |

## Architecture

### Scenario 1: Multi-Tenant Environment
```
┌─────────────────────────────────────────────────────────┐
│  NVIDIA A30 GPU #1 (24GB) - MIG Partitioned            │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌────────────────────────┐  │
│  │ Dev Pod  │ │ Dev Pod  │ │   Staging Pod          │  │
│  │ 1g.6gb   │ │ 1g.6gb   │ │   2g.12gb              │  │
│  │ (6GB)    │ │ (6GB)    │ │   (12GB)               │  │
│  └──────────┘ └──────────┘ └────────────────────────┘  │
│  Namespace: ai-dev (x2)     Namespace: ai-staging      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  NVIDIA A30 GPU #2 (24GB) - MIG Partitioned            │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌────────────────────────┐  │
│  │ Dev Pod  │ │ Dev Pod  │ │   Staging Pod          │  │
│  │ 1g.6gb   │ │ 1g.6gb   │ │   2g.12gb              │  │
│  │ (6GB)    │ │ (6GB)    │ │   (12GB)               │  │
│  └──────────┘ └──────────┘ └────────────────────────┘  │
│  Namespace: ai-dev (x2)     Namespace: ai-staging      │
└─────────────────────────────────────────────────────────┘

Total: 4x dev pods + 2x staging pods = 6 isolated workloads
```

### Scenario 2: Production HA Setup
```
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│  NVIDIA A30 GPU #1 (Full 24GB)  │  │  NVIDIA A30 GPU #2 (Full 24GB)  │
├──────────────────────────────────┤  ├──────────────────────────────────┤
│  ┌────────────────────────────┐  │  │  ┌────────────────────────────┐  │
│  │  Production Pod (Primary)  │  │  │  │  Production Pod (Replica)  │  │
│  │  llama3.1:70b             │  │  │  │  llama3.1:70b             │  │
│  │  Full GPU - 24GB          │  │  │  │  Full GPU - 24GB          │  │
│  └────────────────────────────┘  │  │  └────────────────────────────┘  │
│  Namespace: ai-workloads         │  │  Namespace: ai-workloads         │
└──────────────────────────────────┘  └──────────────────────────────────┘
         │                                          │
         └──────────────┬───────────────────────────┘
                        ▼
              Kubernetes Service (Load Balanced)
```

## Model Comparison

### Small Model (llama3.2:1b)
- **Parameters**: 1 Billion
- **MIG Profile**: 1g.6gb (6GB)
- **Memory Usage**: ~2-3GB
- **Use Cases**: 
  - Development & testing
  - CI/CD pipelines
  - Edge deployments
  - Quick prototyping
- **Performance**: 40-60 tokens/sec (CPU), 100-150+ tokens/sec (GPU)
- **Pods per A30**: 4 (with MIG)

### Medium Model (llama3.2:3b)
- **Parameters**: 3 Billion
- **MIG Profile**: 2g.12gb (12GB)
- **Memory Usage**: ~5-8GB
- **Use Cases**:
  - Staging environments
  - QA testing
  - Medium workloads
  - Customer demos
- **Performance**: 20-40 tokens/sec (CPU), 60-100+ tokens/sec (GPU)
- **Pods per A30**: 2 (with MIG)

### Large Model (llama3.1:8b)
- **Parameters**: 8 Billion
- **MIG Profile**: Full GPU (24GB)
- **Memory Usage**: ~12-18GB
- **Use Cases**:
  - Production APIs
  - Customer-facing services
  - High-quality inference
  - Complex reasoning tasks
- **Performance**: 10-25 tokens/sec (CPU), 40-80+ tokens/sec (GPU)
- **Pods per A30**: 1 (full GPU)

*Note: 70B models would require multiple GPUs or tensor parallelism*

## Demo Components

### 1. Kubernetes Manifests (`k8s-manifests/`)

#### `00-namespace.yaml`
Creates three namespaces for workload isolation:
- `ai-dev` - Development workloads
- `ai-staging` - Staging/QA workloads
- `ai-workloads` - Production workloads

#### `01-ollama-small-deployment.yaml`
- Deploys small model (1B) with MIG 1g.6gb profile
- 2 replicas for redundancy
- 4Gi memory request, 8Gi limit
- Nutanix Files PVC for model storage

#### `02-ollama-medium-deployment.yaml`
- Deploys medium model (3B) with MIG 2g.12gb profile
- 2 replicas with pod anti-affinity
- 10Gi memory request, 16Gi limit
- Supports 2 concurrent requests

#### `03-ollama-large-deployment.yaml`
- Deploys large model (8B/70B) with full A30 GPU
- 2 replicas spread across both GPUs
- 32Gi memory request, 48Gi limit
- Supports 4 concurrent requests
- Production-grade with proper health checks

#### `04-ingress.yaml`
- Exposes services via NGINX Ingress
- Separate hostnames per environment
- Configured timeouts for long-running inference

### 2. Demo Script (`gpu-partitioning-demo.py`)

Interactive Python script that demonstrates:
1. **A30 MIG topology** - Visual representation of partitioning
2. **Model performance comparison** - Real benchmarks across model sizes
3. **Resource allocation scenarios** - Different deployment strategies
4. **Deployment walkthrough** - Step-by-step setup guide
5. **Monitoring commands** - How to track GPU utilization

**Usage:**
```bash
./gpu-partitioning-demo.py
```

## Quick Start

### Prerequisites

1. **Enable MIG on A30 GPUs** (on each node with A30):
```bash
# Enable MIG mode
sudo nvidia-smi -mig 1

# Create MIG instances (example: 1x 2g.12gb + 2x 1g.6gb per GPU)
sudo nvidia-smi mig -cgi 14,9,9 -C

# Verify MIG configuration
nvidia-smi mig -lgi
```

2. **Install NVIDIA Device Plugin**:
```bash
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/main/deployments/static/nvidia-device-plugin.yml
```

3. **Label GPU nodes**:
```bash
kubectl label nodes <node-name> nvidia.com/gpu.product=NVIDIA-A30
```

### Deploy Demo Workloads

```bash
# Navigate to demo directory
cd ~/nutanix-k8s-ai-demo

# Deploy all resources
kubectl apply -f k8s-manifests/

# Verify deployments
kubectl get pods -A -l app=ollama
kubectl get svc -A -l app=ollama

# Check GPU allocation
kubectl describe node <node-name> | grep nvidia.com
```

### Load Models into Pods

```bash
# Small model (dev)
kubectl exec -n ai-dev deploy/ollama-small -- ollama pull llama3.2:1b

# Medium model (staging)
kubectl exec -n ai-staging deploy/ollama-medium -- ollama pull llama3.2:3b

# Large model (production)
kubectl exec -n ai-workloads deploy/ollama-large -- ollama pull llama3.1:8b
```

### Test Inference

```bash
# Port forward to production service
kubectl port-forward -n ai-workloads svc/ollama-large 11434:11434

# Test query
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Explain Kubernetes pod scheduling in 3 sentences",
  "stream": false
}'
```

## Monitoring

### GPU Utilization

```bash
# View nvidia-smi from pod
kubectl exec -n ai-workloads <pod-name> -- nvidia-smi

# Monitor MIG instances
kubectl exec -n ai-workloads <pod-name> -- nvidia-smi mig -lgi

# Watch GPU metrics
watch -n 1 'kubectl exec -n ai-workloads <pod-name> -- nvidia-smi'
```

### Resource Usage

```bash
# Pod resource usage
kubectl top pods -n ai-workloads
kubectl top pods -n ai-staging
kubectl top pods -n ai-dev

# Node resource allocation
kubectl describe node <node-name> | grep -A 10 'Allocated resources'

# Events and logs
kubectl get events -n ai-workloads --sort-by='.lastTimestamp'
kubectl logs -n ai-workloads -l app=ollama --tail=50
```

### DCGM Exporter (Optional)

Deploy NVIDIA DCGM for Prometheus metrics:
```bash
helm repo add gpu-helm-charts https://nvidia.github.io/dcgm-exporter/helm-charts
helm install dcgm-exporter gpu-helm-charts/dcgm-exporter \
  --namespace gpu-monitoring --create-namespace
```

## Benefits for Customer

### 1. **Higher GPU Utilization**
- Without MIG: 30-40% average utilization
- With MIG: 80-90% average utilization
- **2-3x improvement in resource efficiency**

### 2. **Cost Optimization**
- Run 6-8 workloads on 2 GPUs instead of 2
- Reduce hardware requirements by 50-75%
- Better ROI on expensive GPU hardware

### 3. **Workload Isolation**
- Fault isolation: one partition failure doesn't affect others
- QoS guarantees: predictable performance per workload
- Security: tenant separation at GPU level

### 4. **Flexibility**
- Mix different model sizes on same hardware
- Dynamically adjust partitions based on demand
- Support dev/staging/prod on same cluster

### 5. **Redundancy**
- 2 replicas per workload across both GPUs
- No single point of failure
- High availability for production workloads

## Best Practices

1. **Use pod anti-affinity** to spread replicas across nodes
2. **Set proper resource requests/limits** to prevent OOM kills
3. **Use Nutanix Files** for shared model storage (ReadWriteMany)
4. **Monitor GPU utilization** with DCGM or nvidia-smi
5. **Implement health checks** for model availability
6. **Use ingress** for unified access control
7. **Tag GPU nodes** for proper pod scheduling
8. **Test MIG profiles** before production deployment

## Troubleshooting

### Pod stuck in Pending
```bash
# Check GPU availability
kubectl describe node <node-name> | grep nvidia.com

# Verify MIG configuration
kubectl exec -it <any-pod> -- nvidia-smi mig -lgi

# Check events
kubectl describe pod <pod-name> -n <namespace>
```

### Model loading slow
```bash
# Check if using Nutanix Files with proper bandwidth
kubectl describe pvc -n <namespace>

# Increase replica count for faster parallel downloads
kubectl scale deployment -n ai-dev ollama-small --replicas=4
```

### GPU memory errors
```bash
# Verify MIG profile matches resource requests
kubectl get pod <pod-name> -n <namespace> -o yaml | grep nvidia.com

# Check actual GPU memory usage
kubectl exec -n <namespace> <pod-name> -- nvidia-smi
```

## Additional Resources

- [NVIDIA MIG User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/)
- [Kubernetes Device Plugin](https://github.com/NVIDIA/k8s-device-plugin)
- [Nutanix Karbon Documentation](https://portal.nutanix.com/page/documents/details?targetId=Karbon-v2_7:Karbon-v2_7)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/README.md)

## Demo Presentation Tips

1. **Start with topology diagram** - Show how 2 GPUs can host 6-8 workloads
2. **Run performance comparison** - Demonstrate speed differences between models
3. **Show Kubernetes manifests** - Explain resource requests and MIG profiles
4. **Live deployment demo** - Deploy one workload and show GPU allocation
5. **Monitoring showcase** - Run nvidia-smi and kubectl top pods
6. **Business value** - Emphasize cost savings and utilization improvements

## Questions to Address During Demo

- **Can we run production and dev on same GPUs?** Yes, with MIG isolation
- **What if one GPU fails?** Replicas on second GPU continue serving
- **How do we upgrade models?** Rolling updates with zero downtime
- **Can we scale dynamically?** Yes, with HPA based on request latency
- **What about different model sizes?** Mix and match MIG profiles
- **How secure is isolation?** Hardware-level isolation via MIG
- **Can we monitor per-workload GPU usage?** Yes, via DCGM/Prometheus

---

**Contact**: Demo created for Nutanix customer presentation
**Date**: December 2025
