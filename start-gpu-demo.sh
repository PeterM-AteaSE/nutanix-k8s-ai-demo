#!/bin/bash
# GPU Partitioning Demo Launcher

clear
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🚀 NVIDIA A30 GPU Partitioning Demo                        ║
║   📦 Nutanix Kubernetes Platform                             ║
║                                                               ║
║   Demonstrates: MIG partitioning, multi-tenancy,             ║
║   model performance comparison, and resource optimization    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF

echo ""
echo "🔍 Checking prerequisites..."
echo ""

# Check if Ollama is running
if systemctl is-active --quiet ollama 2>/dev/null || pgrep -x ollama > /dev/null; then
    echo "✅ Ollama service is running"
else
    echo "❌ Ollama service is not running"
    echo "   Start with: sudo systemctl start ollama"
    exit 1
fi

# Check available models
echo ""
echo "📦 Available models:"
ollama list | grep llama

# Check if we have at least 2 models
MODEL_COUNT=$(ollama list | grep -c llama || true)
if [ "$MODEL_COUNT" -lt 2 ]; then
    echo ""
    echo "⚠️  Only $MODEL_COUNT model(s) found. Downloading additional models..."
    echo ""
    
    if ! ollama list | grep -q "llama3.2:1b"; then
        echo "📥 Downloading llama3.2:1b (1.3GB)..."
        ollama pull llama3.2:1b
    fi
    
    if ! ollama list | grep -q "llama3.2:3b"; then
        echo "📥 Model llama3.2:3b already available"
    fi
fi

# Check kubectl
echo ""
if command -v kubectl &> /dev/null; then
    echo "✅ kubectl is installed"
    CURRENT_CONTEXT=$(kubectl config current-context 2>/dev/null || echo "none")
    echo "   Current context: $CURRENT_CONTEXT"
else
    echo "⚠️  kubectl not found (optional for local demo)"
fi

# System resources
echo ""
echo "💻 System Resources:"
FREE_MEM=$(free -h | awk '/^Mem:/ {print $7}')
FREE_DISK=$(df -h ~ | awk 'NR==2 {print $4}')
echo "   RAM available: $FREE_MEM"
echo "   Disk available: $FREE_DISK"

# GPU info
echo ""
if command -v rocm-smi &> /dev/null; then
    echo "🎮 GPU Info:"
    rocm-smi --showproductname 2>/dev/null | grep -v "=" | head -3 || echo "   AMD GPU detected"
elif command -v nvidia-smi &> /dev/null; then
    echo "🎮 GPU Info:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | head -1
else
    echo "ℹ️  No GPU detected (running in CPU mode)"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Select demo mode:"
echo ""
echo "  1. 🎯 Interactive Demo (Recommended)"
echo "     - Model performance comparison"
echo "     - GPU partitioning visualization"
echo "     - Kubernetes deployment guide"
echo ""
echo "  2. 📊 Quick Benchmark with Graphs"
echo "     - Fast performance comparison"
echo "     - Generate interactive HTML charts"
echo ""
echo "  3. 📚 View Documentation"
echo "     - GPU Partitioning Guide"
echo "     - Kubernetes manifests"
echo ""
echo "  4. 🔧 Deploy to Kubernetes"
echo "     - Apply manifests to current cluster"
echo ""
read -p "Enter choice (1-4): " CHOICE

case $CHOICE in
    1)
        echo ""
        echo "🚀 Launching interactive demo..."
        echo ""
        python3 gpu-partitioning-demo.py
        ;;
    2)
        echo ""
        echo "📊 Running benchmark and generating graphs..."
        echo ""
        python3 gpu-partitioning-demo.py << 'EOFPYTHON'
3
8
EOFPYTHON
        ;;
    3)
        echo ""
        echo "📚 Opening documentation..."
        echo ""
        less GPU-PARTITIONING-GUIDE.md
        ;;
    4)
        echo ""
        if ! command -v kubectl &> /dev/null; then
            echo "❌ kubectl is required for deployment"
            exit 1
        fi
        
        echo "🔧 Deploying to Kubernetes cluster: $CURRENT_CONTEXT"
        read -p "Continue? (y/N): " CONFIRM
        
        if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
            echo ""
            echo "📦 Applying manifests..."
            kubectl apply -f k8s-manifests/00-namespace.yaml
            kubectl apply -f k8s-manifests/01-ollama-small-deployment.yaml
            kubectl apply -f k8s-manifests/02-ollama-medium-deployment.yaml
            kubectl apply -f k8s-manifests/03-ollama-large-deployment.yaml
            kubectl apply -f k8s-manifests/04-ingress.yaml
            
            echo ""
            echo "✅ Deployment initiated!"
            echo ""
            echo "Check status with:"
            echo "  kubectl get pods -A -l app=ollama"
        fi
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Demo complete! 🎉"
echo ""
echo "Next steps:"
echo "  • Review GPU-PARTITIONING-GUIDE.md for full documentation"
echo "  • Explore k8s-manifests/ for deployment examples"
echo "  • Check README.md for Nutanix-specific AI scenarios"
