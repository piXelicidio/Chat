# Language File Building Guide

This guide explains how to create a language file for Yiperi Voice.
Use this guide when you need to build or review files in:

```text
Resources/Yiperi-voice/LanguageFiles/<code>.json
```

## Goal

It maps written text to Yiperi's shared sound inventory.

The result should be:

- predictable
- readable in the JSON
- good enough for cartoon speech
- explicit about unsupported writing systems
- strict enough that mistakes are visible


## JSON Shape

Use this shape:

```json
{
  "languageName": "Example",
  "stressRules": [ "DUO-F", "PLU-P" ],
  "rewriteRules": [
    { "match": "ch", "replace": "x" }
  ],
  "exceptions": [
    { "key": "example", "value": [ "e", "ka" ] }
  ],
  "letterNames": [
    { "key": "a", "value": [ "a" ] }
  ],
  "onsetPriority": [ "x", "p", "t", "k", "m", "n", "l", "r", "w", "y", "f", "s" ]
}
```

Only `languageName`, `stressRules`, and `rewriteRules` are mandatory. Keep `exceptions`, `letterNames`, and `onsetPriority` empty or omit them unless you need to override the defaults.

The language code is determined by the filename. For example, `pt.json` is loaded as language code `pt`.

Do not leave `stressRules` empty. Even though the engine falls back to first-syllable stress, defining rules makes your intended rhythm explicit.

## Playable Inventory

All output eventually needs to fit this inventory:

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

The engine only has these consonant families:

```text
p t k f s m n l r w y x
```

Use `x` for noisy front sounds such as `ch`, `sh`, `zh`, `j`, or similar approximations.
Use `y` for glide/soft-palatal sounds.

## Processing Order

For each source word, the engine follows this order:

1. Extract word-like chunks from text.
2. Normalize the word.
3. If the normalized word is a single letter and exists in `letterNames`, use that exact token list.
4. Else if the word exists in `exceptions`, use that exact token list.
5. Else apply `rewriteRules` in order.
6. Convert the rewritten result into canonical units.
7. Convert canonical units into playable tokens.
8. Add optional flavor markers.
9. Pick a stress position and uppercase that token.
10. Add pause tokens from punctuation or word boundaries.

This means:

- `letterNames` beat `exceptions`.
- `exceptions` beat `rewriteRules`.
- `rewriteRules` are sequential and order-sensitive.
- A later rewrite sees the result of earlier rewrites.

## Word Extraction And Dialog Markup

The engine treats letters, digits, and apostrophes as source word characters.
Other punctuation is trailing text.

## Normalization

Before lookup or rewrites, each word is normalized:

- converted to lowercase
- apostrophes are removed
- non-letter and non-digit characters are removed

Unicode letters are preserved, so rules can match letters such as `ñ`, `ü`, Cyrillic, kana, or Devanagari.

## Rewrite Rules

Rewrite rules have this shape:

```json
{ "match": "pattern", "replace": "text" }
```

or:

```json
{ "match": "pattern", "replace": "text", "isRegex": true }
```

Rules are applied to the whole normalized word in file order.

Guidelines:

- Put longer and more specific rules before shorter rules.
- Put script transliteration before broad Latin cleanup.
- Put diacritic removal before rules that expect plain vowels.
- Put digraphs before single letters: `sch` before `ch`, `ch` before `c`.
- Use regex only when it clearly makes the rule easier or more precise.
- Rewrites may replace text with an empty string when a letter should disappear.
- Rewrites should usually produce only `a e i o u p t k f s m n l r w y x`.

Examples:

```json
{ "match": "sh", "replace": "x" },
{ "match": "ch", "replace": "x" },
{ "match": "qu", "replace": "k" },
{ "match": "c(?=[eiy])", "replace": "s", "isRegex": true },
{ "match": "c", "replace": "k" }
```

Digits should be handled per language:

```json
{ "match": "1", "replace": "uno" },
{ "match": "2", "replace": "dos" }
```

If a language's native characters do not map directly to pronunciation, use romanized speech text and document it.

## Canonical Units

After rewrites, the engine scans characters one by one.

Vowels are hardcoded in the engine as the shared playable vowels:

```text
a e i o u
```

Rewrite language-specific vowel letters such as `á`, `ü`, `ö`, or `ā` to shared vowels first.

Consonants are mapped like this:

```text
b p -> p
d t -> t
k q g -> k
f v -> f
s z -> s
m -> m
n -> n
l -> l
r -> r
w -> w
y -> y
x -> x
```

Any other character left after rewrites is ignored. While this helps filter unsupported script characters, don't rely on silent dropping as a feature. Clearly document unsupported inputs or handle them in the demo text.

Consecutive vowels collapse into one canonical vowel unit.
For example, `aa` or `ou` will not create two separate playable vowel beats unless a rewrite inserts a consonant or glide between them.
Use this intentionally for broad long-vowel approximation, not for exact syllable timing.

## Token Building

The engine builds roughly one playable token per vowel.

For each vowel, it looks at the consonant cluster before that vowel and chooses one onset.
The chosen onset plus the vowel creates the token:

```text
k + a -> ka
x + o -> xo
no onset + a -> a
```

If there are multiple consonants before a vowel, `onsetPriority` decides which one wins.

Default priority:

```json
[ "x", "p", "t", "k", "m", "n", "l", "r", "w", "y", "f", "s" ]
```

Example:

```text
strange -> s t r a ...
```

Only one onset can be used for the `a`.
The priority decides whether that sounds closer to `ta`, `ra`, etc.

