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

<p align="center">
  <img width="300" alt="SCR-20241023-neuc" src="https://github.com/user-attachments/assets/41675f03-1eee-4acc-88ef-27865a467765">
</p>


# Data Flow Diagram (DFD)

![dfd](https://github.com/user-attachments/assets/79b4959c-f0a6-452c-b873-0f479c0bd04b)
