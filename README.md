# 🌐 Omni Web Browser & Toolbox (Android)

A powerful, feature-rich web browser and multi-tool utility suite for Android built using Kotlin, Jetpack Compose, and the Google Gemini API. Browse the web, extract content, run native privacy/security audits, and leverage state-of-the-art offline utilities—all in a modern mobile interface.

## ✨ Features

- **🔍 Web Browsing** - High-performance browsing powered by Android System WebView
- **🤖 AI-Powered Analysis** - Leverage Google Gemini API for intelligent content analysis, text parsing, and page summaries
- **🎨 Beautiful Visual Customization**:
  - Supports multiple custom design palettes: **Default (Epic Indigo/Slate)**, **Earth** (warm terracotta/beige), **Forest** (sage/moss green), **Water** (ocean blue/cyan), and **Sand** (amber/gold).
  - Perfect Light/Dark system synchronization across the entire web browser, settings panel, and toolbox utility screens, with deeply synchronized accent colors, backgrounds, and elements.
- **🛡️ Secure Privacy Shield**:
  - **AES-256 Text & File Symmetric Cipher** - Encrypt and decrypt raw text or local files with custom passwords and save output locally.
  - **Real App Locker** - Inspect real user-installed apps and toggle persistent locked configurations saved in SharedPreferences.
  - **Live Permission Monitor** - View requested runtime permissions for the package and request or revoke them dynamically.
  - **Native Privacy Scan Audit** - Analyzes Developer Settings, ADB/USB debugging state, Root su binaries, Location/GPS status, and Cleartext traffic security policies.
- **📄 Multiple View Modes**:
  - 🌍 Normal browsing mode
  - 📖 Reader mode for distraction-free reading
  - 💻 Source code viewer
  - 🔄 Markdown conversion
- **🎯 Media Detection** - Automatically detect and extract images, videos, and audio (Media Grabber)
- **🚫 Ad Blocking** - Built-in domain-based ad and tracker blocker
- **📸 Screenshot & PDF Export** - Capture web pages and export as PDF or Full Page Screenshots
- **⚡ High Performance** - Modern Jetpack Compose UI with efficient state management
- **📑 Tab Management** - Multiple tabs, recently closed tabs restoration, and tab hibernation
- **🏠 Custom Homepage** - Configure a custom start page (e.g., Google or GitHub) or use the rich, interactive built-in dashboard
- **👥 Multi-Profile Browsing** - Create, delete, and switch custom browser profiles dynamically (e.g., Default, Personal, Work, Private, Social). Each profile features isolated cookies, LocalStorage, and web storage session states, with color-coded status badges in the address bar
- **⚙️ Unified Toolbox Settings** - Completely integrated and unified Settings panel. All duplicate configuration menus have been merged into a single Settings pane, and the Toolbox now supports a persistent, native bottom navigation bar for a seamless app experience
- **📐 Edge-to-Edge Layout Optimizations** - Corrected system status bars and navigation bar insets, completely eliminating double paddings or extra spacing issues at the top and bottom of loaded websites for a gorgeous visual layout

## 🚀 Quick Start

