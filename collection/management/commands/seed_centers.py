from django.core.management.base import BaseCommand
from collection.models import CollectionCenter

class Command(BaseCommand):
    help = "Add sample e-waste collection centers"

    def handle(self, *args, **kwargs):

        centers = [
            {
                "name": "EcoDrop Bhubaneswar",
                "address": "Saheed Nagar, Bhubaneswar",
                "latitude": 20.2961,
                "longitude": 85.8245,
                "accepted_categories": [
                    "mobile",
                    "laptop",
                    "fan",
                    "mixer",
                ],
                "operating_info": "Mon-Sat, 9 AM - 6 PM",
            },
            {
                "name": "Green E-Waste Center",
                "address": "Patia, Bhubaneswar",
                "latitude": 20.3548,
                "longitude": 85.8188,
                "accepted_categories": [
                    "mobile",
                    "laptop",
                    "refrigerator",
                    "washing_machine",
                ],
                "operating_info": "Mon-Sat, 10 AM - 5 PM",
            },
            {
                "name": "CleanTech Collection Point",
                "address": "Khandagiri, Bhubaneswar",
                "latitude": 20.2547,
                "longitude": 85.7754,
                "accepted_categories": [
                    "mobile",
                    "mixer",
                    "fan",
                    "laptop",
                    "other",
                ],
                "operating_info": "Mon-Fri, 9 AM - 5 PM",
            },
            {
                "name": "Responsible Recycling Hub",
                "address": "Chandrasekharpur, Bhubaneswar",
                "latitude": 20.3340,
                "longitude": 85.8180,
                "accepted_categories": [
                    "mobile",
                    "laptop",
                    "fan",
                    "refrigerator",
                    "washing_machine",
                    "mixer",
                ],
                "operating_info": "Mon-Sun, 9 AM - 7 PM",
            },
        ]

        for center in centers:
            CollectionCenter.objects.update_or_create(
                name=center["name"],
                defaults={
                    "address": center["address"],
                    "latitude": center["latitude"],
                    "longitude": center["longitude"],
                    "accepted_categories": center["accepted_categories"],
                    "operating_info": center["operating_info"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {len(centers)} collection centers."
            )
        )