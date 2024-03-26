import os
import yaml
import torch
from torchvision import transforms, datasets
from pathlib import Path
from kedro.config import OmegaConfigLoader
import logging

def get_project_path():
    return Path.cwd()

def get_images(params):
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize(params['preprocessing']['image_size']),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(params['preprocessing']['augmentation'][1]['rotation_range']),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'valid': transforms.Compose([
            transforms.Resize(params['preprocessing']['image_size']),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }
    
    data_dir = str(get_project_path() / "data" / "01_raw" / "disease_dataset" / "new-plant-diseases-dataset" / "New_Plant_Diseases_Dataset")
    image_datasets = {x: datasets.ImageFolder(root=f"{data_dir}/{x}/", transform=data_transforms[x]) for x in ['train', 'valid']}
    
    logging.info("Data Found!")
    return image_datasets

def get_loaders(image_datasets, params):
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=params['training']['batch_size'], shuffle=True, num_workers=4) for x in ['train', 'valid']}
    
    return dataloaders

def get_sizes(image_datasets):
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'valid']}
    return dataset_sizes