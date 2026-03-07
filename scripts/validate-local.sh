#!/bin/bash
# 本地验证脚本
# Usage: bash scripts/validate-local.sh

set -e

echo "=== 配置验证开始 ==="

# 1. 检查 Surge 配置语法
echo "📋 检查 Surge 配置..."
grep -q "^\[General\]" Surge-Full-Overseas-FullCoverage.conf || (echo "❌ 缺少 [General]" && exit 1)
grep -q "^\[Proxy Group\]" Surge-Full-Overseas-FullCoverage.conf || (echo "❌ 缺少 [Proxy Group]" && exit 1)
grep -q "^\[Rule\]" Surge-Full-Overseas-FullCoverage.conf || (echo "❌ 缺少 [Rule]" && exit 1)
echo "✅ Surge 配置结构正确"

# 2. 检查 Clash YAML 语法
echo "📋 检查 Clash YAML..."
if command -v python3 &> /dev/null; then
  python3 -c "import yaml; yaml.safe_load(open('Clash-Stash-FullCoverage.yaml'))" 2>&1 || (echo "❌ YAML 语法错误" && exit 1)
  echo "✅ Clash YAML 语法正确"
else
  echo "⚠️ 未安装 python3，跳过 YAML 检查"
fi

# 3. 检查重复代理组
echo "📋 检查重复代理组..."
SURGE_DUPS=$(grep "^[^#].*= select" Surge-Full-Overseas-FullCoverage.conf | sort | uniq -d)
if [ -n "$SURGE_DUPS" ]; then
  echo "❌ Surge 存在重复代理组:"
  echo "$SURGE_DUPS"
  exit 1
fi

CLASH_DUPS=$(grep "^  - name:" Clash-Stash-FullCoverage.yaml 2>/dev/null | sort | uniq -d)
if [ -n "$CLASH_DUPS" ]; then
  echo "❌ Clash 存在重复代理组:"
  echo "$CLASH_DUPS"
  exit 1
fi
echo "✅ 无重复代理组"

# 4. 检查规则文件存在（自定义规则）
echo "📋 检查自定义规则文件..."
for f in custom-rules/*.list; do
  if [ -f "$f" ]; then
    echo "  ✅ $f"
  else
    echo "  ❌ 缺失: $f"
  fi
done

# 5. 测试关键 URL 可访问性
echo "📋 测试关键 URL 可访问性..."
FAILED=0

# 检查关键 BM7 规则
TEST_URLS=(
  "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/China/China.list"
  "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Binance/Binance.list"
  "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/OpenAI/OpenAI.list"
  "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Netflix/Netflix.list"
)

for url in "${TEST_URLS[@]}"; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
  if [ "$HTTP_CODE" = "404" ]; then
    echo "❌ URL 404: $url"
    FAILED=1
  elif [ "$HTTP_CODE" = "200" ]; then
    echo "  ✅ $(basename $url)"
  else
    echo "  ⚠️ $HTTP_CODE: $url"
  fi
done

if [ $FAILED -eq 1 ]; then
  exit 1
fi

echo ""
echo "=== ✅ 所有验证通过 ==="