# System Design Interview Volume 1 by Alex Wu

## Chapter 1: Scale from Zero to Millions of Users
This chapter is essentially a high level overview of components for systems

Databases
- Relational DBs represent and store data in tables and rows. Popular examples are MySQL, PostgreSQL, Oracle DB.
- Non-relational DBs can be key-value stores, graph store, column stores and document store. No join operations supported usually.
* Prefer non relational DBs if:
  * app requires super-low latency,
  * data is unstructured or there's not relational data,
  * only need to serialize and deserialize data (JSON, XML, YAML, etc)
  * need to store a massive amount of data

Vertical scaling vs horizontal scaling
* vertical scaling: process of adding more power (CPU, RAM, etc) to your servers
  * drawbacks with DB vertical scaling is higher cost, greater risk of single point of failures, hardware limits can be reached if too large of a user base
* horizontal scaling: scale by adding more servers (this is called "sharding" for DB horizontal scaling)

Load balancer
* Load balancer evenly distributes incoming traffic among web servers

Servers read from "follower" DBs and servers write to "leader" DBs

Database replication benefits:
* better performances, master nodes perform writes, follower DB nodes have read operations distributed across them. This model allows more queries to be processed in parallel
* reliability in event of DB server loss or failure
* high availability - system remains in operation even if a DB is offline in another location

Cache
A cache is a temporary storage area that stores the result of the expensive responses or frequently accessed data in memory so that subsequent requests are served more quickly

Benefits:
- better system performance
- ability to reduce database workloads
- ability to scale cache tier independently

server first checks if cache has the available response, checks DB if not present in cache

consider using cache when data is read frequently but modified infrequently

CDN
a cdn is a network of geographically dispersed servers used to deliver static content (images, videos, CSS, JS files, etc)

Data Centers

Message queue
- a durable component, stored in memory thay supports asynchronous communication. Serves as a buffer and distributes async requests.
- Producers/publishers create messages and publish them to a queue
- Consumers/Subscribers connect to the queue and perform actions defined by the messages
- Helps with failure resilience (durable?) and loose coupling

Logging, monitor error logs
Metrics, collect metrics for business insights and understand health status of the system
- host level metrics: useful metrics: CPU, memory, disk i/o
- aggregated level metrics: performance of entire DB tier, cache tier, etc
- key business metrics: daily active users, retention, revenue

Sharding separates large databases into smaller, more easily managed parts called shards. Each shard shares the same schema though the actual data on each shard is unique to the shard


Summary of how to scale system to support millions of users:
* keep web tier stateless
* build redundancy at every tier
* cache data as much as possible
* support multiple data centers
* host static assets in CDN
* scale data tier by sharding
* split tiers into individual services
* monitor system and use automation tools

## Chapter 2:
