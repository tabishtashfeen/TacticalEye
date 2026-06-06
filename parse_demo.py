from awpy import DemoParser
import json

# Initialize parser for the downloaded pro match
parser = DemoParser(demofile="pro_match_mirage.dem", parse_rate=128)
data = parser.parse()

extracted_lineups = []

# Filter for utility throws (e.g., Smoke grenades)
for round_data in data["gameRounds"]:
    for grenade in round_data["grenades"]:
        if grenade["grenadeType"] == "Smoke":
            # Extract player position and trajectory angles at the exact release frame
            telemetry = {
                "player": grenade["throwerName"],
                "setpos": f"setpos {grenade['throwerX']} {grenade['throwerY']} {grenade['throwerZ']}",
                "setang": f"setang {grenade['throwerPitch']} {grenade['throwerYaw']} 0.00",
                "handing": f"X: {grenade['landingX']}, Y: {grenade['landingY']}"
            }
            extracted_lineups.append(telemetry)

with open("extracted_pro_telemetry.json", "w") as f:
    json.dump(extracted_lineups, f, indent=4)
print(f"Successfully processed {len(extracted_lineups)} pro-tier lineups.")
