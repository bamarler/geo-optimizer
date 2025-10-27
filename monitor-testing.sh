#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         📊 GEO Testing Monitor (EC2)                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

if [ -z "$1" ]; then
    echo "Usage: ./monitor-testing.sh <persona_set_id>"
    echo ""
    echo "Example: ./monitor-testing.sh 67364f8c5e9a2b001234abcd"
    echo ""
    echo "You can find the persona_set_id from the frontend or MongoDB."
    exit 1
fi

PERSONA_SET_ID=$1

echo "Monitoring test run: $PERSONA_SET_ID"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if log file exists on server
echo "1. Checking for log file on EC2..."
ssh -i ~/Downloads/my.pem ec2-user@54.221.56.44 \
  "ls -lh /home/ec2-user/geo-platform/geo-testing/test_run_${PERSONA_SET_ID}.log 2>/dev/null || echo 'Log file not found yet'"

echo ""
echo "2. Checking for running processes..."
ssh -i ~/Downloads/my.pem ec2-user@54.221.56.44 \
  "ps aux | grep -E 'run_from_db|chromium|playwright' | grep -v grep || echo 'No testing processes running'"

echo ""
echo "3. Checking MongoDB for results..."
echo "   (Checking if any results have been saved)"

# Use the API to check results
curl -s "https://test.citable.xyz/api/test-results/${PERSONA_SET_ID}" | \
  python3 -c "import sys, json; data = json.load(sys.stdin); print(f\"   Results found: {data.get('stats', {}).get('total_tests', 0)} tests\") if data.get('success') else print('   No results yet')"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Live log tail (last 50 lines):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

ssh -i ~/Downloads/my.pem ec2-user@54.221.56.44 \
  "tail -50 /home/ec2-user/geo-platform/geo-testing/test_run_${PERSONA_SET_ID}.log 2>/dev/null || echo 'No log content yet'"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 To watch logs in real-time, run:"
echo "   ssh -i ~/Downloads/my.pem ec2-user@54.221.56.44"
echo "   tail -f /home/ec2-user/geo-platform/geo-testing/test_run_${PERSONA_SET_ID}.log"
echo ""
echo "🔄 To refresh this monitor, run:"
echo "   ./monitor-testing.sh $PERSONA_SET_ID"
echo ""

