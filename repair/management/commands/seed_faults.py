from django.core.management.base import BaseCommand
from repair.models import FaultPattern


class Command(BaseCommand):
    help = "Add initial common fault patterns for EcoRepair"

    def handle(self, *args, **kwargs):

        faults = [
            # ---------------- MOBILE ----------------
            {
                "category": "mobile",
                "symptom": "my phone screen is cracked but the phone still turns on",
                "verdict": "repairable",
                "reason": "A cracked screen on a functioning phone is a common repair.",
                "difficulty": "professional",
                "repair_guide": "The screen or display assembly can usually be replaced by a repair professional.",
            },
            {
                "category": "mobile",
                "symptom": "my phone battery drains very quickly",
                "verdict": "repairable",
                "reason": "Rapid battery drain can often be addressed by replacing an aging battery or checking the device.",
                "difficulty": "professional",
                "repair_guide": "Have the battery and charging system checked by a repair professional.",
            },
            {
                "category": "mobile",
                "symptom": "my phone does not charge",
                "verdict": "repairable",
                "reason": "Charging problems are commonly caused by issues that can be inspected and repaired.",
                "difficulty": "professional",
                "repair_guide": "Check the charging cable and port first. If the problem continues, consult a repair professional.",
            },

            # ---------------- LAPTOP ----------------
            {
                "category": "laptop",
                "symptom": "my laptop gets very hot and suddenly turns off",
                "verdict": "repairable",
                "reason": "Overheating and unexpected shutdowns are commonly repairable after checking the cooling system.",
                "difficulty": "professional",
                "repair_guide": "Have the cooling system, fan and ventilation checked and cleaned by a professional.",
            },
            {
                "category": "laptop",
                "symptom": "my laptop is extremely slow",
                "verdict": "repairable",
                "reason": "Slow performance can often be improved through maintenance, software cleanup or hardware upgrades.",
                "difficulty": "professional",
                "repair_guide": "Check storage usage, unnecessary software and available hardware upgrades.",
            },
            {
                "category": "laptop",
                "symptom": "my laptop screen is cracked but it still works",
                "verdict": "repairable",
                "reason": "A damaged laptop display can usually be replaced while the rest of the laptop remains usable.",
                "difficulty": "professional",
                "repair_guide": "A repair professional can inspect and replace the damaged display.",
            },

            # ---------------- FAN ----------------
            {
                "category": "fan",
                "symptom": "my fan is not spinning",
                "verdict": "repairable",
                "reason": "A fan that does not spin may have a repairable electrical or mechanical issue.",
                "difficulty": "professional",
                "repair_guide": "Have the fan inspected by a repair professional before replacing it.",
            },
            {
                "category": "fan",
                "symptom": "my fan is making a strange noise",
                "verdict": "repairable",
                "reason": "Unusual fan noises can often be caused by dirt, loose parts or worn components.",
                "difficulty": "professional",
                "repair_guide": "Switch off the fan and have it inspected for loose or worn parts.",
            },

            # ---------------- MIXER / GRINDER ----------------
            {
                "category": "mixer",
                "symptom": "my mixer is not starting",
                "verdict": "repairable",
                "reason": "A mixer that does not start may have a repairable electrical or mechanical problem.",
                "difficulty": "professional",
                "repair_guide": "Have the mixer inspected by a repair professional.",
            },
            {
                "category": "mixer",
                "symptom": "my mixer makes a noise but the blades are not moving",
                "verdict": "repairable",
                "reason": "The issue may be related to the blade mechanism or internal components and can often be repaired.",
                "difficulty": "professional",
                "repair_guide": "Avoid using the mixer and have the blade mechanism checked.",
            },

            # ---------------- WASHING MACHINE ----------------
            {
                "category": "washing_machine",
                "symptom": "my washing machine is making a loud noise",
                "verdict": "repairable",
                "reason": "Unusual noise during washing or spinning is often caused by a repairable mechanical issue.",
                "difficulty": "professional",
                "repair_guide": "Stop using the machine if the noise is severe and have it inspected.",
            },
            {
                "category": "washing_machine",
                "symptom": "my washing machine is not draining water",
                "verdict": "repairable",
                "reason": "Drainage problems are commonly caused by blockages or components that can be serviced.",
                "difficulty": "professional",
                "repair_guide": "Check for obvious blockages and consult a repair professional if the issue continues.",
            },

            # ---------------- REFRIGERATOR ----------------
            {
                "category": "refrigerator",
                "symptom": "my refrigerator is not cooling properly",
                "verdict": "repairable",
                "reason": "Cooling problems can have several causes and should be inspected before deciding to replace the refrigerator.",
                "difficulty": "professional",
                "repair_guide": "Have the refrigerator inspected by a qualified technician.",
            },
            {
                "category": "refrigerator",
                "symptom": "my refrigerator is making a strange noise",
                "verdict": "repairable",
                "reason": "Unusual refrigerator noises can come from components that may be repairable.",
                "difficulty": "professional",
                "repair_guide": "Have the source of the noise checked by a qualified technician.",
            },

            # ---------------- GENERAL / OTHER ----------------
            {
                "category": "other",
                "symptom": "the device was dropped and now it does not work",
                "verdict": "uncertain",
                "reason": "Physical damage can affect different internal components, so the exact problem cannot be determined from the description alone.",
                "difficulty": "professional",
                "repair_guide": "Have the device inspected before deciding whether to repair or discard it.",
            },
            {
                "category": "other",
                "symptom": "the electronic device smells burnt and stopped working",
                "verdict": "uncertain",
                "reason": "A burning smell can indicate internal electrical damage and requires professional inspection.",
                "difficulty": "professional",
                "repair_guide": "Stop using the device and have it inspected by a qualified professional.",
            },
            {
    "category": "mobile",
    "symptom": "phone is completely dead and repair cost is very high",
    "verdict": "not_economical",
    "reason": "The device may require expensive internal repairs. Replacing it may be more practical than repairing it.",
    "difficulty": "",
    "repair_guide": "",
},
{
    "category": "laptop",
    "symptom": "laptop is very old and has multiple major problems",
    "verdict": "not_economical",
    "reason": "Multiple major faults in an old device can make repair more expensive than replacement.",
    "difficulty": "",
    "repair_guide": "",
},
{
    "category": "refrigerator",
    "symptom": "refrigerator is very old and major repair is extremely expensive",
    "verdict": "not_economical",
    "reason": "A major repair on an old refrigerator may not be economically worthwhile.",
    "difficulty": "",
    "repair_guide": "",
},
        ]

        for fault in faults:
            FaultPattern.objects.update_or_create(
                category=fault["category"],
                symptom=fault["symptom"],
                defaults={
                    "verdict": fault["verdict"],
                    "reason": fault["reason"],
                    "difficulty": fault["difficulty"],
                    "repair_guide": fault["repair_guide"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {len(faults)} fault patterns."
            )
        )