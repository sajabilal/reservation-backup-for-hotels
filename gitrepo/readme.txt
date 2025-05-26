📌 Project Overview
This project provides a failover solution for hotel reservation systems, ensuring customers and employees can still access reservation data even if the primary system goes down. It leverages AWS Route 53, S3, CloudFront, API Gateway, Lambda, and a secondary database to provide seamless failover and data accessibility.

🚀 Features
Automated DNS Failover using AWS Route 53.
Static Failover Page hosted on S3 + CloudFront.
API-Driven Reservation Access via API Gateway & Lambda.
Read-Only Secondary Database for querying reservation details.
Real-Time Health Checks to detect system failures.
🔧 Technologies Used
AWS Route 53, S3, CloudFront
API Gateway, Lambda (Node.js/Python)
DynamoDB / RDS (Secondary Read-Only DB)
AWS Database Migration Service (DMS)
📖 How It Works
1️⃣ Route 53 monitors the primary system via health checks.
2️⃣ If the system fails, Route 53 redirects traffic to CloudFront (failover site).
3️⃣ Users enter their Booking ID to retrieve reservation data.
4️⃣ API Gateway + Lambda fetches data from the secondary database.
5️⃣ Once the primary system is restored, Route 53 switches back automatically.

📂 Project Structure
scss
Copy
Edit
📂 hotel-reservation-failover  
 ├── 📁 backend (API & Lambda functions)  
 ├── 📁 frontend (Failover page on S3)  
 ├── 📁 database (Schema & replication setup)  
 ├── README.md (Project documentation)  
⚡ Setup & Deployment
1️⃣ Configure AWS Route 53 with primary & failover routing policies.
2️⃣ Deploy the failover static website on S3 + CloudFront.
3️⃣ Set up API Gateway & Lambda for reservation queries.
4️⃣ Configure Database Replication (DMS for secondary DB).
5️⃣ Test failover scenarios & system recovery.

📌 Next Steps
Improve real-time data sync to minimize replication lag.
Implement multi-region redundancy for higher availability.

SMTP credentials
IAM user name

ses-smtp-user
SMTP user name

AKIAW6DH3H3LSSALBYC2
SMTP password

BNRM9jZ5ohtKNAy1xAtxLE7F1Q2aI+a58w2o1icDB/Cp
