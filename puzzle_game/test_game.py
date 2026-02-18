#!/usr/bin/env python3
# 测试游戏脚本

import subprocess
import sys

# 游戏答案（每行一个，包括Enter）
inputs = """1
42

HELLO HELLO

11

OPENCLAW

I LOVE

15

themasterkey

149

A

2556

3

13

FF00FF

720

HELLO

5
exit
"""

# 运行游戏
process = subprocess.Popen(
    ['python3', 'main.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 发送输入
stdout, stderr = process.communicate(inputs)

# 输出结果
if process.returncode == 0:
    print("=" * 60)
    print("✅ 游戏运行成功！")
    print("=" * 60)

    # 检查是否完成所有关卡
    if "完成进度: 15/15" in stdout:
        print("✅ 所有15关全部通过！")
    else:
        print("⚠️  未完成所有关卡")

    # 检查通关消息
    if "恭喜你完成了所有关卡" in stdout:
        print("✅ 已显示通关祝贺信息")
    else:
        print("⚠️  未找到通关祝贺信息")

    # 显示最终进度信息
    for line in stdout.split('\n'):
        if '完成进度' in line or '总耗时' in line or '使用提示' in line:
            print(f"📊 {line}")

else:
    print(f"❌ 游戏运行失败！返回码: {process.returncode}")
    if stderr:
        print(f"错误信息: {stderr}")

# 输出完整的尾部信息
print("\n" + "=" * 60)
print("游戏输出尾部：")
print("=" * 60)
print('\n'.join(stdout.split('\n')[-20:]))
