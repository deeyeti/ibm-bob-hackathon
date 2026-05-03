# Shipping Routes Improvements

## Summary
Fixed shipping routes to follow realistic ocean paths and implemented proper storm avoidance routing that intelligently routes around storms instead of through them.

## Changes Made

### 1. New Helper Functions in `apps/frontend/src/data/shipping-routes.ts`

#### `calculateBearing(lat1, lng1, lat2, lng2)`
- Calculates the bearing (direction) from one point to another
- Returns bearing in degrees (0-360)
- Used for navigation calculations

#### `calculateDestination(lat, lng, bearing, distanceNm)`
- Calculates destination point given start point, bearing, and distance
- Essential for creating waypoints around obstacles
- Uses spherical geometry for accuracy

#### `generateGreatCircleRoute(lat1, lng1, lat2, lng2, numWaypoints)`
- Generates waypoints for a great circle route between two points
- Creates realistic ocean routes following the shortest path on a sphere
- Produces smooth, curved routes that avoid straight-line land crossings
- Default: 5 intermediate waypoints (configurable)

#### `generateStormAvoidanceRoute(originalRoute, stormLat, stormLng, stormRadiusNm, safetyMarginNm)`
- **KEY FEATURE**: Intelligently routes AROUND storm locations
- Analyzes each segment of the original route
- Detects if storm is within danger zone (radius + safety margin)
- Creates detour waypoints that go around the storm (not through it)
- Default storm radius: 300 nautical miles
- Default safety margin: 200 nautical miles
- Returns new route with storm avoidance waypoints

#### `calculateRouteDistance(waypoints)`
- Calculates total distance of a multi-waypoint route
- Sums distances between consecutive waypoints
- Returns total distance in nautical miles

### 2. Updated CommandCenter Component (`apps/frontend/src/components/CommandCenter.tsx`)

#### Storm Avoidance Route Generation
- **Before**: Simple offset waypoints that didn't intelligently avoid storms
- **After**: Uses `generateStormAvoidanceRoute()` to create routes that go AROUND storms
- Calculates actual distance of avoidance route
- Adjusts transit time based on actual distance increase

#### Great Circle Route Generation
- **Before**: Direct straight-line routes between ports
- **After**: Uses `generateGreatCircleRoute()` for realistic geodesic paths
- Creates 8 intermediate waypoints for smooth ocean curves
- Follows shortest path on sphere (great circle)

#### Route Options Display
- Primary route now marked as "Storm Warning" (red) when storm is active
- Alternative route uses intelligent storm avoidance (amber)
- Eco-optimized route uses great circle path (green)

### 3. Updated Predefined Routes

#### Trans-Pacific Routes
- **Shanghai to Los Angeles**: Now follows great circle arc through North Pacific
  - Added waypoints to avoid crossing Japan
  - Follows natural shipping lane curvature
  - 10 waypoints for smooth ocean path

- **Singapore to Long Beach**: Southern trans-Pacific route
  - Routes east of Philippines (avoiding land)
  - Follows great circle through Pacific
  - 11 waypoints for realistic curve

- **Hong Kong to New York via Panama**: 
  - Routes around Philippines and through open Pacific
  - Approaches Panama Canal from south
  - Continues through Caribbean to Atlantic
  - 18 waypoints for complete ocean route

#### Trans-Atlantic Routes
- **Rotterdam to New York**: Northern Atlantic route
  - Follows great circle through North Atlantic
  - Routes south of Ireland
  - 11 waypoints for realistic arc

- **Barcelona to Miami**: Southern Atlantic route
  - Passes through Strait of Gibraltar
  - Follows great circle across Atlantic
  - Approaches Caribbean from east
  - 12 waypoints for complete route

## Technical Details

### Geodesic Calculations
- All routes use spherical geometry (Haversine formula)
- Great circle routes follow shortest path on Earth's surface
- Waypoints calculated using spherical interpolation
- Accounts for Earth's curvature

### Storm Avoidance Algorithm
1. Analyzes each segment of original route
2. Calculates distance from storm to segment endpoints
3. If storm is within danger zone:
   - Calculates bearing from storm to route
   - Determines which side to route around
   - Creates 3 detour waypoints around storm
   - Maintains safe distance (radius + margin)
4. Returns modified route with detour waypoints

### Map Visualization
- Routes displayed using Leaflet Geodesic plugin
- Geodesic lines automatically curve on map
- Waypoints shown as markers
- Storm location shown as circle with radius
- Different colors for route types:
  - Red: Primary route (dangerous with storm)
  - Amber: Storm avoidance route
  - Green: Eco-optimized route

## Benefits

1. **Realistic Ocean Routes**: Routes now follow actual shipping lanes and great circle paths
2. **No Land Crossings**: Waypoints carefully placed to avoid landmasses
3. **Intelligent Storm Avoidance**: Routes go AROUND storms, not through them
4. **Accurate Distances**: Calculated using spherical geometry
5. **Smooth Visualization**: Geodesic curves display naturally on map
6. **Flexible Configuration**: Storm radius and safety margins are configurable

## Testing

- TypeScript compilation: ✅ Passed
- ESLint: ✅ Passed (only pre-existing warnings)
- Type checking: ✅ No errors
- All existing functionality: ✅ Preserved

## Usage Example

```typescript
// Generate great circle route
const waypoints = generateGreatCircleRoute(
  31.2304, 121.4737,  // Shanghai
  33.7405, -118.272,  // Los Angeles
  8  // 8 intermediate waypoints
);

// Generate storm avoidance route
const avoidanceRoute = generateStormAvoidanceRoute(
  originalRoute.waypoints,
  35.0, -170.0,  // Storm location
  300,  // Storm radius (nm)
  200   // Safety margin (nm)
);

// Calculate route distance
const distance = calculateRouteDistance(waypoints);
```

## Future Enhancements

- Add more predefined routes with realistic waypoints
- Implement multiple storm avoidance (route around multiple storms)
- Add weather-based route optimization
- Include ocean current considerations
- Add seasonal route variations

---

**Made with Bob - IBM Bob Hackathon 2026**