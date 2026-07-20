package omni.browser

import omni.toolbox.ui.screens.outdoor.PressureReading
import org.junit.Assert.assertEquals
import org.junit.Test
import kotlin.math.abs

class WeatherPredictionTest {

    private fun getPrediction(pressureChange: Float): String {
        return when {
            pressureChange <= -6.0 -> "Storm Warning (Rapid Fall)"
            pressureChange <= -3.0 -> "Gale Warning (Fast Fall)"
            pressureChange <= -1.5 -> "Deteriorating (Steady Fall)"
            pressureChange <= -0.5 -> "Slightly Unsettled"
            pressureChange >= 6.0 -> "Rapid Rise (Fair Weather)"
            pressureChange >= 3.0 -> "Improving (Fast Rise)"
            pressureChange >= 1.5 -> "Fair (Steady Rise)"
            pressureChange >= 0.5 -> "Slightly Improving"
            else -> "Stable / No Change"
        }
    }

    @Test
    fun testWeatherPrediction_TendencyForecasts() {
        assertEquals("Storm Warning (Rapid Fall)", getPrediction(-7.5f))
        assertEquals("Gale Warning (Fast Fall)", getPrediction(-4.2f))
        assertEquals("Deteriorating (Steady Fall)", getPrediction(-2.0f))
        assertEquals("Slightly Unsettled", getPrediction(-1.0f))
        assertEquals("Stable / No Change", getPrediction(0.0f))
        assertEquals("Slightly Improving", getPrediction(0.6f))
        assertEquals("Fair (Steady Rise)", getPrediction(2.0f))
        assertEquals("Improving (Fast Rise)", getPrediction(4.5f))
        assertEquals("Rapid Rise (Fair Weather)", getPrediction(6.1f))
    }

    @Test
    fun testPressureHistory_DisplacementAndCalculation() {
        // Mock a simple history sequence over 4 hours
        val baseTime = System.currentTimeMillis()
        val currentPressure = 1008.5f
        val history = listOf(
            PressureReading(1015.0f, baseTime - 4 * 60 * 60 * 1000), // 4 hours ago
            PressureReading(1014.2f, baseTime - 3 * 60 * 60 * 1000 - 1000), // ~3 hours ago
            PressureReading(1012.0f, baseTime - 2 * 60 * 60 * 1000),
            PressureReading(1010.5f, baseTime - 1 * 60 * 60 * 1000)
        )

        // Same 3-hour calculation logic as in WeatherPredictionScreen
        val threeHoursAgo = baseTime - 3 * 60 * 60 * 1000
        val startReading = history.findLast { it.timestamp <= threeHoursAgo } ?: history.firstOrNull()
        val pressureChange = if (startReading != null) currentPressure - startReading.value else 0f

        // We expect startReading to be the one ~3 hours ago (1014.2f)
        assertEquals(1014.2f, startReading?.value ?: 0f, 0.01f)
        assertEquals(-5.7f, pressureChange, 0.01f)
        assertEquals("Gale Warning (Fast Fall)", getPrediction(pressureChange))
    }
}
