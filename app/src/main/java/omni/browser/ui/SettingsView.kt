package omni.browser.ui

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import omni.browser.BuildConfig
import omni.browser.data.AppDatabase
import omni.browser.data.Settings
import omni.browser.util.BackupManager
import omni.toolbox.model.ToolProvider
import kotlinx.coroutines.flow.firstOrNull
import kotlinx.coroutines.launch
import org.json.JSONArray

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun SettingsView(
    database: AppDatabase,
    onBack: () -> Unit,
    onOpenScripts: () -> Unit = {},
    onOpenPasswords: () -> Unit = {},
    onOpenSearchEngines: () -> Unit = {},
    onOpenParentalControls: () -> Unit = {}
) {
    val context = LocalContext.current
    val settingsState by database.settingsDao().getSettings().collectAsStateWithLifecycle(initialValue = Settings())
    val scope = rememberCoroutineScope()
    val settings = settingsState ?: Settings()

    var showClearDataDialog by remember { mutableStateOf(false) }
    var clearHistory by remember { mutableStateOf(true) }
    var clearCookies by remember { mutableStateOf(true) }
    var clearCache by remember { mutableStateOf(true) }
    var clearWebStorage by remember { mutableStateOf(true) }

    val folderPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocumentTree()
    ) { uri ->
        uri?.let {
            context.contentResolver.takePersistableUriPermission(
                it,
                Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            )
            val path = it.toString()
            scope.launch {
                database.settingsDao().updateSettings(settings.copy(downloadPath = path))
                Toast.makeText(context, "Download path updated", Toast.LENGTH_SHORT).show()
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.onSurface
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.surface)
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            SettingsSection("General", Icons.Default.Search) {
                ListItem(
                    headlineContent = { Text("Search Engines") },
                    supportingContent = { Text("Manage and select search engines") },
                    trailingContent = { Icon(Icons.Default.ChevronRight, contentDescription = null) },
                    modifier = Modifier.clickable { onOpenSearchEngines() }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                var showHomepageDialog by remember { mutableStateOf(false) }
                var homepageInput by remember { mutableStateOf("") }
                ListItem(
                    headlineContent = { Text("Custom Homepage") },
                    supportingContent = { Text(settings.homepage) },
                    trailingContent = { Icon(Icons.Default.Edit, contentDescription = "Edit Homepage") },
                    modifier = Modifier.clickable {
                        homepageInput = settings.homepage
                        showHomepageDialog = true
                    }
                )
                if (showHomepageDialog) {
                    AlertDialog(
                        onDismissRequest = { showHomepageDialog = false },
                        title = { Text("Set Custom Homepage") },
                        text = {
                            Column {
                                Text("Enter a custom URL (e.g. https://www.google.com) or 'about:home' for default dashboard:", fontSize = 12.sp, modifier = Modifier.padding(bottom = 8.dp))
                                OutlinedTextField(
                                    value = homepageInput,
                                    onValueChange = { homepageInput = it },
                                    placeholder = { Text("about:home") },
                                    modifier = Modifier.fillMaxWidth(),
                                    singleLine = true
                                )
                            }
                        },
                        confirmButton = {
                            TextButton(onClick = {
                                val finalUrl = if (homepageInput.isBlank()) {
                                    "about:home"
                                } else {
                                    val trimmed = homepageInput.trim()
                                    if (trimmed.startsWith("http://") || trimmed.startsWith("https://") || trimmed == "about:home") {
                                        trimmed
                                    } else {
                                        "https://$trimmed"
                                    }
                                }
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(homepage = finalUrl))
                                    Toast.makeText(context, "Homepage updated", Toast.LENGTH_SHORT).show()
                                }
                                showHomepageDialog = false
                            }) { Text("Save") }
                        },
                        dismissButton = {
                            TextButton(onClick = { showHomepageDialog = false }) { Text("Cancel") }
                        }
                    )
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Clear data on exit") },
                    supportingContent = { Text("Automatically clear history and cache when app is closed") },
                    trailingContent = {
                        Switch(
                            checked = settings.clearDataOnExit,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(clearDataOnExit = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Force Light Theme") },
                    supportingContent = { Text("Enforce light background on websites") },
                    trailingContent = {
                        Switch(
                            checked = settings.forceLightTheme,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(forceLightTheme = enabled, forceBlackTheme = if (enabled) false else settings.forceBlackTheme))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Force Black Theme") },
                    supportingContent = { Text("Enforce pure black background on websites") },
                    trailingContent = {
                        Switch(
                            checked = settings.forceBlackTheme,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(forceBlackTheme = enabled, forceLightTheme = if (enabled) false else settings.forceLightTheme))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Always Incognito") },
                    supportingContent = { Text("Force all new tabs to be incognito") },
                    trailingContent = {
                        Switch(
                            checked = settings.alwaysIncognito,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(alwaysIncognito = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Strict Privacy Mode") },
                    supportingContent = { Text("Anti-fingerprinting and generic User-Agent") },
                    trailingContent = {
                        Switch(
                            checked = settings.strictPrivacyMode,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(strictPrivacyMode = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Parental Controls") },
                    supportingContent = { Text("Manage blocked sites and protection") },
                    trailingContent = { Icon(Icons.Default.ChevronRight, contentDescription = null) },
                    modifier = Modifier.clickable { onOpenParentalControls() }
                )
                ListItem(
                    headlineContent = { Text("Restore tabs on start") },
                    supportingContent = { Text("Continue where you left off") },
                    trailingContent = {
                        Switch(
                            checked = settings.restoreTabsOnStart,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(restoreTabsOnStart = enabled))
                                }
                            }
                        )
                    }
                )
            }

            SettingsSection("Downloads", Icons.Default.Download) {
                ListItem(
                    headlineContent = { Text("Ask where to save files") },
                    supportingContent = { Text("Always prompt for download location") },
                    trailingContent = {
                        Switch(
                            checked = settings.askDownloadLocation,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(askDownloadLocation = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Download Path") },
                    supportingContent = { Text(settings.downloadPath ?: "Default (Downloads folder)") },
                    trailingContent = {
                        Row {
                            if (settings.downloadPath != null) {
                                IconButton(onClick = {
                                    scope.launch {
                                        database.settingsDao().updateSettings(settings.copy(downloadPath = null))
                                        Toast.makeText(context, "Reset to default download path", Toast.LENGTH_SHORT).show()
                                    }
                                }) {
                                    Icon(Icons.Default.Close, contentDescription = "Clear Path")
                                }
                            }
                            IconButton(onClick = {
                                folderPickerLauncher.launch(null)
                            }) {
                                Icon(Icons.Default.FolderOpen, contentDescription = "Change Folder")
                            }
                        }
                    }
                )
            }

            SettingsSection("Appearance", Icons.Default.Palette) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Theme Mode", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(12.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        ThemeOption("Light", settings.themeMode == "light", Modifier.weight(1f)) {
                            scope.launch { database.settingsDao().updateSettings(settings.copy(themeMode = "light")) }
                        }
                        ThemeOption("Dark", settings.themeMode == "dark", Modifier.weight(1f)) {
                            scope.launch { database.settingsDao().updateSettings(settings.copy(themeMode = "dark")) }
                        }
                        ThemeOption("System", settings.themeMode == "system", Modifier.weight(1f)) {
                            scope.launch { database.settingsDao().updateSettings(settings.copy(themeMode = "system")) }
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        ThemeOption("Earth", settings.themeMode == "earth", Modifier.weight(1f)) {
                            scope.launch { database.settingsDao().updateSettings(settings.copy(themeMode = "earth", accentColor = "#795548")) }
                        }
                        ThemeOption("Forest", settings.themeMode == "forest", Modifier.weight(1f)) {
                            scope.launch { database.settingsDao().updateSettings(settings.copy(themeMode = "forest", accentColor = "#2E7D32")) }
                        }
                        ThemeOption("Water", settings.themeMode == "water", Modifier.weight(1f)) {
                            scope.launch { database.settingsDao().updateSettings(settings.copy(themeMode = "water", accentColor = "#0277BD")) }
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        ThemeOption("Sand", settings.themeMode == "sand", Modifier.weight(1f)) {
                            scope.launch { database.settingsDao().updateSettings(settings.copy(themeMode = "sand", accentColor = "#FBC02D")) }
                        }
                        ThemeOption("Nature", settings.themeMode == "nature", Modifier.weight(1f)) {
                            scope.launch { database.settingsDao().updateSettings(settings.copy(themeMode = "nature", accentColor = "#1B4D3E")) }
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    Text("Accent Color", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(12.dp))
                    val colors = listOf("#3B82F6", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444", "#EC4899", "#6366F1")
                    LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(colors) { colorHex ->
                            val color = Color(android.graphics.Color.parseColor(colorHex))
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(color)
                                    .border(
                                        width = if (settings.accentColor == colorHex) 3.dp else 0.dp,
                                        color = if (settings.accentColor == colorHex) MaterialTheme.colorScheme.onSurface else Color.Transparent,
                                        shape = CircleShape
                                    )
                                    .clickable {
                                        scope.launch {
                                            database.settingsDao().updateSettings(settings.copy(accentColor = colorHex))
                                        }
                                    }
                            )
                        }
                    }
                }
            }

            SettingsSection("Privacy & Security", Icons.Default.Shield) {
                ListItem(
                    headlineContent = { Text("Passwords") },
                    supportingContent = { Text("Manage saved credentials") },
                    trailingContent = { Icon(Icons.Default.ChevronRight, contentDescription = null) },
                    modifier = Modifier.clickable { onOpenPasswords() }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                var showManageProfilesDialog by remember { mutableStateOf(false) }
                val profilePrefs = remember { context.getSharedPreferences("browser_profiles", Context.MODE_PRIVATE) }
                var profileSet by remember {
                    mutableStateOf(
                        profilePrefs.getStringSet("profiles_list", setOf("Default", "Personal", "Work", "Private", "Social")) ?: setOf("Default")
                    )
                }
                var showAddProfileDialog by remember { mutableStateOf(false) }
                var newProfileName by remember { mutableStateOf("") }
                ListItem(
                    headlineContent = { Text("Browser Profiles") },
                    supportingContent = { Text("Active Profile: ${settings.currentProfile}") },
                    trailingContent = { Icon(Icons.Default.Group, contentDescription = "Manage Profiles") },
                    modifier = Modifier.clickable { showManageProfilesDialog = true }
                )
                if (showManageProfilesDialog) {
                    AlertDialog(
                        onDismissRequest = { showManageProfilesDialog = false },
                        title = {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("Browser Profiles")
                                IconButton(onClick = { showAddProfileDialog = true }) {
                                    Icon(Icons.Default.Add, contentDescription = "Add Profile")
                                }
                            }
                        },
                        text = {
                            Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                                profileSet.sorted().forEach { profile ->
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clickable {
                                                scope.launch {
                                                    database.settingsDao().updateSettings(settings.copy(currentProfile = profile))
                                                    Toast.makeText(context, "Switched to profile: $profile", Toast.LENGTH_SHORT).show()
                                                }
                                                showManageProfilesDialog = false
                                            }
                                            .padding(vertical = 12.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        RadioButton(selected = settings.currentProfile == profile, onClick = null)
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Text(profile, modifier = Modifier.weight(1f))
                                        if (profile != "Default") {
                                            IconButton(onClick = {
                                                val updated = profileSet - profile
                                                profileSet = updated
                                                profilePrefs.edit().putStringSet("profiles_list", updated).apply()
                                                if (settings.currentProfile == profile) {
                                                    scope.launch {
                                                        database.settingsDao().updateSettings(settings.copy(currentProfile = "Default"))
                                                    }
                                                }
                                            }) {
                                                Icon(Icons.Default.Delete, contentDescription = "Delete Profile", tint = MaterialTheme.colorScheme.error)
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        confirmButton = {
                            TextButton(onClick = { showManageProfilesDialog = false }) { Text("Close") }
                        }
                    )
                }
                if (showAddProfileDialog) {
                    AlertDialog(
                        onDismissRequest = { showAddProfileDialog = false },
                        title = { Text("Add Custom Profile") },
                        text = {
                            OutlinedTextField(
                                value = newProfileName,
                                onValueChange = { newProfileName = it },
                                label = { Text("Profile Name") },
                                singleLine = true,
                                modifier = Modifier.fillMaxWidth()
                            )
                        },
                        confirmButton = {
                            TextButton(onClick = {
                                val name = newProfileName.trim()
                                if (name.isNotEmpty() && !profileSet.contains(name)) {
                                    val updated = profileSet + name
                                    profileSet = updated
                                    profilePrefs.edit().putStringSet("profiles_list", updated).apply()
                                    scope.launch {
                                        database.settingsDao().updateSettings(settings.copy(currentProfile = name))
                                    }
                                    newProfileName = ""
                                    showAddProfileDialog = false
                                    showManageProfilesDialog = false
                                    Toast.makeText(context, "Created & Switched to profile $name", Toast.LENGTH_SHORT).show()
                                }
                            }) { Text("Create") }
                        },
                        dismissButton = {
                            TextButton(onClick = { showAddProfileDialog = false }) { Text("Cancel") }
                        }
                    )
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Ad Blocking") },
                    supportingContent = { Text("Block ads and trackers") },
                    trailingContent = {
                        Switch(
                            checked = settings.adBlockEnabled,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(adBlockEnabled = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("JavaScript") },
                    supportingContent = { Text("Enable execution of scripts on websites") },
                    trailingContent = {
                        Switch(
                            checked = settings.javaScriptEnabled,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(javaScriptEnabled = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("HTTPS-Only Mode") },
                    supportingContent = { Text("Always try to use a secure connection") },
                    trailingContent = {
                        Switch(
                            checked = settings.httpsOnlyMode,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(httpsOnlyMode = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Block Third-Party Cookies") },
                    supportingContent = { Text("Improved privacy by preventing cross-site tracking") },
                    trailingContent = {
                        Switch(
                            checked = settings.blockThirdPartyCookies,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(blockThirdPartyCookies = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Deep Dark Mode") },
                    supportingContent = { Text("Enforce dark theme on all websites") },
                    trailingContent = {
                        Switch(
                            checked = settings.deepDarkMode,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(deepDarkMode = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Clear Browsing Data", color = MaterialTheme.colorScheme.error) },
                    supportingContent = { Text("History, Cache, and Cookies") },
                    modifier = Modifier.clickable { showClearDataDialog = true }
                )
            }

            SettingsSection("Advanced", Icons.Default.Build) {
                ListItem(
                    headlineContent = { Text("Text Reflow") },
                    supportingContent = { Text("Adjust text to fit screen when zooming") },
                    trailingContent = {
                        Switch(
                            checked = settings.textReflowEnabled,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(textReflowEnabled = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("AMP Blocking") },
                    supportingContent = { Text("Automatically redirect AMP pages to canonical") },
                    trailingContent = {
                        Switch(
                            checked = settings.ampBlockingEnabled,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(ampBlockingEnabled = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Force Zoom") },
                    supportingContent = { Text("Allow zooming on all websites") },
                    trailingContent = {
                        Switch(
                            checked = settings.forceZoom,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(forceZoom = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Invert Page") },
                    supportingContent = { Text("Invert web page colors") },
                    trailingContent = {
                        Switch(
                            checked = settings.invertPageEnabled,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(invertPageEnabled = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Userscripts") },
                    supportingContent = { Text("Manage custom JS injections") },
                    trailingContent = {
                        Icon(Icons.Default.ChevronRight, contentDescription = null)
                    },
                    modifier = Modifier.clickable { onOpenScripts() }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Google Gemini API Key", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = settings.geminiApiKey ?: "",
                        onValueChange = {
                            scope.launch {
                                database.settingsDao().updateSettings(settings.copy(geminiApiKey = it.ifBlank { null }))
                            }
                        },
                        placeholder = { Text("Enter Gemini API Key for AI features") },
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp),
                        singleLine = true
                    )
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Tab Hibernation Timeout", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(8.dp))
                    var timeoutMinutes by remember(settings.hibernationTimeoutMillis) { mutableIntStateOf((settings.hibernationTimeoutMillis / 60000).toInt()) }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Slider(
                            value = timeoutMinutes.toFloat(),
                            onValueChange = { timeoutMinutes = it.toInt() },
                            onValueChangeFinished = {
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(hibernationTimeoutMillis = timeoutMinutes.toLong() * 60000L))
                                }
                            },
                            valueRange = 1f..60f,
                            steps = 59,
                            modifier = Modifier.weight(1f)
                        )
                        Text("${timeoutMinutes}m", modifier = Modifier.width(48.dp), textAlign = androidx.compose.ui.text.style.TextAlign.End, fontWeight = FontWeight.Bold)
                    }
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Max WebView Cache Size", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(8.dp))
                    var cacheSize by remember(settings.maxWebViewCacheSize) { mutableIntStateOf(settings.maxWebViewCacheSize) }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Slider(
                            value = cacheSize.toFloat(),
                            onValueChange = { cacheSize = it.toInt() },
                            onValueChangeFinished = {
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(maxWebViewCacheSize = cacheSize))
                                }
                            },
                            valueRange = 1f..20f,
                            steps = 19,
                            modifier = Modifier.weight(1f)
                        )
                        Text("$cacheSize", modifier = Modifier.width(48.dp), textAlign = androidx.compose.ui.text.style.TextAlign.End, fontWeight = FontWeight.Bold)
                    }
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Import Userscript from URL", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(8.dp))
                    var scriptUrl by remember { mutableStateOf("") }
                    OutlinedTextField(
                        value = scriptUrl,
                        onValueChange = { scriptUrl = it },
                        placeholder = { Text("https://example.com/script.js") },
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp),
                        singleLine = true
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Button(
                        onClick = {
                            if (scriptUrl.isNotBlank()) {
                                scope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                    try {
                                        val connection = java.net.URL(scriptUrl).openConnection() as java.net.HttpURLConnection
                                        val response = connection.inputStream.bufferedReader().readText()
                                        database.userScriptDao().insertScript(
                                            omni.browser.data.UserScript(
                                                name = scriptUrl.substringAfterLast("/"),
                                                script = response,
                                                enabled = true,
                                                type = "userscript"
                                            )
                                        )
                                        kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                                            Toast.makeText(context, "Userscript imported", Toast.LENGTH_SHORT).show()
                                            scriptUrl = ""
                                        }
                                    } catch (e: Exception) {
                                        kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                                            Toast.makeText(context, "Import failed: ${e.message}", Toast.LENGTH_SHORT).show()
                                        }
                                    }
                                }
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Icon(Icons.Default.Download, contentDescription = null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Import Script")
                    }
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Custom User Agent", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = settings.customUserAgent ?: "",
                        onValueChange = {
                            scope.launch {
                                database.settingsDao().updateSettings(settings.copy(customUserAgent = it.ifBlank { null }))
                            }
                        },
                        placeholder = { Text("Leave empty for default") },
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp),
                        singleLine = true
                    )
                }
            }

            SettingsSection("Data Management", Icons.Default.ImportExport) {
                ListItem(
                    headlineContent = { Text("Export Data") },
                    supportingContent = { Text("Copy settings and bookmarks to clipboard") },
                    trailingContent = {
                        IconButton(onClick = {
                            scope.launch {
                                val bookmarks = database.bookmarkDao().getAllBookmarks().firstOrNull() ?: emptyList()
                                val shortcuts = database.shortcutDao().getAllShortcuts().firstOrNull() ?: emptyList()
                                val history = database.historyDao().getAllHistory().firstOrNull() ?: emptyList()
                                val scripts = database.userScriptDao().getAllScripts().firstOrNull() ?: emptyList()
                                // We don't have a simple way to get all PerSiteSettings without a Query, let's assume we want to export them too
                                // For now, let's just export the ones we can easily get
                                val json = BackupManager.exportData(bookmarks, shortcuts, history, scripts, emptyList(), settings)
                                val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                val clip = ClipData.newPlainText("OmniBackup", json)
                                clipboard.setPrimaryClip(clip)
                                Toast.makeText(context, "Data exported to clipboard", Toast.LENGTH_SHORT).show()
                            }
                        }) {
                            Icon(Icons.Default.ContentCopy, contentDescription = "Export")
                        }
                    }
                )
                ListItem(
                    headlineContent = { Text("Import Data") },
                    supportingContent = { Text("Restore data from clipboard") },
                    trailingContent = {
                        IconButton(onClick = {
                            try {
                                val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                val json = clipboard.primaryClip?.getItemAt(0)?.text?.toString()
                                if (json != null) {
                                    scope.launch {
                                        val newBookmarks = BackupManager.importBookmarks(json)
                                        val newShortcuts = BackupManager.importShortcuts(json)
                                        val newHistory = BackupManager.importHistory(json)
                                        val newScripts = BackupManager.importScripts(json)
                                        val newSettings = BackupManager.importSettings(json, settings)

                                        database.settingsDao().updateSettings(newSettings)
                                        newBookmarks.forEach { database.bookmarkDao().insertBookmark(it) }
                                        newShortcuts.forEach { database.shortcutDao().insertShortcut(it) }
                                        newHistory.forEach { database.historyDao().insertHistory(it) }
                                        newScripts.forEach { database.userScriptDao().insertScript(it) }

                                        Toast.makeText(context, "Data imported successfully", Toast.LENGTH_SHORT).show()
                                    }
                                } else {
                                    Toast.makeText(context, "Clipboard is empty", Toast.LENGTH_SHORT).show()
                                }
                            } catch (e: Exception) {
                                Toast.makeText(context, "Import failed: Invalid format", Toast.LENGTH_SHORT).show()
                            }
                        }) {
                            Icon(Icons.Default.ContentPaste, contentDescription = "Import")
                        }
                    }
                )
            }

            SettingsSection("Toolbox Settings", Icons.Default.Build) {
                ListItem(
                    headlineContent = { Text("Show Category Counts") },
                    supportingContent = { Text("Display number of tools in each category in Toolbox") },
                    trailingContent = {
                        Switch(
                            checked = settings.showCategoryCounts,
                            onCheckedChange = { enabled ->
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(showCategoryCounts = enabled))
                                }
                            }
                        )
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Home Grid Columns", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(12.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        (2..4).forEach { cols ->
                            val isSelected = settings.gridColumns == cols
                            ThemeOption("${cols} Columns", isSelected, Modifier.weight(1f)) {
                                scope.launch {
                                    database.settingsDao().updateSettings(settings.copy(gridColumns = cols))
                                }
                            }
                        }
                    }
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Stable Diffusion API URL", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = settings.stableDiffusionUrl,
                        onValueChange = {
                            scope.launch {
                                database.settingsDao().updateSettings(settings.copy(stableDiffusionUrl = it))
                            }
                        },
                        placeholder = { Text("http://your-sd-url:7860") },
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp),
                        singleLine = true
                    )
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Toolbox Quick Tiles Configuration", fontSize = 14.sp, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("Assign tool routes to the 3 custom Quick Tiles:", fontSize = 11.sp, color = MaterialTheme.colorScheme.outline)
                    Spacer(modifier = Modifier.height(12.dp))
                    val tilePrefs = remember { context.getSharedPreferences("dynamic_tiles", Context.MODE_PRIVATE) }
                    (1..3).forEach { i ->
                        var tileRoute by remember { mutableStateOf(tilePrefs.getString("tile_$i", "home") ?: "home") }
                        OutlinedTextField(
                            value = tileRoute,
                            onValueChange = { newValue ->
                                tileRoute = newValue
                                tilePrefs.edit().putString("tile_$i", newValue).apply()
                                val toolName = ToolProvider.tools.find { it.route == newValue }?.name ?: "Nature Tool"
                                tilePrefs.edit().putString("tile_name_$i", toolName).apply()
                            },
                            label = { Text("Quick Tile $i Route") },
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            shape = RoundedCornerShape(12.dp),
                            singleLine = true
                        )
                    }
                }
            }

            SettingsSection("About", Icons.Default.Info) {
                ListItem(
                    headlineContent = { Text("Version") },
                    supportingContent = { Text("${BuildConfig.VERSION_NAME} (${BuildConfig.VERSION_CODE})") }
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp), thickness = 0.5.dp)
                ListItem(
                    headlineContent = { Text("Developer") },
                    supportingContent = { Text("Subbarao") }
                )
            }

            Spacer(modifier = Modifier.height(32.dp))
        }
    }

    if (showClearDataDialog) {
        AlertDialog(
            onDismissRequest = { showClearDataDialog = false },
            title = { Text("Clear Browsing Data") },
            text = {
                Column {
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { clearHistory = !clearHistory }) {
                        Checkbox(checked = clearHistory, onCheckedChange = { clearHistory = it })
                        Text("History")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { clearCookies = !clearCookies }) {
                        Checkbox(checked = clearCookies, onCheckedChange = { clearCookies = it })
                        Text("Cookies")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { clearCache = !clearCache }) {
                        Checkbox(checked = clearCache, onCheckedChange = { clearCache = it })
                        Text("Cache")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { clearWebStorage = !clearWebStorage }) {
                        Checkbox(checked = clearWebStorage, onCheckedChange = { clearWebStorage = it })
                        Text("Web Storage")
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    scope.launch {
                        if (clearHistory) database.historyDao().clearHistory()
                        if (clearCookies) android.webkit.CookieManager.getInstance().removeAllCookies(null)
                        if (clearCache) {
                            // Note: WebView cache clearing is typically done via WebStorage or by deleting files
                        }
                        if (clearWebStorage) android.webkit.WebStorage.getInstance().deleteAllData()

                        Toast.makeText(context, "Selected data cleared", Toast.LENGTH_SHORT).show()
                        showClearDataDialog = false
                    }
                }) { Text("Clear", color = MaterialTheme.colorScheme.error) }
            },
            dismissButton = {
                TextButton(onClick = { showClearDataDialog = false }) { Text("Cancel") }
            }
        )
    }
}

@Composable
fun ThemeOption(label: String, selected: Boolean, modifier: Modifier = Modifier, onClick: () -> Unit) {
    Surface(
        onClick = onClick,
        modifier = modifier,
        shape = RoundedCornerShape(12.dp),
        color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
        contentColor = if (selected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
    ) {
        Box(modifier = Modifier.padding(12.dp), contentAlignment = Alignment.Center) {
            Text(label, fontWeight = FontWeight.Bold, fontSize = 14.sp)
        }
    }
}

