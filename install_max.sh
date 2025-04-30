#!/bin/bash

echo "🧠 Welcome to Max Installer"
echo "Choose your version:"
echo "1. Max Only (Voice Assistant)"
echo "2. Max AI Hand (Voice + Bionic Hand Control)"
read -p "Enter 1 or 2: " choice

# 🔧 Install dependencies
echo "🔧 Installing system packages..."
sudo apt update
sudo apt install -y python3 python3-pip portaudio19-dev python3-pyaudio python3-dev git espeak-ng

echo "📦 Installing Python modules..."
pip3 install pygame SpeechRecognition pyttsx3 groq

# 📁 Clone Max from GitHub
echo "📥 Cloning Max from GitHub..."
git clone https://github.com/coolaaayan/Max_AI.git ~/max_ai

# 🔄 Move sounds just in case (already in repo)
mkdir -p ~/max_ai/sounds
cp ~/max_ai/sounds/*.mp3 ~/max_ai/sounds/

# 🤖 Pick your version
if [ "$choice" == "1" ]; then
    cp ~/max_ai/versions/max_only/main.py ~/max_ai/main.py
    echo "✅ Installed Max (Voice Only)"
elif [ "$choice" == "2" ]; then
    cp ~/max_ai/versions/max_hand/main.py ~/max_ai/main.py
    echo "✅ Installed Max AI Hand"
else
    echo "❌ Invalid choice. Exiting."
    exit 1
fi

# 🚀 Launch Max
echo "🚀 Starting Max..."
cd ~/max_ai
python3 main.py
