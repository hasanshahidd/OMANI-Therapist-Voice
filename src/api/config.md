# Azure Configuration Guide

## File Location
`src/api/config/azure_config.json`

## Purpose
This file securely stores credentials for Azure Speech Services used in both:
- **Speech-to-Text (STT)**
- **Text-to-Speech (TTS)**

Both services use the **same Azure key and region**, but are accessed by different modules to maintain modularity and clarity.

## Example JSON Structure
```json
{
  "subscription_key": "your-azure-subscription-key",
  "region": "eastus"
}
