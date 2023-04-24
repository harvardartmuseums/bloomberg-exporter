import os
import shutil
import requests
import textile
import urllib.parse
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from html_sanitizer import Sanitizer

load_dotenv()

sanitizer = Sanitizer()

audio_mapping = {
     'bc_audio_id': 'id',
     'audio.url': 'url',
     'audio.title': 'title',
     'description': 'description',
     'audio.original_transcript': 'transcript'
}

image_mapping = {
     'imageid': 'id', 
     'baseimageurl': 'url',
     'caption': 'caption',
     'alttext': 'altText'
}

exhibition_mapping = {
     'exhibitionid': 'id',
     'title': 'title',
     'begindate': 'from',
     'enddate': 'to',
     'displayPeriod': 'displayPeriod',
     'description': 'information',
     'lookupNumber': 'lookupNumber',
     'itemsHeading': 'itemsHeading',
     'displayType': 'displayType',
     'published': 'published'
}

exhibition_image_mapping = {
     'exhibitionid': 'exhibitionId',
     'imageid': 'imageId',
     'displayorder': 'position'
}

exhibition_related_content_mapping = {
     'exhibition_id': 'fromExhibitionId',
     'bc_event_id': 'toItemId',
     'toExhibitionId': 'toExhibitionId',
     'position': 'position',
     'relationshipType': 'relationshipType'
}

item_mapping = {
     'bc_event_id': 'id',
     'html_attributes.title': 'title',
     'creatorId': 'creatorId',
     'date': 'date',
     'medium': 'medium',
     'dimensions': 'dimensions',
     'credit': 'credit',
     'accessionNumber': 'accessionNumber',
     'html_attributes.description': 'information',
     'lookupNumber': 'lookupNumber',
     'published': 'published'
}

item_image_mapping = {
    'id': 'itemId',
    'imageid': 'imageId',
    'displayorder': 'position'
}

def main():
     dfExhibitions = []
     dfExhibitionImages = []
     dfExhibitionItems = []
     dfExhibitionRelatedContent = []
     dfImages = []
     dfItems = []
     dfItemImages = []
     dfCreators = []
     dfAudio = []

     # fetch tours
     (dfAudio) = fetchTours()

     # fetch current, upcoming, and past exhibitions
     (dfExhibitions, dfImages, dfExhibitionImages) = fetchExhibitions('current')
     (dfu1, dfu2, dfu3) = fetchExhibitions('upcoming')
     (dfp1, dfp2, dfp3) = fetchExhibitions('past', limit=3)

     # fetch calendar listings
     (dfEvents, dfEventImages, dfEventImageXrefs, dfExhibitionRelatedEvents) = fetchCalendarEvents()

     # join the dataframes
     dfExhibitions = pd.concat([dfExhibitions, dfu1, dfp1], ignore_index=True)
     dfImages = pd.concat([dfImages, dfu2, dfp2, dfEventImages], ignore_index=True)
     dfExhibitionImages = pd.concat([dfExhibitionImages, dfu3, dfp3], ignore_index=True)
     dfItems = pd.concat([dfEvents], ignore_index=True)
     dfItemImages = pd.concat([dfEventImageXrefs], ignore_index=True)
     dfExhibitionRelatedContent = pd.concat([dfExhibitionRelatedEvents], ignore_index=True)
     dfAudio = pd.concat([dfAudio], ignore_index=True)

     #
     # prep output folder
     shutil.rmtree('temp')
     shutil.copytree('templates/CSV_TEMPLATE', 'temp')

     # save the dataframes as csv files to the output folder
     dfExhibitions.to_csv('temp/Exhibition.csv', index=False)
     dfExhibitionImages.to_csv('temp/Exhibition Image.csv', index=False)
     dfExhibitionRelatedContent.to_csv('temp/Exhibition Related Content.csv', index=False)
     dfImages.to_csv('temp/Image.csv', index=False)
     dfItems.to_csv('temp/Item.csv', index=False)
     dfItemImages.to_csv('temp/Item Image.csv', index=False)
     dfAudio.to_csv('temp/Audio.csv', index=False)

     # zip the output folder and save it to the archives folder
     now = datetime.today()
     archive_name = f"archives/data_{now.strftime('%Y-%m-%d')}-{int(now.timestamp())}"
     shutil.make_archive(base_name=archive_name, format='zip', root_dir='temp')

