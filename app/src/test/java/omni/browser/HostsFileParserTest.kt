package omni.browser

import omni.browser.util.adblock.HostsFileParser
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.ByteArrayInputStream
import java.io.InputStreamReader

class HostsFileParserTest {

    @Test
    fun testParseInput_StandardHosts() {
        val input = """
            # This is a comment
            127.0.0.1 doubleclick.net
            0.0.0.0 googleadservices.com
            127.0.0.1 localhost
            0.0.0.0 localhost
        """.trimIndent()

        val parser = HostsFileParser()
        val reader = InputStreamReader(ByteArrayInputStream(input.toByteArray()))
        val result = parser.parseInput(reader).toList()

        assertEquals(2, result.size)
        assertTrue(result.contains("doubleclick.net"))
        assertTrue(result.contains("googleadservices.com"))
    }

    @Test
    fun testParseInput_CommaSeparatedAndLists() {
        val input = """
            # Multiple domains on same line
            adserver.com, tracker.com
            another-ad.net,badsite.org, evil.com
        """.trimIndent()

        val parser = HostsFileParser()
        val reader = InputStreamReader(ByteArrayInputStream(input.toByteArray()))
        val result = parser.parseInput(reader).toList()

        assertEquals(5, result.size)
        assertTrue(result.contains("adserver.com"))
        assertTrue(result.contains("tracker.com"))
        assertTrue(result.contains("another-ad.net"))
        assertTrue(result.contains("badsite.org"))
        assertTrue(result.contains("evil.com"))
    }

    @Test
    fun testParseInput_CommentsOnLines() {
        val input = """
            127.0.0.1 blockme.com # Inline comment
            # Comment line
            ignoreme.com#no spaces comment
        """.trimIndent()

        val parser = HostsFileParser()
        val reader = InputStreamReader(ByteArrayInputStream(input.toByteArray()))
        val result = parser.parseInput(reader).toList()

        assertEquals(2, result.size)
        assertTrue(result.contains("blockme.com"))
        assertTrue(result.contains("ignoreme.com"))
    }

    @Test
    fun testParseInput_InvalidLines() {
        val input = """
            127.0.0.1
            0.0.0.0
            localhost
            notadomain
            ::1 localhost
        """.trimIndent()

        val parser = HostsFileParser()
        val reader = InputStreamReader(ByteArrayInputStream(input.toByteArray()))
        val result = parser.parseInput(reader).toList()

        assertTrue(result.isEmpty())
    }
}
