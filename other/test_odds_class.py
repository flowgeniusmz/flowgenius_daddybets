import streamlit as st
import pandas as pd
import requests
import json

class DraftKingsOdds():
    def __init__(self):
        self.initialize_request_details()

    def initialize_request_details(self):
        self.urlbase = "https://sportsbook-nash-us{regionlower}.draftkings.com/sites/US-{regionupper}-SB/api/v5/eventgroups/{eventgroupid}?format=json"
        self.headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}
    
    def get_data(self, regionlower, regionupper, eventgroupid):
        self.format_url(regionlower=regionlower, regionupper=regionupper, eventgroupid=eventgroupid)
        self.request_odds_data()

    def format_url(self, regionlower, regionupper, eventgroupid):
        self.url = self.urlbase.format(regionlower=regionlower, regionupper=regionupper, eventgroupid=eventgroupid)

    def request_odds_data(self):
        self.odds_response = requests.get(url=self.url, headers=self.headers)
        self.odds_json_data = self.odds_response.json()
        self.odds_dataframe = self.extract_event_data()

    def extract_event_data(self):
        events = self.odds_json_data['eventGroup']['events']
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
            for category in self.odds_json_data['eventGroup'].get('offerCategories', []):
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


a = DraftKingsOdds()
a.get_data("il", "IL", "42133")
print(a.odds_dataframe)
# def get_data():
#     urlbase = "https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/42133?format=json"
#     headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}
#     response = requests.get(url=urlbase, headers=headers)
#     json_data = response.json()
#     return json_data

# def extract_event_data(json_data):
#     events = json_data['eventGroup']['events']
#     event_records = []

#     for event in events:
#         event_record = {
#             'eventId': event.get('eventId'),
#             'displayGroupId': event.get('displayGroupId'),
#             'eventGroupId': event.get('eventGroupId'),
#             'eventGroupName': event.get('eventGroupName'),
#             'name': event.get('name'),
#             'nameIdentifier': event.get('nameIdentifier'),
#             'startDate': event.get('startDate'),
#             'teamName1': event.get('teamName1'),
#             'teamName2': event.get('teamName2'),
#             'teamShortName1': event.get('teamShortName1'),
#             'teamShortName2': event.get('teamShortName2'),
#             'team1Id': event['team1'].get('teamId') if event.get('team1') else None,
#             'team1Name': event['team1'].get('name') if event.get('team1') else None,
#             'team1ShortName': event['team1'].get('shortName') if event.get('team1') else None,
#             'team2Id': event['team2'].get('teamId') if event.get('team2') else None,
#             'team2Name': event['team2'].get('name') if event.get('team2') else None,
#             'team2ShortName': event['team2'].get('shortName') if event.get('team2') else None,
#             'eventState': event['eventStatus'].get('state') if event.get('eventStatus') else None,
#             'isClockDisabled': event['eventStatus'].get('isClockDisabled') if event.get('eventStatus') else None,
#             'minute': event['eventStatus'].get('minute') if event.get('eventStatus') else None,
#             'second': event['eventStatus'].get('second') if event.get('eventStatus') else None,
#             'isClockRunning': event['eventStatus'].get('isClockRunning') if event.get('eventStatus') else None,
#             'scorecardComponentId': event['eventScorecard'].get('scorecardComponentId') if event.get('eventScorecard') else None,
#             'liveBettingOffered': event.get('liveBettingOffered'),
#             'liveBettingEnabled': event.get('liveBettingEnabled'),
#             'flashBetOfferCount': event.get('flashBetOfferCount'),
#         }

#         # Add media metadata
#         for media in event.get('mediaList', []):
#             media_prefix = f"{media.get('mediaProviderName')}_{media.get('mediaTypeName')}_"
#             for key, value in media.get('metadata', {}).items():
#                 event_record[media_prefix + key] = value
#             event_record[media_prefix + 'updatedAt'] = media.get('updatedAt')

#         # Add event tags
#         for tag in event.get('tags', []):
#             event_record[f"tag_{tag}"] = True
        
#         # Add event metadata
#         event_metadata = event.get('eventMetadata', {})
#         participant_metadata = event_metadata.get('participantMetadata', {})
#         for key, value in participant_metadata.items():
#             event_record[f"participant_{key}"] = value
        
#         media_metadata = event_metadata.get('mediaMetadata', {})
#         for key, value in media_metadata.items():
#             for subkey, subvalue in value.items():
#                 event_record[f"media_{key}_{subkey}"] = subvalue

#         # Add offer categories and subcategories
#         for category in json_data['eventGroup'].get('offerCategories', []):
#             for subcategory in category.get('offerSubcategoryDescriptors', []):
#                 for offer_list in subcategory.get('offerSubcategory', {}).get('offers', []):
#                     for offer in offer_list:
#                         offer_record = event_record.copy()
#                         offer_record.update({
#                             'offerCategoryId': category.get('offerCategoryId'),
#                             'offerCategoryName': category.get('name'),
#                             'subcategoryId': subcategory.get('subcategoryId'),
#                             'subcategoryName': subcategory.get('name'),
#                             'providerOfferId': offer.get('providerOfferId'),
#                             'label': offer.get('label'),
#                             'isSuspended': offer.get('isSuspended'),
#                             'isOpen': offer.get('isOpen'),
#                             'offerSubcategoryId': offer.get('offerSubcategoryId'),
#                             'isSubcategoryFeatured': offer.get('isSubcategoryFeatured'),
#                             'betOfferTypeId': offer.get('betOfferTypeId'),
#                             'providerCriterionId': offer.get('providerCriterionId'),
#                             'offerSequence': offer.get('offerSequence'),
#                             'source': offer.get('source'),
#                             'displayGroupId': offer.get('displayGroupId'),
#                             'main': offer.get('main'),
#                         })
#                         for outcome in offer.get('outcomes', []):
#                             outcome_record = offer_record.copy()
#                             outcome_record.update({
#                                 'providerOutcomeId': outcome.get('providerOutcomeId'),
#                                 'providerId': outcome.get('providerId'),
#                                 'oddsAmerican': outcome.get('oddsAmerican'),
#                                 'oddsDecimal': outcome.get('oddsDecimal'),
#                                 'oddsDecimalDisplay': outcome.get('oddsDecimalDisplay'),
#                                 'oddsFractional': outcome.get('oddsFractional'),
#                                 'line': outcome.get('line'),
#                                 'participant': outcome.get('participant'),
#                                 'participantType': outcome.get('participantType'),
#                                 'mainOutcome': outcome.get('main'),
#                                 'sortOrder': outcome.get('sortOrder'),
#                                 'outcomeTags': ", ".join(outcome.get('tags', [])),
#                                 'participants': ", ".join([p.get('name') for p in outcome.get('participants', [])])
#                             })
#                             event_records.append(outcome_record)

#     # Create a DataFrame from the list of event records
#     df = pd.DataFrame(event_records)
#     return df

# # Example usage
# json_data = get_data()

# df = extract_event_data(json_data)
# print(df)