def fetchExhibitions(status='current', limit=5):
    params = urllib.parse.urlencode({
         'apikey': os.getenv('HAM_API_KEY'),
         'status': status,
         'venue': 'HAM',
         'size': limit,
         'sort': 'chronological',
         'sortorder': 'desc',
         'fields': 'title,description,textiledescription,images,exhibitionid,venues'
    })

    # fetch the exhibition records
    url = f'https://api.harvardartmuseums.org/exhibition?{params}'
    response = requests.get(url)
    data = response.json()

    #
    # process exhibition records in to a dataframe
    df = pd.json_normalize(data['records'], 'venues', ['title', 'textiledescription', 'exhibitionid'])
    
    # filter the dataframe to only records where the venue is HAM
    dfExhibitions = df.loc[df['name'] == 'Harvard Art Museums']

    # normalize, scrub, and sanitize the records
    dfExhibitions['description'] = df['textiledescription'].apply(textile.textile).apply(sanitizer.sanitize)
    dfExhibitions['displayPeriod'] = 'true'
    dfExhibitions['lookupNumber'] = ''
    dfExhibitions['itemsHeading'] = 'ITEMS_IN_THIS_EXHIBITION'
    dfExhibitions['displayType'] = 'grid'
    dfExhibitions['published'] = 'true'

    # grab the series required by the mapping doc
    dfExhibitions = dfExhibitions[exhibition_mapping.keys()]
    dfExhibitions.rename(columns=exhibition_mapping, inplace=True)

    #
    # process exhibition image fields in to a dataframe
    df = pd.json_normalize(data['records'], 'images', ['exhibitionid'])
    dfImages = df[image_mapping.keys()]
    dfImages['caption'] = dfImages['caption'].apply(lambda x: f"<p>{x}</p>").apply(sanitizer.sanitize)
    dfImages.rename(columns=image_mapping, inplace=True)

    #
    # process exhibition image relationships in to a dataframe
    dfExhibitionImages = df[exhibition_image_mapping.keys()]
    dfExhibitionImages.rename(columns=exhibition_image_mapping, inplace=True)

    return dfExhibitions, dfImages, dfExhibitionImages

