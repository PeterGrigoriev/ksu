# Flight Search Agents

This document describes the agents and APIs available for searching flights.

## Overview

This project uses various flight search APIs and MCP servers to find and compare flight options.

## Available Flight APIs

### Industry Status: Most Popular APIs for Developers (2025)

**Tier 1 - Enterprise/Production (Most Used Globally)**
- **Amadeus** 🏆 - Industry leader, dominant GDS, 400+ airlines
- **Sabre** - Major GDS, 350+ airlines, enterprise-focused
- **Travelport** - Third major GDS, multi-service (flights/hotels/cars)

**Tier 2 - Developer Favorites (Startups/Independent Developers)**
- **Skyscanner** ⭐ - Most popular for price comparison, 52 markets, 30 languages
- **Kiwi.com** - Unique multi-carrier virtual interlining, creative routing
- **Aviationstack** ⭐ - Most recommended for beginners, simple setup

**Note**: Google's QPX Express API was shut down in April 2018 and is no longer available.

---

### 1. Amadeus Flight Offers Search API ⭐ RECOMMENDED
- **Type**: REST API (GDS)
- **Rating**: 4.8/5
- **Free Tier**: Yes - 200 to 10,000 API calls/month (depends on endpoint)
- **Coverage**: 400+ airlines globally
- **Features**:
  - Flight Offers Search
  - Real-time pricing and availability
  - Booking capabilities
  - 200+ API collections (REST/SOAP)
- **Signup**: https://developers.amadeus.com
  1. Register and activate via email
  2. Create app in "My Self-Service Workspace"
  3. Get API Key + API Secret (auto-generated)
- **Pros**: Production-ready, official airline data, well-documented
- **Cons**: More complex than simple APIs, ticketing requires consolidators
- **Best For**: Serious projects with production intent

### 2. Kiwi.com (Tequila API) ⚠️ INVITATION ONLY
- **Type**: REST API
- **Rating**: 4.4/5
- **Access**: **Invitation-only since 2024** (was previously free)
- **Status**: New partnerships only for those "closely aligned with strategic goals"
- **Features** (if approved):
  - Locations API (cities, airports, stops)
  - Search API (one-way, return flights)
  - Multicity API
  - NOMAD API (n-cities in any order)
  - Booking & VISA APIs
  - Unique virtual interlining (multi-carrier bookings)
- **Signup**: Contact Kiwi.com partnerships team
- **Pros**: Unique flight combinations, free once approved
- **Cons**: Not publicly accessible, uncertain approval
- **Best For**: Strategic business partnerships only

### 3. Aviationstack ⭐ EASIEST TO START
- **Type**: REST API
- **Free Tier**: 500 requests/month (no credit card required)
- **Pricing**: $49.99-$499.99/month for more calls
- **Features**:
  - Real-time flight tracking
  - Historical flight data
  - Airport and airline information
- **Signup**: https://aviationstack.com
- **Pros**: Simple, no credit card, generous free tier
- **Cons**: More focused on tracking than booking/pricing
- **Best For**: Beginners, flight tracking apps, quick prototyping

### 4. Skyscanner API
- **Type**: REST API via RapidAPI
- **Free Tier**: 50 requests/minute
- **Coverage**: 52 markets, 30 languages
- **Features**:
  - Price comparison across providers
  - Real-time booking capabilities
  - Powerful search
- **Access**: Via RapidAPI platform
- **Pros**: Affordable, popular, good rate limits
- **Cons**: Requires RapidAPI account
- **Best For**: Price comparison platforms, travel aggregators

### 5. FlightAPI
- **Type**: REST API
- **Clients**: 8,000+
- **Pricing**: Starting at $49/month
- **Free Tier**: 20 free API calls
- **Features**:
  - Real-time flight status
  - Live pricing
  - Schedule data
  - One-way, round-trip, multi-city
- **Best For**: Comprehensive flight tracking and pricing

