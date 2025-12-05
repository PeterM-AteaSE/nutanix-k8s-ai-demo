#!/bin/bash
# Quick reference for enabling MIG on NVIDIA A30 GPUs

echo "🔧 NVIDIA A30 MIG Configuration Script"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo "❌ Please run as root (sudo)"
   exit 1
fi

echo "📋 Step 1: Disable all compute processes"
nvidia-smi -pm 1

echo ""
echo "📋 Step 2: Enable MIG mode"
nvidia-smi -mig 1

echo ""
echo "📋 Step 3: Reset GPU (requires reboot or GPU reset)"
echo "⚠️  Run: sudo nvidia-smi -r (or reboot system)"
read -p "Press Enter after GPU reset/reboot..."

echo ""
echo "📋 Step 4: Create MIG instances"
echo ""
echo "Choose MIG configuration:"
echo "  1) 4x 1g.6gb (Max development pods)"
echo "  2) 2x 2g.12gb (Staging workloads)"
echo "  3) Mixed: 1x 2g.12gb + 2x 1g.6gb (Multi-tenant)"
echo "  4) Full GPU (No partitioning)"
read -p "Enter choice (1-4): " choice

case $choice in
  1)
    echo "Creating 4x 1g.6gb instances..."
    nvidia-smi mig -cgi 9,9,9,9 -C
    ;;
  2)
    echo "Creating 2x 2g.12gb instances..."
    nvidia-smi mig -cgi 14,14 -C
    ;;
  3)
    echo "Creating 1x 2g.12gb + 2x 1g.6gb instances..."
    nvidia-smi mig -cgi 14,9,9 -C
    ;;
  4)
    echo "Disabling MIG mode..."
    nvidia-smi -mig 0
    nvidia-smi -r
    ;;
  *)
    echo "❌ Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "📋 Step 5: Verify MIG configuration"
nvidia-smi mig -lgi

echo ""
echo "✅ MIG configuration complete!"
echo ""
echo "Next steps:"
echo "  1. Install NVIDIA Device Plugin on Kubernetes"
echo "  2. Deploy GPU workloads with nvidia.com/mig-* resource requests"
echo "  3. Monitor with: kubectl exec <pod> -- nvidia-smi"
