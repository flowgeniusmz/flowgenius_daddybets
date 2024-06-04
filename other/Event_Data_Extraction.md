# JSON Schema and Data Extraction

## JSON Schema

The JSON output provides detailed information about event groups, offers, and events. Here is the schema:

### Root Object
- `eventGroup`: Object
  - `eventGroupId`: String
  - `displayGroupId`: String
  - `name`: String
  - `offerCategories`: Array of Objects
    - `offerCategoryId`: Integer
    - `name`: String
    - `offerSubcategoryDescriptors`: Array of Objects
      - `subcategoryId`: Integer
      - `name`: String
      - `offerSubcategory`: Object
        - `name`: String
        - `subcategoryId`: Integer
        - `componentId`: Integer
        - `tags`: Array of Strings
        - `offers`: Array of Arrays of Objects
          - `providerOfferId`: String
          - `eventId`: String
          - `eventGroupId`: String
          - `label`: String
          - `isSuspended`: Boolean
          - `isOpen`: Boolean
          - `offerSubcategoryId`: Integer
          - `isSubcategoryFeatured`: Boolean
          - `betOfferTypeId`: Integer
          - `providerCriterionId`: String
          - `outcomes`: Array of Objects
            - `providerOutcomeId`: String
            - `providerId`: Integer
            - `providerOfferId`: String
            - `label`: String
            - `oddsAmerican`: String
            - `oddsDecimal`: Float
            - `oddsDecimalDisplay`: String
            - `oddsFractional`: String
            - `line`: Float
            - `participant`: String
            - `participantType`: String
            - `main`: Boolean
            - `sortOrder`: Integer
            - `tags`: Array of Strings
            - `participants`: Array of Objects
              - `id`: String
              - `name`: String
              - `type`: String
          - `offerSequence`: Integer
          - `source`: String
          - `displayGroupId`: String
          - `main`: Boolean
          - `tags`: Array of Strings
    - `tags`: Array of Strings
  - `events`: Array of Objects
    - `eventId`: String
    - `displayGroupId`: String
    - `eventGroupId`: String
    - `eventGroupName`: String
    - `name`: String
    - `nameIdentifier`: String
    - `startDate`: String (ISO 8601 Date)
    - `teamName1`: String
    - `teamName2`: String
    - `teamShortName1`: String
    - `teamShortName2`: String
    - `team1`: Object
      - `teamId`: String
      - `name`: String
      - `shortName`: String
    - `team2`: Object
      - `teamId`: String
      - `name`: String
      - `shortName`: String
    - `eventStatus`: Object
      - `state`: String
      - `isClockDisabled`: Boolean
      - `minute`: Integer
      - `second`: Integer
      - `isClockRunning`: Boolean
    - `eventScorecard`: Object
      - `scorecardComponentId`: Integer
    - `mediaList`: Array of Objects
      - `mediaProviderName`: String
      - `mediaId`: String
      - `mediaTypeName`: String
      - `metadata`: Object
      - `updatedAt`: String (ISO 8601 Date)
    - `liveBettingOffered`: Boolean
    - `liveBettingEnabled`: Boolean
    - `tags`: Array of Strings
    - `flashBetOfferCount`: Integer
    - `eventMetadata`: Object
      - `participantMetadata`: Object
      - `mediaMetadata`: Object
        - `BetRadarStats_Stats`: Object
        - `BetRadarV3_MatchTracker`: Object
        - `BetRadarV3_Scoreboard`: Object
  - `tags`: Array of Strings
  - `nameIdentifier`: String

## Python Code to Extract Event Data

Below is the Python function to extract each `eventId` as a record and include every data attribute as a column, including the nested ones, to return a clean DataFrame:

