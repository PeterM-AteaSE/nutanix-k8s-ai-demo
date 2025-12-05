#!/usr/bin/env python3
"""
Nutanix & Kubernetes AI Assistant Demo
Interactive demo for colleagues showcasing AI-powered infrastructure assistance
"""

import subprocess
import json
import sys
import os
from datetime import datetime

class NutanixK8sAssistant:
    def __init__(self):
        self.model = "llama3.2:3b"
        self.context_history = []
        
    def query_ollama(self, prompt, system_prompt=None):
        """Query Ollama with a prompt"""
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add context history
        for msg in self.context_history[-6:]:  # Keep last 3 exchanges
            messages.append(msg)
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            # Call ollama API
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=json.dumps({"messages": messages}),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Simple prompt for interactive mode
                result = subprocess.run(
                    ["ollama", "run", self.model, prompt],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                response = result.stdout.strip()
                
                # Update context
                self.context_history.append({"role": "user", "content": prompt})
                self.context_history.append({"role": "assistant", "content": response})
                
                return response
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Error querying model: {e}"
    
    def get_k8s_info(self):
        """Get current Kubernetes cluster info"""
        try:
            # Get current context
            ctx_result = subprocess.run(
                ["kubectl", "config", "current-context"],
                capture_output=True,
                text=True,
                timeout=5
            )
            current_context = ctx_result.stdout.strip() if ctx_result.returncode == 0 else "Unknown"
            
            # Get cluster info
            cluster_result = subprocess.run(
                ["kubectl", "cluster-info"],
                capture_output=True,
                text=True,
                timeout=5
            )
            cluster_info = cluster_result.stdout if cluster_result.returncode == 0 else "Not available"
            
            # Get node count
            nodes_result = subprocess.run(
                ["kubectl", "get", "nodes", "--no-headers"],
                capture_output=True,
                text=True,
                timeout=5
            )
            node_count = len(nodes_result.stdout.strip().split('\n')) if nodes_result.returncode == 0 else 0
            
            return {
                "context": current_context,
                "cluster_info": cluster_info,
                "node_count": node_count
            }
        except Exception as e:
            return {"error": str(e)}
    
    def demo_scenarios(self):
        """Show demo scenarios"""
        scenarios = {
            "1": {
                "title": "Kubernetes Troubleshooting",
                "prompt": "I have a pod that's in CrashLoopBackOff state. What are the most common causes and how do I troubleshoot it step by step?"
            },
            "2": {
                "title": "Nutanix Storage Best Practices",
                "prompt": "What are the best practices for configuring storage classes in Kubernetes on Nutanix infrastructure?"
            },
            "3": {
                "title": "Scaling Strategy",
                "prompt": "Explain the difference between horizontal pod autoscaling and vertical pod autoscaling in Kubernetes. When should I use each?"
            },
            "4": {
                "title": "Nutanix Cluster Optimization",
                "prompt": "What are the key metrics I should monitor in a Nutanix cluster running Kubernetes workloads?"
            },
            "5": {
                "title": "Disaster Recovery",
                "prompt": "How do I implement a disaster recovery strategy for Kubernetes workloads on Nutanix? Include backup and restore procedures."
            },
            "6": {
                "title": "Network Policies",
                "prompt": "Create a Kubernetes network policy that allows traffic only from specific namespaces to my database pods."
            },
            "7": {
                "title": "Custom Query",
                "prompt": None
            }
        }
        
        return scenarios
    
    def print_header(self):
        """Print demo header"""
        print("\n" + "="*70)
        print("  🤖 NUTANIX & KUBERNETES AI ASSISTANT")
        print("  Interactive Demo for Infrastructure Teams")
        print("="*70)
        
        # Show current K8s context
        k8s_info = self.get_k8s_info()
        if "context" in k8s_info:
            print(f"\n📊 Current Kubernetes Context: {k8s_info['context']}")
            if k8s_info.get('node_count', 0) > 0:
                print(f"📦 Cluster Nodes: {k8s_info['node_count']}")
        print()
    
    def interactive_mode(self):
        """Run interactive demo mode"""
        self.print_header()
        
        print("Choose a demo scenario or ask your own question:\n")
        scenarios = self.demo_scenarios()
        
        for key, scenario in scenarios.items():
            print(f"  [{key}] {scenario['title']}")
        
        print("\n  [q] Quit\n")
        
        while True:
            try:
                choice = input("Your choice: ").strip()
                
                if choice.lower() == 'q':
                    print("\n👋 Thanks for trying the demo!\n")
                    break
                
                if choice in scenarios:
                    scenario = scenarios[choice]
                    
                    if scenario['prompt']:
                        prompt = scenario['prompt']
                        print(f"\n🔍 Scenario: {scenario['title']}")
                    else:
                        prompt = input("\n💬 Your question: ").strip()
                        if not prompt:
                            continue
                    
                    print(f"\n❓ Question:\n{prompt}\n")
                    print("🤖 AI Response:")
                    print("-" * 70)
                    
                    # Add Nutanix/K8s context to the query
                    enhanced_prompt = f"""As an expert in Nutanix infrastructure and Kubernetes, answer this question:

{prompt}

Provide practical, actionable advice suitable for enterprise infrastructure teams."""
                    
                    response = self.query_ollama(enhanced_prompt)
                    print(response)
                    print("-" * 70)
                    
                    # Ask if they want to continue
                    print("\n[Enter] Continue | [q] Quit")
                    cont = input().strip()
                    if cont.lower() == 'q':
                        print("\n👋 Thanks for trying the demo!\n")
                        break
                    
                    # Show menu again
                    print("\n" + "="*70)
                    print("Choose another scenario or ask your own question:\n")
                    for key, scenario in scenarios.items():
                        print(f"  [{key}] {scenario['title']}")
                    print("\n  [q] Quit\n")
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for trying the demo!\n")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}\n")
                continue

def main():
    assistant = NutanixK8sAssistant()
    
    # Check if ollama is available
    try:
        subprocess.run(["ollama", "list"], capture_output=True, timeout=5)
    except:
        print("❌ Error: Ollama is not installed or not running.")
        print("Please install Ollama first: curl -fsSL https://ollama.com/install.sh | sh")
        sys.exit(1)
    
    assistant.interactive_mode()

if __name__ == "__main__":
    main()
