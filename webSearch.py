import pandas as pd
from duckduckgo_search import DDGS

def search(keywords):
    search_query = keywords

    # Fetch search results from DuckDuckGo
    results = DDGS().text(
        keywords=search_query,
        region='wt-wt',
        safesearch='off',
        max_results=20  # Limit the number of results
    )

    # Print the results for verification
    print(results)
    results_df = pd.DataFrame(results)
    results_df.to_csv(f'{''.join(keywords.split())}.csv', index=False)
