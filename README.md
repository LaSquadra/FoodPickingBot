**How to set up**
NOTE:  This project uses UV (an alternative to pip) --> https://docs.astral.sh/uv/getting-started/installation/
1. Run the 'uv sync' command to initialize the UV environment.
   ```
   uv sync
   ```
2. Copy your API keys to the .env file.
   
    - Note:  This project uses Tavily so make sure you have your Tavily API key ready.
    - https://www.tavily.com/ --> You can create a FREE account with no credit card required (at time of writing).
3. Run the agents_file.py script to start the agents.
   ```
   uv run agents_file.py
   ```