### 6. Travelpayouts/Aviasales API
- **Type**: REST API
- **Free Tier**: 200 queries/hour per IP
- **Features**: Real-time flight search, multi-city search
- **Best For**: High-volume searches

### 7. SerpApi Google Flights API
- **Type**: REST API (scrapes Google Flights)
- **Free Tier**: 100 searches/month
- **Features**: Access to Google Flights data
- **Signup**: https://serpapi.com/users/sign_up
- **Pros**: High-quality data from Google Flights
- **Cons**: Requires SerpApi subscription
- **Best For**: When you need Google Flights results specifically

### 8. FlightAware (AeroAPI)
- **Type**: REST API
- **Features**:
  - Real-time flight tracking
  - Flight history
  - Airport data
  - Advanced analytics
- **Best For**: Aviation apps, tracking services

## Agent Capabilities

### Flight Search Agent
- Search one-way flights
- Search round-trip flights
- Search multi-city itineraries
- Compare prices across multiple airlines
- Filter by departure time, duration, stops
- Track price changes

## Example Usage

### Search Round Trip: Berlin to London

```
Origin: BER (Berlin Brandenburg Airport)
Destination: LHR/LGW/STN/LTN (London airports)
Type: Round trip
```

### Common Airlines on this Route
- British Airways
- easyJet
- Ryanair
- Lufthansa
- Eurowings

## MCP Server Integration

### Available MCP Servers for Flights

Several MCP (Model Context Protocol) servers exist for flight search integration:

#### 1. mcp-flight-search (arjunprabhulal)
- **Repository**: https://github.com/arjunprabhulal/mcp-flight-search
- **Installation**: `pip install mcp-flight-search`
- **Requirements**: SerpAPI key (backend uses SerpApi)
- **Features**: Real-time flight search via MCP, one-way and round-trip
- **Usage**:
  ```bash
  export SERP_API_KEY="your-api-key-here"
  mcp-flight-search --connection_type http
  ```
- **Note**: Requires SerpApi subscription

#### 2. Amadeus MCP Server
- **Features**: Access Amadeus Flight Offers Search API
- **Data**: Airline info, times, duration, pricing
- **Best For**: Production-grade flight data

#### 3. Google Flights MCP
- **Features**: Travel agent-level flight plans
- **API**: Uses fast-flights API backend
- **Best For**: Google Flights data access

#### 4. VariFlight MCP Server
- **Features**: Flight info, weather, comfort metrics, lowest fares
- **Scope**: Civil aviation data

### Setup
Configure the MCP server in your Claude Code MCP settings to enable flight search tools. Once configured, flight search capabilities become available as native tools.

## Decision Matrix

| Use Case | Recommended API | Why |
|----------|----------------|-----|
| Learning/Testing | Aviationstack | No credit card, simple, 500 free calls |
| Production App | Amadeus | Industry standard, reliable, 400+ airlines |
| Price Comparison | Skyscanner | Popular, good coverage, affordable |
| Unique Routes | Kiwi.com | Multi-carrier combos (if you can get access) |
| Google Flights Data | SerpApi | Direct Google Flights scraping |
| MCP Integration | mcp-flight-search | Native Claude Code integration |

## Next Steps

### For This Project (Berlin to London Search)

1. **Choose API Provider**:
   - **Recommended**: Amadeus (best balance of features and accessibility)
   - **Alternative**: Aviationstack (easiest start, no credit card)

2. **Sign Up & Get Credentials**:
   - Amadeus: https://developers.amadeus.com
   - Aviationstack: https://aviationstack.com

3. **Implement Integration**:
   - Create API client script (Python or Node.js)
   - Implement authentication
   - Add flight search endpoint

4. **Search Berlin-London Flights**:
   - Origin: BER (Berlin Brandenburg)
   - Destination: LHR/LGW/STN/LTN (London airports)
   - Date range: Flexible round-trip

5. **Display & Track**:
   - Parse results
   - Show flight options with prices
   - Optional: Add price tracking/notifications
