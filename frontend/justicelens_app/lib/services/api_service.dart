import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Change this when backend is live
  static const String baseUrl = 'http://127.0.0.1:8000';

  static Future<String> preprocessText(String processedText) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/preprocess'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'text': processedText,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['processed_text'];
      } else {
        return 'Error: Backend failed';
      }
    } catch (e) {
      // Backend not running yet — fallback
      return processedText;
    }
  }
}
