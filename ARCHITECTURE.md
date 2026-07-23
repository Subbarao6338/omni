# 📐 Omni Web Browser & Toolbox Architecture Documentation

This document describes the high-level architecture, directory layout, technical capabilities, design patterns, and core security modules implemented in the **Omni Web Browser & Toolbox** Android application.

---

## 🏛️ 1. Architectural Overview & Design Patterns

Omni Web Browser is built from the ground up as a fully modern Android application using **100% Kotlin**, **Jetpack Compose** for native UI rendering, and the **MVVM (Model-ViewModel-View)** architecture pattern.

```
       ┌────────────────────────────────────────────────────────┐
       │                      View (UI)                         │
       │  (Jetpack Compose Screens: BrowserView, HomeView, etc) │
       └──────────────────────────┬─────────────────────────────┘
                                  │  User Interactions (Intent)
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │                   ViewModel                            │
       │  (BrowserViewModel, OmniViewModel, NoteViewModel, etc) │
       └──────────────────────────┬─────────────────────────────┘
                                  │  Repository / Database Flow
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │                     Model (Data)                       │
       │    (Room AppDatabase, SharedPreferences, API Assets)   │
       └────────────────────────────────────────────────────────┘
```

### **Core Design Principles**
- **Model-ViewModel-View (MVVM)**: Separates the presentation logic from database persistence and background processing, facilitating responsive user interfaces and testability.
- **Unidirectional Data Flow (UDF)**: View states are exposed via Kotlin's `StateFlow` and Compose state properties, while user intents are dispatched back via ViewModel method calls.
- **Type-Safe Navigation**: Custom screen destinations and argument passes are managed cleanly using `Jetpack Navigation Compose`.
- **Resource/Dependency Externalization**: Build version numbers and libraries are maintained globally within `variables.gradle`.

---

## 📂 2. Repository & Source Tree Organization

```
Omni-Web/
├── app/
│   ├── src/main/java/omni/
│   │   ├── browser/                     # 🌍 Web Browser Module
│   │   │   ├── data/                    # Room DB schemas, DAOs (AppDatabase.kt)
│   │   │   ├── discovery/               # Feed managers and RSS utilities
│   │   │   ├── ui/                      # Browser UI views, Compose layouts, BrowserViewModel.kt
│   │   │   └── util/                    # Helper components (AdBlockManager, CryptoUtils, UrlUtils)
│   │   └── toolbox/                     # 🧰 General Utility Module
│   │       ├── service/                 # System tile services and foreground tasks
│   │       ├── ui/                      # Interactive tool dashboards, menus & styling
│   │       └── viewmodel/               # ViewModels managing specific sub-utility configurations
│   ├── src/main/res/                    # Android resources (Layouts, Drawables, XML metadata)
│   └── src/main/assets/                 # Locally bundled javascript and diagnostic files
├── build.gradle                         # Project-level configuration
├── settings.gradle                      # Module declarations
└── variables.gradle                     # Dependency & Version management
```

---

## 🌍 3. Web Browser Module & WebView Enhancements

The browser module offers high-performance browsing utilizing Android's System WebView, supplemented with powerful customization and analysis tools.

### **Profile Isolation**
- **Isolated Cookiestores & LocalStorage**: Supported dynamically using standard WebView features to switch between user profiles (e.g., *Default, Personal, Work, Private, Social*). Each profile features decoupled sessions and badge identifiers on the interface.

### **Ad and Tracker Blocking**
- **Trie-based Prefix Filter**: Optimizes categorizations of tracking requests (*Ad*, *Analytics*, *Social*, *Malware*).
- **Fast-Path Bloom Filter**: Features custom-coded, low-overhead Bloom Filters checking incoming URLs against standard hosts files prior to hitting the fallback Trie.

### **Content Extractions & Utilities**
- **Media Grabber**: Monitors assets (images, audio, video) inside active web pages, allowing direct downloads via the custom `OmniDownloadManager`.
- **Page Summarizer**: Integrated with the **Google Gemini API** (Generative AI SDK) to summarize active pages or run diagnostic chat assistance directly within the app.

---

## 🧰 4. Omni Toolbox & General Utilities

The multi-tool Toolbox delivers dozens of highly practical utilities organized into categorized dashboards.

### **Symmetric AES Cryptography**
- Supports secure AES encryption/decryption of local text blobs and files.
- Upgraded to robust **AES-CBC ciphers** featuring securely generated random 16-byte Initialization Vectors (`SecureRandom`) prepended to ciphertexts, and password key derivation via SHA-256.

### **Real-time App Locker**
- Integrates with Android's `PackageManager` to safely retrieve user and system package names.
- Saves locker preferences persistently inside `SharedPreferences` to secure unauthorized application access.

### **Native Diagnostic Security Scan**
- Scans system development configurations directly via local hardware and system properties.
- **Audited Metrics**: Developer Options status, ADB/USB debugging state, presence of `su` binary execution flags on the filesystem, Cleartext network permissions (`NetworkSecurityPolicy`), and active Location/GPS hardware providers.

---

## ⚡ 5. Performance & Composition Optimizations

To ensure an ultra-responsive interface, the codebase enforces several strict performance optimizations:

1. **State Collection Optimization**: Standard list allocations backed by standard state containers are replaced with Compose-native primitive states (`mutableIntStateOf`, `mutableFloatStateOf`) and snapshot-aware collections (`mutableStateListOf`) to drastically cut down autoboxing overhead and redundant layouts.
2. **Avoiding Static Field Leaks**: View references (such as `WebView`) are kept clear of static declarations or raw ViewModel properties. When prewarmed web elements are handled inside the VM, they are wrapped within the Application Context lifecycle to avoid activity leaks.
3. **Locale-Aware Formatting**: Explicit formatting locales (`Locale.getDefault()`) are supplied throughout the application's utilities, guaranteeing translation-safe UI updates.

---

## 🧪 6. Testing & Quality Control

Our codebase includes a comprehensive, JVM-based unit testing suite to verify the application's critical systems without physical hardware:

- **Mathematical Calculations**: Verified via local unit test deltas (e.g., barometric forecasting histories, mathematical converter scales, Minesweeper generation maps).
- **Domain & Address Parsing**: Validated using extensive unit tests for `UrlUtils` to confirm edge-case URL formats and bang shortcuts.
- **Bloom Filters**: Tests correct element inclusion rates and validates bounds on false-positives.
- **Hosts File Extraction**: Assures accurate stripping of standard comments and invalid IP declarations.

**Command to run Unit Tests locally**:
```bash
./gradlew :app:testStableUnitTest
```

**Command to execute Android Lint checks**:
```bash
./gradlew lintStable
```
