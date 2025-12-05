# 🎯 GPU PARTITIONING DEMO - PRESENTATION CHEAT SHEET

## Opening (2 minutes)

**Hook**: "What if I told you that your 2x A30 GPUs could run 6-8 AI workloads instead of just 2?"

**Customer Pain Points**:
- Low GPU utilization (30-40% typical)
- Expensive hardware sitting idle
- Can't justify more GPUs due to cost
- Need dev/staging/prod isolation

**Our Solution**: NVIDIA MIG + Kubernetes multi-tenancy

---

## Part 1: The Problem (3 minutes)

### Current State
```
GPU 1 (24GB) → 1 Production workload  (40% utilized)
GPU 2 (24GB) → 1 Staging workload     (25% utilized)

Problem: 48GB of GPU memory, only using ~15GB
Result: Wasting $15,000+ per GPU annually
```

### What They Need
- Run dev, staging, AND production on same hardware
- Isolate workloads (security + fault tolerance)
- Predictable performance per workload
- Better ROI on GPU investment

---

## Part 2: The Solution - MIG Partitioning (5 minutes)

### What is MIG?
"Multi-Instance GPU - Hardware-level partitioning of A30 into isolated slices"

### A30 Partition Options
```
┌─────────────────────────────────────┐
│  1g.6gb  → 6GB  → 4 per GPU → Dev   │
│  2g.12gb → 12GB → 2 per GPU → Stage │
│  Full    → 24GB → 1 per GPU → Prod  │
└─────────────────────────────────────┘
```

### Live Demo
```bash
./start-gpu-demo.sh
# Select option 1 - Interactive Demo
# Navigate to: Show A30 MIG topology
```

**Key Points to Emphasize**:
- Hardware isolation (not just process isolation)
- Each partition has dedicated compute + memory
- One partition crash doesn't affect others
- QoS guarantees per workload

---

## Part 3: Performance Comparison (5 minutes)

### Model Sizes Explained
```
llama3.2:1b  → Fast, lightweight  → Dev/CI/CD
llama3.2:3b  → Balanced           → Staging/QA
llama3.1:8b  → High quality       → Production APIs
```

### Live Benchmark with Graphs
```bash
# From demo menu, select option 2 or 3
./start-gpu-demo.sh → Option 2 (generates graphs automatically)
# Or interactive:
./gpu-partitioning-demo.py → Option 3
```

**What Happens:**
1. Runs benchmarks on all available models
2. Generates beautiful HTML report with charts
3. Auto-opens in browser
4. Shows throughput, response time, memory efficiency

**Expected Results**:
- 1B model: 100-150 tokens/sec (fits in 6GB)
- 3B model: 60-100 tokens/sec (needs 12GB)
- 8B model: 40-80 tokens/sec (needs 24GB)

**Customer Insight**: "Different workloads need different GPU sizes. Why give everyone 24GB?"

---

## Part 4: Kubernetes Deployment (8 minutes)

### Architecture Overview
```
Show: GPU-PARTITIONING-GUIDE.md
Section: "Scenario 1: Multi-Tenant Environment"
```

### Key Manifest Features

**1. Small Model Deployment** (`01-ollama-small-deployment.yaml`)
```yaml
resources:
  requests:
    nvidia.com/mig-1g.6gb: 1  # ← Request specific MIG profile
```

**2. Medium Model Deployment** (`02-ollama-medium-deployment.yaml`)
```yaml
replicas: 2                    # ← HA across both GPUs
affinity:
  podAntiAffinity: ...         # ← Spread across nodes
```

**3. Large Model Deployment** (`03-ollama-large-deployment.yaml`)
```yaml
resources:
  requests:
    nvidia.com/gpu: 1          # ← Full GPU for production
```

### Demo Walkthrough
```bash
# Show the manifests
cat k8s-manifests/01-ollama-small-deployment.yaml

# Explain namespace isolation
kubectl get namespaces | grep ai-

# If connected to cluster, deploy:
kubectl apply -f k8s-manifests/00-namespace.yaml
kubectl apply -f k8s-manifests/01-ollama-small-deployment.yaml

# Watch pods schedule
kubectl get pods -n ai-dev -w
```

---

## Part 5: Resource Allocation Scenarios (5 minutes)

### Scenario A: "We need dev + staging + prod"
```
GPU 1: 2x dev (1g.6gb) + 1x staging (2g.12gb)
GPU 2: 2x dev (1g.6gb) + 1x staging (2g.12gb)

Result: 4 dev pods + 2 staging pods + spare capacity
```

### Scenario B: "Production is critical, but we also need dev"
```
GPU 1: 1x production (full 24GB)
GPU 2: 1x production replica (full 24GB)

Result: HA production with load balancing
```

### Scenario C: "Mix everything"
```
GPU 1: 1x prod (24GB)
GPU 2: 2x staging (12GB each) or 4x dev (6GB each)

Result: Production + lower environments
```

