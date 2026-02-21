# Transcript Extractor Skill

## What It Does
Extracts transcripts from any video URL (YouTube, Instagram, Twitter, TikTok, etc.) using the SuperData API. Allows the agent to pull video content as text for analysis, reference, or storage in Notion.

## Why It's Useful
- Pull competitor content for voice/style analysis
- Extract your own content library for reference
- Build context libraries (e.g., "Callaway short form scripts")
- Avoid sketchy websites with ads/viruses
- Works across ALL major platforms (not just YouTube)

## How to Set Up

### 1. Get SuperData API Key
- Go to: https://superdata.app
- Sign up (free tier or $15/mo for 3,000 pulls)
- Copy your API key from the dashboard

### 2. Store the Key
Tell the agent:
```
I want to create a skill that extracts content transcripts on all platforms. 
Please search SuperData API and learn what you can do with this.
Then I'll give you my API key and you should create a skill that allows you to 
always extract any transcript from the platforms that SuperData allows.
I'll give you the key below. Do research in the meantime.
```

Then paste:
```
Here is the key: [YOUR_API_KEY]

Fully create and test this skill. I want you to always use this when video 
content is useful. Transcripts provide great context.
```

### 3. Test It
Reset the chat, then:
```
Please summarize this video: [VIDEO_URL]
Then add a document to your notebook in Notion explaining it.
Please at the bottom include the full transcript for the video.
```

The agent should:
- Pull the transcript via SuperData
- Summarize the content
- Create a Notion doc with summary + full transcript
- Return a clickable link to the doc

## Usage Examples

**Build a style reference:**
```
Please create a Notion page in your notes and extract these scripts 
so that we can reference them later:
- [URL 1]
- [URL 2]
- [URL 3]

Put them in Notion.
```

**Quick analysis:**
```
Extract the transcript from this video and tell me the 3 main takeaways:
[URL]
```

**Content library:**
```
Pull transcripts for my 10 most recent YouTube videos and store them 
in a Notion page titled "My Content Voice Reference"
```

## Supported Platforms
- YouTube
- Instagram (Reels, IGTV)
- Twitter/X
- TikTok
- Facebook
- LinkedIn

## Cost
- SuperData: ~$15/mo for 3,000 transcript pulls
- Works out to $0.005 per transcript
- Free tier available for testing

## Tips
- **Always give the agent the Notion link preference:** "Please always give me the link to the notion doc when you create one"
- **Pair with Notion skill** for automatic storage
- **Name your reference docs clearly** so the agent can find them later
- **Tag docs with "when to use"** descriptions for future context

## From Riley Brown Video
Source: https://youtu.be/ryhzpLe9O_U (Skill #4 in his 7 OpenClaw Skills breakdown)

Quote: "Since I already know that with the SuperData API, I created a skill that now pulls the transcript from any video on social media... the most important thing with AI agents is making sure that you collect a ton of relevant context."

