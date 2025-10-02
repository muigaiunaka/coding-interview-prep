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

