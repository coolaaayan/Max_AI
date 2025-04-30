#!/bin/bash
echo "🧠 Welcome to Max Installer"
echo "Choose your version:"
echo "1. Max Only (Voice Assistant)"
echo "2. Max AI Hand (Voice + Bionic Hand Control)"
read -p "Enter 1 or 2: " choice

echo "🔧 Installing dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip portaudio19-dev python3-pyaudio python3-dev git

pip3 install pygame SpeechRecognition pyttsx3 groq

echo "📦 Cloning Max from GitHub..."
git clone https://github.com/YOUR_USERNAME/Max_AI.git ~/max_ai

mkdir -p ~/max_ai/sounds
cp ~/max_ai/sounds/*.mp3 ~/max_ai/sounds/

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

echo "🚀 Running Max..."
cd ~/max_ai
python3 main.py
