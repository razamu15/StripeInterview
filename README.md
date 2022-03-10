# StripeInterview
Stripe interview questions gathered from Internet, no guarantee of authenticity of source or the correctness of solutions. 

##Phone Interview
- Stripe Capital
- Compress URL
- HTTP Header Parser
- Mutual Rank
- Server Penalty
- User Points

##Virtual Onsite

###Coding
- Money Transfer
- Load Balancer
- Invoicer
- Rate Limiter

###Integration
- Request Replay
- Bike Map

###Bug Swash
- [Jackson-Core](https://github.com/FasterXML/jackson-core)
- [Moshi](https://github.com/square/moshi)

###System Design
- Payment Webhook
  - Background: [https://stripe.com/docs/webhooks](https://stripe.com/docs/webhooks)
  - Reference Design: [https://tianpan.co/notes/166-designing-payment-webhook](https://tianpan.co/notes/166-designing-payment-webhook)
- Counter Logging System
  - Just take a look on how AWS or Azure or GCP handles metrics
- Identity and Access Management System
  - Same as above, just refer to IAM systems in public clouds
- Ledger
  - Nothing special, just use message queue to receive transactions, and consume by subscribing to different merchant accounts
  - You can use NoSQL such as Cassandra or others to store transaction data as there is no ACID requirement
  - For each merchant account, do an aggregation on all transactions to get balance.
  - Periodically run aggregation to boost performance. For example, run it daily so you only need to run aggregation upon request for current day
