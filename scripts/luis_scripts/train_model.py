import json
import time

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

from intent_detector_service.config import LUIS_LANGUAGE_APPS, AUTHORING_KEY

app_id = LUIS_LANGUAGE_APPS.get("english")
versionId = "0.1"

if not app_id:
    raise Exception("Missing app_id")

if not AUTHORING_KEY:
    raise Exception("Missing AUTHORING_KEY")

client = LUISAuthoringClient(
    'https://westus.api.cognitive.microsoft.com',
    CognitiveServicesCredentials(AUTHORING_KEY),
)

# Add Prebuilt entity
# client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["number"])


# Opening JSON file
with open('scripts/luis_scripts/en_train_data.json') as json_file:
    data = json.load(json_file)


try:  # try to add intents if they are not already added
    # add intents to app
    for intent in data["intent_list"]:
        modelId = client.model.add_intent(app_id, versionId, intent)

    # add entity to app
    for entity in data["entities"]:
        modelId = client.model.add_entity(app_id, versionId, name=entity["name"])
except Exception:
    pass

# define phraselist - add phrases as significant vocabulary to app
phraseList = {
    "enabledForAllModels": False,
    "isExchangeable": True,
    "name": "QuantityPhraselist",
    "phrases": "few,more,extra"
}

client.examples.batch(app_id, versionId, data["example_utterances"], {"enableNestedChildren": False})

print("\nUtterances added")

# Training the model
print("\nWe'll start training the app...")

async_training = client.train.train_version(app_id, versionId)
is_trained = async_training.status == "UpToDate"

trained_status = ["UpToDate", "Success"]
while not is_trained:
    time.sleep(1)
    status = client.train.get_status(app_id, versionId)
    is_trained = all(
        m.details.status in trained_status for m in status)

print("App is trained. Check LUIS portal and test it!")

# Publish the app
print("\npublishing app...")
client.apps.update_settings(app_id, is_public=True)
publish_result = client.apps.publish(
    app_id,
    versionId,
    is_staging=False
)
