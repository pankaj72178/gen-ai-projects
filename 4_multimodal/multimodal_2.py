from dotenv import load_dotenv
import json
import base64
from pathlib import Path

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatGroq(model="qwen/qwen3.8-27b",temperature=0)

def get_item_code(item_name: str) -> str:
    """
    Return the item code corresponding to the provided item name.
    Expected item_nmae: "saree", "t-shirt", "jeans", "shirt".
    """
    if item_name == "saree":
        return "ITM001"
    if item_name == "t-shirt":
        return "ITM002"
    if item_name == "jeans":
        return "ITM003"
    if item_name == "shirt":
        return "ITM004"
    return "ITM999"

def encode_image_to_data_url(path: Path) -> str:
    """Convert a local image file to a data URL usable in image_url inputs."""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"

base_dir = Path(__file__).parent
img1_url = encode_image_to_data_url(base_dir/"images"/"image1.jpeg")
img2_url = encode_image_to_data_url(base_dir/"images"/"image2.jpeg")
img3_url = encode_image_to_data_url(base_dir/"images"/"image3.jpeg")



system_propmt = '''For each image, generate a JSON record that looks like this: 
    {
        "item_name": "saree",
        "item_code": "ITM001",
        "color": "red",
        "gender": "female",
        "age_category": "adult"
    }
    Output must be a JSON array of these records, one per image, as a string that Python can parse it directly.
    Do not put any pre-amble instructions or event 'json' in front of the response string.
    item_name should be one of the following: saree, t-shirt, jeans, shirt
    age_category should be one of the following: adult, child
    '''


human_content = [
    {"type": "text", "text": "Analyze each image and return a JSON array of records as instructed."},
    {"type": "image_url", "image_url": {"url": img1_url}},
    {"type": "image_url", "image_url": {"url": img2_url}},
    {"type": "image_url", "image_url": {"url": img3_url}},
]

response = llm.invoke([
    SystemMessage(content=system_propmt),
    HumanMessage(content=human_content),
])

raw = response.content.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
records = json.loads(raw)
if isinstance(records, dict):
    records = [records]

for record in records:
    record["item_code"] = get_item_code(record["item_name"])

print(json.dumps(records,indent=2))