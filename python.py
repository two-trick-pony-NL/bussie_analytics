
import pandas as pd
import numpy as np
import requests


response = requests.get("http://localhost:8000/API/V1/vehicles")
response = response.json()
df = pd.DataFrame.from_dict(response)

print(df.T)