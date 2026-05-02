#!/bin/bash
set -e

echo "=== 配置验证开始 ==="

echo "📋 检查当前 YAML 配置..."
python3 - <<'PY'
import yaml
for path in [
    'stash/Stash-v4-public-airport-android.yaml',
    'custom-rules-clash/My-Crypto.yaml',
    'custom-rules-clash/My-Finance-Direct.yaml',
]:
    with open(path, encoding='utf-8') as f:
        yaml.safe_load(f)
    print('✅ YAML 语法正确:', path)
PY

echo "📋 检查重复策略组..."
for f in stash/Stash-v4-public-airport-android.yaml; do
  DUPS=$(grep "^  - name:" "$f" 2>/dev/null | sort | uniq -d)
  if [ -n "$DUPS" ]; then
    echo "❌ 存在重复策略组: $f"
    echo "$DUPS"
    exit 1
  fi
done
echo "✅ 无重复策略组"

echo "📋 检查自维护规则文件..."
for f in custom-rules/My-Crypto.list custom-rules/My-Finance-Direct.list custom-rules-clash/My-Crypto.yaml custom-rules-clash/My-Finance-Direct.yaml; do
  test -f "$f"
  echo "  ✅ $f"
done

echo "📋 测试关键 URL 可访问性..."
FAILED=0
TEST_URLS=(
  "https://raw.githubusercontent.com/dodo258/surge/main/custom-rules-clash/My-Crypto.yaml"
  "https://raw.githubusercontent.com/dodo258/surge/main/custom-rules-clash/My-Finance-Direct.yaml"
)
for url in "${TEST_URLS[@]}"; do
  HTTP_CODE=$(curl -L -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
  if [ "$HTTP_CODE" = "404" ]; then
    echo "❌ URL 404: $url"
    FAILED=1
  elif [ "$HTTP_CODE" = "200" ]; then
    echo "  ✅ $(basename "$url")"
  else
    echo "  ⚠️ $HTTP_CODE: $url"
  fi
done
if [ $FAILED -eq 1 ]; then
  exit 1
fi

echo ""
echo "=== ✅ 所有验证通过 ==="
