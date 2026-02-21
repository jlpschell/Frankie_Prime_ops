#!/usr/bin/env python3
"""
Generate ElevenLabs voice drops for 5 priority niches.
Uses Brian voice (nPczCjzI2devNBz1zQrb) — deep, resonant, proven on contractor campaigns.
"""

import os
import sys
import time
import requests

API_KEY = os.environ.get("ELEVENLABS_API_KEY", "9a7ea3d8c90e8550990ec82da85a0f25e2a42c035081a942c12214bb50ee1e44")
VOICE_ID = "nPczCjzI2devNBz1zQrb"  # Brian — Deep, Resonant and Comforting
BASE_URL = "https://api.elevenlabs.io/v1"
OUTPUT_DIR = "/home/plotting1/frankie-bot/workspace/campaigns/audio"

SCRIPTS = {
    "septic": {
        "v1_pain": "Hey, this is Jay with Human Led AI. I work with septic companies in the DFW area, and I know your world — emergencies don't wait for business hours. When someone's septic backs up at 10pm, they're calling every company in the phone book until someone answers. We built a system that answers every call, 24/7, qualifies the emergency, and gets your crew dispatched while the other guys are still sleeping. If you're losing emergency jobs to slow response, let's fix that. Give me a call back at your convenience.",
        "v2_social": "Hey, Jay again from Human Led AI. Quick follow-up — we just helped a septic company near Rockwall capture 8 extra emergency calls last month that would've gone to voicemail. In your business, a missed call on a backed-up system is a 2 to 5 thousand dollar job walking to someone else. Our AI answers instantly, day or night. Worth a quick call back when you get a chance.",
        "v3_referral": "Hey, Jay one last time. If you're slammed with work and don't need more emergency calls, that's a great problem to have. But if you know another septic company that's losing jobs to slow callbacks, send them my way — I'll take care of you. Either way, the offer stands whenever you're ready.",
    },
    "pool-builders": {
        "v1_pain": "Hey, this is Jay with Human Led AI. I work with pool builders in the DFW area, and I keep hearing the same thing — you're out on a build site, phone's ringing, and by the time you call back, that homeowner already got three other quotes. We built a system that answers your calls instantly, qualifies the project, and books the consultation while you're still pouring gunite. If missed calls are costing you pool jobs, let's fix that. Give me a call back at your convenience.",
        "v2_social": "Hey, Jay again from Human Led AI. Quick follow-up — we just helped a pool builder in Frisco stop losing leads to voicemail. He was missing 5 to 6 calls a week during build season. Now his AI handles initial calls and he's booking 35% more consultations without chasing people down. Same system, takes 15 minutes to set up. Worth a quick look? Give me a call back.",
        "v3_referral": "Hey, Jay one last time. If you've got more builds than you can handle right now, that's a good problem. But if you know another pool company that's tired of losing jobs to slow callbacks, send them my way — I'll make it worth your while. Either way, offer's open whenever you're ready.",
    },
    "concrete": {
        "v1_pain": "Hey, this is Jay with Human Led AI. I work with concrete contractors in the DFW area, and I know your problem — once you start a pour, you can't stop to answer the phone. By the time you call back, that homeowner already got three other quotes. We built a system that answers your calls instantly, qualifies the project scope, and books the estimate while you're still finishing the job. If missed calls are costing you work, let's fix that. Give me a call back at your convenience.",
        "v2_social": "Hey, Jay again from Human Led AI. Quick follow-up — we just helped a concrete contractor in Allen go from missing 6 to 7 calls a week to catching every single one. He booked 12 more estimates last month without changing anything else. Same system, works for flatwork, foundations, hardscape — any concrete operation. Worth 10 minutes? Give me a call back.",
        "v3_referral": "Hey, Jay one last time. If you're booked through summer and don't need more leads, that's a good sign. But if you know another concrete guy who's tired of losing jobs to whoever calls back first, send them my way. I'll make it worth your while. Either way, offer's open whenever you're ready.",
    },
    "garage-doors": {
        "v1_pain": "Hey, this is Jay with Human Led AI. I work with garage door companies in the DFW area. When someone's garage door is stuck open or won't close, they're not leaving a voicemail and waiting — they're calling the next company. We built a system that answers every call instantly, qualifies the job, and books the appointment before your competition even sees the missed call. If you're losing service calls to slow response, let's fix that. Give me a call back at your convenience.",
        "v2_social": "Hey, Jay again from Human Led AI. Quick follow-up — we just helped a garage door company in Plano catch 15 extra service calls last month that would've gone to voicemail. In your business, a missed call on a broken spring is a 400 to 800 dollar job walking to someone else. Our AI answers instantly, day or night. Worth a quick call back when you get a chance.",
        "v3_referral": "Hey, Jay one last time. If you've got more installs than you can handle right now, good for you. But if you know another garage door company losing service calls to voicemail, send them my way — I'll take care of you. Either way, the offer stands whenever you're ready.",
    },
    "steel-metal": {
        "v1_pain": "Hey, this is Jay with Human Led AI. I work with steel building and barndominium companies in the DFW area. Your projects are big-ticket — barndos, shops, warehouses — and one missed call could be a six-figure job walking to someone else. We built a system that answers every call instantly, qualifies the project, and books the consultation while you're still on the job site. If you're losing big projects to slow callbacks, let's fix that. Give me a call back at your convenience.",
        "v2_social": "Hey, Jay again from Human Led AI. Quick follow-up — we just helped a metal building company near Rockwall stop losing leads to voicemail. He was missing calls during the day and losing out on bids. Now every call gets answered and he's quoting 40% more projects. Same system, takes 15 minutes. Worth a quick look? Give me a call back.",
        "v3_referral": "Hey, Jay one last time. If you've got more projects than you can bid right now, that's a great position. But if you know another steel building company that's losing bids to slow response times, send them my way. I'll take care of you for the referral. Either way, offer stands whenever you're ready.",
    },
}


