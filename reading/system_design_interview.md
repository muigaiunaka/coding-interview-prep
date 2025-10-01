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

## Chapter 6 design a key galue store

#### design scope
- size of key value pair is below 10kb
- able to store big data
- high availability
- high scalability to support large data sets
- auto scale (addition/deletion of server is automatic)
- tunable consistency
- low latency

CAP Theorem
consistency means all clients see the same data at the same time no matter which node they connect to
availability means any client that requests data gets a response even if some nodes are down
partition tolerance indicates a communication break between two nodes. system continues to operate despite network partitions

A over C means system keeps accepting reads even if it may return stale data
C over A means system must block all write ops to avoid inconsistency 

Data Partition
two challenges:
distribute data across multiple servers evenly
minimize data movement when nodes are addedor removed

great technique to solve is consistent hashing

data replicas
for better reliability, replicas are places in distinct data centers and data centers are connected through high speed networks

consistency
consistency models
strong consistency means any read operation returns a value corresponding to the result of the most updated write data item. client never sees out of date data
weak consistency means subsequent read operations may not see the most updated value
eventusl consistency means given enough time, all updates are made and all replicas are consisteng

gossip protocol
decentralized failure detection method whicg has nodes with id and heartbeat counters, if heartbeat not increased for a node, consider it offline

## chapter 7 design a unique id generator in distributed systems
twitter snowflake - scalable in a distributed environment
uuid
multi master replica
ticket server

## chapter 8 design a url shortenere

clarifying questions
- can you give an example of how this works?
- what is traffic volume?
- length of output?
- char restrictions?
- can urls be deleted / updated?

requirements
- shorten url
- redirect to long url
- high availability, scalability, fault tolerance

API - REST
POST api/v1/data/shorten
takes in longUrl
returns shortURL

GET api/v1/shortUrl
return long url for http redirection, 301 redirect code

301 permanent redirect better for reduced server loads
302 temporary, better for analytics

deep dives
data model 
hash function
url shortening
url redirecting

detail data flow and conditions for API responses

## chapter 9 design a web crawler

used by search engines to discover new or updayed content on the web

used for:
- search engine indexing
- web archiving
- web mining
- web monitoring

clarify:
what is the purpose of the crawler? any of the used for above?
how many pages does it collect per month?
what content type is included? http only or pdf and more
need to store html pages?
how do we handle oages with duicate content?

requirements
scalability for handling billions of pages in parallel
robust in handling bad html, unresponsive pages, crashes, bad links
do not overload other pages with requests
extensible to handle other types with minimal changes

HLD 
seed urls -> url frontier -> HTML downloader DNS resolver , content parser  -> Content Seen?
either check Comtent DB or link extractor to url filter to url seen? to url storage or back to url frontier

## Chapter 10 - Design A notification System
3 types: mobile push notifications, SMS message, and Email

### Understand the problem and Establish design scope
#### Clarifying question to gather functional and non functional requirements
Me: What types of notifications does the system support?
Interviewer: Push notification, SMS message and email

Me: Is it a real time system?
Interviewer: want user to receive notification as soon as possible. slight delay is acceptable if system under high workload

Me: What are supported devices?
Interviewer: iOS devices, android devices, laptop/desktop

Me: What triggers notifications?
Interviewer: triggered by client apps. Also can be server-side scheduled

Me: can users opt out?
Interviewer: yes

Me: how many notifications are sent out each day?
Interviewer: 10 million mobile push notifications, 1 million SMS messages, and 5 million emails

### High Level Design

Each has a Provider -> 3P Service (Apple Push Notifications Service (APNS) or Firebase Cloud Messaging (Android) or SMS Service like Twilio or Email Service like Sendgrid) -> Client Device 

Initial Design would be something like:

Service 1 to N --> Notification System --> 3P Services --> Client Device (iOS/Android/SMS/Email)

- A service can be a micro-service, cron job or distributed system that triggers notifcation sending events

Problems identified with above initial design (during an interview, convey these scaling concerns or how a design falls short then try to address if possible):
- single point of failure
- hard to scale
- performance bottlenecks due to processing and sending notifications potentially being resource intensive.

Updated Design:
Service 1 to N --> Notification Servers --> IOS/Android Push Notification --> Workers --> APNS/FCM --> iOS/Android
                          |             --> SMS/Email Queue --> Workers --> Workers --> Twilio/SendGrid --> SMS/Email
                          v
                        Cache
                          |
                          v
                       Database

