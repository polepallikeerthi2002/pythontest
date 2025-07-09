
from papers.fetch_papers import fetch_papers

def test_fetch_papers():
    results = fetch_papers("cancer", max_results=2)
    assert isinstance(results, list)
    assert len(results) <= 2