### Prerequisites
- Android Studio Ladybug | 2024.2.1 or newer
- JDK 21
- Android SDK 35 (API 35)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Subbarao6338/Omni-Web.git
cd Omni-Web
```

2. **Generate consistent Keystore**
Both the debug and stable releases share the exact same signing config to prevent reinstallation for updates. Generate the keystore file at `app/debug.keystore`:
```bash
keytool -genkey -v -keystore app/debug.keystore -alias androiddebugkey -storepass android -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Android Debug,O=Android,C=US"
```

3. **Build Stable Release**
```bash
./gradlew assembleStable
```

4. **Run on Device/Emulator**
```bash
./gradlew installStable
```

## 🏗️ Project Structure

```
Omni-Web/
├── app/
│   ├── src/main/java/omni/
│   │   ├── browser/       # Web browser UI, settings, and main activities
│   │   └── toolbox/       # All general utilities, sensors, and navigation
│   │       ├── ui/screens # Custom utility layouts (AI, calculation, security, etc.)
│   │       └── ui/theme   # Shared styling, material typographies, and color palettes
│   └── src/main/res/      # Android resources (drawables, layouts, values)
├── build.gradle           # Project-level build configuration
├── settings.gradle        # Project settings
└── variables.gradle       # Version management for dependencies
```

## 🔧 Tech Stack

- **UI Framework**: Jetpack Compose (Material 3)
- **Language**: Kotlin
- **Database**: Room Persistence Library
- **Navigation**: Jetpack Navigation Compose
- **Network/Web**: Android WebView, OkHttp
- **AI**: Google Generative AI SDK
- **Media**: youtube-dl-android for video extraction support
- **Export**: Zxing for QR Codes, Android Print Framework for PDF

## 🧪 Testing

The repository contains extensive test coverage including custom cryptographic file encoders, text structural extractors, barometric weather prediction tendency algorithms, and storage calculators.

Run the unit tests:
```bash
./gradlew :app:testStableUnitTest
```

## 📈 Quality of Improvements (Log)

We continuously optimize, refine, and add new capabilities to the Omni Web Browser & Toolbox. Here is the detailed log of the latest quality improvements, optimizations, and additions:

1. **State Mutation & Compose Optimization**:
   - **File**: `WeatherPredictionScreen.kt`
   - **Improvement**: Replaced `mutableStateOf(mutableListOf(...))` with Compose-native `mutableStateListOf<PressureReading>()` to eliminate state notification bugs, improve recomposition performance, and resolve Android Lint's `MutableCollectionMutableState` warnings.

2. **Obsolete SDK Code Cleanup**:
   - **Files**: `AppDecompilerScreen.kt`, `AutomationService.kt`, `MainActivity.kt`, `PageToolsSheet.kt`, `ShortcutUtils.kt`, `YoutubeForegroundService.kt`
   - **Improvement**: Cleaned up obsolete Oreo (API 26) version checks (`Build.VERSION.SDK_INT >= Build.VERSION_CODES.O`) across all identified source files, since our `minSdkVersion` is 26. This streamlines logic and eliminates `ObsoleteSdkInt` warnings.

3. **Resource Folder & Layout Optimization**:
   - **Directories**: Relocated resources from obsolete folders (`drawable-v24` and `mipmap-anydpi-v26`) into their non-version-qualified directories (`drawable` and `mipmap-anydpi` respectively). This resolves folder configuration warnings and simplifies project structure.
   - **Files**: `ToolGroupScreen.kt`, `PerchanceHubScreen.kt`
   - **Improvement**: Optimized the item layout within subtools list view in the Omni toolbox by converting standard static trailing spacers into list-index-conditional spacers. This successfully eliminates the unwanted extra whitespace gaps and vertical offsets after the last subtool card in each section, rendering a highly polished, tight, and professional user interface.

4. **Robust Barometric Forecasting Unit Tests**:
   - **File**: `WeatherPredictionTest.kt`
   - **Addition**: Implemented a new, high-quality JUnit test suite verifying the weather prediction barometric tendencies (Storm Warning, Gale Warning, Deteriorating, Stable, Improving, etc.) and confirming mathematical delta-tendency calculations over history sequences.

## 🎮 Usage

1. **Custom Themes** - Open Settings from the Home Screen or Browser toolbar and choose from Default, Earth, Forest, Water, or Sand. Accent colors are applied globally.
2. **Text & File Cryptography** - Go to Toolbox > Privacy & Security > Encryption tab. Toggle between Text Cipher and File Cipher to encrypt local files using AES-256.
3. **Run Privacy Audit** - Tap the "Privacy Scan" sub-utility under Security to run a real-time native device diagnostic.

---

**Made with ❤️ by [Subbarao6338](https://github.com/Subbarao6338)**
