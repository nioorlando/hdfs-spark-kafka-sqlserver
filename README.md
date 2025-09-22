# HDFS → Spark Batch → Kafka → SQL Server

## 📖 Overview
This project demonstrates how **Apache Spark (batch)** reads JSON data, applies simple transformations, and publishes messages into **Apache Kafka** in **schemaful envelope format** (mimicking Kafka Connect style: `{"schema": {...}, "payload": {...}}`).  
This approach is useful for bootstrapping Kafka topics with initial data or preparing data for downstream consumers.

---
 
## 🏗 Architecture
<img src="images/hdfs_spark_kafka_sqlserver.jpg" alt="Spark Batch to Kafka" width="800"/>

**Flow:**
1. **Source JSON** → input dataset (e.g. `id:int`, `name:string`).  
2. **Spark Batch Job** → clean & transform (trim, uppercase, drop nulls).  
3. **Schemaful envelope** → Spark wraps each record into Connect-style `schema` + `payload`.  
4. **Kafka Topic** → receives structured events.  
5. (Optional) **Downstream** → HDFS Sink / JDBC Sink.

---

## 🛠 Tech Stack
- Apache Spark 3 (batch mode)  
- Apache Kafka (SASL/Kerberos + TLS enabled)  
- JDK 8/11  
- (Optional) Cron for scheduling jobs  

---

## ⚡ Key Features
- Simple ETL with Spark (cleaning & uppercase transform).  
- Publishes records to Kafka in **schemaful envelope** (compatible with Kafka Connect).  
- Secure Kafka connection using **Kerberos + TLS** (JAAS & krb5 configs included as templates).  

---

## 🚀 Components
- **Spark Batch Publisher**  
  Located at [`spark/spark_batch_to_kafka.py`](spark/spark_batch_to_kafka.py).  
  Reads JSON, transforms, wraps into schemaful envelope, and publishes to Kafka.  

- **Security Configs**  
  - [`configs/kafka_client_jaas.conf`](configs/kafka_client_jaas.conf) → JAAS template for Kafka client.  
  - [`configs/krb5.conf`](configs/krb5.conf) → Kerberos realm & domain mapping template.  

- **Notebook (Optional)**  
  [`notebooks/UC2_Spark_Cron.ipynb`](notebooks/UC2_Spark_Cron.ipynb) – shows how to schedule the Spark job periodically with cron.

---

## 📂 Repository Structure
```text
hdfs-spark-kafka-sql-server/
├── README.md
├── images/
│   └── hdfs_spark_kafka_sqlserver.jpg
├── spark/
│   └── spark_batch_to_kafka.py
├── configs/
│   ├── kafka_client_jaas.conf
│   └── kafka-truststore.jks
│   └── krb5.conf
│   └── mssql-sink.json
├── sample_data/
│   └── input.jsonl
│   └── output_envelope.json
└── notebooks/
    └── UC2_Spark_Cron.ipynb
```

## 🧪 Sample Input & Output

- [`sample_data/input.jsonl`](sample_data/input.jsonl) → source JSON file.  
- [`sample_data/output_envelope.json`](sample_data/output_envelope.json) → example schemaful envelope published to Kafka.

**Input JSON (placed in `/uc2/<username>/uc2_src`):**