- Cache user info, device info, notification templates
- DB stores user, notification and settings data
- Message queues remove dependencies between components
- Workers are servers that pull notification events from message queues and send them to corresponding third party service

### Deep Dive
Explore reliability, additional component and considerations, updated design

- Notifications need to prevent data loss; fine if delayed or re-ordered but never can be lost. To mitigate this, store data in DB and use retry mechanism
- can introduce de-dupe logic by checking if event id has been seen, if so, discard it, if not, send notification
- check if a user is opted-in to receive a given notification type before sending
- introduce monitoring of queued notifications to see if bottlenecks or slow processing is occurring and if more workers are needed (horizontal scale workers)

During the interview, can update the design to reflect any of this additional deep dive solutions

Final Design adds authentication/rate limiting at the notification servers level, analytics services connected to the client device, workers and notification servers, and notification log DB with notification template connected to workers

## Chapter 11 - Design a News Feed System
### Step 1 Understand the problem and Establish Design Scope
#### Clarifying Questions to gather Functional and Non Functional Requirements
Me: is this a mobile app, web app or both?
Interviewer: Both

Me: what are the important features?
Interviewer: a user can publish a post and see her friend's post on the news feed page

Me: is the news feed sorted by reverse chronological order or any particular order such as rank/scores? E.g. close friend posts have higher scores
Interviewer: To keep things simple, let's assume the feed is sorted reverse chronological order (most recent at top)

Me: how many friends can a user have?
Interviewer: 5000

Me: what is the traffic volume?
Interviewer: 10 Million DAU

Me: can feed contain images, videos or just text?
Interviewer: it can contain media files, including both images and videos

### Step 2 - Propose High Level Design and get buy-in then iterate
Initial design has two parts: feed publishing and news feed building

Need Feed Publishing API to publish a post
POST /v1/me/feed
Params:
- content: content is the text of the post
- auth_token: used to authenticate API requests

Newsfeed retrieval API
GET /v1/me/feed
Params:
- auth_token: used to authenticate API requests

Initial Design
DNS <--- User on Web Browser or Mobile App
                        |
                        |
                        v
                  Load Balancer
                        |
                        |
                        v
                   Web servers
                        |
                        |
                        v
                News Feed Service
                        |
                        |
                        v
                 News Feed Cache
### Step 3 Deep Dive
Deep dive introduces Post service -> Post Cache -> Post DB being called by web servers. Also introduce rate limiting and authentication at the Web Server level similar to like what an API Gateway would do.

Web servers also now connect to a Notification Service. Also connects to a Fanout Service which will (1) get friend ids from a Graph DB, (2) get friends data from a user cache -> User DB and (3) connnect to message queues -> Fanout workers --> News Feed Cache

*Fanout* is the process of delivering a post to all friends. Two Models:
- fanout on write (push model)
- fanout on read (pull model)

Graph Databases great for managing relationship data or recommendations (followers/friends and follower/friend recs)

Newsfeed retrieval deep dive
- introduces CDN for for fast retrieval
- broken down cache architecture fors news feed, content, social graph (followers/following), action (liked, replied, etc) and counters (like counters, reply counters, etc)

Other Potential Paths to follow if time allows:
- scaling (horizontal vs vertical)
- read replicas
- Leader-follower data replication
- consistency odels
- database sharding
- keep stateless
- support multiple data centers
- monitor key metrics

## Ch. 12 - Design a Chat System
### Step 1 - Understand the problem and establish design scope
- Different types of chat apps
- one on one (messenger, we chat, whatsapp)
- office group chat (Slack)
- game chat with large group and low voice latency (Discord)

Requirement Gathering Questions
- What type of chat app shall we design? 1 on 1 or group based? A: Both 1 on 1 and group chat
- Is it a mobile app, web app or both? A: Boht
- What is the scale? A: 50 million DAU
- For group chat what is the group member limit? A: 100 people
- What features are important for the chat app? Can it support attachment? A: 1 on 1 chat, group chat, online indicator. Only supports text messages
- Is there a message size limit? A: Yes, max 100,000 characters long
- Is end to end encryption required? A: Not for now but maybe if time allows we can discuss
- How long should we store the chat history? A: Forever

