# System Design Interview Volume 2
## Framework
1. Ask clarifying questions for design scope
2. Functional Requirements
3. Non Functional Requirements
4. API Design
5. Data Model
6. High Level Design Diagram
7. Algorithms
8. Scale the Database
9. Caching
10. Region and Availbility Zones
11. Final Design Diagram

In distributed systems, utilize stateless services for horizontal scaling
In distributed systems, utilize database clusters with Primary and Backup database replications strategies for read heavy systems. Write to Primary, read from replicas. Accept eventual consistency.

## Chapter 1 - Proximity Service
- used to discover nearby places such as restaurants, hotels, theaters, museums, etc.

### Step 1 - Understand the problem and establish design scope
- Can a user specify search radius? If no results in radius does it auto epand search?
- max radius allowed?
- can a user change radius? Yes, various options range
- how does business information get added, deleted or updated?

### Functional Requirements
- return all businesses based on a user's location (long, lat) and radius
- Business owners can add, delete or update a business (not real time)
- Custoemrs can view detailed information about a business
### Non Functional requirements
- low latency for nearby business search
- data privacy for location info
- high availability and scalability to handle peak hour spukes and usage in densely populated areas

### Step 2 - Propose High Level Design and Get Buy IN
API Design
GET /v1/search/nearby with Request parameters of latitude, longitude, radius
Business APIs
GET /v1/businesses/:id 
POST /v1/businesses
PUT /v1/businesses/:id 
DELETE /v1/businesses/:id 

Read volume high for searching nearby businesses and viewing business information
Write volumes are lower, less often that a business is added, deleted, updated

relational database good for a read-heavy system

High Level Design
                     /--> /buinesses/{:id} --> Business Service --> Write to Primary Datbase in Database Cluster
User --> Load Balancer
                     \--> /search/nearby --> Location Based Service --> Read from Database cluster replicas

Different types of geospatial indexes: Even Hash (grid, geohash, cartesian tiers) or Tree (Quadtree, Google S2, RTree)
high level idea is to divide the map into smaller areas and build indexes for fast search

For interviews, use geohash or quadtree 

### Step 3 Design Deep Dive
Focus on:
- Scale the database
- Caching
- Region and availability zones
- filter results by time or business type

Filter results by time or business type
- how to filter by open now or return only restaurants? Ok to Use business ID and hydrate business objects then filter by business type or opening time

Region and availability zones
- Deploy location based swervice to different regions and availability zones to improve availability, to make users physically closer to the servers and to comply better with local privacy laws

Final Design
                     /--> /buinesses/{:id} --> Business Service --> Write to Primary Datbase in Database Cluster
User --> Load Balancer                                           \___________/V (Business Service reads from redis cluster)
                     \--> /search/nearby --> Location Based Service <--> Redis Cluster with Business Info and Geohash that syncs from Database Replica

## Chapter 2 Nearby Friends
for an opt-in user who grants permissions to access their location, the mobile client presents a list of friends who are geographically nearby

Functional Requirements
- users can see nearby friends on mobile apps. Each entry in nearby friends list has a distance a timestamp indicating when the distance was last updated
- nearby friends list should be updated every few seconds

Non-functional requirements
- low latency. Receive location updates from friends without too much delay
- reliability but occasional data point loss is acceptable
- eventual consistency for location data. A few seconds delay in receiving location data in different replicas is acceptable
- scale for 100 million DAU

High Level Design
To satisfy functional requirements:
                                                         --> User Database (user profile, friendship)
       --> http -->                      --> API Servers (cluster of stateless servers for user management, friendship management request response traffic)
Mobile                     Load Balancer
      <--> Web Socket -->                --> WebSocket Servers (bi-directional location info) --> Location History DB
                                                                                              --> Cache (Location cache for storing most recent location data for active user)
                                                                                              Redis Pub/Sub (Message bus)

