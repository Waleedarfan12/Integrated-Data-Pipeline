
### 1. How to run
To run the interactive public API consumer on a fresh machine:
1. Ensure Python 3.x is installed.
2. Install the necessary lightweight dependencies: `pip install requests`
3. Execute the client interface from your terminal: `python app.py`

*(Note: The broader production-grade Retail Intelligence ETL pipeline is fully detailed in the main README.md).*

### 2. Stack choice
I selected **Python** alongside the standard `requests` network library for this client. Python acts as the unified language across my entire Retail Intelligence project. It allows for highly readable extraction scripts, native string transformations, and clean exception-catching blocks without compiling steps.

*What would have been a worse choice?* **Java or C++**. Building a simple public JSON client in Java introduces heavy boilerplate code, strong type-casting layers for basic dictionaries, and slow deployment agility, which goes against modern data engineering scripting guidelines for lightweight API gateways.

### 3. One real edge case
* **The Edge Case:** Network Latency/API unresponsive hangs handled via explicit timeouts.
* **File and Line Number:** `app.py`, Line 15 (`requests.get(geo_url, timeout=5)`) and Line 27 (`requests.get(weather_url, timeout=5)`).
* **Explanation:** If the open-source Open-Meteo API experiences service spikes or server lag, omitting a timeout will cause the Python thread to block indefinitely. This completely freezes downstream pipeline transformations. By applying a strict 5-second timeout constraint and catching `requests.exceptions.Timeout`, the script cuts the hanging connection cleanly, outputs a safe user log, and exits gracefully with a system status code of 1.

### 4. AI usage
* **Tool Used:** Gemini
* **Prompt Given:** "Provide the unauthenticated endpoint parameters for searching a city by string name using the open-meteo geocoding tool."
* **Output Received:** A standard request template matching `https://geocoding-api.open-meteo.com/v1/search?name=London`.
* **What I Modified & Why:** The AI generated a raw return dump directly printing the coordinate results dictionary. I modified the code to check if `.get('results')` was empty or invalid, turning a potential frontend execution crash (a missing key error) into a clean, friendly user validation check inside the CLI wrapper.

### 5. Honest gap
Because of the strict 48-hour assessment constraint, the parsed weather-to-retail metrics live entirely in-memory and print directly to the user terminal console. If I had an extra calendar day, I would integrate a structural ingestion layer that appends these live-queried rows directly into an un-orchestrated SQLite or local `.csv` transaction log file to serve as an immutable data audit trail.
