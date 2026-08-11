-- GhostMiles analytical SQL examples
-- Source: City of Chicago Taxi Trips - 2026 (Socrata)
-- The app derives estimated deadhead by pairing each taxi's completed trip
-- with its next reported trip. This is an inference, not GPS truth.

-- 1. Consecutive-trip gaps
SELECT
  taxi_id,
  trip_end_timestamp,
  LEAD(trip_start_timestamp) OVER (
    PARTITION BY taxi_id ORDER BY trip_end_timestamp
  ) AS next_trip_start
FROM taxi_trips;

-- 2. Peak hours by inferred deadhead (after materializing the Python
-- haversine calculation)
SELECT
  EXTRACT(HOUR FROM trip_end_timestamp) AS hour,
  SUM(estimated_deadhead_miles) AS estimated_deadhead_miles,
  COUNT(*) FILTER (WHERE reposition_flag) AS ghost_events
FROM ghost_trip_events
GROUP BY 1
ORDER BY 2 DESC;

-- 3. Top waste areas
SELECT
  dropoff_community_area,
  SUM(estimated_deadhead_miles) AS estimated_deadhead_miles
FROM ghost_trip_events
WHERE reposition_flag
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
