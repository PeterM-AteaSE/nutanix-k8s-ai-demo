# System Requirements

## Overview
This demo runs 100% locally on your laptop. No cloud services or internet connectivity required (except for initial downloads).

---

## Hardware Requirements

### Minimum Specifications
- **CPU**: 4 cores (8+ recommended)
- **RAM**: 16GB (32GB+ recommended for 8B models)
- **Storage**: 20GB free space
  - Ollama: ~500MB
  - Models: 8.2GB (1B: 1.3GB, 3B: 2.0GB, 8B: 4.9GB)
  - Demo files: ~100MB
  - Working space: ~10GB

### Recommended Specifications
- **CPU**: 8+ cores (AMD Ryzen or Intel i7/i9)
- **RAM**: 32GB+ (allows smooth 8B model inference)
- **Storage**: 50GB+ SSD
- **GPU**: Optional but highly recommended
  - NVIDIA GPU: GTX 1660+, RTX 3060+, or datacenter (A30, A100)
  - AMD GPU: RX 6000/7000 series, Radeon 780M/880M/890M integrated
  - Apple Silicon: M1/M2/M3 (native support)

### Tested Configurations

#### Configuration 1 (Demo Author)
- **CPU**: AMD Ryzen AI 9 HX PRO 375 (24 cores)
- **RAM**: 64GB DDR5
- **GPU**: AMD Radeon 890M (integrated)
- **OS**: Fedora 43
- **Performance**: 
  - 1B model: ~150 tokens/sec (GPU)
  - 3B model: ~100 tokens/sec (GPU)
  - 8B model: ~50 tokens/sec (GPU)

#### Configuration 2 (Cloud/Server)
- **CPU**: 8-16 vCPUs
- **RAM**: 32-64GB
- **GPU**: NVIDIA A30 (MIG enabled)
- **OS**: Ubuntu 22.04 LTS
- **Performance**:
  - 1B model: 200+ tokens/sec
  - 3B model: 150+ tokens/sec
  - 8B model: 80+ tokens/sec

---

## Software Requirements

### Operating System
**Supported:**
- Linux: Fedora 38+, Ubuntu 20.04+, Debian 11+, RHEL 8+
- macOS: 12+ (Monterey or newer)
- Windows: 10/11 with WSL2

**Recommended:**
- Fedora 43 or Ubuntu 22.04 LTS

### Required Software

#### 1. Python 3
```bash
# Check version (3.8+ required)
python3 --version

# Fedora/RHEL
sudo dnf install python3

# Ubuntu/Debian
sudo apt install python3

# macOS (via Homebrew)
brew install python3
```

#### 2. Ollama
**Purpose**: Local LLM inference engine

**Installation:**
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Verify installation
ollama --version
```

**Start Service:**
```bash
# Linux (systemd)
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama

# macOS
ollama serve &
```

#### 3. Git
```bash
# Check if installed
git --version

# Fedora/RHEL
sudo dnf install git

# Ubuntu/Debian
sudo apt install git

# macOS
brew install git
```

#### 4. kubectl (Optional - for K8s deployment)
**Required only if deploying to Kubernetes cluster**

```bash
# Download latest version
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify
kubectl version --client
```

---

## GPU Acceleration Setup

### NVIDIA GPU (CUDA)

#### Check GPU Compatibility
```bash
# List NVIDIA GPUs
lspci | grep -i nvidia

# Check NVIDIA driver
nvidia-smi
```

#### Install NVIDIA Drivers & CUDA
```bash
# Fedora
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda

# Ubuntu
sudo apt install nvidia-driver-535 nvidia-cuda-toolkit

# Verify
nvidia-smi
```

#### Configure Ollama for NVIDIA
```bash
# Create systemd override
sudo mkdir -p /etc/systemd/system/ollama.service.d

# No additional config needed - Ollama auto-detects NVIDIA GPUs
sudo systemctl restart ollama

# Verify GPU is detected
journalctl -u ollama -n 50 | grep -i gpu
```

**Expected Output:**
```
level=INFO msg="discovering available GPUs..."
level=INFO msg="discovered GPU" gpu="NVIDIA GeForce RTX 3060" compute="8.6" vram="12GB"
```

---

### AMD GPU (ROCm)

#### Check GPU Compatibility
```bash
# List AMD GPUs
lspci | grep -i amd | grep -i vga

