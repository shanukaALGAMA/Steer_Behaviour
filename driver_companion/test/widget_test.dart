import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:driver_companion/main.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const DriverCompanionApp());
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
