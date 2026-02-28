import 'package:flutter/material.dart';
import 'package:flutter_pdfview/flutter_pdfview.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'package:flutter/services.dart';

class PdfViewerScreen extends StatefulWidget {
  const PdfViewerScreen({super.key});

  @override
  State<PdfViewerScreen> createState() => _PdfViewerScreenState();
}

class _PdfViewerScreenState extends State<PdfViewerScreen> {
  String? localPdfPath;

  @override
  void initState() {
    super.initState();
    loadPdf();
  }

  Future<void> loadPdf() async {
    final byteData =
        await rootBundle.load('assets/pdfs/sample.pdf');

    final file =
        File('${(await getTemporaryDirectory()).path}/sample.pdf');

    await file.writeAsBytes(byteData.buffer.asUint8List());

    setState(() {
      localPdfPath = file.path;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Legal Report PDF"),
      ),
      body: localPdfPath == null
          ? const Center(child: CircularProgressIndicator())
          : PDFView(
              filePath: localPdfPath!,
            ),
    );
  }
}
