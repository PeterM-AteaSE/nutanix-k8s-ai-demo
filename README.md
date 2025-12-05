# Nutanix & Kubernetes AI Assistant Demo

## Overview
Complete demo suite for NVIDIA A30 GPU partitioning and AI workload management on Nutanix Kubernetes. Includes interactive performance analysis, Kubernetes manifests, and presentation materials.

## What It Does
- **GPU Partitioning Demo**: Interactive showcase of NVIDIA MIG technology
- **Performance Benchmarks**: Compare 1B, 3B, and 8B parameter models
- **Interactive Graphs**: Beautiful HTML charts with performance metrics
- **Kubernetes Manifests**: Production-ready deployments with MIG profiles
- **AI Assistant**: Nutanix infrastructure and Kubernetes troubleshooting
- **Complete Documentation**: Deployment guides and presentation materials

## Features
✅ **GPU Partitioning Demo**: NVIDIA A30 MIG visualization and benchmarks
✅ **Interactive Performance Graphs**: Auto-generated HTML charts
✅ **Production K8s Manifests**: Multi-tenant GPU deployments
✅ **Runs 100% locally**: No internet needed for LLM inference
✅ **Multiple Models**: 1B, 3B models included (8B ready)
✅ **ROCm GPU Acceleration**: AMD Radeon 890M support
✅ **Complete Documentation**: Guides, cheat sheets, and walkthroughs

## Quick Start

### GPU Partitioning Demo (Recommended)
```bash
cd ~/projects/nutanix-k8s-ai-demo
./start-gpu-demo.sh
```

**Demo Options:**
1. 🎯 Interactive Demo - Full walkthrough with explanations
2. 📊 Quick Benchmark with Graphs - Generate performance charts
3. 📚 View Documentation - Browse guides in terminal
4. 🔧 Deploy to Kubernetes - Apply manifests to cluster

### AI Assistant (Legacy)
```bash
cd ~/projects/nutanix-k8s-ai-demo
./nutanix-ai-assistant.py
```

### 2. Choose a Scenario
Pick from pre-built scenarios:
- Kubernetes troubleshooting
- Nutanix storage best practices
- Scaling strategies
- Cluster optimization
- Disaster recovery
- Network policies
- Or ask your own questions

## Demo Scenarios

### 1. Kubernetes Troubleshooting
Shows how to diagnose CrashLoopBackOff and common pod issues

### 2. Nutanix Storage Best Practices
Storage class configuration for Kubernetes on Nutanix

### 3. Scaling Strategy
HPA vs VPA - when to use each autoscaling method

### 4. Nutanix Cluster Optimization
Key metrics for Kubernetes workloads on Nutanix

### 5. Disaster Recovery
Backup and restore strategies for K8s on Nutanix

### 6. Network Policies
Creating secure network policies for pods

## System Requirements
- AMD/Intel CPU
- 8GB+ RAM
- Ollama installed ✓
- Python 3 ✓
- kubectl configured (optional, enhances demo)

## Technical Details

### Model
- **Engine**: Ollama
- **Model**: llama3.2:3b (2GB, fast responses)
- **Deployment**: Local, no external API calls
- **Context**: Maintains conversation history

### Architecture
```
┌─────────────────┐
│  Demo Script    │ ← Python interactive UI
└────────┬────────┘
         │
┌────────▼────────┐
│  Ollama API     │ ← Local inference
└────────┬────────┘
         │
┌────────▼────────┐
│  llama3.2 Model │ ← 3B parameters
└─────────────────┘
```

## Tips for Great Demos

### 1. Start with Context
Show your current K8s cluster when demo starts

### 2. Use Scenarios
Walk through pre-built scenarios first to show capabilities

### 3. Custom Questions
Then demonstrate custom question mode for real problems

### 4. Show the Model
```bash
ollama list
```
Proves it's running locally!

### 5. Compare Responses
Ask same question twice to show consistency

## Advanced Usage

### Query from Command Line
```bash
ollama run llama3.2:3b "How do I troubleshoot a pending pod in Kubernetes?"
```

### List Available Models
```bash
ollama list
```

### Pull Additional Models
```bash
# Larger, more capable model (7GB)
ollama pull llama3.2

# Code-focused model
ollama pull codellama

# Specialized for specific tasks
ollama pull mistral
```

## Customization

### Add Your Own Scenarios
Edit `nutanix-ai-assistant.py` and add to the `demo_scenarios()` function:

```python
"8": {
    "title": "Your Custom Scenario",
    "prompt": "Your question here..."
}
```

### Change the Model
Edit the `__init__` method:
```python
self.model = "llama3.2"  # or any other model
```

### Adjust Context History
Edit the `query_ollama` method:
```python
for msg in self.context_history[-6:]:  # Change 6 to keep more/less context
```

## Presentation Tips

### Opening
"Let me show you how AI can help us with our Nutanix and Kubernetes infrastructure..."

### Demo Flow
1. Show it knows your cluster (displays current context)
2. Pick a troubleshooting scenario
3. Show how it provides step-by-step guidance
4. Let colleagues ask their own questions
5. Emphasize: "This runs locally, no data leaves the building"

### Key Points
- ✅ Private - runs on your laptop
- ✅ Fast - responses in seconds
- ✅ Smart - understands Nutanix + K8s context
- ✅ Practical - gives actionable advice
- ✅ Free - no API costs

## Troubleshooting

### Model not found?
```bash
ollama pull llama3.2:3b
```

### Ollama not running?
```bash
sudo systemctl status ollama
sudo systemctl start ollama
```

### Slow responses?
Try a smaller model:
```bash
ollama pull llama3.2:1b
```

### Want better quality?
Try a larger model (needs more RAM):
```bash
ollama pull llama3.2  # 7B version
```

## What Your Colleagues Will Say

> "Wait, this runs locally? No cloud?"

> "Can it actually help with our cluster issues?"

> "How do I get this on my laptop?"

## Next Steps After Demo

### 1. Install on More Machines
Share the install commands with team members

### 2. Create Team Models
Fine-tune models with your specific infrastructure docs

### 3. Integrate with Tools
Connect to your monitoring/alerting systems

### 4. Build Custom Assistants
Create specialized bots for different teams

## Resources
- Ollama: https://ollama.com
- Model Library: https://ollama.com/library
- Nutanix Docs: https://portal.nutanix.com/
- Kubernetes Docs: https://kubernetes.io/docs/

---

Built for infrastructure teams who love Nutanix and Kubernetes! 🚀
