#!/usr/bin/env python3
"""
NVIDIA A30 GPU Partitioning Demo
Demonstrates model performance across different GPU partition sizes
Simulates: 2x NVIDIA A30 GPUs with MIG partitioning on Nutanix K8s
"""

import subprocess
import json
import time
import sys
from datetime import datetime

class GPUPartitioningDemo:
    def __init__(self):
        self.models = {
            'small': {
                'name': 'llama3.2:1b',
                'size': '1B parameters',
                'mig_profile': '1g.6gb',
                'gpu_memory': '6GB',
                'use_case': 'Development, CI/CD, Edge Devices',
                'pods_per_gpu': 4,
                'namespace': 'ai-dev'
            },
            'medium': {
                'name': 'llama3.2:3b',
                'size': '3B parameters',
                'mig_profile': '2g.12gb',
                'gpu_memory': '12GB',
                'use_case': 'Staging, QA, Medium Workloads',
                'pods_per_gpu': 2,
                'namespace': 'ai-staging'
            },
            'large': {
                'name': 'llama3.1:8b',
                'size': '8B parameters',
                'mig_profile': 'Full A30 (24GB)',
                'gpu_memory': '24GB',
                'use_case': 'Production, Customer APIs',
                'pods_per_gpu': 1,
                'namespace': 'ai-workloads'
            }
        }
        
        self.test_prompt = """Explain how to troubleshoot a Kubernetes pod that is stuck in CrashLoopBackOff state. 
Be specific and provide kubectl commands."""

    def print_header(self, text):
        """Print formatted section header"""
        print(f"\n{'='*80}")
        print(f"  {text}")
        print(f"{'='*80}\n")

    def print_gpu_topology(self):
        """Display A30 MIG topology explanation"""
        self.print_header("NVIDIA A30 GPU Partitioning Topology")
        
        print("📊 Customer Hardware: 2x NVIDIA A30 GPUs (24GB each)")
        print("\n🔧 MIG Partition Options per A30:")
        print("   ┌─────────────────────────────────────────────┐")
        print("   │  Profile      │  Memory  │  Pods  │  Use    │")
        print("   ├─────────────────────────────────────────────┤")
        print("   │  1g.6gb       │   6GB    │   4    │  Dev    │")
        print("   │  2g.12gb      │  12GB    │   2    │  Stage  │")
        print("   │  Full GPU     │  24GB    │   1    │  Prod   │")
        print("   └─────────────────────────────────────────────┘")
        
        print("\n💡 Total Capacity with 2x A30:")
        print("   • Option 1: 8x development pods (1g.6gb each)")
        print("   • Option 2: 4x staging pods (2g.12gb each)")
        print("   • Option 3: 2x production pods (full GPU)")
        print("   • Option 4: Mix profiles for multi-tenancy")
        
        print("\n✅ Benefits:")
        print("   ✓ GPU isolation between workloads")
        print("   ✓ Predictable performance per partition")
        print("   ✓ Higher utilization (80-90% vs 30-40%)")
        print("   ✓ Cost optimization (more workloads per GPU)")
        print("   ✓ Fault isolation (one partition failure doesn't affect others)")

    def check_model_available(self, model_name):
        """Check if model is downloaded"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return model_name in result.stdout
        except:
            return False

    def query_model(self, model_name, prompt):
        """Query a model and measure performance"""
        print(f"🔄 Loading {model_name}...")
        start_time = time.time()
        
        try:
            result = subprocess.run(
                ['ollama', 'run', model_name, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if result.returncode == 0:
                response = result.stdout.strip()
                tokens = len(response.split())
                tokens_per_second = tokens / duration if duration > 0 else 0
                
                return {
                    'success': True,
                    'response': response,
                    'duration': duration,
                    'tokens': tokens,
                    'tokens_per_second': tokens_per_second
                }
            else:
                return {'success': False, 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Query timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def run_model_comparison(self):
        """Compare performance across all model sizes"""
        self.print_header("Model Performance Comparison")
        
        results = {}
        
        for size, config in self.models.items():
            model_name = config['name']
            
            print(f"\n📦 Testing {size.upper()} model: {model_name}")
            print(f"   MIG Profile: {config['mig_profile']}")
            print(f"   GPU Memory: {config['gpu_memory']}")
            print(f"   Namespace: {config['namespace']}")
            print(f"   Pods per GPU: {config['pods_per_gpu']}")
            
            if not self.check_model_available(model_name):
                print(f"   ⚠️  Model not downloaded. Run: ollama pull {model_name}")
                continue
            
            result = self.query_model(model_name, self.test_prompt)
            
            if result['success']:
                print(f"\n   ✅ Response generated in {result['duration']:.2f}s")
                print(f"   📊 Tokens: {result['tokens']}")
                print(f"   ⚡ Speed: {result['tokens_per_second']:.1f} tokens/sec")
                print(f"\n   Response preview:")
                preview = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
                print(f"   {preview}\n")
                
                results[size] = result
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown error')}")

        return results

    def show_resource_allocation(self):
        """Show how resources would be allocated in K8s"""
        self.print_header("Kubernetes Resource Allocation")
        
        print("📋 Deployment Strategy for 2x NVIDIA A30:\n")
        
        total_small_pods = 8
        total_medium_pods = 4
        total_large_pods = 2
        
        print("🎯 Scenario 1: Multi-Tenant Environment")
        print("   GPU 1 (MIG Partitioned):")
        print("      ├─ 2x dev pods      (1g.6gb each)  → ai-dev namespace")
        print("      ├─ 1x staging pod   (2g.12gb)      → ai-staging namespace")
        print("      └─ Remaining: 6GB")
        print("\n   GPU 2 (MIG Partitioned):")
        print("      ├─ 2x dev pods      (1g.6gb each)  → ai-dev namespace")
        print("      ├─ 1x staging pod   (2g.12gb)      → ai-staging namespace")
        print("      └─ Remaining: 6GB")
        
        print("\n🎯 Scenario 2: Production + Development")
        print("   GPU 1 (Full):")
        print("      └─ 1x prod pod      (24GB)         → ai-workloads namespace")
        print("\n   GPU 2 (MIG Partitioned):")
        print("      ├─ 4x dev pods      (1g.6gb each)  → ai-dev namespace")
        print("      └─ Fully utilized")
        
        print("\n🎯 Scenario 3: High-Availability Production")
        print("   GPU 1 (Full):")
        print("      └─ 1x prod pod      (24GB)         → ai-workloads (primary)")
        print("\n   GPU 2 (Full):")
        print("      └─ 1x prod pod      (24GB)         → ai-workloads (replica)")
        print("      └─ Load balanced via K8s Service")

    def show_monitoring_commands(self):
        """Display monitoring commands for GPU utilization"""
        self.print_header("Monitoring & Troubleshooting Commands")
        
        print("🔍 Check GPU utilization:")
        print("   kubectl exec -it <pod-name> -n ai-workloads -- nvidia-smi")
        print("   kubectl exec -it <pod-name> -n ai-workloads -- nvidia-smi -L")
        
        print("\n📊 View MIG configuration:")
        print("   kubectl exec -it <pod-name> -n ai-workloads -- nvidia-smi mig -lgi")
        
        print("\n📈 Monitor pod resources:")
        print("   kubectl top pods -n ai-workloads")
        print("   kubectl top pods -n ai-staging")
        print("   kubectl top pods -n ai-dev")
        
        print("\n🔧 Check GPU allocation:")
        print("   kubectl describe node <node-name> | grep -A 10 'Allocated resources'")
        
        print("\n📋 View events:")
        print("   kubectl get events -n ai-workloads --sort-by='.lastTimestamp'")
        
        print("\n🎯 Port forward for testing:")
        print("   kubectl port-forward -n ai-workloads svc/ollama-large 11434:11434")
        print("   curl http://localhost:11434/api/generate -d '{\"model\":\"llama3.1:8b\",\"prompt\":\"test\"}'")

    def deployment_walkthrough(self):
        """Interactive deployment demonstration"""
        self.print_header("Deployment Walkthrough")
        
        print("📦 Step 1: Enable MIG mode on A30 GPUs")
        print("   $ sudo nvidia-smi -mig 1")
        print("   $ sudo nvidia-smi mig -cgi 9,14,14,14 -C")
        print("   Creates: 1x 2g.12gb + 3x 1g.6gb per GPU\n")
        
        print("📦 Step 2: Install NVIDIA Device Plugin")
        print("   $ kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/main/deployments/static/nvidia-device-plugin.yml\n")
        
        print("📦 Step 3: Deploy AI workloads")
        print("   $ kubectl apply -f k8s-manifests/00-namespace.yaml")
        print("   $ kubectl apply -f k8s-manifests/01-ollama-small-deployment.yaml")
        print("   $ kubectl apply -f k8s-manifests/02-ollama-medium-deployment.yaml")
        print("   $ kubectl apply -f k8s-manifests/03-ollama-large-deployment.yaml\n")
        
        print("📦 Step 4: Verify deployments")
        print("   $ kubectl get pods -A -l app=ollama")
        print("   $ kubectl get svc -A -l app=ollama\n")
        
        print("📦 Step 5: Load models into pods")
        print("   $ kubectl exec -n ai-dev deploy/ollama-small -- ollama pull llama3.2:1b")
        print("   $ kubectl exec -n ai-staging deploy/ollama-medium -- ollama pull llama3.2:3b")
        print("   $ kubectl exec -n ai-workloads deploy/ollama-large -- ollama pull llama3.1:8b\n")

    def interactive_menu(self):
        """Main interactive menu"""
        while True:
            self.print_header("NVIDIA A30 GPU Partitioning Demo - Main Menu")
            
            print("Select a demo option:\n")
            print("  1. Show A30 MIG topology and partitioning strategy")
            print("  2. Run model performance comparison (1B vs 3B vs 8B)")
            print("  3. Show Kubernetes resource allocation scenarios")
            print("  4. Display deployment walkthrough")
            print("  5. Show monitoring commands")
            print("  6. Run all demos")
            print("  7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.print_gpu_topology()
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.run_model_comparison()
                input("\nPress Enter to continue...")
            elif choice == '3':
                self.show_resource_allocation()
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.deployment_walkthrough()
                input("\nPress Enter to continue...")
            elif choice == '5':
                self.show_monitoring_commands()
                input("\nPress Enter to continue...")
            elif choice == '6':
                self.print_gpu_topology()
                time.sleep(2)
                self.run_model_comparison()
                time.sleep(2)
                self.show_resource_allocation()
                time.sleep(2)
                self.deployment_walkthrough()
                time.sleep(2)
                self.show_monitoring_commands()
                input("\nPress Enter to continue...")
            elif choice == '7':
                print("\n👋 Thank you for exploring GPU partitioning!")
                print("💡 Remember: MIG enables efficient multi-tenancy on A30 GPUs")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice. Please select 1-7.")
                time.sleep(1)

def main():
    print("\n" + "="*80)
    print("  🚀 NVIDIA A30 GPU Partitioning & Multi-Tenancy Demo")
    print("  📦 Nutanix Kubernetes Platform")
    print("="*80)
    
    demo = GPUPartitioningDemo()
    demo.interactive_menu()

if __name__ == "__main__":
    main()
