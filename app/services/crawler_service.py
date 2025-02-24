import requests
from bs4 import BeautifulSoup
import json  # JSON 저장을 위해 추가

# 매일경제 주식 뉴스 URL
url = "https://stock.mk.co.kr/news/company"

# User-Agent 설정 (크롤링 차단 방지)
headers = {"User-Agent": "Mozilla/5.0"}

# 요청 보내기
response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # 뉴스 기사 목록 선택
    items = soup.select("li.news_node")  # 뉴스 항목 리스트

    # 크롤링한 데이터를 저장할 리스트
    news_data = []

    for item in items[:5]:  # 상위 5개 뉴스만 가져오기
        title_tag = item.select_one("h3.news_ttl")  # 제목 태그
        link_tag = item.select_one("a.news_item")  # 뉴스 링크 태그
        img_tag = item.select_one("div.thumb_area img")  # 뉴스 이미지 태그

        # 제목 가져오기
        title = title_tag.text.strip() if title_tag else "제목 없음"

        # 링크 가져오기
        link = (
            link_tag["href"] if link_tag and "href" in link_tag.attrs else "링크 없음"
        )
        if not link.startswith("http"):  # 상대경로 처리
            link = "https://stock.mk.co.kr" + link

        # 이미지 URL 가져오기
        img_url = (
            img_tag["src"] if img_tag and "src" in img_tag.attrs else "이미지 없음"
        )

        # 개별 뉴스 페이지 요청 → 본문 전체 크롤링
        news_response = requests.get(link, headers=headers)
        if news_response.status_code == 200:
            news_soup = BeautifulSoup(news_response.text, "html.parser")

            # 본문 가져오기 (`div.news_detail_wrap` 내부 텍스트 추출)
            content_tag = news_soup.select_one("div.news_detail_wrap")
            content_text = (
                "\n".join(content_tag.stripped_strings) if content_tag else "본문 없음"
            )
        else:
            content_text = "본문 로드 실패"

        # 결과 저장
        news_data.append(
            {"제목": title, "링크": link, "본문": content_text, "이미지": img_url}
        )

    # 📌 JSON 파일로 저장
    with open("news_data.json", "w", encoding="utf-8") as json_file:
        json.dump(
            news_data, json_file, ensure_ascii=False, indent=4
        )  # 한글 깨짐 방지 + 예쁘게 저장

    print("✅ 뉴스 데이터가 news_data.json 파일로 저장되었습니다!")

else:
    print("페이지 요청 실패:", response.status_code)
