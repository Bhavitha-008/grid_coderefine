import re

def analyze_code(code):
    errors = []
    suggestions = []

    # ----------------------------
    # 1️⃣ Loop Detection (Better)
    # ----------------------------
    loop_pattern = r'\b(for|while|do)\b'
    loops = re.findall(loop_pattern, code)
    loop_count = len(loops)

    # Detect nested loops (basic heuristic)
    nested_loops = len(re.findall(r'for\s*\(.*?\)\s*\{[^{}]*for\s*\(', code, re.DOTALL))

    # ----------------------------
    # 2️⃣ Function Detection
    # ----------------------------
    function_pattern = r'\b(int|float|double|char|void)\s+\w+\s*\([^)]*\)\s*\{'
    function_count = len(re.findall(function_pattern, code))

    # ----------------------------
    # 3️⃣ Braces & Parentheses Check
    # ----------------------------
    if code.count("{") != code.count("}"):
        errors.append("❌ Mismatched curly braces { }")

    if code.count("(") != code.count(")"):
        errors.append("❌ Mismatched parentheses ( )")

    # ----------------------------
    # 4️⃣ Missing Semicolon Check
    # ----------------------------
    lines = code.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (
            stripped
            and not stripped.startswith("#")
            and not stripped.endswith(";")
            and not stripped.endswith("{")
            and not stripped.endswith("}")
            and not stripped.startswith("//")
            and "(" not in stripped
            and ")" not in stripped
        ):
            errors.append(f"❌ Possible missing semicolon at line {i+1}")

    # ----------------------------
    # 5️⃣ Infinite Loop Check
    # ----------------------------
    if re.search(r'while\s*\(\s*1\s*\)', code) or re.search(r'for\s*\(\s*;\s*;\s*\)', code):
        errors.append("⚠️ Possible infinite loop detected")

    # ----------------------------
    # 6️⃣ Time Complexity Estimation
    # ----------------------------
    if nested_loops > 0:
        complexity = "O(n^2) or higher (Nested loops detected)"
    elif loop_count == 1:
        complexity = "O(n)"
    elif loop_count > 1:
        complexity = "O(n^k)"
    else:
        complexity = "O(1)"

    # ----------------------------
    # 7️⃣ Efficiency Suggestions
    # ----------------------------
    if "printf" in code and loop_count > 0:
        suggestions.append("💡 Avoid excessive printf inside loops (can slow execution).")

    if nested_loops > 0:
        suggestions.append("💡 Consider optimizing nested loops (maybe use hashing or precomputation).")

    if loop_count == 0:
        suggestions.append("💡 No loops detected. Code runs in constant time.")

    # ----------------------------
    # REPORT
    # ----------------------------
    print("\n===== ANALYSIS REPORT =====")
    print("Total Loops:", loop_count)
    print("Nested Loops:", nested_loops)
    print("Functions:", function_count)
    print("Estimated Time Complexity:", complexity)

    print("\n--- Errors ---")
    if errors:
        for err in errors:
            print(err)
    else:
        print("✅ No obvious syntax errors detected.")

    print("\n--- Efficiency Suggestions ---")
    if suggestions:
        for sug in suggestions:
            print(sug)
    else:
        print("✅ Code looks efficient for its structure.")


# 🔹 Paste your C code below
code_input = """
#include<stdio.h>

int main() {
    int i;

    for(i = 0; i < 10; i++) {
        printf("%d\\n", i);
    }

    return 0;
}
"""

analyze_code(code_input)