API Design
Web Socket (user send and receive location updates through the WebSocket protocol
- Periodic location update API
- Client receives locaiton updates
- Websocket initilization
- Subscribe to a new friend
- Unsubscribe to a friend
HTTP
- API servers handle tasks like adding/removing friends, updating user profiles

Data Model
Location cache
- key: user_id , value: {latitude, longitude, timestamp}

Shard data by user id for relational database scaling

Note to self: Web Socket servers are stateful so must allowe existing connections to drain when removing existing nodes


!!!!!!!!!!!!!
SKIPPED AHEAD TO CHAPTER 4, REVISIT AND FINISH NOTES IF EVER NECESSARY
!!!!!!!!!!!!!

## Chapter 4 Distributed Message Queue
Message queue benefits are decoupling, improved scalability, increased availability, better performance (async communication)

### Step 1 - Understand the problem and establish design scope
producers send message to a queue and consumers consume messages from it.

- What's the format and average size of messages? Is it text only or multimedia? Text only. Messages are generally KBs
- Can messages be repeatedly consumed? Yes for this design (not normally in traditional mesage queues)
- are messages consumed in the same order they were produced? Yes , FIFO (not normally a feature in traditional distributed message queue)
- Does data need to be persisted and what's the data retention policy? Yes, two weeks
- How many producers and consumers are we going to support? As much as possible
- Data semantics to support? at-most-once, at-least once, exactly once? Definitely at-least-once. Support all and make configurable
- What's the target throughput and end to end latency? High throughput for log aggregation for example. Low latency delivery for traditional message queue use cases

#### Functional Requirements
- Producers send messages to a message queue
- Consumers consume messages from a message queue
- Messages can be consumed repeatedly or only once
- Historical data can be truncated
- message size is in the kilobyte range
- deliver messages to consumers in the order they were added to the queue
- data delivery semantics are configurable

#### Non functional requirements
- high throughput or low latency, configurable
- scalable. Can support sudden surge in message volume
- persistent and durable. Data should be persisted on disk and replicated across multiple nodes

### Step 2 High Level Design

Note to self: Topic - cateogies used to organize messages. Each has a name that is unique across message queue service. Messages are sent to and read from a specific topic.

Messaging Models
- point-to-point - message is sent to a queue and consumed by one and only one consumer
- Publish-subscribe model

Topics, partitions, brokers
- partition - a small subset of messages for a topic
- brokers - servers that hold partitions
- offset - the position os a message in the partition
- consumer group - a set of consumers working together to consume messages from topics . (e.g. one consumer group for billing and the other for accounting)

High Level Design

        Metadata storage       Coordination Service
                ^            __ ^
                |            /
                v           /
          ________________
          | Brokers      |
Producers | Data storage |  --> Consumers (consumer groups)
          |--------------|
          | State storage|

Producers push messages to specific topics
Consumer group subscribes to topics and consumes messages
Core Service and Storage
- Broker holds multiple partitions
- Storage
  - Messages are persisted in data storage in partitions
  - consumer states are managed by state storage
  - config and properties of topics are persisted in metadata storage
- coordination service
  - ...

### Step 3 Design Deep Dive
- have a design that encourages batching
- NOTE TO SELF: BATCHING GOOD FOR HIGH THROUGHPUT
- 
Data Storage
- can use Write ahead log (WAL) which is a plain file where new entries are appended to an append-only log. Persist messages as WAL log files on disk. Better tradeoffs than using database since traditional DBs (NoSQL, Relational DB) are not ideal for handling BOTH write-heavy and read heavy access patterns at a large scale.

Message Data Structure
key byte[]
value  byte[]
topic string
partition integer
offset long
timestamp long
size  integer
crc  integer

consumer flow
- push vs pull
  - push model
    - Pros: low latency, broker can push messages to consumer immediately
    - Cons: consumers could get owerwhelmed
  - pull model
    - pros: consumers control cnosumptin rate. Also, more suitable for batch processing
Most message queues, choose pull model.

ZooKeeper - essential service for distributed systems, offering a hierarchical key-value store. Used toprovide a distributed configuration service, synchronization service, and naming registry.
Use ZooKeeper for storing metadata

Replication is classic solution to achieve high availability

Scalability
- Producers can scale by adding or removing producer instances
- consumers groups, it's easy to add or remove a consumer group AND can have a rebalancing mechanism in the consumer group to handle caes if it crashes or consumer gets added/removed
- broker

- Data Delivery Semantics
- at-most-once: a message will be delivered not more than once. Messages may be lost but are not redelivered
- at-least-once: a message can be delivered more than once, no message should be lost (ok when data-duplication is not an issue)
- exactly once: a message can be sent only once. Important when duplication is not acceptable and downstream service or third party doesn't support idempotency (repeated operations yield the same outcome)

Read: Ch.4 Distributed Message Queue, Ch.5 Metrics Monitoring, Ch.9 S3-like Object Storage, Ch.11 Payment System, Ch.12 Digital Wallet.
