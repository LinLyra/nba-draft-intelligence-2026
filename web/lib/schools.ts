const SCHOOL_SLUGS: Record<string, string> = {
  Alabama: "alabama",
  "Alba Berlin": "alba-berlin",
  Arizona: "arizona",
  Arkansas: "arkansas",
  Auburn: "auburn",
  "BC Oostende": "bc-oostende",
  BYU: "byu",
  Baylor: "baylor",
  Butler: "butler",
  Cincinnati: "cincinnati",
  Duke: "duke",
  Florida: "florida",
  "George Washington": "george-washington",
  Houston: "houston",
  Illinois: "illinois",
  Indiana: "indiana",
  Iowa: "iowa",
  "Iowa State": "iowa-state",
  "KK Mega Basket": "kk-mega-basket",
  Kansas: "kansas",
  Kentucky: "kentucky",
  Louisville: "louisville",
  Miami: "miami",
  "Miami (Ohio)": "miami-ohio",
  Michigan: "michigan",
  Missouri: "missouri",
  "NC State": "nc-state",
  "New Zealand": "new-zealand",
  "North Carolina": "north-carolina",
  Northwestern: "northwestern",
  "Ohio State": "ohio-state",
  Oregon: "oregon",
  Purdue: "purdue",
  "Santa Clara": "santa-clara",
  "South Florida": "south-florida",
  Stanford: "stanford",
  Tennessee: "tennessee",
  "Tennessee State": "tennessee-state",
  Texas: "texas",
  "Texas Tech": "texas-tech",
  UCLA: "ucla",
  UConn: "uconn",
  Valencia: "valencia",
  Vanderbilt: "vanderbilt",
  Virginia: "virginia",
  "Virginia Tech": "virginia-tech",
  Washington: "washington",
  Wisconsin: "wisconsin",
};

const TANKATHON_NCAA_CDN = "https://d2uki2uvp6v3wr.cloudfront.net/ncaa";

export function schoolSlug(school: string): string {
  return SCHOOL_SLUGS[school] ?? school.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

export function schoolLogoUrl(school: string): string {
  const slug = schoolSlug(school);
  return `${TANKATHON_NCAA_CDN}/${slug}.svg`;
}