def fetchCalendarEvents():
     params = urllib.parse.urlencode({
          'status': 0,
          'enabled': 1,
          'start_date': datetime.today().strftime('%Y-%m-%d')
     })

     url = f'https://harvardartmuseums.org/calendar/json?{params}'
     response = requests.get(url)
     data = response.json()

     # df = pd.read_json(url)
     # print(df[['id','title']])
     # descriptions = pd.DataFrame.from_records(df.html_attributes)
     # print(descriptions['description'])

     #
     # process events records in to a dataframe
     df = pd.json_normalize(data)
     
    # normalize, scrub, and sanitize the records
     df['bc_event_id'] = df['id'].add(100000000)
     df['bc_event_image_id'] = df['id'].add(110000000)

     df['start_timestamp'] = pd.to_datetime(df['date'])
     df['start_timestamp'] = df['start_timestamp'].dt.tz_convert(tz='US/Eastern')
     df['start_date'] = df['start_timestamp'].dt.date
     df['start_time'] = df['start_timestamp'].dt.time

     df['end_timestamp'] = pd.to_datetime(df['end_date'])
     df['end_timestamp'] = df['end_timestamp'].dt.tz_convert(tz='US/Eastern')
     df['end_date'] = df['end_timestamp'].dt.date
     df['end_time'] = df['end_timestamp'].dt.time
     
     # df['date'] = f'{df["start_time"]} to {df["end_time"]}'
     df['date'] = df["start_timestamp"].dt.strftime('%A, %B %d, %Y') 
     df['time'] = df["start_timestamp"].dt.strftime("%#I:%M %p") + ' - ' + df["end_timestamp"].dt.strftime("%#I:%M %p")
     df['date'] = df['date'] + ', ' + df['time'].str.lower()

     df['html_attributes.title'] = df['html_attributes.title'].apply(html_parser)
     df['html_attributes.description'] = df['html_attributes.description'].apply(sanitizer.sanitize)

     df['creatorId'] = ''
     df['dimensions'] = ''
     df['medium'] = ''
     df['lookupNumber'] = ''
     df['accessionNumber'] = ''
     df['credit'] = ''
     df['published'] = 'true'
     
     # grab the series required by the mapping doc
     dfEvents = df[item_mapping.keys()]
     dfEvents.rename(columns=item_mapping, inplace=True)

     #
     # process event image fields in to a dataframe
     dfImages = df[['bc_event_image_id', 'image_styles.home', 'html_attributes.image_caption', 'image_alt']]
     dfImages.rename(columns={'bc_event_image_id': 'id', 'html_attributes.image_caption': 'caption', 'image_styles.home': 'baseimageurl', 'image_alt': 'alttext'}, inplace=True)

     dfImages['caption'] = dfImages['caption'].apply(lambda x: f"<p>{x}</p>").apply(sanitizer.sanitize)
     dfImages.rename(columns=image_mapping, inplace=True)

     #
     # process exhibition image relationships
     dfEventImages = df[['bc_event_image_id', 'bc_event_id']]
     dfEventImages.rename(columns={'bc_event_image_id': 'imageid', 'bc_event_id': 'id'}, inplace=True)
     dfEventImages['displayorder'] = '1'
     dfEventImages.rename(columns=item_image_mapping, inplace=True)

     #
     # filter the dataframe to only records where events are tied to exhibitions
     dfExhibitionRelatedEvents = df.loc[df['exhibition_id'] > 0]
     
     # reduce the dataframe to the columns needed
     dfExhibitionRelatedEvents = dfExhibitionRelatedEvents[['exhibition_id', 'bc_event_id', 'start_timestamp']]
     
     # sort the data, reset the index to create a clean sequence number
     dfExhibitionRelatedEvents.sort_values(by=['exhibition_id', 'start_timestamp'], inplace=True)
     dfExhibitionRelatedEvents.reset_index(inplace=True, drop=True)
     dfExhibitionRelatedEvents.drop('start_timestamp', axis=1, inplace=True)
     
     # format the fields
     dfExhibitionRelatedEvents['exhibition_id'] = dfExhibitionRelatedEvents['exhibition_id'].astype(int)
     dfExhibitionRelatedEvents['relationshipType'] = 'Related Event'
     dfExhibitionRelatedEvents['toExhibitionId'] = ''
     dfExhibitionRelatedEvents['position'] = dfExhibitionRelatedEvents.index
     dfExhibitionRelatedEvents.rename(columns=exhibition_related_content_mapping, inplace=True)


     return dfEvents, dfImages, dfEventImages, dfExhibitionRelatedEvents

def fetchObjects():
     return ""

def fetchTours():
     
     tours = [660]
     params = 660   # Pigment Audio Tour
     
     url = f'https://harvardartmuseums.org/api/tours/{params}/getsnapshot'
     response = requests.get(url)
     data = response.json()

     # extract all modules
     df = pd.json_normalize(data['tour'], record_path=['stops', 'slides', 'modules'])
     
     # normalize, scrub, and sanitize the records
     dfAudioModules = df.loc[df['type'] == 5]

     dfAudioModules['bc_audio_id'] = dfAudioModules['id'] + dfAudioModules['audio.id'] + dfAudioModules['slide_id'] + params
     dfAudioModules['bc_audio_id'] = dfAudioModules['bc_audio_id'].astype(int)

     dfAudio = dfAudioModules[['bc_audio_id', 'audio.url', 'audio.original_transcript', 'audio.title']]
     dfAudio['audio.original_transcript'] = dfAudio['audio.original_transcript'].apply(textile.textile).apply(sanitizer.sanitize)

     dfAudio['description'] = ''
     dfAudio.rename(columns=audio_mapping, inplace=True)

     return dfAudio

def html_parser(raw_html):
     soup = BeautifulSoup(raw_html, 'html.parser')
     return soup.get_text()

if __name__ == "__main__":
	main()