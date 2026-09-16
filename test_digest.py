from datetime import datetime, timezone

from smart_data_radar.digest import render_markdown
from smart_data_radar.models import AnalysedArticle, Article, ArticleAnalysis
from test_llm import sample_analysis


def test_digest_contains_pestle_swot_and_hashtags():
    article = Article(
        url="https://example.com/a",
        canonical_url="https://example.com/a",
        title="Agentic AI and Smart Data",
        discovered_at=datetime.now(timezone.utc),
        discovery_method="test",
    )
    analysis = ArticleAnalysis.model_validate(sample_analysis())
    item = AnalysedArticle(
        article=article,
        analysis=analysis,
        final_score=88.5,
        priority_score=91.0,
        mode="weekly",
    )
    text = render_markdown([item], mode="weekly")
    assert "PESTLE" in text
    assert "SWOT" in text
    assert "#AIxSmartData" in text
    assert "Policy priority" in text
