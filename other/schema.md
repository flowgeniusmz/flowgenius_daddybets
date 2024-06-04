JSON Schema for Event Group and Related Data
The JSON output provides detailed information about event groups, offers, and events. Here is the schema:

Root Object
eventGroup: Object
eventGroupId: String
displayGroupId: String
name: String
offerCategories: Array of Objects
offerCategoryId: Integer
name: String
offerSubcategoryDescriptors: Array of Objects
subcategoryId: Integer
name: String
offerSubcategory: Object
name: String
subcategoryId: Integer
componentId: Integer
tags: Array of Strings
offers: Array of Arrays of Objects
providerOfferId: String
eventId: String
eventGroupId: String
label: String
isSuspended: Boolean
isOpen: Boolean
offerSubcategoryId: Integer
isSubcategoryFeatured: Boolean
betOfferTypeId: Integer
providerCriterionId: String
outcomes: Array of Objects
providerOutcomeId: String
providerId: Integer
providerOfferId: String
label: String
oddsAmerican: String
oddsDecimal: Float
oddsDecimalDisplay: String
oddsFractional: String
line: Float
participant: String
participantType: String
main: Boolean
sortOrder: Integer
tags: Array of Strings
participants: Array of Objects
id: String
name: String
type: String
offerSequence: Integer
source: String
displayGroupId: String
main: Boolean
tags: Array of Strings
tags: Array of Strings
events: Array of Objects
eventId: String
displayGroupId: String
eventGroupId: String
eventGroupName: String
name: String
nameIdentifier: String
startDate: String (ISO 8601 Date)
teamName1: String
teamName2: String
teamShortName1: String
teamShortName2: String
team1: Object
teamId: String
name: String
shortName: String
team2: Object
teamId: String
name: String
shortName: String
eventStatus: Object
state: String
isClockDisabled: Boolean
minute: Integer
second: Integer
isClockRunning: Boolean
eventScorecard: Object
scorecardComponentId: Integer
mediaList: Array of Objects
mediaProviderName: String
mediaId: String
mediaTypeName: String
metadata: Object
updatedAt: String (ISO 8601 Date)
liveBettingOffered: Boolean
liveBettingEnabled: Boolean
tags: Array of Strings
flashBetOfferCount: Integer
eventMetadata: Object
participantMetadata: Object
mediaMetadata: Object
BetRadarStats_Stats: Object
BetRadarV3_MatchTracker: Object
BetRadarV3_Scoreboard: Object
tags: Array of Strings
nameIdentifier: String



