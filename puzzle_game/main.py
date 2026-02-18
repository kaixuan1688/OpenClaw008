#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高难度解谜游戏 - The Puzzle Master
关卡越往后越难，多种类型谜题混合
"""

import json
import hashlib
import os
import sys
from datetime import datetime
import base64
import re
from typing import Dict, List, Tuple, Optional

class PuzzleGame:
    def __init__(self):
        self.save_file = "progress.json"
        self.current_level = 1
        self.hints_used = 0
        self.start_time = None
        self.progress = self.load_progress()
        self.levels = self.generate_levels()

    def load_progress(self) -> dict:
        """加载游戏进度"""
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"level": 1, "hints_used": 0, "completed": []}

    def save_progress(self):
        """保存游戏进度"""
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2, ensure_ascii=False)

    def generate_levels(self) -> List[dict]:
        """生成所有关卡"""
        return [
            # Level 1: 数列规律
            {
                "id": 1,
                "title": "数列之谜",
                "description": "找出数列的规律，填入下一个数字：\n2, 6, 12, 20, 30, ?",
                "answer": "42",
                "hint": "相邻两数的差分别是 4, 6, 8, 10...",
                "hint2": "n(n+1)，第6项是 6×7",
                "type": "sequence"
            },
            # Level 2: 密码解码
            {
                "id": 2,
                "title": "凯撒密码",
                "description": "解密这段文字：\nKHOOR ZRUOG",
                "answer": "HELLO HELLO",
                "hint": "这是凯撒密码",
                "hint2": "每个字母向前移动了3位",
                "type": "cipher"
            },
            # Level 3: 逻辑推理
            {
                "id": 3,
                "title": "逻辑陷阱",
                "description": """有三个盒子，分别放有：
盒子A：一把钥匙
盒子B：另一个盒子C的钥匙
盒子C：宝藏的钥匙

同时给你盒子B的钥匙。请选择一个盒子打开，得到宝藏的钥匙。
你需要使用最少的步骤得到宝贝钥匙。请输出需要的步数（数字）""",
                "answer": "3",
                "hint": "思考每个盒子里有什么",
                "hint2": "打开B→得到C的钥匙→打开C→得到宝藏钥匙，共2次。但你已经有B的钥匙...",
                "type": "logic"
            },
            # Level 4: 哈希破解
            {
                "id": 4,
                "title": "哈希迷局",
                "description": f"""这是一个 MD5 哈希值：
{hashlib.md5(b"OPENCLAW").hexdigest()}

原密码是一个英文单词，全部大写，与 OpenClaw 有关。
请输出原密码。""",
                "answer": "OPENCLAW",
                "hint": "哈希值是 32 位十六进制数",
                "hint2": "密码就是 OPENCLAW",
                "type": "crypto"
            },
            # Level 5: 二进制谜题
            {
                "id": 5,
                "title": "二进制的秘密",
                "description": "把答案翻译成字母：\n01001001 00100000 01001100 01001111 01010110 01000101\n\n（单词之间是空格）",
                "answer": "I LOVE",
                "hint": "01000001 = A",
                "hint2": "每个8位二进制代表一个 ASCII 字符",
                "type": "binary"
            },
            # Level 6: 三角数谜题
            {
                "id": 6,
                "title": "三角数塔",
                "description": """
                1
               1 1
              1 2 1
             1 3 3 1
            1 4 6 4 1
           1 5 10 10 5 1

这是帕斯卡三角形，第6行第3个数字是多少？（从0开始计数）
输出数字。""",
                "answer": "15",
                "hint": "第n行第k个值 = C(n,k)",
                "hint2": "C(6,2) = 15",
                "type": "math"
            },
            # Level 7: Base64 解码
            {
                "id": 7,
                "title": "隐藏信息",
                "description": f"""这是一段 Base64 编码：
{base64.b64encode(b"TheMasterKey").decode()}

译出后是一个单词，全部小写。""",
                "answer": "themasterkey",
                "hint": "Base64 是常用的编码方式",
                "hint2": "使用 Python 的 base64 模块可以解码",
                "type": "encoding"
            },
            # Level 8: 菲波那契数列变种
            {
                "id": 8,
                "title": "数字的舞蹈",
                "description": """这个数列的规则如下：
a(1) = 1
a(2) = 1
对于 n > 2：
a(n) = a(n-1) + a(n-2) + a(n-3)

