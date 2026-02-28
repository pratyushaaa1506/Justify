import 'package:flutter/material.dart';

class SummaryScreen extends StatelessWidget {
  const SummaryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Case Summary"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            // CATEGORY
            const Text(
              "Category",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            const Text("Tenant / Landlord Dispute"),
            const SizedBox(height: 16),

            // LAWS
            const Text(
              "Applicable Laws",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            const Text("• Rent Control Act\n• Transfer of Property Act"),
            const SizedBox(height: 16),

            // STEPS
            const Text(
              "Recommended Steps",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            const Text(
              "1. Collect rent receipts\n"
              "2. Send legal notice\n"
              "3. Approach Rent Tribunal",
            ),
            const SizedBox(height: 16),

            // SCHEMES
            const Text(
              "Government Schemes",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            const Text("• Free Legal Aid Services\n• District Legal Services Authority"),
          ],
        ),
      ),
    );
  }
}
