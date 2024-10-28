# Realtime-Stock-Analysis
This project leverages the power of Apache Airflow, Confluent Kafka, ksqlDB, and a Telegram bot to create a robust real-time stock alert system. The system is designed to monitor stocks from Yahoo Finance, identify significant price movements and volume surges, and deliver timely alerts to users via Telegram.

## Key Components:

### 1. Data Ingestion:

  * **Apache Airflow**: 
          Orchestrates the data ingestion process, scheduling and monitoring data pipelines.
    
  * **Yahoo Finance API**: 
          Fetches real-time stock data, including price, volume, and historical data.
    
  *  **Confluent Kafka**: 
          Receives and stores the ingested data in a reliable and scalable manner.
### 2. Data Processing:

* **ksqlDB:**
  A real-time stream processing engine that :
  
  a. Identifies stocks with a price change of more than 3% within an hour and having current volume more than 10-day average volume.
  
  b. Filters stocks based on the 10-day average volume and price change criteria.

### 3. Alert Notification:

* **Telegram Bot:** Delivers real-time alerts to users via Telegram, providing information about the stock symbol, current price, and percentage change.

  <img height="500" width="1275" alt="SCR-20241023-neuc" src="https://github.com/user-attachments/assets/fe93ca72-26fd-41ec-ab7b-3f833aad0b20">


# Data Flow Diagram (DFD)

![dfd](https://github.com/user-attachments/assets/79b4959c-f0a6-452c-b873-0f479c0bd04b)
