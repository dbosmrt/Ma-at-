import logging
from ddgs import DDGS
logging.basicConfig(level=logging.INFO)

print("Starting DDGS search...")
try:
    with DDGS() as ddgs:
        results = ddgs.text("Nirbhaya Case Punishment", region='in-en', max_results=3)
        print(list(results))
except Exception as e:
    print(f"Error: {e}")
