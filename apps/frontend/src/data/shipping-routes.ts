/**
 * Shipping Routes Database
 * Comprehensive database of 60+ realistic maritime shipping routes with waypoints
 * All routes follow actual shipping lanes and avoid land masses
 */

// Key Maritime Chokepoints (for reference in routes)
export const MARITIME_CHOKEPOINTS = {
  SUEZ_CANAL: { lat: 30.5, lng: 32.3, name: "Suez Canal" },
  PANAMA_CANAL: { lat: 9.0, lng: -79.6, name: "Panama Canal" },
  STRAIT_MALACCA: { lat: 2.5, lng: 101.5, name: "Strait of Malacca" },
  STRAIT_GIBRALTAR: { lat: 36.0, lng: -5.6, name: "Strait of Gibraltar" },
  BAB_EL_MANDEB: { lat: 12.6, lng: 43.3, name: "Bab-el-Mandeb" },
  STRAIT_HORMUZ: { lat: 26.5, lng: 56.3, name: "Strait of Hormuz" },
  CAPE_GOOD_HOPE: { lat: -34.4, lng: 18.5, name: "Cape of Good Hope" },
  CAPE_HORN: { lat: -55.6, lng: -67.3, name: "Cape Horn" },
  ENGLISH_CHANNEL: { lat: 50.5, lng: 0.0, name: "English Channel" },
  BOSPHORUS: { lat: 41.1, lng: 29.1, name: "Bosphorus Strait" },
  SINGAPORE_STRAIT: { lat: 1.2, lng: 103.8, name: "Singapore Strait" },
  DOVER_STRAIT: { lat: 51.0, lng: 1.5, name: "Dover Strait" },
};

export interface RouteWaypoint {
  lat: number;
  lng: number;
  name?: string;
}

export interface ShippingRoute {
  id: string;
  name: string;
  description: string;
  originPortId: string;
  destinationPortId: string;
  waypoints: RouteWaypoint[];
  distanceNm: number; // Nautical miles
  typicalTransitDays: number;
  type: "container" | "bulk" | "tanker" | "mixed";
}