**Ask Customer**: "Which scenario fits your needs?"

---

## Part 6: Monitoring & Operations (5 minutes)

### GPU Utilization Monitoring
```bash
# Show live GPU stats
kubectl exec -n ai-workloads <pod> -- nvidia-smi

# Expected output:
# - GPU 0: 85% util, 20GB/24GB memory
# - MIG instances listed separately
```

### Prometheus Metrics
```bash
# Deploy monitoring
cd k8s-manifests
./deploy-monitoring.sh

# Port forward to see metrics
kubectl port-forward -n gpu-monitoring svc/dcgm-exporter 9400:9400
curl localhost:9400/metrics | grep DCGM_FI_DEV_GPU_UTIL
```

### Key Metrics to Track
- `DCGM_FI_DEV_GPU_UTIL` - GPU utilization %
- `DCGM_FI_DEV_FB_USED` - Memory usage
- `DCGM_FI_DEV_GPU_TEMP` - Temperature
- `DCGM_FI_DEV_POWER_USAGE` - Power consumption

---

## Part 7: Business Value (3 minutes)

### Cost Savings
```
Without MIG:
  2 GPUs × $10,000 = $20,000
  Running 2 workloads = $10,000 per workload

With MIG:
  2 GPUs × $10,000 = $20,000
  Running 6-8 workloads = $2,500-$3,300 per workload

Savings: 60-70% better ROI
```

### Utilization Improvement
```
Before: 30-40% avg utilization
After:  80-90% avg utilization

Result: 2-3x more workloads, no new hardware
```

### Other Benefits
- ✅ Faster dev cycles (no waiting for GPU access)
- ✅ Better isolation (dev can't crash prod)
- ✅ Simplified management (one cluster, not three)
- ✅ Nutanix integration (Volumes, Files, networking)

---

## Part 8: Next Steps (2 minutes)

### Immediate Actions
1. **Proof of Concept**
   - Enable MIG on one node
   - Deploy small + medium workloads
   - Measure utilization improvement

2. **Production Planning**
   - Identify workload types (dev/stage/prod)
   - Map to MIG profiles
   - Plan namespace strategy

3. **Monitoring Setup**
   - Deploy DCGM exporter
   - Configure Prometheus/Grafana
   - Set up alerts

### Nutanix Integration
- Use **Nutanix Files** for model storage (RWX PVCs)
- Use **Nutanix Volumes** for high-IOPS workloads
- Integrate with **Prism** for GPU node monitoring
- Use **Flow** for micro-segmentation

---

## Q&A Preparation

### "What if we don't need dev/staging, just prod?"
→ Run 2 production replicas for HA, or use both GPUs in tensor parallelism for larger models (70B+)

### "Is MIG as fast as full GPU?"
→ Yes, within partition - you get dedicated compute/memory. No performance penalty.

### "Can we change MIG profiles dynamically?"
→ Requires GPU drain + reconfiguration. Plan profiles based on workload patterns.

### "What about security between partitions?"
→ Hardware-level isolation. More secure than containerization alone.

### "Does this work with vGPU?"
→ MIG and vGPU are different. MIG is better for containerized workloads on bare metal K8s.

### "What models are too big for A30?"
→ 70B+ models need 40GB+. Use multi-GPU (tensor parallelism) or switch to A100/H100.

---

## Demo Commands Quick Reference

```bash
# Start demo
./start-gpu-demo.sh

# Interactive menu
./gpu-partitioning-demo.py

# Deploy to K8s
kubectl apply -f k8s-manifests/

# Check GPU allocation
kubectl describe node <node> | grep nvidia.com

# View GPU utilization
kubectl exec -n ai-workloads <pod> -- nvidia-smi

# Port forward for testing
kubectl port-forward -n ai-workloads svc/ollama-large 11434:11434

# Test inference
curl http://localhost:11434/api/generate -d '{"model":"llama3.1:8b","prompt":"test"}'

# Monitor pods
kubectl get pods -A -l app=ollama -w
kubectl top pods -n ai-workloads
```

---

## Closing

**Summary**: 
"With MIG partitioning on your 2x A30 GPUs, you can run 6-8 isolated AI workloads, improve utilization from 30% to 80%+, and reduce per-workload costs by 60-70%."

**Call to Action**: 
"Schedule a POC to enable MIG on one of your nodes and measure the utilization improvement."

**Leave Behind**: 
"Full deployment manifests, monitoring setup, and this guide are available in the repo. Everything is production-ready."

---

## Files Reference
- `GPU-PARTITIONING-GUIDE.md` - Full technical documentation
- `k8s-manifests/` - Production-ready Kubernetes manifests
- `gpu-partitioning-demo.py` - Interactive demo script
- `start-gpu-demo.sh` - Quick launcher
- `enable-mig.sh` - MIG configuration script
- `deploy-monitoring.sh` - Monitoring stack setup

**Good luck with your demo! 🚀**
