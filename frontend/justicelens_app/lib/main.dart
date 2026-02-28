import 'package:flutter/material.dart';
import 'screens/chat_screen.dart';

void main() {
  runApp(const JusticeLensApp());
}

class JusticeLensApp extends StatelessWidget {
  const JusticeLensApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'JusticeLens',
      theme: ThemeData(primarySwatch: Colors.indigo),
      home: const ChatScreen(),
    );
  }
}
