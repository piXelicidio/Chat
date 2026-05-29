# Getting Started with Yiperi Voice

**Yiperi Voice** is a lightweight speech engine for Unity. It turns text into a sequence of retro, cartoonish, or stylized gibberish speech sounds in real-time. It is not intended to be a full dialogue management system—it is simply a text-to-voice player.

This guide covers the core API required to get speech playing in your game using your own custom scripts.

---

## Minimal Setup

The engine works by loading a voice bank into memory, analyzing your string of text into a predictable sequence of phonetic tokens, and playing them through an `AudioSource`.

Here is the minimal script required to play speech. This example requires a GameObject with an `AudioSource` attached:

```csharp
void Start()
{
    var audioSource = GetComponent<AudioSource>();

    // 1. Load the voice bank into memory ("neni" in Resources)
    VoicePlayer.LoadVoice("neni");

    // 2. Configure playback settings
    var profile = new VoiceProfile 
    { 
        VoiceCode = "neni", 
        Speed = 1f 
    };

    // 3. Analyze the text into Yiperi's playable tokens
    var text = SpeechEngine.AnalyzeText("Hello world!", "en");

    // 4. Play it!
    StartCoroutine(VoicePlayer.PlaySpokenText(audioSource, profile, text, null, OnWordRevealed));
}

private void OnWordRevealed(SpeechEngine.SpokenWord word)
{
    // (Optional) Fires as each word is spoken.
    // Useful for showing text word-by-word.
    Debug.Log("Spoke: " + word.Display);
}
```

## Demos

The quickest way to understand the engine is to review the included demo scenes inside `Demos/`:

1. **Demo-2-minimal.unity**: Shows the script above in action. It is the best starting point for integrating Yiperi into your own custom UI or systems.
2. **Demo-1-Dialog.unity**: A showcase of two animated 3D characters conversing. The demo itself acts as a tutorial, explaining how the speech system works as the characters talk.
3. **Demo-3-Voices.unity**: A showcase demonstrating the 12 available voices and 20 supported languages.

**NOTE**: If Text Mesh Pro isn't already installed in you project you must install TMP Essensial in order to see the UI texts in the demos.

## Next Steps

- Understand how it works: [How_It_Works.md](How_It_Works.md)
- Read [Languages.md](Languages.md) to see supported languages.
- View available voice styles: [Voices.md](Voices.md)
- Create your own voices: [Adding_Custom_Voices.md](Adding_Custom_Voices.md)
- Learn how to configure language files: [Language_File_Guide.md](Language_File_Guide.md)
