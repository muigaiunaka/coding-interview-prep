# System Design Interview Volume 2
## Framework
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

#### Step 2 - Propose High Level Design and Get Buy IN
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
