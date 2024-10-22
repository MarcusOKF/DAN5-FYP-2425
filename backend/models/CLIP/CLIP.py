from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel
import torch
import requests
from PIL import Image

device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
model_id = "openai/clip-vit-base-patch32"

model = CLIPModel.from_pretrained(model_id).to(device)
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)

def vectorizeTextCLIP (prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs['input_ids']
    attention_masks = inputs['attention_mask']
    text_vector = model.get_text_features(input_ids=torch.tensor(input_ids, device=device), attention_mask=torch.tensor(attention_masks, device=device))

    return text_vector

def vectorizeFrameCLIP(frame_path):
    raw_image = Image.open(requests.get(frame_path, stream=True).raw)
    image = processor(
        text=None,
        images=raw_image,
        return_tensors="pt"
    )['pixel_values'].to(device)

    img_vector = model.get_image_features(image)

    return torch.tensor(img_vector, device="cpu").numpy()
    # return img_vector.detach().numpy()