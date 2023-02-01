# A Look at Global Emissions, Storms and Temperatures
### Group Members: Armin Nouri, Carol Lopez, Salma Tahlil, and Zach Bonk

## Github Navigation
  - Dash Folder:
    - Pages Folder - contains the code for each individual page of the Dash dashboard. (pg1.py, pg2.py, pg3.py, pg4.py, and pg5.py)
    - app.py - the actual application file for the Dash dashboard. Running this file compiles the pages together into one dashboard.
  - EDA Folder:
    - CO2_EDA.ipynb - contains EDA for static CO2 emissions dataset ranging from 1988 to 2019. This dataset contains factors like GDP and energy consumption as well.
    - CO2_EDA_2022.ipynb - contains EDA for other static CO2 emissions dataset ranging from 1750 (most countries have no data this far back) to 2022. This dataset contains only CO2 emissions.
    - InitialEDA.ipynb - contains EDA across all datasets. This was the first EDA file created and acted as our initial scratchpad for ideas.
    - Storm_mergeCO2_EDA.ipynb - contains EDA on storm dataset. 
    - temperature_EDA.ipynb - contains EDA on temperature dataset.
  - ETL Folder:
    - C02_ETL.ipynb - The ETL report related to our first CO2 emissions dataset.
    - CO2_ETL_2022 (1).ipynb - ETL report related to the other CO2 emissions dataset.
    - Cloud_ETL_Report.pdf - Text file that dicusses the ETL process in our kafka pipeline. Includes code snippets from our Azure Databricks files.
    - Storm_data_etl.ipynb - ETL report on the storm dataset.
    - Temperature_data_ETL.ipynb - ETL report on the temperature dataset.
  - Capstone Project Plan.pdf: This files is a text document containing our initial questions, project timeline, and a link to our project management plan built using monday.com.
  - Napkin_Capstone.pdf: This files contains photos of our original mock-ups for visualizations and the Dash dashboard
  - ml_co2_topredict_temperatures.ipynb: This file contains the code for our machine learning algorithms that use CO2 emissions to predict temperatures.
  - time-series-forecasting-with-xgboost.ipynb: The code for our machine learning model related to storm data and predicting various factors including property damage or injuries.
  - Technical_Report.pdf - to be added
  - Presentation_Slides.pdf - to be added
## Inital Questions 
- What is the overall trend of emissions in relation to severe weather events over a certain period of time? What types of storms are most affected?
- How does increase or decrease in storms affect overall damage caused by storms to property? To crops?
- What is the distribution of CO2 emissions by continent/region? 
- What are the correlation between different fossil fuel sources and other factors with co2 emissions  
- Which countries are highest in carbon emissions, has this changed within recent years ?  ( top 10 countries)
- How does temperature change over time and how does it relate to carbon emissions?
- How has CO2 emissions changed in the top 5 countries over time? As GDP increases or decreases does this impact CO2 emissions? 
- What are the most consumed energy types and changes in energy consumption patterns in the United States? 
- What is the Energy Intensity Per Capita and by GDP of Top 5 Energy Consumers?

## Tech Stack
tech needed --> vs code, jupyter, python libraries: dash, dash_bootstrap_components, plotly.express, pandas, numpy, matplotlib, seaborn

## Visualizations at a Glance
<img width="700" alt="image" src="https://user-images.githubusercontent.com/117112928/216142846-145616fd-b2d3-4b7a-ada5-95e957aad132.png">
<img width="700" alt="image" src="https://user-images.githubusercontent.com/117112928/216150890-25acaf94-0b7b-4c2f-8db3-4dc77ebbfc40.png">
<img width="700" alt="image" src="https://user-images.githubusercontent.com/117112928/216150804-c44a74ce-7107-43bc-b2b4-01c9abe92129.png">

