# Frankie Voice - ElevenLabs TTS Skill

Generate voice audio files using ElevenLabs API with Frankie's configured voice.

## Usage

```bash
# Basic usage
./scripts/speak.sh "Your text here" output.mp3

# Generate voicemail script
./scripts/speak.sh "$(cat voicemail-script.txt)" vm-hvac-v1.mp3
```

## Configuration

API key is auto-pulled from `~/.openclaw/openclaw.json` under `skills.entries.sag.apiKey`.

Default voice ID: `21m00Tcm4TlvDq8ikWAM` (Rachel - professional female voice)

To use a different voice, edit `scripts/speak.sh` and change the `VOICE_ID` variable.

## Available Voices

Common ElevenLabs voices:
- `21m00Tcm4TlvDq8ikWAM` - Rachel (default)
- `pNInz6obpgDQGcFmaJgB` - Adam (professional male)
- `EXAVITQu4vr4xnSDxMaL` - Sarah (warm female)
- `VR6AewLTigWG4xSOukaG` - Arnold (deep authoritative male)

Get your full voice list:
```bash
curl -H "xi-api-key: YOUR_KEY" https://api.elevenlabs.io/v1/voices
```

## Dependencies

- `curl` (installed by default)
- `jq` (for parsing openclaw.json)

Install jq if needed:
```bash
sudo apt install jq
```

## Files

- `SKILL.md` - This documentation
- `scripts/speak.sh` - TTS generation script