# Check GPU model
rocm-smi --showproductname
```

#### Supported AMD GPUs
- **Desktop**: RX 6000/7000 series (RDNA2/RDNA3)
- **Integrated**: Radeon 780M, 880M, 890M (Ryzen AI)
- **Datacenter**: MI100, MI200, MI300

#### Install ROCm Drivers
```bash
# Fedora 39+
sudo dnf install rocm-hip rocm-opencl rocm-smi

# Ubuntu 22.04
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/amdgpu-install_*_all.deb
sudo apt install ./amdgpu-install_*_all.deb
sudo amdgpu-install --usecase=rocm

# Verify installation
rocm-smi
rocminfo | grep "Name:"
```

#### Configure Ollama for AMD GPU
```bash
# Create systemd override for AMD GPU
sudo mkdir -p /etc/systemd/system/ollama.service.d

sudo tee /etc/systemd/system/ollama.service.d/gpu.conf << 'EOF'
[Service]
Environment="HSA_OVERRIDE_GFX_VERSION=11.0.0"
Environment="OLLAMA_NUM_GPU=1"
Environment="OLLAMA_GPU_OVERHEAD=0"
EOF

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart ollama

# Verify GPU detection
journalctl -u ollama -n 100 | grep -E "ROCm|GPU|compute"
```

**Expected Output:**
```
level=INFO msg="discovering available GPUs..."
level=WARN msg="user overrode visible devices" HSA_OVERRIDE_GFX_VERSION=11.0.0
level=INFO msg="ROCm GPU detected" device="Radeon 890M"
llama_context: ROCm0 compute buffer size = 256.50 MiB
```

#### Troubleshooting AMD GPU
If GPU not detected:
```bash
# Check ROCm installation
rocminfo | grep "Agent"

# Check available devices
ls -la /dev/kfd /dev/dri/render*

# Add user to render group
sudo usermod -a -G render $USER
sudo usermod -a -G video $USER

# Reboot required for group changes
sudo reboot
```

---

### Apple Silicon (M1/M2/M3)

**Good News**: Ollama has native Metal acceleration - no additional setup needed!

```bash
# Install Ollama
brew install ollama

# Start service
ollama serve &

# Verify Metal acceleration
# Check Activity Monitor → GPU tab while running inference
```

---

## Demo Installation

### 1. Clone Repository
```bash
# Create projects directory
mkdir -p ~/projects
cd ~/projects

# Clone demo
git clone https://github.com/PeterM-AteaSE/nutanix-k8s-ai-demo.git
cd nutanix-k8s-ai-demo
```

### 2. Download Models
```bash
# Small model (1.3GB) - Fast, lightweight
ollama pull llama3.2:1b

# Medium model (2.0GB) - Balanced
ollama pull llama3.2:3b

# Large model (4.9GB) - High quality
ollama pull llama3.1:8b