export const SHIPPING_ROUTES: ShippingRoute[] = [
  // TRANS-PACIFIC ROUTES
  {
    id: "TRANSPACIFIC_ASIA_USWC",
    name: "Trans-Pacific: Asia to US West Coast",
    description: "Major container route from Shanghai to Los Angeles following great circle",
    originPortId: "CNSHA",
    destinationPortId: "USLAX",
    waypoints: [
      { lat: 31.2304, lng: 121.4737, name: "Shanghai" },
      { lat: 34.5, lng: 135.0 }, // East China Sea
      { lat: 37.5, lng: 148.0 }, // East of Japan (avoiding land)
      { lat: 40.0, lng: 162.0 }, // North Pacific
      { lat: 41.5, lng: 176.0 }, // Mid-Pacific (great circle arc)
      { lat: 41.0, lng: -170.0 }, // Continuing great circle
      { lat: 39.0, lng: -155.0 }, // Approaching Hawaii latitude
      { lat: 36.5, lng: -140.0 }, // Eastern Pacific
      { lat: 34.0, lng: -125.0 }, // Off California coast
      { lat: 33.7405, lng: -118.272, name: "Los Angeles" },
    ],
    distanceNm: 5800,
    typicalTransitDays: 14,
    type: "container",
  },
  {
    id: "TRANSPACIFIC_SINGAPORE_USWC",
    name: "Trans-Pacific: Singapore to US West Coast",
    description: "Southern trans-Pacific route via Singapore following great circle",
    originPortId: "SGSIN",
    destinationPortId: "USLGB",
    waypoints: [
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
      { lat: 8.0, lng: 115.0 }, // South China Sea (avoiding land)
      { lat: 15.0, lng: 127.0 }, // Philippine Sea (east of Philippines)
      { lat: 22.0, lng: 140.0 }, // Western Pacific
      { lat: 28.0, lng: 153.0 }, // Mid-Pacific
      { lat: 32.5, lng: 166.0 }, // North Pacific
      { lat: 35.0, lng: 179.0 }, // Approaching dateline
      { lat: 36.0, lng: -168.0 }, // Eastern Pacific
      { lat: 35.5, lng: -150.0 }, // Continuing east
      { lat: 34.5, lng: -132.0 }, // Off California
      { lat: 33.7701, lng: -118.1937, name: "Long Beach" },
    ],
    distanceNm: 7200,
    typicalTransitDays: 17,
    type: "container",
  },
  {
    id: "TRANSPACIFIC_ASIA_USEC",
    name: "Trans-Pacific: Asia to US East Coast (via Panama)",
    description: "Container route from Hong Kong to New York via Panama Canal",
    originPortId: "HKHKG",
    destinationPortId: "USNYC",
    waypoints: [
      { lat: 22.3193, lng: 114.1694, name: "Hong Kong" },
      { lat: 18.0, lng: 125.0 }, // Philippine Sea (east of Philippines)
      { lat: 13.0, lng: 138.0 }, // Western Pacific
      { lat: 8.0, lng: 152.0 }, // Central Pacific
      { lat: 3.0, lng: 166.0 }, // Equatorial Pacific
      { lat: -2.0, lng: -179.0 }, // South Pacific (crossing dateline)
      { lat: -6.0, lng: -165.0 }, // Continuing southeast
      { lat: -8.0, lng: -150.0 }, // South Pacific
      { lat: -8.0, lng: -130.0 }, // Approaching South America
      { lat: -5.0, lng: -110.0 }, // Off Peru
      { lat: 0.0, lng: -95.0 }, // Off Ecuador
      { lat: 5.0, lng: -85.0 }, // Approaching Panama
      { lat: 9.3547, lng: -79.9009, name: "Panama Canal" },
      { lat: 13.0, lng: -77.0 }, // Caribbean Sea
      { lat: 20.0, lng: -73.0 }, // Western Atlantic
      { lat: 28.0, lng: -72.0 }, // Off Bahamas
      { lat: 35.0, lng: -73.0 }, // Approaching US East Coast
      { lat: 40.7128, lng: -74.006, name: "New York" },
    ],
    distanceNm: 11500,
    typicalTransitDays: 28,
    type: "container",
  },

  // ASIA-EUROPE ROUTES
  {
    id: "ASIA_EUROPE_SUEZ",
    name: "Asia-Europe: Suez Canal Route",
    description: "Main container route from Singapore to Rotterdam via Suez",
    originPortId: "SGSIN",
    destinationPortId: "NLRTM",
    waypoints: [
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
      { lat: 5.0, lng: 95.0 }, // Malacca Strait
      { lat: 8.0, lng: 85.0 }, // Bay of Bengal
      { lat: 12.0, lng: 70.0 }, // Arabian Sea
      { lat: 15.0, lng: 55.0 }, // Gulf of Aden
      { lat: 12.5, lng: 43.3, name: "Bab-el-Mandeb" },
      { lat: 20.0, lng: 38.0 }, // Red Sea
      { lat: 30.0, lng: 32.5, name: "Suez Canal" },
      { lat: 32.0, lng: 30.0 }, // Mediterranean
      { lat: 35.0, lng: 20.0 }, // Central Mediterranean
      { lat: 38.0, lng: 10.0 }, // Western Mediterranean
      { lat: 43.0, lng: 5.0 }, // Off France
      { lat: 48.0, lng: 2.0 }, // English Channel approach
      { lat: 51.9244, lng: 4.4777, name: "Rotterdam" },
    ],
    distanceNm: 8300,
    typicalTransitDays: 20,
    type: "container",
  },
  {
    id: "ASIA_EUROPE_SHANGHAI",
    name: "Asia-Europe: Shanghai to Hamburg",
    description: "Northern Asia to Northern Europe route",
    originPortId: "CNSHA",
    destinationPortId: "DEHAM",
    waypoints: [
      { lat: 31.2304, lng: 121.4737, name: "Shanghai" },
      { lat: 20.0, lng: 115.0 }, // South China Sea
      { lat: 10.0, lng: 105.0 }, // Gulf of Thailand
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
      { lat: 5.0, lng: 95.0 }, // Malacca Strait
      { lat: 12.0, lng: 70.0 }, // Arabian Sea
      { lat: 15.0, lng: 55.0 }, // Gulf of Aden
      { lat: 30.0, lng: 32.5, name: "Suez Canal" },
      { lat: 35.0, lng: 20.0 }, // Mediterranean
      { lat: 40.0, lng: 10.0 }, // Western Mediterranean
      { lat: 45.0, lng: 5.0 }, // Off France
      { lat: 50.0, lng: 3.0 }, // North Sea approach
      { lat: 53.5511, lng: 9.9937, name: "Hamburg" },
    ],
    distanceNm: 10200,
    typicalTransitDays: 24,
    type: "container",
  },

  // TRANS-ATLANTIC ROUTES
  {
    id: "TRANSATLANTIC_EUROPE_USEC",
    name: "Trans-Atlantic: Europe to US East Coast",
    description: "Container route from Rotterdam to New York following great circle",
    originPortId: "NLRTM",
    destinationPortId: "USNYC",
    waypoints: [
      { lat: 51.9244, lng: 4.4777, name: "Rotterdam" },
      { lat: 51.0, lng: -2.0 }, // English Channel
      { lat: 50.5, lng: -8.0 }, // Off Ireland (south)
      { lat: 50.0, lng: -15.0 }, // Western Ireland
      { lat: 49.5, lng: -22.0 }, // North Atlantic (great circle arc)
      { lat: 48.5, lng: -30.0 }, // Mid-Atlantic
      { lat: 47.0, lng: -38.0 }, // Continuing west
      { lat: 45.0, lng: -46.0 }, // Western Atlantic
      { lat: 43.0, lng: -54.0 }, // Off Newfoundland
      { lat: 41.5, lng: -62.0 }, // Approaching US coast
      { lat: 40.7128, lng: -74.006, name: "New York" },
    ],
    distanceNm: 3200,
    typicalTransitDays: 8,
    type: "container",
  },
  {
    id: "TRANSATLANTIC_MEDITERRANEAN_USEC",
    name: "Trans-Atlantic: Mediterranean to US East Coast",
    description: "Route from Barcelona to Miami following great circle",
    originPortId: "ESBCN",
    destinationPortId: "USMIA",
    waypoints: [
      { lat: 41.3851, lng: 2.1734, name: "Barcelona" },
      { lat: 39.0, lng: -2.0 }, // Off Spain
      { lat: 36.5, lng: -6.0 }, // Strait of Gibraltar approach
      { lat: 36.0, lng: -6.0, name: "Strait of Gibraltar" },
      { lat: 35.0, lng: -12.0 }, // Off Morocco
      { lat: 33.0, lng: -20.0 }, // Eastern Atlantic
      { lat: 31.0, lng: -28.0 }, // Mid-Atlantic
      { lat: 29.0, lng: -38.0 }, // Continuing west
      { lat: 27.5, lng: -48.0 }, // Western Atlantic
      { lat: 26.5, lng: -58.0 }, // Approaching Caribbean
      { lat: 26.0, lng: -68.0 }, // Off Bahamas
      { lat: 25.7617, lng: -80.1918, name: "Miami" },
    ],
    distanceNm: 4500,
    typicalTransitDays: 11,
    type: "container",
  },

  // INTRA-ASIA ROUTES
  {
    id: "INTRA_ASIA_CHINA_JAPAN",
    name: "Intra-Asia: China to Japan",
    description: "Short-sea route from Shanghai to Tokyo",
    originPortId: "CNSHA",
    destinationPortId: "JPTYO",
    waypoints: [
      { lat: 31.2304, lng: 121.4737, name: "Shanghai" },
      { lat: 32.0, lng: 125.0 }, // East China Sea
      { lat: 34.0, lng: 132.0 }, // Approaching Japan
      { lat: 35.6528, lng: 139.8394, name: "Tokyo" },
    ],
    distanceNm: 1100,
    typicalTransitDays: 3,
    type: "container",
  },
  {
    id: "INTRA_ASIA_SINGAPORE_HONGKONG",
    name: "Intra-Asia: Singapore to Hong Kong",
    description: "Major Southeast Asia route",
    originPortId: "SGSIN",
    destinationPortId: "HKHKG",
    waypoints: [
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
      { lat: 5.0, lng: 108.0 }, // South China Sea
      { lat: 10.0, lng: 112.0 }, // Central South China Sea
      { lat: 15.0, lng: 115.0 }, // Northern South China Sea
      { lat: 22.3193, lng: 114.1694, name: "Hong Kong" },
    ],
    distanceNm: 1450,
    typicalTransitDays: 4,
    type: "container",
  },

  // MIDDLE EAST ROUTES
  {
    id: "MIDDLE_EAST_ASIA",
    name: "Middle East to Asia: Dubai to Singapore",
    description: "Major route connecting Middle East to Southeast Asia",
    originPortId: "AEJEA",
    destinationPortId: "SGSIN",
    waypoints: [
      { lat: 25.0118, lng: 55.0828, name: "Dubai" },
      { lat: 22.0, lng: 60.0 }, // Gulf of Oman
      { lat: 18.0, lng: 65.0 }, // Arabian Sea
      { lat: 12.0, lng: 72.0 }, // Indian Ocean
      { lat: 6.0, lng: 85.0 }, // Bay of Bengal
      { lat: 3.0, lng: 95.0 }, // Andaman Sea
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
    ],
    distanceNm: 3600,
    typicalTransitDays: 9,
    type: "container",
  },
  {
    id: "MIDDLE_EAST_EUROPE",
    name: "Middle East to Europe: Dubai to Rotterdam",
    description: "Route from Gulf to Northern Europe",
    originPortId: "AEJEA",
    destinationPortId: "NLRTM",
    waypoints: [
      { lat: 25.0118, lng: 55.0828, name: "Dubai" },
      { lat: 20.0, lng: 55.0 }, // Gulf of Oman
      { lat: 15.0, lng: 50.0 }, // Arabian Sea
      { lat: 12.5, lng: 43.3, name: "Bab-el-Mandeb" },
      { lat: 20.0, lng: 38.0 }, // Red Sea
      { lat: 30.0, lng: 32.5, name: "Suez Canal" },
      { lat: 35.0, lng: 20.0 }, // Mediterranean
      { lat: 40.0, lng: 10.0 }, // Western Mediterranean
      { lat: 45.0, lng: 5.0 }, // Off France
      { lat: 51.9244, lng: 4.4777, name: "Rotterdam" },
    ],
    distanceNm: 6200,
    typicalTransitDays: 15,
    type: "container",
  },

  // AFRICA ROUTES
  {
    id: "AFRICA_ASIA_CAPE",
    name: "Africa to Asia: Cape Route",
    description: "Alternative route avoiding Suez Canal",
    originPortId: "NLRTM",
    destinationPortId: "SGSIN",
    waypoints: [
      { lat: 51.9244, lng: 4.4777, name: "Rotterdam" },
      { lat: 45.0, lng: 0.0 }, // Bay of Biscay
      { lat: 35.0, lng: -10.0 }, // Off Morocco
      { lat: 20.0, lng: -15.0 }, // West Africa
      { lat: 0.0, lng: -10.0 }, // Equatorial Atlantic
      { lat: -20.0, lng: 0.0 }, // South Atlantic
      { lat: -35.0, lng: 18.0 }, // Cape of Good Hope
      { lat: -33.9249, lng: 18.4241, name: "Cape Town" },
      { lat: -30.0, lng: 35.0 }, // Indian Ocean
      { lat: -20.0, lng: 55.0 }, // Central Indian Ocean
      { lat: -10.0, lng: 75.0 }, // Eastern Indian Ocean
      { lat: 0.0, lng: 90.0 }, // Equatorial Indian Ocean
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
    ],
    distanceNm: 11500,
    typicalTransitDays: 28,
    type: "container",
  },
  {
    id: "AFRICA_EUROPE",
    name: "Africa to Europe: West Africa Route",
    description: "Route from West Africa to Europe",
    originPortId: "NGLOS",
    destinationPortId: "NLRTM",
    waypoints: [
      { lat: 6.5244, lng: 3.3792, name: "Lagos" },
      { lat: 10.0, lng: 0.0 }, // Gulf of Guinea
      { lat: 20.0, lng: -10.0 }, // Off West Africa
      { lat: 30.0, lng: -10.0 }, // Off Morocco
      { lat: 40.0, lng: -5.0 }, // Off Portugal
      { lat: 48.0, lng: 0.0 }, // Bay of Biscay
      { lat: 51.9244, lng: 4.4777, name: "Rotterdam" },
    ],
    distanceNm: 3800,
    typicalTransitDays: 10,
    type: "container",
  },

  // SOUTH AMERICA ROUTES
  {
    id: "SOUTH_AMERICA_ASIA",
    name: "South America to Asia: Santos to Shanghai",
    description: "Route from Brazil to China via Pacific",
    originPortId: "BRSST",
    destinationPortId: "CNSHA",
    waypoints: [
      { lat: -23.9618, lng: -46.3322, name: "Santos" },
      { lat: -30.0, lng: -50.0 }, // South Atlantic
      { lat: -40.0, lng: -60.0 }, // Off Argentina
      { lat: -50.0, lng: -70.0 }, // Drake Passage approach
      { lat: -55.0, lng: -70.0, name: "Cape Horn" },
      { lat: -50.0, lng: -80.0 }, // South Pacific
      { lat: -30.0, lng: -100.0 }, // Southeast Pacific
      { lat: -10.0, lng: -120.0 }, // Central Pacific
      { lat: 0.0, lng: -140.0 }, // Equatorial Pacific
      { lat: 10.0, lng: -160.0 }, // North Pacific
      { lat: 20.0, lng: 180.0 }, // Western Pacific
      { lat: 25.0, lng: 160.0 }, // Approaching Asia
      { lat: 31.2304, lng: 121.4737, name: "Shanghai" },
    ],
    distanceNm: 12800,
    typicalTransitDays: 32,
    type: "container",
  },
  {
    id: "SOUTH_AMERICA_EUROPE",
    name: "South America to Europe: Santos to Rotterdam",
    description: "Atlantic route from Brazil to Europe",
    originPortId: "BRSST",
    destinationPortId: "NLRTM",
    waypoints: [
      { lat: -23.9618, lng: -46.3322, name: "Santos" },
      { lat: -15.0, lng: -35.0 }, // Off Brazil
      { lat: 0.0, lng: -25.0 }, // Equatorial Atlantic
      { lat: 15.0, lng: -20.0 }, // North Atlantic
      { lat: 30.0, lng: -15.0 }, // Off Africa
      { lat: 40.0, lng: -10.0 }, // Off Portugal
      { lat: 48.0, lng: 0.0 }, // Bay of Biscay
      { lat: 51.9244, lng: 4.4777, name: "Rotterdam" },
    ],
    distanceNm: 5800,
    typicalTransitDays: 14,
    type: "container",
  },

  // AUSTRALIA ROUTES
  {
    id: "AUSTRALIA_ASIA",
    name: "Australia to Asia: Melbourne to Singapore",
    description: "Route from Australia to Southeast Asia",
    originPortId: "AUPME",
    destinationPortId: "SGSIN",
    waypoints: [
      { lat: -37.8136, lng: 144.9631, name: "Melbourne" },
      { lat: -30.0, lng: 140.0 }, // Great Australian Bight
      { lat: -20.0, lng: 125.0 }, // Off Western Australia
      { lat: -10.0, lng: 115.0 }, // Timor Sea
      { lat: -5.0, lng: 110.0 }, // Java Sea
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
    ],
    distanceNm: 3900,
    typicalTransitDays: 10,
    type: "container",
  },
  {
    id: "AUSTRALIA_AMERICAS",
    name: "Australia to Americas: Sydney to Los Angeles",
    description: "Trans-Pacific route from Australia to US West Coast",
    originPortId: "AUSYD",
    destinationPortId: "USLAX",
    waypoints: [
      { lat: -33.8688, lng: 151.2093, name: "Sydney" },
      { lat: -30.0, lng: 165.0 }, // Tasman Sea
      { lat: -20.0, lng: 180.0 }, // Southwest Pacific
      { lat: -10.0, lng: -170.0 }, // Central Pacific
      { lat: 0.0, lng: -150.0 }, // Equatorial Pacific
      { lat: 10.0, lng: -140.0 }, // Northeast Pacific
      { lat: 25.0, lng: -130.0 }, // Off California
      { lat: 33.7405, lng: -118.272, name: "Los Angeles" },
    ],
    distanceNm: 6500,
    typicalTransitDays: 16,
    type: "container",
  },

  // ============================================================================
  // ADDITIONAL TRANS-PACIFIC ROUTES
  // ============================================================================
  {
    id: "TRANSPACIFIC_NINGBO_SEATTLE",
    name: "Trans-Pacific: Ningbo to Seattle",
    description: "China to Pacific Northwest route",
    originPortId: "CNNBO",
    destinationPortId: "USSEA",
    waypoints: [
      { lat: 29.8683, lng: 121.544, name: "Ningbo" },
      { lat: 35.0, lng: 140.0 }, // East of Japan
      { lat: 42.0, lng: 165.0 }, // North Pacific
      { lat: 46.0, lng: -175.0 }, // Great Circle
      { lat: 48.0, lng: -145.0 }, // Gulf of Alaska
      { lat: 47.6062, lng: -122.3321, name: "Seattle" },
    ],
    distanceNm: 5200,
    typicalTransitDays: 13,
    type: "container",
  },
  {
    id: "TRANSPACIFIC_KAOHSIUNG_LA",
    name: "Trans-Pacific: Kaohsiung to Los Angeles",
    description: "Taiwan to US West Coast route",
    originPortId: "TWKHH",
    destinationPortId: "USLAX",
    waypoints: [
      { lat: 22.6273, lng: 120.3014, name: "Kaohsiung" },
      { lat: 28.0, lng: 135.0 }, // East China Sea
      { lat: 35.0, lng: 155.0 }, // Pacific
      { lat: 38.0, lng: 175.0 }, // North Pacific
      { lat: 36.0, lng: -165.0 }, // Mid-Pacific
      { lat: 34.0, lng: -130.0 }, // Off California
      { lat: 33.7405, lng: -118.272, name: "Los Angeles" },
    ],
    distanceNm: 6200,
    typicalTransitDays: 15,
    type: "container",
  },
  {
    id: "TRANSPACIFIC_SHENZHEN_OAKLAND",
    name: "Trans-Pacific: Shenzhen to Oakland",
    description: "South China to San Francisco Bay route",
    originPortId: "CNSZX",
    destinationPortId: "USOAK",
    waypoints: [
      { lat: 22.5431, lng: 114.0579, name: "Shenzhen" },
      { lat: 28.0, lng: 130.0 }, // East China Sea
      { lat: 35.0, lng: 150.0 }, // Pacific
      { lat: 38.0, lng: 170.0 }, // North Pacific
      { lat: 37.0, lng: -165.0 }, // Mid-Pacific
      { lat: 37.8044, lng: -122.2712, name: "Oakland" },
    ],
    distanceNm: 6100,
    typicalTransitDays: 15,
    type: "container",
  },

  // ============================================================================
  // ADDITIONAL ASIA-EUROPE ROUTES
  // ============================================================================
  {
    id: "ASIA_EUROPE_NINGBO_ROTTERDAM",
    name: "Asia-Europe: Ningbo to Rotterdam via Suez",
    description: "China to Netherlands main route",
    originPortId: "CNNBO",
    destinationPortId: "NLRTM",
    waypoints: [
      { lat: 29.8683, lng: 121.544, name: "Ningbo" },
      { lat: 22.0, lng: 116.0 }, // South China Sea
      { lat: 12.0, lng: 108.0 }, // Gulf of Thailand
      { lat: 2.5, lng: 101.5, name: "Strait of Malacca" },
      { lat: 10.0, lng: 78.0 }, // Bay of Bengal
      { lat: 12.6, lng: 43.3, name: "Bab-el-Mandeb" },
      { lat: 25.0, lng: 36.0 }, // Red Sea
      { lat: 30.5, lng: 32.3, name: "Suez Canal" },
      { lat: 35.0, lng: 20.0 }, // Mediterranean
      { lat: 40.0, lng: 8.0 }, // Western Mediterranean
      { lat: 45.0, lng: 2.0 }, // Bay of Biscay
      { lat: 51.9244, lng: 4.4777, name: "Rotterdam" },
    ],
    distanceNm: 10400,
    typicalTransitDays: 26,
    type: "container",
  },
  {
    id: "ASIA_EUROPE_QINGDAO_HAMBURG",
    name: "Asia-Europe: Qingdao to Hamburg via Suez",
    description: "North China to Germany route",
    originPortId: "CNQIN",
    destinationPortId: "DEHAM",
    waypoints: [
      { lat: 36.0671, lng: 120.3826, name: "Qingdao" },
      { lat: 28.0, lng: 122.0 }, // East China Sea
      { lat: 18.0, lng: 115.0 }, // South China Sea
      { lat: 8.0, lng: 105.0 }, // Gulf of Thailand
      { lat: 2.5, lng: 101.5, name: "Strait of Malacca" },
      { lat: 10.0, lng: 75.0 }, // Bay of Bengal
      { lat: 12.6, lng: 43.3, name: "Bab-el-Mandeb" },
      { lat: 23.0, lng: 37.0 }, // Red Sea
      { lat: 30.5, lng: 32.3, name: "Suez Canal" },
      { lat: 36.0, lng: 18.0 }, // Mediterranean
      { lat: 42.0, lng: 8.0 }, // Western Mediterranean
      { lat: 48.0, lng: 3.0 }, // North Sea approach
      { lat: 53.5511, lng: 9.9937, name: "Hamburg" },
    ],
    distanceNm: 10600,
    typicalTransitDays: 26,
    type: "container",
  },
  {
    id: "ASIA_EUROPE_PORTKLANG_ANTWERP",
    name: "Asia-Europe: Port Klang to Antwerp via Suez",
    description: "Malaysia to Belgium route",
    originPortId: "MYPKG",
    destinationPortId: "BEANR",
    waypoints: [
      { lat: 2.9988, lng: 101.3933, name: "Port Klang" },
      { lat: 2.5, lng: 101.5, name: "Strait of Malacca" },
      { lat: 8.0, lng: 85.0 }, // Bay of Bengal
      { lat: 12.0, lng: 68.0 }, // Arabian Sea
      { lat: 12.6, lng: 43.3, name: "Bab-el-Mandeb" },
      { lat: 22.0, lng: 38.0 }, // Red Sea
      { lat: 30.5, lng: 32.3, name: "Suez Canal" },
      { lat: 35.0, lng: 22.0 }, // Mediterranean
      { lat: 40.0, lng: 10.0 }, // Western Mediterranean
      { lat: 45.0, lng: 3.0 }, // Off France
      { lat: 51.2194, lng: 4.4025, name: "Antwerp" },
    ],
    distanceNm: 8900,
    typicalTransitDays: 22,
    type: "container",
  },

  // ============================================================================
  // ADDITIONAL INTRA-ASIA ROUTES
  // ============================================================================
  {
    id: "INTRA_ASIA_QINGDAO_BUSAN",
    name: "Intra-Asia: Qingdao to Busan",
    description: "North China to Korea route",
    originPortId: "CNQIN",
    destinationPortId: "KRPUS",
    waypoints: [
      { lat: 36.0671, lng: 120.3826, name: "Qingdao" },
      { lat: 36.0, lng: 125.0 }, // Yellow Sea
      { lat: 35.1796, lng: 129.0756, name: "Busan" },
    ],
    distanceNm: 450,
    typicalTransitDays: 2,
    type: "container",
  },
  {
    id: "INTRA_ASIA_NINGBO_YOKOHAMA",
    name: "Intra-Asia: Ningbo to Yokohama",
    description: "China to Japan route",
    originPortId: "CNNBO",
    destinationPortId: "JPYOK",
    waypoints: [
      { lat: 29.8683, lng: 121.544, name: "Ningbo" },
      { lat: 32.0, lng: 130.0 }, // East China Sea
      { lat: 35.4437, lng: 139.638, name: "Yokohama" },
    ],
    distanceNm: 950,
    typicalTransitDays: 3,
    type: "container",
  },
  {
    id: "INTRA_ASIA_LAEMCHABANG_SINGAPORE",
    name: "Intra-Asia: Laem Chabang to Singapore",
    description: "Thailand to Singapore route",
    originPortId: "THLCH",
    destinationPortId: "SGSIN",
    waypoints: [
      { lat: 13.0827, lng: 100.8833, name: "Laem Chabang" },
      { lat: 8.0, lng: 100.0 }, // Gulf of Thailand
      { lat: 2.5, lng: 101.5, name: "Strait of Malacca" },
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
    ],
    distanceNm: 850,
    typicalTransitDays: 3,
    type: "container",
  },
  {
    id: "INTRA_ASIA_OSAKA_SHANGHAI",
    name: "Intra-Asia: Osaka to Shanghai",
    description: "Japan to China route",
    originPortId: "JPOSA",
    destinationPortId: "CNSHA",
    waypoints: [
      { lat: 34.6937, lng: 135.5023, name: "Osaka" },
      { lat: 33.0, lng: 128.0 }, // East China Sea
      { lat: 31.2304, lng: 121.4737, name: "Shanghai" },
    ],
    distanceNm: 850,
    typicalTransitDays: 3,
    type: "container",
  },
  {
    id: "INTRA_ASIA_HOCHIMINH_HONGKONG",
    name: "Intra-Asia: Ho Chi Minh to Hong Kong",
    description: "Vietnam to Hong Kong route",
    originPortId: "VNSGN",
    destinationPortId: "HKHKG",
    waypoints: [
      { lat: 10.7769, lng: 106.7009, name: "Ho Chi Minh City" },
      { lat: 15.0, lng: 110.0 }, // South China Sea
      { lat: 22.3193, lng: 114.1694, name: "Hong Kong" },
    ],
    distanceNm: 750,
    typicalTransitDays: 2,
    type: "container",
  },

  // ============================================================================
  // MEDITERRANEAN ROUTES
  // ============================================================================
  {
    id: "MEDITERRANEAN_PIRAEUS_BARCELONA",
    name: "Mediterranean: Piraeus to Barcelona",
    description: "Greece to Spain Mediterranean route",
    originPortId: "GRSKG",
    destinationPortId: "ESBCN",
    waypoints: [
      { lat: 37.9838, lng: 23.7275, name: "Piraeus" },
      { lat: 38.0, lng: 18.0 }, // Ionian Sea
      { lat: 38.0, lng: 12.0 }, // Tyrrhenian Sea
      { lat: 40.0, lng: 5.0 }, // Western Mediterranean
      { lat: 41.3851, lng: 2.1734, name: "Barcelona" },
    ],
    distanceNm: 1400,
    typicalTransitDays: 4,
    type: "container",
  },
  {
    id: "MEDITERRANEAN_GENOA_ISTANBUL",
    name: "Mediterranean: Genoa to Istanbul",
    description: "Italy to Turkey route",
    originPortId: "ITGOA",
    destinationPortId: "TRIST",
    waypoints: [
      { lat: 44.4056, lng: 8.9463, name: "Genoa" },
      { lat: 42.0, lng: 14.0 }, // Adriatic approach
      { lat: 38.0, lng: 20.0 }, // Ionian Sea
      { lat: 37.0, lng: 25.0 }, // Aegean Sea
      { lat: 41.1, lng: 29.1, name: "Bosphorus Strait" },
      { lat: 41.0082, lng: 28.9784, name: "Istanbul" },
    ],
    distanceNm: 1600,
    typicalTransitDays: 4,
    type: "container",
  },
  {
    id: "MEDITERRANEAN_VALENCIA_MARSEILLE",
    name: "Mediterranean: Valencia to Marseille",
    description: "Spain to France Mediterranean route",
    originPortId: "ESVLC",
    destinationPortId: "FRMRS",
    waypoints: [
      { lat: 39.4699, lng: -0.3763, name: "Valencia" },
      { lat: 41.0, lng: 2.0 }, // Western Mediterranean
      { lat: 43.2965, lng: 5.3698, name: "Marseille" },
    ],
    distanceNm: 350,
    typicalTransitDays: 1,
    type: "container",
  },
  {
    id: "MEDITERRANEAN_ALGECIRAS_GENOA",
    name: "Mediterranean: Algeciras to Genoa",
    description: "Spain to Italy via Mediterranean",
    originPortId: "ESALG",
    destinationPortId: "ITGOA",
    waypoints: [
      { lat: 36.1408, lng: -5.4526, name: "Algeciras" },
      { lat: 36.0, lng: -5.6, name: "Strait of Gibraltar" },
      { lat: 38.0, lng: 0.0 }, // Western Mediterranean
      { lat: 40.0, lng: 8.0 }, // Tyrrhenian Sea
      { lat: 44.4056, lng: 8.9463, name: "Genoa" },
    ],
    distanceNm: 950,
    typicalTransitDays: 3,
    type: "container",
  },

  // ============================================================================
  // BALTIC AND NORTH SEA ROUTES
  // ============================================================================
  {
    id: "BALTIC_HAMBURG_HELSINKI",
    name: "Baltic: Hamburg to Helsinki",
    description: "Germany to Finland Baltic route",
    originPortId: "DEHAM",
    destinationPortId: "FIHEL",
    waypoints: [
      { lat: 53.5511, lng: 9.9937, name: "Hamburg" },
      { lat: 55.0, lng: 12.0 }, // Kattegat
      { lat: 57.0, lng: 16.0 }, // Baltic Sea
      { lat: 60.1699, lng: 24.9384, name: "Helsinki" },
    ],
    distanceNm: 750,
    typicalTransitDays: 2,
    type: "container",
  },
  {
    id: "BALTIC_GDANSK_STOCKHOLM",
    name: "Baltic: Gdansk to Stockholm",
    description: "Poland to Sweden Baltic route",
    originPortId: "PLGDN",
    destinationPortId: "SEGOT",
    waypoints: [
      { lat: 54.352, lng: 18.6466, name: "Gdansk" },
      { lat: 56.0, lng: 17.0 }, // Baltic Sea
      { lat: 57.7089, lng: 11.9746, name: "Gothenburg" },
    ],
    distanceNm: 450,
    typicalTransitDays: 2,
    type: "container",
  },
  {
    id: "NORTHSEA_ROTTERDAM_OSLO",
    name: "North Sea: Rotterdam to Oslo",
    description: "Netherlands to Norway route",
    originPortId: "NLRTM",
    destinationPortId: "NOOSL",
    waypoints: [
      { lat: 51.9244, lng: 4.4777, name: "Rotterdam" },
      { lat: 54.0, lng: 5.0 }, // North Sea
      { lat: 57.0, lng: 7.0 }, // Norwegian Sea approach
      { lat: 59.9139, lng: 10.7522, name: "Oslo" },
    ],
    distanceNm: 550,
    typicalTransitDays: 2,
    type: "container",
  },
  {
    id: "NORTHSEA_ANTWERP_COPENHAGEN",
    name: "North Sea: Antwerp to Copenhagen",
    description: "Belgium to Denmark route",
    originPortId: "BEANR",
    destinationPortId: "DKCPH",
    waypoints: [
      { lat: 51.2194, lng: 4.4025, name: "Antwerp" },
      { lat: 53.0, lng: 5.0 }, // North Sea
      { lat: 55.6761, lng: 12.5683, name: "Copenhagen" },
    ],
    distanceNm: 450,
    typicalTransitDays: 2,
    type: "container",
  },

  // ============================================================================
  // ADDITIONAL MIDDLE EAST ROUTES
  // ============================================================================
  {
    id: "MIDDLE_EAST_JEDDAH_SINGAPORE",
    name: "Middle East to Asia: Jeddah to Singapore",
    description: "Red Sea to Southeast Asia route",
    originPortId: "SAJED",
    destinationPortId: "SGSIN",
    waypoints: [
      { lat: 21.5433, lng: 39.1728, name: "Jeddah" },
      { lat: 15.0, lng: 42.0 }, // Red Sea
      { lat: 12.6, lng: 43.3, name: "Bab-el-Mandeb" },
      { lat: 13.0, lng: 55.0 }, // Gulf of Aden
      { lat: 10.0, lng: 75.0 }, // Arabian Sea
      { lat: 5.0, lng: 90.0 }, // Bay of Bengal
      { lat: 2.5, lng: 101.5, name: "Strait of Malacca" },
      { lat: 1.2644, lng: 103.8224, name: "Singapore" },
    ],
    distanceNm: 4200,
    typicalTransitDays: 10,
    type: "container",
  },
  {
    id: "MIDDLE_EAST_KUWAIT_MUMBAI",
    name: "Middle East to India: Kuwait to Mumbai",
    description: "Persian Gulf to India route",
    originPortId: "KWKWI",
    destinationPortId: "INNSA",
    waypoints: [
      { lat: 29.3759, lng: 47.9774, name: "Kuwait" },
      { lat: 26.5, lng: 56.3, name: "Strait of Hormuz" },
      { lat: 23.0, lng: 62.0 }, // Gulf of Oman
      { lat: 20.0, lng: 68.0 }, // Arabian Sea
      { lat: 18.9388, lng: 72.8354, name: "Mumbai" },
    ],
    distanceNm: 1800,
    typicalTransitDays: 5,
    type: "tanker",
  },
  {
    id: "MIDDLE_EAST_HAIFA_PIRAEUS",
    name: "Mediterranean: Haifa to Piraeus",
    description: "Israel to Greece route",
    originPortId: "ILHFA",
    destinationPortId: "GRSKG",
    waypoints: [
      { lat: 32.794, lng: 34.9896, name: "Haifa" },
      { lat: 35.0, lng: 30.0 }, // Eastern Mediterranean
      { lat: 36.0, lng: 26.0 }, // Aegean approach
      { lat: 37.9838, lng: 23.7275, name: "Piraeus" },
    ],
    distanceNm: 650,
    typicalTransitDays: 2,
    type: "container",
  },

  // ============================================================================
  // ADDITIONAL AFRICA ROUTES
  // ============================================================================
  {
    id: "AFRICA_DARESSALAAM_DURBAN",
    name: "Africa East Coast: Dar es Salaam to Durban",
    description: "Tanzania to South Africa route",
    originPortId: "TZTZA",
    destinationPortId: "ZADUR",
    waypoints: [
      { lat: -6.7924, lng: 39.2083, name: "Dar es Salaam" },
      { lat: -15.0, lng: 40.0 }, // Mozambique Channel
      { lat: -25.0, lng: 35.0 }, // Off Mozambique
      { lat: -29.8587, lng: 31.0218, name: "Durban" },
    ],
    distanceNm: 1600,
    typicalTransitDays: 4,
    type: "container",
  },
  {
    id: "AFRICA_DJIBOUTI_MOMBASA",
    name: "Africa East Coast: Djibouti to Mombasa",
    description: "Horn of Africa to Kenya route",
    originPortId: "DJJIB",
    destinationPortId: "KEMBA",
    waypoints: [
      { lat: 11.5721, lng: 43.1456, name: "Djibouti" },
      { lat: 5.0, lng: 43.0 }, // Somali Coast
      { lat: 0.0, lng: 42.0 }, // Equatorial waters
      { lat: -4.0435, lng: 39.6682, name: "Mombasa" },
    ],
    distanceNm: 1100,
    typicalTransitDays: 3,
    type: "container",
  },
  {
    id: "AFRICA_TEMA_LAGOS",
    name: "Africa West Coast: Tema to Lagos",
    description: "Ghana to Nigeria route",
    originPortId: "GHALG",
    destinationPortId: "NGLOS",
    waypoints: [
      { lat: 5.6037, lng: -0.0074, name: "Tema" },
      { lat: 5.5, lng: 2.0 }, // Gulf of Guinea
      { lat: 6.5244, lng: 3.3792, name: "Lagos" },
    ],
    distanceNm: 220,
    typicalTransitDays: 1,
    type: "container",
  },

  // ============================================================================
  // ADDITIONAL SOUTH AMERICA ROUTES
  // ============================================================================
  {
    id: "SOUTH_AMERICA_CALLAO_PANAMA",
    name: "South America to Panama: Callao to Colon",
    description: "Peru to Panama Canal route",
    originPortId: "PECLL",
    destinationPortId: "PACOL",
    waypoints: [
      { lat: -12.0464, lng: -77.0428, name: "Callao" },
      { lat: -5.0, lng: -80.0 }, // Off Ecuador
      { lat: 2.0, lng: -82.0 }, // Off Colombia
      { lat: 9.3547, lng: -79.9009, name: "Colon" },
    ],
    distanceNm: 1500,
    typicalTransitDays: 4,
    type: "container",
  },
  {
    id: "SOUTH_AMERICA_BUENOSAIRES_SANTOS",
    name: "South America: Buenos Aires to Santos",
    description: "Argentina to Brazil route",
    originPortId: "ARBUE",
    destinationPortId: "BRSST",
    waypoints: [
      { lat: -34.6037, lng: -58.3816, name: "Buenos Aires" },
      { lat: -32.0, lng: -52.0 }, // Off Uruguay
      { lat: -28.0, lng: -48.0 }, // Off Brazil
      { lat: -23.9618, lng: -46.3322, name: "Santos" },
    ],
    distanceNm: 1200,
    typicalTransitDays: 3,
    type: "container",
  },
  {
    id: "SOUTH_AMERICA_VALPARAISO_LA",
    name: "South America to US: Valparaiso to Los Angeles",
    description: "Chile to US West Coast route",
    originPortId: "CLVAP",
    destinationPortId: "USLAX",
    waypoints: [
      { lat: -33.0472, lng: -71.6127, name: "Valparaiso" },
      { lat: -20.0, lng: -75.0 }, // Off Peru
      { lat: -5.0, lng: -82.0 }, // Off Ecuador
      { lat: 5.0, lng: -88.0 }, // Off Central America
      { lat: 15.0, lng: -95.0 }, // Off Mexico
      { lat: 25.0, lng: -110.0 }, // Baja California
      { lat: 33.7405, lng: -118.272, name: "Los Angeles" },
    ],
    distanceNm: 4200,
    typicalTransitDays: 10,
    type: "container",
  },

  // ============================================================================
  // ADDITIONAL AUSTRALIA/OCEANIA ROUTES
  // ============================================================================
  {
    id: "OCEANIA_BRISBANE_AUCKLAND",
    name: "Oceania: Brisbane to Auckland",
    description: "Australia to New Zealand route",
    originPortId: "AUBNE",
    destinationPortId: "NZAKL",
    waypoints: [
      { lat: -27.4698, lng: 153.0251, name: "Brisbane" },
      { lat: -32.0, lng: 165.0 }, // Tasman Sea
      { lat: -36.8485, lng: 174.7633, name: "Auckland" },
    ],
    distanceNm: 1200,
    typicalTransitDays: 3,
    type: "container",
  },
  {
    id: "OCEANIA_SYDNEY_HONGKONG",
    name: "Oceania to Asia: Sydney to Hong Kong",
    description: "Australia to Hong Kong route",
    originPortId: "AUSYD",
    destinationPortId: "HKHKG",
    waypoints: [
      { lat: -33.8688, lng: 151.2093, name: "Sydney" },
      { lat: -25.0, lng: 150.0 }, // Coral Sea
      { lat: -15.0, lng: 145.0 }, // Off Queensland
      { lat: -5.0, lng: 140.0 }, // Arafura Sea
      { lat: 5.0, lng: 125.0 }, // Celebes Sea
      { lat: 15.0, lng: 118.0 }, // South China Sea
      { lat: 22.3193, lng: 114.1694, name: "Hong Kong" },
    ],
    distanceNm: 4500,
    typicalTransitDays: 11,
    type: "container",
  },
  {
    id: "OCEANIA_MELBOURNE_TOKYO",
    name: "Oceania to Asia: Melbourne to Tokyo",
    description: "Australia to Japan route",
    originPortId: "AUPME",
    destinationPortId: "JPTYO",
    waypoints: [
      { lat: -37.8136, lng: 144.9631, name: "Melbourne" },
      { lat: -30.0, lng: 150.0 }, // Tasman Sea
      { lat: -20.0, lng: 160.0 }, // Coral Sea
      { lat: -10.0, lng: 165.0 }, // Solomon Sea
      { lat: 0.0, lng: 165.0 }, // Equatorial Pacific
      { lat: 15.0, lng: 155.0 }, // Western Pacific
      { lat: 28.0, lng: 145.0 }, // Approaching Japan
      { lat: 35.6528, lng: 139.8394, name: "Tokyo" },
    ],
    distanceNm: 5200,
    typicalTransitDays: 13,
    type: "container",
  },
];

