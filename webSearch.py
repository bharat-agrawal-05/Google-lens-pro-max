import pandas as pd
from duckduckgo_search import DDGS

# Define the search query
search_query = 'Ratan Tata'

# Fetch search results from DuckDuckGo
results = DDGS().text(
    keywords=search_query,
    region='wt-wt',
    safesearch='off',
    max_results=50  # Limit the number of results
)

# Print the results for verification
print(results)

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Save the DataFrame to a CSV file
results_df.to_csv('duckduck_tutorial.csv', index=False)
