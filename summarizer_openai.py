from typing import List, Dict
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_TEXT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

SYS = "음성 뉴스 대본 작성자입니다. 각 뉴스를 2~3문장으로 핵심만 요약하고, 일반인이 이해하기 쉬운 한 문장 해설을 덧붙이세요. 과장 금지, 출처 언급."

def summarize_items(items: List[Dict]) -> List[Dict]:
    """Return list with added fields: 'bullet', 'explain', 'caption'"""
    out = []
    for it in items:
        content = f"""제목: {it['title']}
요약(원문): {it['summary']}
링크: {it['link']}"""
        prompt = (
            "다음 기사를 한국어로 2~3문장 브리핑 + 1문장 해설로 압축해 주세요.\n"
            "출력 JSON 키는 bullet(요약), explain(해설), caption(영상 자막용 2줄) 입니다.\n"
            "JSON만 출력:\n"
            f"{content}"
        )
        resp = client.chat.completions.create(
            model=OPENAI_TEXT_MODEL,
            messages=[
                {"role":"system", "content": SYS},
                {"role":"user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type":"json_object"},
        )
        try:
            data = resp.choices[0].message.content
        except Exception as e:
            print(f"API 응답 처리 오류: {e}")
            # 기본값으로 대체
            data = '{"bullet": "뉴스 요약", "explain": "뉴스 해설", "caption": "뉴스 자막"}'
        
        import json
        try:
            j = json.loads(data)
        except json.JSONDecodeError:
            print(f"JSON 파싱 오류: {data}")
            j = {"bullet": "뉴스 요약", "explain": "뉴스 해설", "caption": "뉴스 자막"}
        
        it.update({
            "bullet": j.get("bullet"),
            "explain": j.get("explain"),
            "caption": j.get("caption", j.get("bullet"))
        })
        out.append(it)
    return out