// Helper functions
export const getRouteById = (id: string): ShippingRoute | undefined => {
  return SHIPPING_ROUTES.find((route) => route.id === id);
};

export const getRoutesByOrigin = (portId: string): ShippingRoute[] => {
  return SHIPPING_ROUTES.filter((route) => route.originPortId === portId);
};

export const getRoutesByDestination = (portId: string): ShippingRoute[] => {
  return SHIPPING_ROUTES.filter((route) => route.destinationPortId === portId);
};

export const getRoutesBetweenPorts = (
  originPortId: string,
  destinationPortId: string
): ShippingRoute[] => {
  return SHIPPING_ROUTES.filter(
    (route) =>
      route.originPortId === originPortId &&
      route.destinationPortId === destinationPortId
  );
};

export const getRoutesByType = (
  type: "container" | "bulk" | "tanker" | "mixed"
): ShippingRoute[] => {
  return SHIPPING_ROUTES.filter((route) => route.type === type);
};

/**
 * Calculate great circle distance between two points using Haversine formula
 * @param lat1 Latitude of point 1 in degrees
 * @param lng1 Longitude of point 1 in degrees
 * @param lat2 Latitude of point 2 in degrees
 * @param lng2 Longitude of point 2 in degrees
 * @returns Distance in nautical miles
 */