def generate_audio(text, output_path):
    """Generate audio using ElevenLabs TTS API."""
    url = f"{BASE_URL}/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        size_kb = len(response.content) / 1024
        return True, f"{size_kb:.0f}KB"
    else:
        return False, f"HTTP {response.status_code}: {response.text[:200]}"


def main():
    total = sum(len(scripts) for scripts in SCRIPTS.values())
    generated = 0
    failed = 0
    results = []

    print(f"Generating {total} voice drops across {len(SCRIPTS)} niches...")
    print(f"Voice: Brian ({VOICE_ID})")
    print(f"Output: {OUTPUT_DIR}/")
    print("-" * 60)

    for niche, scripts in SCRIPTS.items():
        niche_dir = os.path.join(OUTPUT_DIR, niche)
        os.makedirs(niche_dir, exist_ok=True)

        for script_name, text in scripts.items():
            filename = f"{niche}_{script_name}_brian.mp3"
            output_path = os.path.join(niche_dir, filename)

            print(f"  [{generated + failed + 1}/{total}] {niche}/{filename}...", end=" ", flush=True)

            success, detail = generate_audio(text, output_path)
            if success:
                generated += 1
                print(f"OK ({detail})")
                results.append({"niche": niche, "file": filename, "status": "OK", "detail": detail})
            else:
                failed += 1
                print(f"FAILED ({detail})")
                results.append({"niche": niche, "file": filename, "status": "FAILED", "detail": detail})

            # Rate limit — be respectful to the API
            time.sleep(1.5)

    print("-" * 60)
    print(f"DONE: {generated} generated, {failed} failed out of {total} total")
    print()

    # Summary table
    print("NICHE SUMMARY:")
    for niche in SCRIPTS:
        niche_results = [r for r in results if r["niche"] == niche]
        ok_count = sum(1 for r in niche_results if r["status"] == "OK")
        print(f"  {niche}: {ok_count}/{len(niche_results)} generated")

    if failed > 0:
        print(f"\nFAILED FILES:")
        for r in results:
            if r["status"] == "FAILED":
                print(f"  {r['niche']}/{r['file']}: {r['detail']}")


if __name__ == "__main__":
    main()
