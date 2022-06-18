# pharos
A market analysis toolset focused on financial and ESG metrics sourced from various private and government data providers.

# Install:
1. Clone repository and navigate to top-level local directory.
2. Optionally create and activate virtual environment.
3. In terminal, run: `pip install .`

# Datamodel:
`core`: 
  * `Source` - Enum representing datasources and their top-level domains.
  * `Client` - Interface that constructs queries and retrieves data from a `Source`.  
  
`alpha_vantage`:
  * `Component` - Enum representing various datasets associated with an exchange listing, called by AlphaVantage `Client`.
  * `Ticker` - A NYSE or NASDAQ listing populated by datasets defined in `Component`.
  * `Portfolio` - Collection of `Tickers` to perform comparative analysis 
 
# Use:
Functionality currently limited to `alpha_vantage` package. An [alphavantage api key](https://www.alphavantage.co/support/#api-key) is required to execute queries.
Paste this key into an empty text file named `key.txt` formated as:
`apikey=YOURKEYHERE`
Future releases will embed this process via cli upon install.

Example: Summarize recent FAANG data:
  ```
  import alpha_vantage as av
  symbols = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOG']
  faang = av.Portfolio(symbols)
  print(faang.overview)
  ```
