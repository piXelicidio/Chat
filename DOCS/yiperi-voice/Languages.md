# Languages

Language files live in:

```text
Resources/Yiperi-voice/LanguageFiles
```

This file keeps short notes about current language support.
For creating or reviewing language files, use [Language_File_Guide.md](Language_File_Guide.md).

## Current Languages

- `en`: reference language and the most tuned file.
- `de`: German approximation using Unicode-preserving normalization and rewrite rules.
- `cz`: Czech approximation handling syllabic r/l, palatalization of ě, vowel/glide swaps, and native letter/digit pronunciation.
- `es`: Spanish approximation around glide and `x`-family tuning.
- `fr`: broad French approximation using shared vowels, `x`, and spelling rewrites.
- `hi`: Hindi romanized approximation with digit names, diacritic cleanup, and common-word exceptions. `[display<>say]` is mandatory when displaying Devanagari text.
- `ja`: Japanese approximation for romaji, hiragana, and katakana. `[display<>say]` is recommended for kanji text.
- `ko`: Korean approximation for Hangul and romanized Korean. Hangul is romanized by a small utility pass before language-file rewrites, then folded into the shared cartoon voice inventory.
- `nl`: Dutch approximation with hard `g/ch/sch` folded into `x`, vowel digraph cleanup, common-word exceptions, digit names, and Latin letter names.
- `pt`: Portuguese approximation with accent cleanup, nasal-ending rewrites, common-word exceptions, and Latin letter names.
- `ru`: Russian approximation for Cyrillic text, with broad Latin transliteration cleanup.
- `th`: Thai Romanized approximation using phonetic Karaoke Thai (spelled how it sounds, e.g., `kan` instead of orthographic `kar`), handling consonant aspirations (ph, th, kh), diphthong splitting (ai, ao, ia, ua), and digit/letter pronunciations. `[display<>say]` is mandatory when displaying Thai characters.
- `tr`: Turkish approximation with final-syllable stress, Turkish character cleanup, soft `ğ` handling, common-word exceptions, digit names, and Latin/Turkish consonant letter names.
- `yiperi`: language-neutral Yiperi phonetic input. This intentionally boring file has no rewrite rules, exceptions, or letter names, so developers can write Yiperi-like text directly, such as `li popo te fefa si mofe mu riku`, and let the normal engine tokenize it.
- `zh`: Mandarin pinyin approximation that strips tone marks/numbers and folds pinyin into the shared inventory. `[display<>say]` is mandatory when displaying Chinese characters.


## Note about [Display<>Say] Sintax:

Dialog can use `[display<>say]` when the text shown to the player should be different from the text processed by Yiperi. For example, the UI can show native writing while the engine reads a romanized or pronunciation-friendly version.
