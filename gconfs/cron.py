import os
import googleapiclient.discovery

from django_cron import CronJobBase, Schedule
from django.conf import settings

from dashboard.models import Video

class FetchYoutube(CronJobBase):
    schedule = Schedule(run_every_mins=settings.YOUTUBE_RUN_EVERY_MINS)
    code = 'fetch_youtube'

    slugs = set()

    def purge_orphans(self):
        for video in Video.objects.all():
            if video.slug not in self.slugs:
                video.delete()

    def fetch_videos(self, youtube, response):
        request = youtube.playlistItems().list(
            part='snippet',
            maxResults=50,
            pageToken=response['nextPageToken'] if response else None,
            playlistId='UUp40wxsX2co5bNb8LXJhk5w',
        )
        return request.execute()


    def parse(self, youtube):
        response = None

        while True:
            response = self.fetch_videos(youtube, response)

            for item in response['items']:
                print(item['snippet']['title'])

                self.slugs.add(item['snippet']['resourceId']['videoId'])
                obj, created = Video.objects.update_or_create(
                    slug=item['snippet']['resourceId']['videoId'],
                    defaults={
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'date': item['snippet']['publishedAt'],
                        'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    }
                )

            if 'nextPageToken' not in response:
                break

    def do(self):
        api_service_name = "youtube"
        api_version = "v3"
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = settings.YOUTUBE_API_KEY)

        self.parse(youtube)
        self.purge_orphans()