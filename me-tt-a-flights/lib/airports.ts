export interface Airport {
  code: string;
  name: string;
  city: string;
  state: string;
}

export const airports: Airport[] = [
  { code: "ABQ", name: "Albuquerque International Sunport", city: "Albuquerque", state: "NM" },
  { code: "ACK", name: "Nantucket Memorial Airport", city: "Nantucket", state: "MA" },
  { code: "ALB", name: "Albany International Airport", city: "Albany", state: "NY" },
  { code: "ATL", name: "Hartsfield-Jackson Atlanta International Airport", city: "Atlanta", state: "GA" },
  { code: "AUS", name: "Austin-Bergstrom International Airport", city: "Austin", state: "TX" },
  { code: "AVL", name: "Asheville Regional Airport", city: "Asheville", state: "NC" },
  { code: "BDL", name: "Bradley International Airport", city: "Hartford", state: "CT" },
  { code: "BGR", name: "Bangor International Airport", city: "Bangor", state: "ME" },
  { code: "BHM", name: "Birmingham-Shuttlesworth International Airport", city: "Birmingham", state: "AL" },
  { code: "BNA", name: "Nashville International Airport", city: "Nashville", state: "TN" },
  { code: "BOS", name: "Boston Logan International Airport", city: "Boston", state: "MA" },
  { code: "BQN", name: "Rafael Hernandez Airport", city: "Aguadilla", state: "PR" },
  { code: "BTV", name: "Burlington International Airport", city: "Burlington", state: "VT" },
  { code: "BUF", name: "Buffalo Niagara International Airport", city: "Buffalo", state: "NY" },
  { code: "BUR", name: "Bob Hope Airport", city: "Burbank", state: "CA" },
  { code: "BWI", name: "Baltimore/Washington International Airport", city: "Baltimore", state: "MD" },
  { code: "BZN", name: "Bozeman Yellowstone International Airport", city: "Bozeman", state: "MT" },
  { code: "CAE", name: "Columbia Metropolitan Airport", city: "Columbia", state: "SC" },
  { code: "CAK", name: "Akron-Canton Regional Airport", city: "Akron", state: "OH" },
  { code: "CHS", name: "Charleston International Airport", city: "Charleston", state: "SC" },
  { code: "CLE", name: "Cleveland Hopkins International Airport", city: "Cleveland", state: "OH" },
  { code: "CLT", name: "Charlotte Douglas International Airport", city: "Charlotte", state: "NC" },
  { code: "CMH", name: "John Glenn Columbus International Airport", city: "Columbus", state: "OH" },
  { code: "CRW", name: "Yeager Airport", city: "Charleston", state: "WV" },
  { code: "CVG", name: "Cincinnati/Northern Kentucky International Airport", city: "Cincinnati", state: "KY" },
  { code: "DAY", name: "Dayton International Airport", city: "Dayton", state: "OH" },
  { code: "DCA", name: "Ronald Reagan Washington National Airport", city: "Washington", state: "DC" },
  { code: "DEN", name: "Denver International Airport", city: "Denver", state: "CO" },
  { code: "DFW", name: "Dallas/Fort Worth International Airport", city: "Dallas", state: "TX" },
  { code: "DSM", name: "Des Moines International Airport", city: "Des Moines", state: "IA" },
  { code: "DTW", name: "Detroit Metropolitan Wayne County Airport", city: "Detroit", state: "MI" },
  { code: "EGE", name: "Eagle County Regional Airport", city: "Vail", state: "CO" },
  { code: "EWR", name: "Newark Liberty International Airport", city: "Newark", state: "NJ" },
  { code: "EYW", name: "Key West International Airport", city: "Key West", state: "FL" },
  { code: "FLL", name: "Fort Lauderdale-Hollywood International Airport", city: "Fort Lauderdale", state: "FL" },
  { code: "GRR", name: "Gerald R. Ford International Airport", city: "Grand Rapids", state: "MI" },
  { code: "GSO", name: "Piedmont Triad International Airport", city: "Greensboro", state: "NC" },
  { code: "GSP", name: "Greenville-Spartanburg International Airport", city: "Greenville", state: "SC" },
  { code: "HDN", name: "Yampa Valley Regional Airport", city: "Hayden", state: "CO" },
  { code: "HNL", name: "Daniel K. Inouye International Airport", city: "Honolulu", state: "HI" },
  { code: "HOU", name: "William P. Hobby Airport", city: "Houston", state: "TX" },
  { code: "IAD", name: "Washington Dulles International Airport", city: "Washington", state: "DC" },
  { code: "IAH", name: "George Bush Intercontinental Airport", city: "Houston", state: "TX" },
  { code: "ILM", name: "Wilmington International Airport", city: "Wilmington", state: "NC" },
  { code: "IND", name: "Indianapolis International Airport", city: "Indianapolis", state: "IN" },
  { code: "JAC", name: "Jackson Hole Airport", city: "Jackson", state: "WY" },
  { code: "JAX", name: "Jacksonville International Airport", city: "Jacksonville", state: "FL" },
  { code: "JFK", name: "John F. Kennedy International Airport", city: "New York", state: "NY" },
  { code: "LAS", name: "McCarran International Airport", city: "Las Vegas", state: "NV" },
  { code: "LAX", name: "Los Angeles International Airport", city: "Los Angeles", state: "CA" },
  { code: "LGA", name: "LaGuardia Airport", city: "New York", state: "NY" },
  { code: "LGB", name: "Long Beach Airport", city: "Long Beach", state: "CA" },
  { code: "MCI", name: "Kansas City International Airport", city: "Kansas City", state: "MO" },
  { code: "MCO", name: "Orlando International Airport", city: "Orlando", state: "FL" },
  { code: "MDW", name: "Chicago Midway International Airport", city: "Chicago", state: "IL" },
  { code: "MEM", name: "Memphis International Airport", city: "Memphis", state: "TN" },
  { code: "MHT", name: "Manchester-Boston Regional Airport", city: "Manchester", state: "NH" },
  { code: "MIA", name: "Miami International Airport", city: "Miami", state: "FL" },
  { code: "MKE", name: "Milwaukee Mitchell International Airport", city: "Milwaukee", state: "WI" },
  { code: "MSN", name: "Dane County Regional Airport", city: "Madison", state: "WI" },
  { code: "MSP", name: "Minneapolis-Saint Paul International Airport", city: "Minneapolis", state: "MN" },
  { code: "MSY", name: "Louis Armstrong New Orleans International Airport", city: "New Orleans", state: "LA" },
  { code: "MTJ", name: "Montrose Regional Airport", city: "Montrose", state: "CO" },
  { code: "MVY", name: "Martha's Vineyard Airport", city: "Martha's Vineyard", state: "MA" },
  { code: "MYR", name: "Myrtle Beach International Airport", city: "Myrtle Beach", state: "SC" },
  { code: "OAK", name: "Oakland International Airport", city: "Oakland", state: "CA" },
  { code: "OKC", name: "Will Rogers World Airport", city: "Oklahoma City", state: "OK" },
  { code: "OMA", name: "Eppley Airfield", city: "Omaha", state: "NE" },
  { code: "ORD", name: "O'Hare International Airport", city: "Chicago", state: "IL" },
  { code: "ORF", name: "Norfolk International Airport", city: "Norfolk", state: "VA" },
  { code: "PBI", name: "Palm Beach International Airport", city: "West Palm Beach", state: "FL" },
  { code: "PDX", name: "Portland International Airport", city: "Portland", state: "OR" },
  { code: "PHL", name: "Philadelphia International Airport", city: "Philadelphia", state: "PA" },
  { code: "PHX", name: "Phoenix Sky Harbor International Airport", city: "Phoenix", state: "AZ" },
  { code: "PIT", name: "Pittsburgh International Airport", city: "Pittsburgh", state: "PA" },
  { code: "PSE", name: "Mercedita Airport", city: "Ponce", state: "PR" },
  { code: "PSP", name: "Palm Springs International Airport", city: "Palm Springs", state: "CA" },
  { code: "PVD", name: "T.F. Green International Airport", city: "Providence", state: "RI" },
  { code: "PWM", name: "Portland International Jetport", city: "Portland", state: "ME" },
  { code: "RDU", name: "Raleigh-Durham International Airport", city: "Raleigh", state: "NC" },
  { code: "RIC", name: "Richmond International Airport", city: "Richmond", state: "VA" },
  { code: "ROC", name: "Greater Rochester International Airport", city: "Rochester", state: "NY" },
  { code: "RSW", name: "Southwest Florida International Airport", city: "Fort Myers", state: "FL" },
  { code: "SAN", name: "San Diego International Airport", city: "San Diego", state: "CA" },
  { code: "SAT", name: "San Antonio International Airport", city: "San Antonio", state: "TX" },
  { code: "SAV", name: "Savannah/Hilton Head International Airport", city: "Savannah", state: "GA" },
  { code: "SBN", name: "South Bend International Airport", city: "South Bend", state: "IN" },
  { code: "SDF", name: "Louisville Muhammad Ali International Airport", city: "Louisville", state: "KY" },
  { code: "SEA", name: "Seattle-Tacoma International Airport", city: "Seattle", state: "WA" },
  { code: "SFO", name: "San Francisco International Airport", city: "San Francisco", state: "CA" },
  { code: "SJC", name: "Norman Y. Mineta San Jose International Airport", city: "San Jose", state: "CA" },
  { code: "SJU", name: "Luis Muñoz Marín International Airport", city: "San Juan", state: "PR" },
  { code: "SLC", name: "Salt Lake City International Airport", city: "Salt Lake City", state: "UT" },
  { code: "SMF", name: "Sacramento International Airport", city: "Sacramento", state: "CA" },
  { code: "SNA", name: "John Wayne Airport", city: "Santa Ana", state: "CA" },
  { code: "SRQ", name: "Sarasota-Bradenton International Airport", city: "Sarasota", state: "FL" },
  { code: "STL", name: "St. Louis Lambert International Airport", city: "St. Louis", state: "MO" },
  { code: "STT", name: "Cyril E. King Airport", city: "Charlotte Amalie", state: "VI" },
  { code: "SYR", name: "Syracuse Hancock International Airport", city: "Syracuse", state: "NY" },
  { code: "TPA", name: "Tampa International Airport", city: "Tampa", state: "FL" },
  { code: "TUL", name: "Tulsa International Airport", city: "Tulsa", state: "OK" },
  { code: "TYS", name: "McGhee Tyson Airport", city: "Knoxville", state: "TN" },
  { code: "XNA", name: "Northwest Arkansas National Airport", city: "Fayetteville", state: "AR" }
];

// Create a map for quick lookup
export const airportMap = new Map<string, Airport>();
airports.forEach(airport => {
  airportMap.set(airport.code, airport);
});

// Helper function to get airport info by code
export function getAirportInfo(code: string): Airport | undefined {
  return airportMap.get(code);
}

// Helper function to get airport display name
export function getAirportDisplayName(code: string): string {
  const airport = airportMap.get(code);
  if (!airport) return code;
  return `${airport.code} - ${airport.name}`;
}

// Helper function to get airport city and state
export function getAirportLocation(code: string): string {
  const airport = airportMap.get(code);
  if (!airport) return code;
  return `${airport.city}, ${airport.state}`;
} 