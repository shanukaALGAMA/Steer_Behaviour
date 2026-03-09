import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/profile_provider.dart';
import 'screens/dashboard_screen.dart';
import 'screens/settings_screen.dart';

void main() {
  runApp(const DriverCompanionApp());
}

class DriverCompanionApp extends StatelessWidget {
  const DriverCompanionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Driver Companion',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6C63FF),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
        fontFamily: 'Roboto',
      ),
      home: const _AppRoot(),
    );
  }
}

class _AppRoot extends StatefulWidget {
  const _AppRoot();
  @override
  State<_AppRoot> createState() => _AppRootState();
}

class _AppRootState extends State<_AppRoot> {
  // Default host — user can change via settings
  String _host = '192.168.1.100:8765';
  ProfileProvider? _provider;

  @override
  void initState() {
    super.initState();
    _provider = ProfileProvider(_host);
  }

  void _onHostChanged(String newHost) {
    _provider?.dispose();
    setState(() {
      _host = newHost;
      _provider = ProfileProvider(newHost);
    });
  }

  @override
  void dispose() {
    _provider?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider.value(
      value: _provider!,
      child: _MainNav(host: _host, onHostChanged: _onHostChanged),
    );
  }
}

class _MainNav extends StatefulWidget {
  final String host;
  final void Function(String) onHostChanged;
  const _MainNav({required this.host, required this.onHostChanged});

  @override
  State<_MainNav> createState() => _MainNavState();
}

class _MainNavState extends State<_MainNav> {
  int _index = 0;

  @override
  Widget build(BuildContext context) {
    final screens = [
      const DashboardScreen(),
      SettingsScreen(
        currentHost: widget.host,
        onHostChanged: widget.onHostChanged,
      ),
    ];

    return Scaffold(
      body: screens[_index],
      bottomNavigationBar: NavigationBar(
        backgroundColor: const Color(0xFF0D1220),
        indicatorColor: const Color(0xFF6C63FF).withAlpha(64),
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.dashboard_outlined),
            selectedIcon: Icon(Icons.dashboard, color: Color(0xFF6C63FF)),
            label: 'Dashboard',
          ),
          NavigationDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings, color: Color(0xFF6C63FF)),
            label: 'Settings',
          ),
        ],
      ),
    );
  }
}
