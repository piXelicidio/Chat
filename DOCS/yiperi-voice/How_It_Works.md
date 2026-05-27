# What is Yiperi-voice engine?

A lightweight dialogue voice engine for cartoon, retro, and funny speech effects in Unity.

Yiperi turns written dialogue into a small, predictable sequence of playable voice tokens.
As text appears on screen, those tokens add a simple speech-like cadence without full voice acting or heavy runtime systems.

The project is built for offline, real-time playback in Unity. It maps different languages into one shared stylized voice inventory, so multilingual dialogue can keep a consistent sound.

## How It Works

- **Text Analysis**: `SpeechEngine` parses the dialogue text into words, tokens, pauses, and stress markers.
- **Language Mapping**: JSON files in `Resources` define how specific languages map written text to the shared Yiperi inventory.
- **Playback**: `VoicePlayer` loads the voice clips matching the `VoiceProfile` config, plays them, and triggers word/token/viseme callbacks.


Language-specific data lives in:

```text
Resources/Yiperi-voice/LanguageFiles/<code>.json
```

For language-file details, use [Language_File_Guide.md](Language_File_Guide.md).

## Shared Voice Inventory

All languages map into this shared playback inventory:

```text
a e i o u
s n r

pa pe pi po pu
ta te ti to tu
ka ke ki ko ku
fa fe fi fo fu
sa se si so su
ma me mi mo mu
na ne ni no nu
la le li lo lu
ra re ri ro ru
wa we wi wo wu
ya ye yi yo yu
xa xe xi xo xu
```

Total playable tokens: `68`

`y` is the internal and playable symbol for glide or soft-palatal sounds.
`x` is the internal and playable symbol for narrow noisy front sounds such as `ch`, `sh`, and `zh`.

The inventory was originally designed around English and Spanish phonetics, but isn't strict.
You can record different voice banks with unique characters/styles as long as the file names match.

## Languages

Language support lives in `Resources/Yiperi-voice/LanguageFiles`.
See [Languages.md](Languages.md) for current language notes and support status.
See [Language_File_Guide.md](Language_File_Guide.md) for creating or reviewing language files.

## Project Layout

```text
Scripts/
  SpeechEngine.cs          Core text-to-token logic.
  LanguageLoader.cs        Language JSON loading, validation, and caching.
  LanguageUtilities.cs     Script prepass helpers for supported languages.
  VoicePlayer.cs           Clip loading, timing, playback, and callbacks.
  VoiceProfile.cs          Runtime voice config.
  DialogPiece.cs           Parsed dialogue line piece.
  SimpleDialogPlayer.cs    Simple dialogue playback component.
  OverlayConsole.cs        Optional in-game console for demo/debug text.

Resources/Yiperi-voice/
  LanguageFiles/
    <code>.json            Language rewrite, exception, stress, and letter-name data.

  Sounds/
    voice_<code>/          Normal clips for one voice bank.
      a.wav
      pa.wav
      ...

      stress/              Optional stressed variants using the same file names.
        pa.wav
        ...

Documentation/
  Languages.md            Language notes and support status.
  Language_File_Guide.md  Language file authoring guide.

Demos/
  Demo-1-Dialog.unity     Dialogue showcase scene.
  Demo-2-minimal.unity    Minimal playback scene.
  Demo-3-Voices.unity     Voice bank showcase scene.

  Demo-only-assets/
    Data/                 Demo dialogue text files.
    ScriptsAndPrefabs/
      DemoDialog.cs       Sample driver for Demo-1-Dialog.unity.
      DemoMinimal.cs      Sample driver for Demo-2-minimal.unity.
      DemoVoices.cs       Sample driver for Demo-3-Voices.unity.
```

Unity `Resources` paths are used directly by the loader, so these folder names matter.
Voice folders are named with the value used by `VoiceProfile.VoiceCode`, for example:

```text
Resources/Yiperi-voice/Sounds/voice_neni
```