### Requirements
- one on one chat with low delivery latency
- small group chat (max 100 people)
- online presence indicator
- multiple device support. The same account can be logged in to multiple accounts at the same time
- push notifications
- supports 50 million DAU for scale

### Step 2 - Propose high level design and get buy in
(Mobile/Web) Client -----(message)-----> Chat Service (stores message and relays message) -----(message)-----> (Mobile/Web) Receiver Device

Options for protocol or technique for sending and receiving message may be different.
Server (Chat Service) sending through HTTP connection might be fine in some cases

- Polling: client periodically asks the server if there are messages available.
 - Tradeoffs: could be costly by consuming server resources to answer a question that offers no as an answer most of the time
- Long polling: client holds the connection open until there are actually new messages available or a timeout threshold has been reached.
 - Tradeoffs:
  * Sender and receiver may not connect to the same chat server
  * Server has no good way to tell if a client is disconnected
  * inefficient if a user does not chat much
- Web Socket: initiated by client, bi-directional and persistent. Most common solution for sending async updates from server to client.

Sender <----- WebSocket -----> 
                                 Chat Service
Receiver <----- WebSocket ----->

Stateless Services: traditional public facing request/response serviecs used to manage login, signup, user profile, etc
Stateful service: each client maintains a persistent network connection (e.g. to a chat server)

Adjusted HLD
User (Web/Mobile) connects to Load balancer through HTTP connection
User (Web/Mobile) connects to Real Time Services (Chat Servers, Online Indicator Presence Servers) through WebSockets connection
LB and Real Time Services connect one way and bi-directionally to API Servers (for login, suignup, change profile, etc)
API Servers connect one way to Notification Servers (for push notifications)
API Servers, Notification Servers, Real Time Services connect to Key Value Store DBs (for chat history soring)

Tip: examine data types and read/write patterns to land on database solution

Message Data Model: message_id (bigint), message_from, message_to, content (text), created_at (timestamp)
Group Chat message data model: channel_id (bigint) message_id, user_id, content (text), created_at (timestamp)

### Step 3 Design Deep Dive
Worth deeper exploration: service discovery, messaging flows, online/offline indicators

Service Discovery recommends the best chat server for a client based on criteria like geographical location, server capacity, etc. Apache Zookeeper is a popular open source solution.

Message flow: user A sends chat message, chat server gets message id and sends message to message sync queue, message is stored in key-value store, if user B online it's forwarded to chat server 2 where user B is connected and if offline a push notification is sent from Push notification servers, chat server 2 sends the message to user B

Online Presence Indicator: can be triggered by user login, user log out, user disconnection. Publish subscribe model works fine for publishing event to channel for each combination of user but it gets expensive for large chats. To solve large group bottleneck, can fetch online status only when a user enters a group or manually refreshes the friend list

### Step 4 Wrap Up
If there's extra time can explore:
- extending chat app to support media files other than text. Calls for compression, cloud storage and thumbnails.
- End to end encryption [faq.wahtsapp.com/en/androd/28030015]
- caching messages on the client side to reduce data transfer between client and server
- how to improve load time
- error handling. Retry mechanisms or queueing for failed message resend


## Chapter 13 - Design a search autocomplete system or Design Top K most searched queries
Other names: search as you type, typeahead, autocomplete, incremental search

### Step 1 - Understanding the problem and establish design scope
#### Questions for Requirements
- Ask about where matching is supported in search query (beginning or middle too)
- how amny autocomplete suggestions should be returned by the system?
- How does the system know which suggestions to return? By popularity? By historical query frequency?
- Should we include spell check? Autocorrect?
- What language are search queries in? Discuss multi-language during deep dive but low priority
- how many users use the product?

#### Requirements Focus
- Response time within 100 ms
- Relevant to the search term
- Results are sorted by poularity
- Scalable to handle 10 MM DAU
- highly available (chose availability over consistency meaning some customers will get different ordering of suggestions for example due to delayed read popularity)

### Step 2 - High Level Design
At a high level, the system contains:
1. Data gathering service - gathers user input queries and aggregates them in real time
2. Query service - returns 5 most frquently searched items

simplified approach is a key value store of query to frequency but this is ineffcient for large data sets.