# Verify models
ollama list
```

**Expected Output:**
```
NAME           ID              SIZE      MODIFIED
llama3.1:8b    46e0c10c039e    4.9 GB    2 minutes ago
llama3.2:3b    a80c4f17acd5    2.0 GB    5 minutes ago
llama3.2:1b    baf6a787fdff    1.3 GB    8 minutes ago
```

### 3. Make Scripts Executable
```bash
chmod +x *.py *.sh k8s-manifests/*.sh
```

### 4. Test Installation
```bash
# Quick test
./start-gpu-demo.sh

# Select option 2 for benchmark with graphs
```

---

## Performance Tuning

### CPU-Only Optimization
If running without GPU:
```bash
# Set CPU threads (adjust based on your CPU cores)
export OLLAMA_NUM_THREAD=8

# Restart Ollama
sudo systemctl restart ollama
```

### GPU Memory Management
```bash
# Limit GPU memory usage (if running multiple workloads)
export OLLAMA_MAX_LOADED_MODELS=1

# For multiple GPUs
export CUDA_VISIBLE_DEVICES=0  # Use first GPU only

# Restart Ollama
sudo systemctl restart ollama
```

### Model Loading Speed
```bash
# Use faster storage for models (SSD recommended)
sudo mkdir -p /mnt/fast-storage/ollama
sudo chown ollama:ollama /mnt/fast-storage/ollama

# Configure Ollama model path
sudo systemctl edit ollama

# Add:
[Service]
Environment="OLLAMA_MODELS=/mnt/fast-storage/ollama"
```

---

## Verification Checklist

Run these commands to verify your setup:

```bash
echo "=== System Check ==="

# 1. Python
python3 --version

# 2. Ollama
ollama --version
systemctl is-active ollama

# 3. Models
ollama list | grep llama

# 4. GPU (if applicable)
nvidia-smi 2>/dev/null || rocm-smi 2>/dev/null || echo "Running in CPU mode"

# 5. Demo files
ls -lh ~/projects/nutanix-k8s-ai-demo/*.py

# 6. Test inference
ollama run llama3.2:1b "Say hello in one sentence"

echo "=== All checks complete ==="
```

**Expected Result:** All commands should succeed without errors.

---

## Common Issues

### Issue: "Ollama service not running"
```bash
# Check status
sudo systemctl status ollama

# View logs
journalctl -u ollama -f

# Restart service
sudo systemctl restart ollama
```

### Issue: "Model download fails"
```bash
# Check disk space
df -h

# Clear Ollama cache
rm -rf ~/.ollama/models
ollama pull llama3.2:1b
```

### Issue: "GPU not detected"
```bash
# NVIDIA
nvidia-smi

# AMD
rocm-smi

# Check Ollama logs
journalctl -u ollama -n 100 | grep -i gpu
```

### Issue: "Out of memory"
```bash
# Check available RAM
free -h

# Try smaller model
ollama pull llama3.2:1b

# Or reduce concurrent requests
export OLLAMA_NUM_PARALLEL=1
sudo systemctl restart ollama
```

### Issue: "Slow inference speed"
**CPU-only**: 10-30 tokens/sec is normal
**GPU**: Should be 50-200+ tokens/sec

```bash
# Test model speed
time ollama run llama3.2:1b "Count from 1 to 10"

# If slow on GPU, check GPU utilization
nvidia-smi dmon -s u -c 10
# or
rocm-smi --showuse
```

---

## Kubernetes Deployment (Optional)

### Additional Requirements
- Access to Kubernetes cluster
- kubectl configured with cluster context
- Cluster has GPU nodes (for actual GPU partitioning)

### Kubernetes Cluster Requirements
- **Version**: 1.24+
- **Nodes**: 2+ nodes with NVIDIA A30 GPUs
- **Storage**: Nutanix Files or NFS for PVCs
- **Networking**: Ingress controller (NGINX recommended)
- **GPU Support**: NVIDIA Device Plugin installed

### Pre-deployment Checks
```bash
# Verify cluster access
kubectl cluster-info

# Check GPU nodes
kubectl get nodes -l nvidia.com/gpu.product=NVIDIA-A30

# Verify storage classes
kubectl get storageclass

# Check available GPU resources
kubectl describe nodes | grep -A 5 "nvidia.com/gpu"
```

---

## Resource Planning

### Disk Space Breakdown
- **Ollama binary**: ~500MB
- **llama3.2:1b**: 1.3GB
- **llama3.2:3b**: 2.0GB
- **llama3.1:8b**: 4.9GB
- **Demo repository**: ~100MB
- **Generated reports**: ~10MB per benchmark
- **Temp/cache**: ~2GB
- **Total**: ~15-20GB

### Memory Requirements per Model
| Model | Minimum RAM | Recommended RAM | GPU VRAM |
|-------|-------------|-----------------|----------|
| 1B    | 4GB         | 8GB             | 2GB      |
| 3B    | 8GB         | 16GB            | 6GB      |
| 8B    | 16GB        | 32GB            | 12GB     |

### CPU Requirements
- **Minimum**: 4 cores for smooth demo
- **Recommended**: 8+ cores for concurrent models
- **Optimal**: 16+ cores for production workloads

---

## Next Steps

After completing installation:

1. **Test Demo**: Run `./start-gpu-demo.sh` → Option 2
2. **Review Documentation**: Read `GPU-PARTITIONING-GUIDE.md`
3. **Prepare Presentation**: Study `PRESENTATION-CHEAT-SHEET.md`
4. **Practice**: Run through demo scenarios 2-3 times
5. **Customize**: Modify prompts for your specific use case

---

## Support & Resources

- **Demo Repository**: https://github.com/PeterM-AteaSE/nutanix-k8s-ai-demo
- **Ollama Documentation**: https://github.com/ollama/ollama
- **ROCm Compatibility**: https://rocm.docs.amd.com/
- **NVIDIA CUDA**: https://developer.nvidia.com/cuda-downloads
- **Kubernetes GPU Support**: https://kubernetes.io/docs/tasks/manage-gpus/

---

**Installation Time**: 20-30 minutes (including model downloads)
**Demo Ready**: After verification checklist passes ✅