```python
import pandas as pd

def extract_event_data(json_data):
    events = json_data['eventGroup']['events']
    event_records = []

    for event in events:
        event_record = {
            'eventId': event.get('eventId'),
            'displayGroupId': event.get('displayGroupId'),
            'eventGroupId': event.get('eventGroupId'),
            'eventGroupName': event.get('eventGroupName'),
            'name': event.get('name'),
            'nameIdentifier': event.get('nameIdentifier'),
            'startDate': event.get('startDate'),
            'teamName1': event.get('teamName1'),
            'teamName2': event.get('teamName2'),
            'teamShortName1': event.get('teamShortName1'),
            'teamShortName2': event.get('teamShortName2'),
            'team1Id': event['team1'].get('teamId') if event.get('team1') else None,
            'team1Name': event['team1'].get('name') if event.get('team1') else None,
            'team1ShortName': event['team1'].get('shortName') if event.get('team1') else None,
            'team2Id': event['team2'].get('teamId') if event.get('team2') else None,
            'team2Name': event['team2'].get('name') if event.get('team2') else None,
            'team2ShortName': event['team2'].get('shortName') if event.get('team2') else None,
            'eventState': event['eventStatus'].get('state') if event.get('eventStatus') else None,
            'isClockDisabled': event['eventStatus'].get('isClockDisabled') if event.get('eventStatus') else None,
            'minute': event['eventStatus'].get('minute') if event.get('eventStatus') else None,
            'second': event['eventStatus'].get('second') if event.get('eventStatus') else None,
            'isClockRunning': event['eventStatus'].get('isClockRunning') if event.get('eventStatus') else None,
            'scorecardComponentId': event['eventScorecard'].get('scorecardComponentId') if event.get('eventScorecard') else None,
            'liveBettingOffered': event.get('liveBettingOffered'),
            'liveBettingEnabled': event.get('liveBettingEnabled'),
            'flashBetOfferCount': event.get('flashBetOfferCount'),
        }

        # Add media metadata
        for media in event.get('mediaList', []):
            media_prefix = f"{media.get('mediaProviderName')}_{media.get('mediaTypeName')}_"
            for key, value in media.get('metadata', {}).items():
                event_record[media_prefix + key] = value
            event_record[media_prefix + 'updatedAt'] = media.get('updatedAt')

        # Add event tags
        for tag in event.get('tags', []):
            event_record[f"tag_{tag}"] = True
        
        # Add event metadata
        event_metadata = event.get('eventMetadata', {})
        participant_metadata = event_metadata.get('participantMetadata', {})
        for key, value in participant_metadata.items():
            event_record[f"participant_{key}"] = value
        
        media_metadata = event_metadata.get('mediaMetadata', {})
        for key, value in media_metadata.items():
            for subkey, subvalue in value.items():
                event_record[f"media_{key}_{subkey}"] = subvalue

        # Add offer categories and subcategories
        for category in json_data['eventGroup'].get('offerCategories', []):
            for subcategory in category.get('offerSubcategoryDescriptors', []):
                for offer_list in subcategory.get('offerSubcategory', {}).get('offers', []):
                    for offer in offer_list:
                        offer_record = event_record.copy()
                        offer_record.update({
                            'offerCategoryId': category.get('offerCategoryId'),
                            'offerCategoryName': category.get('name'),
                            'subcategoryId': subcategory.get('subcategoryId'),
                            'subcategoryName': subcategory.get('name'),
                            'providerOfferId': offer.get('providerOfferId'),
                            'label': offer.get('label'),
                            'isSuspended': offer.get('isSuspended'),
                            'isOpen': offer.get('isOpen'),
                            'offerSubcategoryId': offer.get('offerSubcategoryId'),
                            'isSubcategoryFeatured': offer.get('isSubcategoryFeatured'),
                            'betOfferTypeId': offer.get('betOfferTypeId'),
                            'providerCriterionId': offer.get('providerCriterionId'),
                            'offerSequence': offer.get('offerSequence'),
                            'source': offer.get('source'),
                            'displayGroupId': offer.get('displayGroupId'),
                            'main': offer.get('main'),
                        })
                        for outcome in offer.get('outcomes', []):
                            outcome_record = offer_record.copy()
                            outcome_record.update({
                                'providerOutcomeId': outcome.get('providerOutcomeId'),
                                'providerId': outcome.get('providerId'),
                                'oddsAmerican': outcome.get('oddsAmerican'),
                                'oddsDecimal': outcome.get('oddsDecimal'),
                                'oddsDecimalDisplay': outcome.get('oddsDecimalDisplay'),
                                'oddsFractional': outcome.get('oddsFractional'),
                                'line': outcome.get('line'),
                                'participant': outcome.get('participant'),
                                'participantType': outcome.get('participantType'),
                                'mainOutcome': outcome.get('main'),
                                'sortOrder': outcome.get('sortOrder'),
                                'outcomeTags': ", ".join(outcome.get('tags', [])),
                                'participants': ", ".join([p.get('name') for p in outcome.get('participants', [])])
                            })
                            event_records.append(outcome_record)

    # Create a DataFrame from the list of event records
    df = pd.DataFrame(event_records)
    return df

# Example usage
json_data = {
    # Insert the JSON data here
}

df = extract_event_data(json_data)
print(df)