#!/bin/bash
# Deploy the BibleAgent MCP service to Hostinger VPS

echo "=== BibleAgent MCP Service Deployment ==="
echo "Project: BibleStudy Agent (x402 payments)"

# Check if Hostinger VPS is reachable
echo -n "Checking VPS connection... "
if ssh -o BatchMode=yes -o ConnectTimeout=5 vikto@136.65.185.232 exit 2>/dev/null; then
    echo "OK"
else
    echo "FAILED"
    echo "Cannot connect to VPS. Check SSH credentials and network."
    exit 1
fi

# Create service directory on VPS
echo "Creating service directory on VPS..."
ssh vikto@136.65.185.232 << 'REMOTE'
mkdir -p ~/agent-services/bible-agent-mcp
cp -r /c/Users/vikto/agent-services/my-agent-mcp/* ~/agent-services/bible-agent-mcp/
