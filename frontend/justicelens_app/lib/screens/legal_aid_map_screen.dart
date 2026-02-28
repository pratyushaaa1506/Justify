import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class LegalAidMapScreen extends StatefulWidget {
  const LegalAidMapScreen({super.key});

  @override
  State<LegalAidMapScreen> createState() => _LegalAidMapScreenState();
}

class _LegalAidMapScreenState extends State<LegalAidMapScreen> {
  late GoogleMapController mapController;

  final LatLng _initialPosition =
      const LatLng(17.385044, 78.486671); // Hyderabad

  final Set<Marker> _markers = {
    const Marker(
      markerId: MarkerId("center1"),
      position: LatLng(17.387140, 78.491684),
      infoWindow: InfoWindow(title: "District Legal Services Authority"),
    ),
    const Marker(
      markerId: MarkerId("center2"),
      position: LatLng(17.370000, 78.480000),
      infoWindow: InfoWindow(title: "Free Legal Aid Center"),
    ),
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Legal Aid Centers"),
      ),
      body: GoogleMap(
        initialCameraPosition: CameraPosition(
          target: _initialPosition,
          zoom: 13,
        ),
        markers: _markers,
        onMapCreated: (controller) {
          mapController = controller;
        },
      ),
    );
  }
}