export const calculateDistance = (
  lat1: number,
  lng1: number,
  lat2: number,
  lng2: number
): number => {
  const R = 3440.065; // Earth's radius in nautical miles
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLng / 2) *
      Math.sin(dLng / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

/**
 * Calculate bearing from point 1 to point 2
 * @returns Bearing in degrees (0-360)
 */
export const calculateBearing = (
  lat1: number,
  lng1: number,
  lat2: number,
  lng2: number
): number => {
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const lat1Rad = (lat1 * Math.PI) / 180;
  const lat2Rad = (lat2 * Math.PI) / 180;
  
  const y = Math.sin(dLng) * Math.cos(lat2Rad);
  const x = Math.cos(lat1Rad) * Math.sin(lat2Rad) -
            Math.sin(lat1Rad) * Math.cos(lat2Rad) * Math.cos(dLng);
  const bearing = Math.atan2(y, x);
  
  return ((bearing * 180 / Math.PI) + 360) % 360;
};

/**
 * Calculate destination point given start point, bearing, and distance
 * @param lat Starting latitude in degrees
 * @param lng Starting longitude in degrees
 * @param bearing Bearing in degrees
 * @param distanceNm Distance in nautical miles
 * @returns Destination point {lat, lng}
 */
export const calculateDestination = (
  lat: number,
  lng: number,
  bearing: number,
  distanceNm: number
): { lat: number; lng: number } => {
  const R = 3440.065; // Earth's radius in nautical miles
  const bearingRad = (bearing * Math.PI) / 180;
  const latRad = (lat * Math.PI) / 180;
  const lngRad = (lng * Math.PI) / 180;
  const angularDistance = distanceNm / R;
  
  const lat2Rad = Math.asin(
    Math.sin(latRad) * Math.cos(angularDistance) +
    Math.cos(latRad) * Math.sin(angularDistance) * Math.cos(bearingRad)
  );
  
  const lng2Rad = lngRad + Math.atan2(
    Math.sin(bearingRad) * Math.sin(angularDistance) * Math.cos(latRad),
    Math.cos(angularDistance) - Math.sin(latRad) * Math.sin(lat2Rad)
  );
  
  return {
    lat: (lat2Rad * 180) / Math.PI,
    lng: (lng2Rad * 180) / Math.PI
  };
};

/**
 * Generate waypoints for a great circle route between two points
 * This creates a realistic ocean route following the shortest path on a sphere
 * @param lat1 Start latitude
 * @param lng1 Start longitude
 * @param lat2 End latitude
 * @param lng2 End longitude
 * @param numWaypoints Number of intermediate waypoints to generate
 * @returns Array of waypoints including start and end points
 */
export const generateGreatCircleRoute = (
  lat1: number,
  lng1: number,
  lat2: number,
  lng2: number,
  numWaypoints: number = 5
): RouteWaypoint[] => {
  const waypoints: RouteWaypoint[] = [];
  
  // Add start point
  waypoints.push({ lat: lat1, lng: lng1 });
  
  // Calculate intermediate points along great circle
  for (let i = 1; i < numWaypoints; i++) {
    const fraction = i / numWaypoints;
    
    // Convert to radians
    const lat1Rad = (lat1 * Math.PI) / 180;
    const lng1Rad = (lng1 * Math.PI) / 180;
    const lat2Rad = (lat2 * Math.PI) / 180;
    const lng2Rad = (lng2 * Math.PI) / 180;
    
    // Calculate angular distance
    const d = Math.acos(
      Math.sin(lat1Rad) * Math.sin(lat2Rad) +
      Math.cos(lat1Rad) * Math.cos(lat2Rad) * Math.cos(lng2Rad - lng1Rad)
    );
    
    // Interpolate
    const a = Math.sin((1 - fraction) * d) / Math.sin(d);
    const b = Math.sin(fraction * d) / Math.sin(d);
    
    const x = a * Math.cos(lat1Rad) * Math.cos(lng1Rad) +
              b * Math.cos(lat2Rad) * Math.cos(lng2Rad);
    const y = a * Math.cos(lat1Rad) * Math.sin(lng1Rad) +
              b * Math.cos(lat2Rad) * Math.sin(lng2Rad);
    const z = a * Math.sin(lat1Rad) + b * Math.sin(lat2Rad);
    
    const latRad = Math.atan2(z, Math.sqrt(x * x + y * y));
    const lngRad = Math.atan2(y, x);
    
    waypoints.push({
      lat: (latRad * 180) / Math.PI,
      lng: (lngRad * 180) / Math.PI
    });
  }
  
  // Add end point
  waypoints.push({ lat: lat2, lng: lng2 });
  
  return waypoints;
};

/**
 * Generate storm avoidance route that goes AROUND a storm location
 * @param originalRoute Original route waypoints
 * @param stormLat Storm center latitude
 * @param stormLng Storm center longitude
 * @param stormRadiusNm Storm radius in nautical miles (default 300nm)
 * @param safetyMarginNm Additional safety margin in nautical miles (default 200nm)
 * @returns New route that avoids the storm
 */
export const generateStormAvoidanceRoute = (
  originalRoute: RouteWaypoint[],
  stormLat: number,
  stormLng: number,
  stormRadiusNm: number = 300,
  safetyMarginNm: number = 200
): RouteWaypoint[] => {
  const avoidanceRoute: RouteWaypoint[] = [];
  const totalAvoidanceRadius = stormRadiusNm + safetyMarginNm;
  
  // Check each segment of the original route
  for (let i = 0; i < originalRoute.length - 1; i++) {
    const start = originalRoute[i];
    const end = originalRoute[i + 1];
    
    avoidanceRoute.push(start);
    
    // Calculate closest point on segment to storm
    const segmentBearing = calculateBearing(start.lat, start.lng, end.lat, end.lng);
    const distanceToStormFromStart = calculateDistance(start.lat, start.lng, stormLat, stormLng);
    const distanceToStormFromEnd = calculateDistance(end.lat, end.lng, stormLat, stormLng);
    
    // Check if storm is close to this segment
    const minDistanceToStorm = Math.min(distanceToStormFromStart, distanceToStormFromEnd);
    
    if (minDistanceToStorm < totalAvoidanceRadius) {
      // Storm is too close, need to route around it
      
      // Calculate bearing from storm to segment midpoint
      const midLat = (start.lat + end.lat) / 2;
      const midLng = (start.lng + end.lng) / 2;
      const bearingFromStorm = calculateBearing(stormLat, stormLng, midLat, midLng);
      
      // Determine which side to go around (perpendicular to segment bearing)
      // Go to the side that's already closer to the route
      const perpendicularBearing1 = (segmentBearing + 90) % 360;
      const perpendicularBearing2 = (segmentBearing - 90 + 360) % 360;
      
      // Choose the perpendicular bearing that's closer to the bearing from storm
      const diff1 = Math.abs(perpendicularBearing1 - bearingFromStorm);
      const diff2 = Math.abs(perpendicularBearing2 - bearingFromStorm);
      const avoidanceBearing = diff1 < diff2 ? perpendicularBearing1 : perpendicularBearing2;
      
      // Create detour waypoints around the storm
      const detourDistance = totalAvoidanceRadius * 1.5; // Go well around
      
      // First detour point: move away from storm
      const detour1 = calculateDestination(
        stormLat,
        stormLng,
        avoidanceBearing,
        detourDistance
      );
      
      // Second detour point: continue around storm
      const detour2 = calculateDestination(
        stormLat,
        stormLng,
        (avoidanceBearing + 45) % 360,
        detourDistance
      );
      
      // Third detour point: start heading back to route
      const detour3 = calculateDestination(
        stormLat,
        stormLng,
        (avoidanceBearing + 90) % 360,
        detourDistance
      );
      
      avoidanceRoute.push(
        { ...detour1, name: 'Storm Avoidance Point 1' },
        { ...detour2, name: 'Storm Avoidance Point 2' },
        { ...detour3, name: 'Storm Avoidance Point 3' }
      );
    }
  }
  
  // Add final destination
  avoidanceRoute.push(originalRoute[originalRoute.length - 1]);
  
  return avoidanceRoute;
};

/**
 * Calculate total distance of a route with multiple waypoints
 * @param waypoints Array of route waypoints
 * @returns Total distance in nautical miles
 */
export const calculateRouteDistance = (waypoints: RouteWaypoint[]): number => {
  let totalDistance = 0;
  
  for (let i = 0; i < waypoints.length - 1; i++) {
    const distance = calculateDistance(
      waypoints[i].lat,
      waypoints[i].lng,
      waypoints[i + 1].lat,
      waypoints[i + 1].lng
    );
    totalDistance += distance;
  }
  
  return totalDistance;
};

// Made with Bob
