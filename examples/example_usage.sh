#!/bin/bash
# Example usage script for the reorganizer tool

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Question Bank Reorganizer - Example Usage${NC}"
echo ""

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source ../.venv/bin/activate
fi

echo -e "${GREEN}Example 1: Export GIFT questions${NC}"
echo "Command: reorganizer export gift sample.gift -o gift_backup"
echo ""

echo -e "${GREEN}Example 2: Collect GIFT questions${NC}"
echo "Command: reorganizer collect gift gift_backup -o rebuilt.gift"
echo ""

echo -e "${GREEN}Example 3: Export XML questions${NC}"
echo "Command: reorganizer export xml questions.xml -o xml_backup"
echo ""

echo -e "${GREEN}Example 4: Collect XML questions${NC}"
echo "Command: reorganizer collect xml xml_backup -o rebuilt.xml"
echo ""

echo "See USAGE.md for more examples"
