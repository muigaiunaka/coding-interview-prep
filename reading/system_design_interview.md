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

## Chapter 2: Back of the envelope estimation

Power of Two

| Power | Approximate Value | Full Name  | Short Name |
| ----: | ----------------- | ---------- | ---------- |
|    10 | 1 thousand        | 1 kilobyte | 1 kB       |
|    20 | 1 million         | 1 megabyte | 1 MB       |
|    30 | 1 billion         | 1 gigabyte | 1 GB       |
|    40 | 1 trillion        | 1 terabyte | 1 TB       |
|    50 | 1 quadrillion     | 1 petabyte | 1 PB       |


Latency Numbers Tips
- memory is fast but the disk is slow
- avoid disk seeks if possible
- simple compression algorithms are fast
- compress data before sending it over the internet if possible
- data centers are usually in different regions, and it takes time to send data between them

Availability Numbers
- Service Level Agreement (SLA) - agreement between service provider and customer, which defines the level of uptime the service will deliver
- 99% 14.40 minutes downtime per day to 99.9999% is 86.40 milliseconds downtime per day. range of adding 9s which drops downtime relationally

## Chapter 3: A framework for system design interviews
System design interview gives signals on one's ability:
- to collaborate
- to work under pressure
- to resolve ambiguity constructively
- to ask good questions
- present technical design skills

4 Step process
#### Step 1 - Understand the problem and establish design scope
_Time allocation: 3 to 10 minutes_
- don't jump right in to give a solution. Think deeply, ask questions to clarify requirements and assumptions
- Questions to ask
  - what specific features are we going to build?
  - how many users does the product have?
  - how fast does the company anticipate to scale up? What are the anticipated scales in 3 months, 6 months and a year?
News Feed Example
  - is this a mobile app or web app or both?
  - what are the most important features for the product?
  - is the news feed sorted in reverse chronological order or a particular order? The particular order means each post is given a different weight. For example, close friend's posts are more important than posts from a group
  - how many friends can a user have?
  - *what is the traffic volume?*
  - can the feed contain images, videos or just text?

#### Step 2 - propose high level design and get buy-in
_Time allocation: 10 to 15 minutes_
- Aim to develop a high level design and reach an agreement with the interviewer on the design. Collaborate with the interviewer during the process
- Start small with initial blueprint for the design, ask for feedback, iterate. Treat interviewer like teammate
- Draw box diagrams with key components
- if possible, go through a few concrete use cases to help frame the high level design and discover edge cases

#### Step 3 - Design deep dive
_Time allocation: 10 to 25 minutes_
At this step, you and interviewer should have already achieved the following objectives:
- agreed on overall goals and feature scope
- sketched out high level design
- obtained feedback from interviewer on high level design
- had some initial ideas about areas to focus on in deep dive based

Sometimes the discussion could be on the system perforamcne characteristics, likely focusing on bottlenecks and resource estimations

#### Step 4 - Wrap up
_Time allocation: 3 to 5 minutes_
You may get a few follow-up questions or get the freedom to discuss other additional points. Some directions to follow:
- interviewer might want you to identify the system bottlenecks and discuss potential improvements
- could be useful to give recap of design
- error cases (server failure, network los, etc)
- operation issues such as monitoring metrics and error logs or how to roll out the system
- how to handle the next scale curve

Dos and Don'ts
Do's
- always ask for clarification
- understand the requirements of the problem
- There's no right or best answer
- Communicate and think aloud
- Suggest multiple approaches if possible
- Once you agree with interviewer on HLD, go into details on each component. Design the most critical components first
- Bounce ideas off the interviewer

Don'ts
- don't be unprepared for typical interview questions
- don't jump into a solution without clarifying the requirements and assumptions
- don't go into too much detail on a single component in the beginning
- don't hesitate to ask for hints if stuck
- don't think in silence

## Chapter 4 - Design a rate limiter
In a network system, a rate limiter is used to control the rate of traffic sent by a client or a service. 
In the HTTP world, a rate limiter limits the number of client requests allowed to be sent over a specified period

#### Benefits of Rate Limiter:
- prevent resource starvation caused by denial of service attack
- Reduce cost
- prevent servers from being overloaded

Questions to Ask interviewer
- what kind of rate limiter, client side or server side?
- what are the throttle rules? (by IP, user id, or other properties)
- will the system work in a distributed environment
- is it a separate service or should it be implemented in application code?
- do we need to inform the users who are throttled?

#### Requirements
- accurately limit excessive requests
- low latency response time
- use as little memory as possible
- distributed rate limiting. Can be shared across multiple servers or processes
- Show clear exceptions to users when their requests are throttled
- high fault tolerance; if there are problems with the rate limiter, it does not affect the entire system

#### Options for Rate Limiter
- client side rate limiting (unreliable place to enforce rate limiting because client requests can be forged by malicious actors. Also, we might not have control over the client implementation.)
- server side rate limiting
- middleware for rate limiting

Rate limiting is usually implemented in an API Gateway. API Gateway is a fully managed service that supports *rate limiting, SSL termination, authentication, IP whitelisting, servicing static content, etc.*

#### Algorithms for Rate limiting
- token bucket, leaking bucket, fixed window counter, sliding window log, sliding window counter

High level architecture
- Client (sends request to) --> rate limiter middleware --> (checks corresponding bucket in Redis) Redis
                                                        --> (limit is not reached, request goes through to) API Servers

Deep Dive
- HTTP response headers inform clients whether they're throttled
- Headers
  - X-ratelimit-remaining
  - X-ratelimit-limit
  - X-ratelimit-retry-after
- Return 429 HTTP code for _too many requests_

In a distributed environment, rate limiter encounter two challenges when scaling the system to support multiple servers and concurrent threads:
- race condition (to solve this, commonly used solutions are Lua script and sorted sets data structure)
- synchronization issue (use centralized data store, Redis to solve this)

Performance optimization options:
- multi data center setup. Automatically route traffic to the closest edge server to reduce latency
- synchronize data with an eventual consistency model


## Chapter 5 - Design Consistent Hasing
Consistent hasing is a commonly used technique to achieve horizontal scaling and distributing requests/data efficiently and evenly across servers

Consistent hasing is a special kind of hasing such that when a hash table is re-sized and consistent hasing is used, only k/n keys need to be remapped on average, where k is the number of keys, and n is the number of slots


