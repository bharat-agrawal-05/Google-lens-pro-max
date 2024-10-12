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

    # Create a DataFrame from the results
    results_df = pd.DataFrame(results)

    # Save the DataFrame to a CSV file
    results_df.to_csv('duckduck_tutorial.csv', index=False)