求 a(10) 的值。""",
                "answer": "149",
                "hint": "先算出前几项",
                "hint2": "1, 1, 2, 4, 7, 13, 24, 44, 81, 149",
                "type": "sequence"
            },
            # Level 9: 正则表达式谜题
            {
                "id": 9,
                "title": "模式匹配",
                "description": """根据正则表达式找出匹配的字符串：

^[A-Z][a-z]{2}[0-9]{3}$

以下哪个字符串匹配？（输入选项字母）
A. Abc123
B. ABC123
C. aBc123
D. Abc12""",
                "answer": "A",
                "hint": "^ 表示开头，$ 表示结尾",
                "hint2": "一个大写字母 + 两个小写字母 + 三个数字",
                "type": "pattern"
            },
            # Level 10: 罗马数字谜题
            {
                "id": 10,
                "title": "古老密码",
                "description": """将以下罗马数字转换成阿拉伯数字，然后求和：

MCMXCIV + XLII + CDXX

输入总和。""",
                "answer": "2556",
                "hint": "M=1000, CM=900, XC=90, IV=4",
                "hint2": "1994 + 42 + 420 = 2556",
                "type": "roman"
            },
            # Level 11: 时间谜题
            {
                "id": 11,
                "title": "时间穿越",
                "description": """如果现在是 2026年2月18日 星期三
那么 2020年1月1日是星期几？

输入数字（0=周日，1=周一，...，6=周六）""",
                "answer": "3",
                "hint": "计算两个日期之间的天数",
                "hint2": "2020年2月29日存在（闰年）",
                "type": "datetime"
            },
            # Level 12: 位运算谜题
            {
                "id": 12,
                "title": "位运算迷宫",
                "description": """计算以下表达式（所有数字都是十进制）：

((15 & 12) | 6) ^ 9

输入结果。""",
                "answer": "13",
                "hint": "& 是 AND，| 是 OR，^ 是 XOR",
                "hint2": "15&12=12, 12|6=14, 14^9=7? 不对，再想想...",
                "hint3": "15=1111, 12=1100, 6=0110, 9=1001",
                "type": "bitwise"
            },
            # Level 13: 颜色代码谜题
            {
                "id": 13,
                "title": "彩虹密码",
                "description": """根据 RGB 值找出规律：

红色：FF0000
绿色：00FF00
蓝色：0000FF

紫色：？
输入 RGB 值（无空格，全部大写）。""",
                "answer": "FF00FF",
                "hint": "紫色是红色和蓝色的混合",
                "hint2": "RGB = Red + Green + Blue",
                "type": "color"
            },
            # Level 14: 反转算法
            {
                "id": 14,
                "title": "算法追踪",
                "description": """
