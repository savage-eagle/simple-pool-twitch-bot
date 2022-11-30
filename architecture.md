# Where will your solution be hosted

Hosting this solution in AWS we should use the following services:

- Lightsail
- EC2
- Elastic Beanstalk

If we are going to use AWS infrastructure, I would go with Lightsail.

Hosting this solution in GCP could be in:

- Compute Engine
- App Engine

If we are going to use GCP infrastructure, I would go with Compute Engine.

# What tools will be used to guarantee performance and security

We can use AWS WAF or GCP WAF to protect our application from attacks on AWS.

We can use GCP WAF to protect our application from attacks on GCP.

# How well does it scale if the number of users rises exponentially

AWS Lightsail and GCP App Engine are good options to scale our application.

# How would implement a data architecture for future analytics

We can use AWS RDS, GCP BigQuery to store our data and make queries.