### Step 3 - Deep dive
Utilize a Trie data structure for a more optimal approach. Root is empty, each node is word or prefix, leaf (end of tree paths) is a full word.
Designing algorithm for Trie interaction is out of scope of system design interview but optimizations like below are in scope:
- limit the max length of a prefix
- cache top search queries at each node: store top k most frequently used queries at each node (e.g. b node in trie would have 5 queries mapped to it, "be" prefix same thing, ber prefix

Real time is hard to scale. Trie being rebuilt weekly or monthly from analytics logs or a logging services is a better way that scales

Utilize *Workers* to perform async jobs at regular intervals. User workers to rebuild trie and store in Trie DB

Utilize a Trie Cache to keep trie in memory for fast read and take weekly snapshot of Trie DB

Trie DB can be either document store or key-value store (each prefix is mapped to a K/Value store of prefix to list of most frequent results). 

##### Query Service
Client (Mobile/Web) --> Load Balancer --> API Servers --> Trie Cache --> Trie DB

- for faster response turn time use AJAX and browser caching on top of the query service design

Scaling Storage
- Naive solution: shard data based on the first charcter. Results in splitting search queries up to 26 servers. can go further to shard by two leter prefix or range (e.g. aa-ag) but this will result in uneven distribution
- Optimize: analyze historical data distribution pattern and apply smarter sharding logic with a Shard Map Manager that maintains a lookup DB for identifying where rows should be stored

### Follow Up
How to handle multi languages?
- store using unicode characters instead of alphabetic characters
What if top search queries in one country are different from others?
- might built different Tries for different countries. Store tries in CDNs to improve response time
How can we support trending (real-time) search queries?
- hard to fully say but the current design does not work becauses of the weekly update worker cadence and it takes a long time to build out a trie
- some ways to consider:
  - change ranking model (more weight to recent search queries)
  - stream instead of batch data input. Calls for Apache Hadoop/MapReduce/Spark Streaming/Storm/Kafka etc domain knowledge 


## Chapter 14 Design Youtube
Requirement Gathering
- what features are important? users can upload a video and watch a video
- mobile, web and tv clients
- 5 MM DAU
- Do we need to support international users? Yes
- video resolutions? all
- file size requirements for videos?

### Requirements
- Ability to upload videos fast
- Users can change video quality
- High availability, scalability and reliability requirements

CDN costs would be too high to serve all videos from a CDN

### High Level Design
Leverage cloud blob storage and cloud CDN like S3 and CloudFront

Client (Mobile, Phone, TV) --> (Stream video from) CDN
                           --> (feed recommendation, generating video upload URL, updating metadata DB and cache, user signup) --> API Servers

Note to self: when you see the API servers box in high-level component drawings, read it as the backend app/service layer that implements the system’s public APIs and coordinates everything else.

##### Video Uploading HLD
Client <-- Load Balancer <-- API Servers --> Metadata Cache <--\
  |                                      --> Metadata DB <-- Completion Handler  <--
  |                                                                                 |
  v                                                                                 |
Blob Storage --> Transcoding Servers --> (transcoding complete) Completion Queue -- |
                                     --> Blob Storage (holds transcoded data) --> CDN

Full flow for video upload then Client to Metadata for the metadata updates

Optimizations:
- Parallelization
- Only store popular videos or more frequently accessed videos in CDN
- Retry mechanism for error handling and return proper error code to client for non-recoverable system failures

## Chapter 15 Design Google Drive
File storage and synchronization service that helps store documents, photos, videos and other files in the cloud

What are the most important features?
- Upload and download files, file sync, notifications
What are the support files formats?
- any file type
Is there a file size limit?
- 10GB or smaller
How many users?
- 10 MM DAU

#### Requirements
- User can add files
- User can download files
- The system syncs files across multiple devices
- User can see file revisions
- User can share files with other users or non-users
- The system sends a notification when a file is edited, deleted or shared with the user
Out of scope: Document editing and collaboration

#### Non-Functional Requirements
- Reliability. Data loss is unacceptable
- Fast sync speed
- Scalable to handle high volumes of traffic
- Highly available and system is still useable when servers are offline, slowed down or have unexpected network errors

strong consistency for file sync since one client cannot see a different thing than another. Strong consistency for metadata cache and database layers

Choose relational database because ACID (Atomicity, Consistency, Isolation and Durability) are natively supported

Define ACID
- Atomicity -
- Consistency -
- Isolation -
- Durability -

- 
