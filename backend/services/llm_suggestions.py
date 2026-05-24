import json
import os
import sys
import traceback
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from llm_config import (
        LLM_PROVIDER, LLM_API_KEY, LLM_MODEL, LLM_BASE_URL,
    )
except ImportError:
    LLM_PROVIDER = "none"
    LLM_API_KEY = ""
    LLM_MODEL = ""
    LLM_BASE_URL = ""


def _build_prompt(text, predictions, summary):
    pos_count = summary.get('正面', 0)
    neg_count = summary.get('负面', 0)
    neu_count = summary.get('中性', 0)

    pos_dims = []
    neg_dims = []
    neu_dims = []
    for key, val in predictions.items():
        name = val.get('display_name', key)
        sent = val.get('sentiment', '未提及')
        if sent == '正面':
            pos_dims.append(name)
        elif sent == '负面':
            neg_dims.append(name)
        elif sent == '中性':
            neu_dims.append(name)

    return f"""你是一位资深的餐饮行业顾问。请根据以下顾客评论的情感分析结果，为餐厅经营者提供具体、可操作的改进建议。

【顾客评论原文】
{text}

【情感分析结果】
- 正面维度（{pos_count}个）：{', '.join(pos_dims) if pos_dims else '无'}
- 负面维度（{neg_count}个）：{', '.join(neg_dims) if neg_dims else '无'}
- 中性维度（{neu_count}个）：{', '.join(neu_dims) if neu_dims else '无'}

【要求】
请用中文输出一个严格的JSON对象（不要包含markdown代码块标记），格式如下：
{{
    "overall_advice": "针对这篇评论反映的整体情况的总结建议（50-80字）",
    "improvements": [
        {{
            "dimension": "维度名称",
            "priority": "high 或 medium",
            "advice": "结合评论原文具体问题给出的针对性改进措施（30-60字）"
        }}
    ],
    "strengths_summary": "对于表现好的方面的总结和保持建议（30-50字）"
}}

注意：
1. 建议必须结合评论原文的具体措辞，不要给泛泛的模板化建议
2. priority: 负面=high, 中性=medium
3. 只输出JSON，不要输出其他任何文字"""


def _parse_response(content):
    content = content.strip()

    if content.startswith('```'):
        lines = content.split('\n')
        if lines[-1].strip() == '```':
            content = '\n'.join(lines[1:-1])
        else:
            content = '\n'.join(lines[1:])
        content = content.strip()

    content = content.lstrip('\ufeff')

    import re

    match = re.search(r'\{[\s\S]*\}', content)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    for fmt in (content, content + '}', content + ']}'):
        try:
            return json.loads(fmt)
        except json.JSONDecodeError:
            continue

    depth = 0
    for i, ch in enumerate(content):
        if ch == '{' or ch == '[':
            depth += 1
        elif ch == '}' or ch == ']':
            depth -= 1
        if depth == 0 and i > 0 and ch in ('}', ']'):
            try:
                return json.loads(content[:i + 1])
            except json.JSONDecodeError:
                pass

    raise ValueError(f"Cannot parse JSON from response: {content[:200]}")


def _call_openai_compatible(prompt):
    url = LLM_BASE_URL.rstrip('/') + '/chat/completions'
    data = json.dumps({
        'model': LLM_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.1,
        'max_tokens': 2048,
    }).encode('utf-8')

    print(f"[LLM] Calling {LLM_PROVIDER} API: {url}")
    print(f"[LLM] Model: {LLM_MODEL}")

    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LLM_API_KEY}',
    })

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        print(f"[LLM] API response received ({len(json.dumps(result))} chars)")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(f"[LLM ERROR] HTTP {e.code}: {body}")
        raise
    except Exception as e:
        print(f"[LLM ERROR] {type(e).__name__}: {e}")
        raise

    content = result['choices'][0]['message']['content']
    print(f"[LLM] Raw response (first 300 chars): {content[:300]}")
    parsed = _parse_response(content)
    return parsed


def _call_ollama(prompt):
    import ollama
    print("[LLM] Falling back to local ollama (qwen2.5:3b) ...")
    response = ollama.chat(
        model='qwen2.5:3b',
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0.3, 'num_predict': 1024},
    )
    return _parse_response(response['message']['content'])


def generate_llm_suggestions(text, predictions, summary):
    prompt = _build_prompt(text, predictions, summary)

    print(f"[LLM] Provider={LLM_PROVIDER}, Key={'***' if LLM_API_KEY else 'EMPTY'}, Model={LLM_MODEL}")

    if LLM_PROVIDER in ('siliconflow', 'deepseek', 'openai', 'custom') and LLM_API_KEY and 'xxxxxxxx' not in LLM_API_KEY:
        for attempt in range(3):
            try:
                print(f"[LLM] Attempt {attempt + 1}/3...")
                result = _call_openai_compatible(prompt)
                if result and 'overall_advice' in result:
                    print("[LLM] Success - valid JSON received")
                    return result
                print("[LLM] Response missing required fields, retrying...")
            except Exception as e:
                print(f"[LLM] Attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    traceback.print_exc()

    try:
        import ollama
        return _call_ollama(prompt)
    except Exception as e:
        print(f"[LLM] ollama not available: {e}")

    print("[LLM] All methods failed, no suggestions available.")
    return None
