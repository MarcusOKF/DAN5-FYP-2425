from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel
import torch
import requests
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
model_id = "openai/clip-vit-base-patch32"

model = CLIPModel.from_pretrained(model_id).to(device)
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)

def vectoriz_text_CLIP (prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs['input_ids']
    attention_masks = inputs['attention_mask']
    text_vector = model.get_text_features(input_ids=torch.tensor(input_ids, device=device), attention_mask=torch.tensor(attention_masks, device=device))

    return text_vector

def vectorize_frame_CLIP(frame_path):
    raw_image = Image.open(requests.get(frame_path, stream=True).raw)
    image = processor(
        text=None,
        images=raw_image,
        return_tensors="pt"
    )['pixel_values'].to(device)

    img_vector = model.get_image_features(image)

    return torch.tensor(img_vector, device="cpu").numpy()
    # return img_vector.detach().numpy()

def batch_vectorize_frames_CLIP(frames_arr): #frames_arr is an array of ndarrays
    frames_embs = None
    batch_size = 16

    for i in range(0, len(frames_arr), batch_size):
        batch = frames_arr[i:i+batch_size]

        batch = processor(
            text=None,
            images=batch,
            return_tensors="pt",
            padding=True
        )['pixel_values'].to(device)

        batch_emb = model.get_image_features(pixel_values=batch)

        batch_emb = batch_emb.squeeze(0)
        batch_emb = batch_emb.cpu().detach().numpy()

        if frames_embs is None:
            frames_embs = batch_emb
        else:
            frames_embs = np.concatenate((frames_embs, batch_emb), axis=0)

    return frames_embs