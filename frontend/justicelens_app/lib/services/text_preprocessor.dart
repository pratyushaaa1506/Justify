class TextPreprocessor {
  // Common useless words
  static final List<String> stopWords = [
    'is',
    'am',
    'are',
    'the',
    'a',
    'an',
    'and',
    'or',
    'to',
    'of',
    'in',
    'on',
    'with',
    'for',
    'i',
    'my',
    'me'
  ];

  static String preprocess(String input) {
    // 1. Convert to lowercase
    String text = input.toLowerCase();

    // 2. Remove special characters & emojis
    text = text.replaceAll(RegExp(r'[^\w\s]'), '');

    // 3. Tokenize (split sentence into words)
    List<String> tokens = text.split(' ');

    // 4. Remove stopwords
    tokens = tokens
        .where((word) => word.isNotEmpty && !stopWords.contains(word))
        .toList();

    // 5. Join back into sentence
    return tokens.join(' ');
  }
}