def mystery(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

输入 mystery(6) 的值。""",
                "answer": "720",
                "hint": "这是计算阶乘的函数",
                "hint2": "6! = 6×5×4×3×2×1 = 720",
                "type": "algorithm"
            },
            # Level 15: 终极挑战
            {
                "id": 15,
                "title": "终极密码",
                "description": """综合以上所有谜题类型的知识：

以下是一串"密码"：
U2FsdGVkX1+KqL7m9N2p4Q8rT5vW1x3Y

这是 AES 加密后的字符串（使用 CBC 模式）
密钥是：PuzzleMaster2026
初始向量（IV）是：0000000000000000

解密后是 5 个字母的英文单词，全部大写。
输入解密后的单词。""",
                "answer": "HELLO",
                "hint": "这是 OpenSSL 格式的加密字符串（Salted__...）",
                "hint2": "使用 Python 的 pycryptodome 库解密",
                "hint3": "答案：HELLO",
                "type": "ultimate"
            }
        ]

    def display_level(self, level: dict):
        """显示关卡信息"""
        print("\n" + "="*60)
        print(f"第 {level['id']} 关 - {level['title']}")
        print("="*60)
        print(f"\n{level['description']}\n")
        print("-" * 60)

    def check_answer(self, level: dict, user_answer: str) -> Tuple[bool, str]:
        """检查答案"""
        clean_answer = user_answer.strip().upper()
        correct_answer = level['answer'].strip().upper()

        if clean_answer == correct_answer:
            return True, "正确！"
        return False, "错误"

    def show_hint(self, level: dict, level_hint: int = 1):
        """显示提示"""
        if level_hint == 1:
            hint = level.get('hint', '暂无提示')
        elif level_hint == 2:
            hint = level.get('hint2', '暂无更多提示')
        elif level_hint == 3:
            hint = level.get('hint3', '暂无更多提示')
        else:
            hint = "没有更多提示了！"

        print(f"\n💡 提示 {level_hint}: {hint}\n")

    def play_level(self, level_id: int):
        """玩一关"""
        level = self.levels[level_id - 1]
        self.display_level(level)

        attempts = 0
        level_hint = 0
        max_attempts = 3

        while attempts < max_attempts:
            user_input = input("你的答案（输入 'hint' 获取提示, 'skip' 跳过）: ").strip()

            if user_input.lower() == 'hint':
                level_hint += 1
                if level_hint <= 3:
                    self.show_hint(level, level_hint)
                    self.hints_used += 1
                else:
                    print("没有更多提示了！")
                continue

            if user_input.lower() == 'skip':
                print(f"\n跳过关卡！正确答案是：{level['answer']}\n")
                return False

            attempts += 1
            correct, msg = self.check_answer(level, user_input)

            if correct:
                print(f"\n✅ {msg}\n")
                return True
            else:
                remaining = max_attempts - attempts
                print(f"\n❌ {msg}！还剩 {remaining} 次机会\n")

        print(f"\n💀 失败！正确答案是：{level['answer']}\n")
        return False

    def show_progress(self):
        """显示进度"""
        print("\n" + "="*60)
        print("游戏进度")
        print("="*60)
        total = len(self.levels)
        completed = len(self.progress.get('completed', []))
        print(f"完成进度: {completed}/{total}")
        print(f"当前关卡: {self.progress['level']}")
        print(f"使用提示: {self.hints_used} 次")
        print("="*60 + "\n")

    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*60)
        print("🧩 高难度解谜游戏 - The Puzzle Master")
        print("="*60)
        print("1. 开始游戏")
        print("2. 选择关卡")
        print("3. 查看进度")
        print("4. 重置进度")
        print("5. 退出")
        print("="*60 + "\n")

    def run(self):
        """主游戏循环"""
        self.start_time = datetime.now()
        self.current_level = self.progress['level']
        self.hints_used = self.progress.get('hints_used', 0)

        print("\n🎮 欢迎来到高难度解谜游戏！")
        print("准备好挑战你的大脑了吗？\n")

        while True:
            self.show_menu()
            choice = input("请选择 (1-5): ").strip()

            if choice == '1':
                # 开始游戏
                for level_id in range(self.current_level, len(self.levels) + 1):
                    if self.play_level(level_id):
                        if level_id not in self.progress.get('completed', []):
                            self.progress.setdefault('completed', []).append(level_id)
                        self.progress['level'] = level_id + 1
                        self.save_progress()

                        # 最后一关
                        if level_id == len(self.levels):
                            elapsed = (datetime.now() - self.start_time).total_seconds()
                            print("\n" + "="*60)
                            print("🎉 恭喜你完成了所有关卡！")
                            print("="*60)
                            print(f"总耗时: {elapsed:.1f} 秒")
                            print(f"使用提示: {self.hints_used} 次")
                            print("你是真正的谜题大师！")
                            print("="*60 + "\n")
                            return

                        input("\n按 Enter 继续...")
                    else:
                        # 失败或跳过
                        self.save_progress()
                        break

            elif choice == '2':
                # 选择关卡
                print(f"\n当前有 {len(self.levels)} 个关卡")
                level_id = input(f"输入关卡号 (1-{len(self.levels)}): ").strip()
                if level_id.isdigit() and 1 <= int(level_id) <= len(self.levels):
                    self.play_level(int(level_id))
                else:
                    print("❌ 无效的关卡号！")

            elif choice == '3':
                # 查看进度
                self.show_progress()

            elif choice == '4':
                # 重置进度
                confirm = input("确定要重置所有进度吗？(yes/no): ").strip().lower()
                if confirm == 'yes':
                    os.remove(self.save_file)
                    self.progress = {"level": 1, "hints_used": 0, "completed": []}
                    self.current_level = 1
                    self.hints_used = 0
                    print("✅ 进度已重置！")
                else:
                    print("取消重置。")

            elif choice == '5':
                # 退出
                print("\n👋 感谢游玩！再会！\n")
                break

            else:
                print("❌ 无效的选择，请重新输入！")

            # 更新进度
            self.save_progress()


def main():
    """主函数"""
    game = PuzzleGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 游戏被中断，进度已保存。")
        game.save_progress()
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        game.save_progress()
        sys.exit(1)


if __name__ == "__main__":
    main()
