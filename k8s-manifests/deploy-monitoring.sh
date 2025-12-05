#!/bin/bash
# Deploy GPU monitoring stack

echo "📊 Deploying GPU Monitoring Stack"
echo "================================="
echo ""

# Create monitoring namespace
echo "📋 Creating gpu-monitoring namespace..."
kubectl create namespace gpu-monitoring 2>/dev/null || echo "Namespace already exists"

# Install DCGM Exporter
echo ""
echo "📋 Installing NVIDIA DCGM Exporter..."
helm repo add gpu-helm-charts https://nvidia.github.io/dcgm-exporter/helm-charts 2>/dev/null
helm repo update

helm install dcgm-exporter gpu-helm-charts/dcgm-exporter \
  --namespace gpu-monitoring \
  --set serviceMonitor.enabled=true \
  --set serviceMonitor.interval=30s

# Wait for DCGM to be ready
echo ""
echo "⏳ Waiting for DCGM Exporter to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=dcgm-exporter \
  -n gpu-monitoring --timeout=120s

# Apply monitoring configs
echo ""
echo "📋 Applying Prometheus rules and Grafana dashboards..."
kubectl apply -f 05-monitoring.yaml

echo ""
echo "✅ Monitoring stack deployed!"
echo ""
echo "Access metrics:"
echo "  1. Port forward DCGM exporter:"
echo "     kubectl port-forward -n gpu-monitoring svc/dcgm-exporter 9400:9400"
echo "  2. View metrics:"
echo "     curl http://localhost:9400/metrics | grep DCGM"
echo ""
echo "Sample queries:"
echo "  - GPU Utilization: DCGM_FI_DEV_GPU_UTIL"
echo "  - GPU Memory: DCGM_FI_DEV_FB_USED"
echo "  - GPU Temperature: DCGM_FI_DEV_GPU_TEMP"
echo "  - Power Usage: DCGM_FI_DEV_POWER_USAGE"
