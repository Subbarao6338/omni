package omni.toolbox.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val EpicPrimary = Color(0xFF4F46E5)
private val EpicSecondary = Color(0xFF6366F1)

private val DarkColorScheme = darkColorScheme(
    primary = EpicPrimary,
    secondary = EpicSecondary,
    tertiary = Color(0xFF1E293B),
    background = Color(0xFF0F172A),
    surface = Color(0xFF0F172A),
    onPrimary = Color.White,
    onSecondary = Color(0xFFF8FAFC),
    onTertiary = Color(0xFFF8FAFC),
    onBackground = Color(0xFFF8FAFC),
    onSurface = Color(0xFFF8FAFC),
    outline = EpicPrimary.copy(alpha = 0.5f)
)

private val LightColorScheme = lightColorScheme(
    primary = EpicPrimary,
    secondary = EpicSecondary,
    tertiary = Color.White,
    background = Color(0xFFF8FAFC),
    surface = Color.White,
    surfaceVariant = Color.White,
    onPrimary = Color.White,
    onSecondary = Color(0xFF0F172A),
    onTertiary = Color(0xFF0F172A),
    onBackground = Color(0xFF0F172A),
    onSurface = Color(0xFF0F172A),
    outline = EpicPrimary.copy(alpha = 0.5f)
)

@Composable
fun OmniToolboxTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    accentColor: Color? = null,
    content: @Composable () -> Unit
) {
    // Force the Epic Bookmarx theme for entire app
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            @Suppress("DEPRECATION")
            window.statusBarColor = colorScheme.primary.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
