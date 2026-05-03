// Type declarations for leaflet.geodesic
import * as L from 'leaflet'

declare module 'leaflet' {
  interface GeodesicOptions extends L.PolylineOptions {
    steps?: number
  }

  function geodesic(
    latlngs: L.LatLngExpression[] | L.LatLngExpression[][],
    options?: GeodesicOptions
  ): L.Polyline
}

declare module 'leaflet.geodesic' {
  // Empty module declaration to allow import
}

// Made with Bob
