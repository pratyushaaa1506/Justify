import 'package:flutter/material.dart';

class LegalCentersScreen extends StatelessWidget {
  const LegalCentersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Legal Aid Centers'),
      ),
      body: const Center(
        child: Text(
          'Legal aid centers screen coming soon',
          style: TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
