#!/usr/bin/env bash

set -e

echo "========================================"
echo "Running All Relay System Scenarios"
echo "========================================"

echo ""
echo "Running Scenario 001..."
bash relay-system/tests/run_scenario_001.sh
python3 relay-system/tests/verify_scenario_001.py

echo ""
echo "Running Scenario 002..."
bash relay-system/tests/run_scenario_002.sh
python3 relay-system/tests/verify_scenario_002.py

echo ""
echo "Running Scenario 003..."
bash relay-system/tests/run_scenario_003.sh
python3 relay-system/tests/verify_scenario_003.py

echo ""
echo "========================================"
echo "ALL SCENARIOS PASSED"
echo "========================================"