Trailing consonants are usually dropped because they do not lead into a vowel.
Optional flavor markers can still add final `s`, `n`, or `r`.

If a rewritten word has no vowels, the engine falls back to one support token, usually based on the first consonant plus `a`.

## Flavor Markers

When enabled by the caller, the engine adds extra tokens for:

- leading `s` before a consonant cluster
- final `s`
- final `n`
- final `r`

These markers are toon-style flavor, not exact pronunciation.
They are excluded from stress selection.

If a language has many words ending in `n` or `r`, be aware that this creates extra final marker sounds.
Use rewrite rules or exceptions when that feels too strong.

## Stress Rules

Stress changes playback variation by uppercasing one playable token.
The voice player can use stressed clip variants for uppercase tokens.

Available rules:

```text
MARK
FIRST
PENULT
LAST
ANTE
DUO-F
PLU-P
```

Meaning:

- `MARK`: stress the vowel marked with an accent in the original `say` word.
- `FIRST`: stress the first syllable.
- `PENULT`: stress the second-to-last syllable.
- `LAST`: stress the last syllable.
- `ANTE`: stress the third-to-last syllable.
- `DUO-F`: if the word has exactly 2 syllables, stress the first.
- `PLU-P`: if the word has 3 or more syllables, stress the second-to-last.

Rules are tried in order.
The first rule that can produce a position wins.
If no rule produces a position and the word has at least 2 syllables, the engine stresses the first syllable.
One-syllable words are not stressed.

Recommended choices:

```json
"stressRules": [ "DUO-F", "PLU-P" ]
```

Good general-purpose cartoon rhythm.

```json
"stressRules": [ "MARK", "PENULT" ]
```

Good for languages with written stress marks or tone marks that should influence variation, followed by a simple fallback.

```json
"stressRules": [ "FIRST" ]
```

Good for a language where first-syllable stress is a reasonable broad approximation.

```json
"stressRules": [ "LAST" ]
```

Good for a language where final stress gives a better broad rhythm.

Don't worry about perfect linguistic stress if the language uses pitch accent, tones, or complex rules. Pick a simple rule set that creates pleasant variation and document the approximation.

## Exceptions

Exceptions map exact normalized words to exact playable tokens:

```json
{ "key": "one", "value": [ "wa" ] }
```

Use exceptions for:

- very common irregular words
- particles or short function words
- words where rewrite rules produce bad results
- demo phrases that must sound stable

Exception values must use playable tokens only.
They cannot contain arbitrary letters.

If this is not wanted, use the `[Display<>Say]` markup to separate the display spelling from the voice playback spelling.

## Letter Names

`letterNames` handles a single-character word before exceptions and rewrite rules.

Example:

```json
{ "key": "x", "value": [ "e", "ku", "su" ] }
```

Use this for spelling, acronyms, and standalone letters.
Values must use playable tokens only.

Do not add the shared vowel keys `a`, `e`, `i`, `o`, or `u` to `letterNames`.
Single-character `letterNames` entries are handled before exceptions and rewrite rules, so vowel entries would turn common one-letter words into spelling/acronym output.
Use `exceptions` or normal rewrite behavior for vowel words instead.

If a language has no useful native letter names for the expected input, it is acceptable to leave this empty.
For Latin-script languages, include at least common Latin letters.

## Non-Latin Scripts

There are three ways to support non-Latin scripts:

Raw script support:
Use direct rewrite rules when characters mostly map to sounds.
Good examples: Cyrillic, Greek, kana.

Romanized support:
Require the speech side to use Latin pronunciation text.
Good examples: Chinese pinyin, Japanese romaji for kanji, Arabic when vowels are omitted.

Mixed support:
Support the easy script subset directly, and require markup for the hard subset.
Language files are meant for text where a relatively small character set maps roughly to the shared token inventory.
Do not try to map huge character sets, such as Japanese kanji, directly into the language file.
For more complex readings or custom symbol constructions, the engine supports `[Display<>Say]`: the UI shows the display text, while the engine processes the say text through the language file.
Japanese currently follows this pattern:

```text
romaji: supported
hiragana: supported
katakana: supported
kanji: use [Display<>Say]
```

## Validation Checklist

- The filename is `Resources/Yiperi-voice/LanguageFiles/<code>.json`.
- `languageName` is present and not blank.
- No `.meta` file was created manually.
- JSON parses.
- `stressRules` is defined and not empty.
- Every `exceptions` value token is playable.
- Every `letterNames` value token is playable.
- Rewrite rules are ordered from specific to general.
- Digits are handled.
- Unsupported scripts are documented or handled via `[Display<>Say]`.
- The rules do not attempt to guess readings they cannot determine.

## Minimal Template

```json
{
  "languageName": "Example",
  "stressRules": [ "DUO-F", "PLU-P" ],
  "rewriteRules": [
    { "match": "0", "replace": "zero" },
    { "match": "1", "replace": "one" },
    { "match": "2", "replace": "two" },
    { "match": "3", "replace": "three" },
    { "match": "4", "replace": "four" },
    { "match": "5", "replace": "five" },
    { "match": "6", "replace": "six" },
    { "match": "7", "replace": "seven" },
    { "match": "8", "replace": "eight" },
    { "match": "9", "replace": "nine" }
  ],
  "exceptions": [],
  "letterNames": [],
  "onsetPriority": [ "x", "p", "t", "k", "m", "n", "l", "r", "w", "y", "f", "s" ]
}
```
