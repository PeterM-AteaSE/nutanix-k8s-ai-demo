#!/bin/bash
# Quick Demo Launcher for Nutanix & Kubernetes AI Assistant

echo "======================================"
echo "  🚀 Starting Nutanix K8s AI Demo"
echo "======================================"
echo ""

# Check if Ollama is running
if ! systemctl is-active --quiet ollama; then
    echo "⚠️  Ollama service not running, starting it..."
    sudo systemctl start ollama
    sleep 2
fi

# Check if model is available
if ! ollama list | grep -q "llama3.2:3b"; then
    echo "📥 Model not found, downloading llama3.2:3b (this may take a minute)..."
    ollama pull llama3.2:3b
fi

echo "✓ Ollama is ready"
echo "✓ Model loaded: llama3.2:3b"
echo ""

# Show system info
echo "💻 System Resources:"
echo "   - CPU: $(lscpu | grep "Model name" | cut -d: -f2 | xargs)"
echo "   - RAM: $(free -h | awk '/^Mem:/ {print $2}')"
echo ""

# Show K8s context if available
if command -v kubectl &> /dev/null; then
    K8S_CTX=$(kubectl config current-context 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "🔧 Kubernetes Context: $K8S_CTX"
    fi
fi
echo ""

# Run the demo
cd "$(dirname "$0")"
python3 ./nutanix-ai-assistant.py
