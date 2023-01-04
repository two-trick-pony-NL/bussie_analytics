
import pandas as pd
import numpy as np
import requests


response = requests.get("https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/API/V1/get_all_vehicle_information")
response = response.json()
df = pd.DataFrame.from_dict(response)

print(df.T)
