# 🎯 Demo Presentation Cheat Sheet

## Quick Start
```bash
cd ~/nutanix-k8s-ai-demo
./start-demo.sh
```

## Demo Script (5-10 minutes)

### 1. Opening (30 seconds)
**Say**: "Let me show you something cool - an AI assistant that runs locally and knows Nutanix and Kubernetes"

**Show**:
- Open terminal
- Run `./start-demo.sh`
- Point out: "Running on my laptop, not in the cloud"

### 2. Show Current Context (30 seconds)
**Say**: "It's aware of our current Kubernetes cluster"

**Show**:
- Demo displays current K8s context
- Point out your actual cluster name

### 3. First Scenario - Troubleshooting (2 minutes)
**Say**: "Let's try a common problem - CrashLoopBackOff"

**Do**:
- Select option `[1]` Kubernetes Troubleshooting
- Wait for response
- **Highlight**: Step-by-step guidance, practical advice

### 4. Second Scenario - Nutanix Storage (2 minutes)
**Say**: "Now something specific to our infrastructure"

**Do**:
- Press Enter to continue
- Select option `[2]` Nutanix Storage Best Practices
- **Point out**: Understands Nutanix-specific concepts

### 5. Interactive Q&A (3 minutes)
**Say**: "Now let's ask it something from our actual work"

**Do**:
- Select option `[7]` Custom Query
- Ask a real question from your team, like:
  - "How do I check Nutanix storage performance from kubectl?"
  - "What's the best way to handle persistent volumes on Nutanix?"
  - "How do I troubleshoot network connectivity between pods?"

### 6. Show It's Local (1 minute)
**Say**: "And this is all running locally"

**Do**:
```bash
# Open another terminal
ollama list  # Show installed models
systemctl status ollama  # Show it's running locally
```

### 7. Closing (30 seconds)
**Say**: "This is available now. Takes 5 minutes to set up on any laptop."

---

## Key Points to Emphasize

### Privacy ✓
- "All your questions stay on your laptop"
- "No data sent to external APIs"
- "Perfect for sensitive infrastructure discussions"

### Speed ✓
- "Responses in seconds"
- "No internet latency"
- "Works offline"

### Cost ✓
- "Completely free"
- "No API charges"
- "Run it 24/7 if you want"

### Smart ✓
- "Understands Nutanix and Kubernetes"
- "Gives practical advice"
- "Learns from context in conversation"

---

## Common Questions from Colleagues

### "How did you set this up?"
**Answer**: 
```bash
# Install Ollama (1 command, 30 seconds)
curl -fsSL https://ollama.com/install.sh | sh

# Download model (2 minutes)
ollama pull llama3.2:3b

# That's it!
```

### "Can it access our cluster?"
**Answer**: "Only if you have kubectl configured. It can read context but doesn't make changes."

### "How accurate is it?"
**Answer**: "It's an LLM trained on public docs. Good for general guidance. Always verify critical decisions."

### "Can we customize it?"
**Answer**: "Yes! We can fine-tune with our runbooks and docs."

### "What about bigger/better models?"
**Answer**: 
```bash
# More capable models
ollama pull llama3.2      # 7GB, smarter
ollama pull llama3.2:70b  # 40GB, very smart (needs GPU)
```

### "Will this work on my laptop?"
**Answer**: "If you have 8GB+ RAM, yes. More RAM = bigger models."

---

## Demo Recovery

### If Response is Slow
**Say**: "This is the 3B model for speed. We can use bigger models for better responses."

### If Response is Generic
**Say**: "Let me ask it something more specific..." (use custom query)

### If Ollama Not Running
```bash
sudo systemctl start ollama
# Wait 5 seconds, try again
```

### If Model Not Found
```bash
ollama pull llama3.2:3b
# Takes 1-2 minutes
```

---

## Follow-up Actions

### Share with Team
1. Send them the README.md
2. One-liner install: `curl -fsSL https://ollama.com/install.sh | sh`
3. Point to demo directory: `~/nutanix-k8s-ai-demo/`

### Next Steps
- Install on more team members' laptops
- Create custom scenarios for your specific use cases
- Fine-tune with your internal documentation
- Integrate with your monitoring tools

---

## Impressive Demo Additions

### Show Multiple Models
```bash
ollama list  # Show what's available
```

### Live Comparison
Ask same question to different models:
```bash
ollama run llama3.2:3b "Your question"
ollama run mistral "Your question"
```

### Show Context Memory
- Ask a question
- Follow up with "Can you elaborate on point 3?"
- It remembers the previous response!

---

## Time-Based Demo Plans

### Quick (2 minutes)
1. Start demo
2. Run one pre-built scenario
3. "And it's all local!"

### Standard (5 minutes)
1. Start demo + show context
2. Two scenarios (troubleshooting + Nutanix)
3. One custom question
4. Show `ollama list`

### Extended (10 minutes)
1. All of standard
2. Multiple custom questions
3. Show model comparison
4. Take live questions from audience
5. Installation walkthrough

---

## Pro Tips

### Prep Before Demo
```bash
# Make sure everything is ready
cd ~/nutanix-k8s-ai-demo
./start-demo.sh  # Run once to warm up
# Exit with 'q'
```

### Have Backup Questions Ready
1. "How do I check if my persistent volume is bound?"
2. "What's the difference between a StatefulSet and a Deployment?"
3. "How do I configure resource limits for a pod?"

### Terminal Setup
- Use a large font (colleagues need to see)
- Dark background, light text
- Full screen terminal

### Timing
- Let responses finish fully
- Don't rush through reading
- Pause for questions

---

## Success Indicators

### Your colleagues will:
- ✓ Lean forward to see the screen
- ✓ Ask "how do I get this?"
- ✓ Start suggesting their own questions
- ✓ Take photos of the terminal
- ✓ Ask about costs (answer: FREE!)

---

**Remember**: You're not showing off AI magic. You're showing a practical tool that helps your team do their job better. Keep it focused on real problems and real solutions.

Good luck! 🚀
