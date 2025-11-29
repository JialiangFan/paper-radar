"""测试论文抓取功能（不调用 OpenAI）"""
import arxiv
from datetime import datetime, timedelta

KEYWORDS = ["Large Language Models", "Agentic Workflow"]
MAX_RESULTS = 3  # 测试时只抓 3 篇

def test_fetch_papers():
    """测试从 arXiv 获取论文"""
    print("=" * 50)
    print("测试论文抓取功能")
    print("=" * 50)
    
    for keyword in KEYWORDS:
        print(f"\n🔍 搜索关键词: {keyword}")
        try:
            search = arxiv.Search(
                query=keyword,
                max_results=MAX_RESULTS,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            # 使用新的 Client API
            client = arxiv.Client()
            papers = []
            for result in client.results(search):
                if result.published.date() >= (datetime.now().date() - timedelta(days=2)):
                    papers.append({
                        "title": result.title,
                        "url": result.entry_id,
                        "abstract": result.summary[:200] + "...",  # 只显示前200字符
                        "authors": ", ".join([a.name for a in result.authors]),
                        "date": result.published.strftime("%Y-%m-%d"),
                    })
            
            if papers:
                print(f"✅ 找到 {len(papers)} 篇最近 2 天的论文：")
                for i, paper in enumerate(papers, 1):
                    print(f"\n  {i}. {paper['title']}")
                    print(f"     作者: {paper['authors']}")
                    print(f"     日期: {paper['date']}")
                    print(f"     链接: {paper['url']}")
            else:
                print(f"⚠️  最近 2 天没有找到新论文")
                
        except Exception as e:
            print(f"❌ 获取论文失败: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("✅ 论文抓取功能测试完成！")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_fetch_papers()

