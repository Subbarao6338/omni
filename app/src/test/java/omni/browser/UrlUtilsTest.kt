package omni.browser

import omni.browser.util.UrlUtils
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class UrlUtilsTest {

    private val searchEngine = "https://www.google.com/search?q="

    @Test
    fun testResolveUrl_ValidUrl() {
        assertEquals("https://google.com", UrlUtils.resolveUrl("google.com", searchEngine))
        assertEquals("https://www.github.com", UrlUtils.resolveUrl("www.github.com", searchEngine))
        assertEquals("https://example.com/path", UrlUtils.resolveUrl("https://example.com/path", searchEngine))
    }

    @Test
    fun testResolveUrl_SearchQuery() {
        assertEquals("${searchEngine}hello%20world", UrlUtils.resolveUrl("hello world", searchEngine))
        assertEquals("${searchEngine}testing", UrlUtils.resolveUrl("testing", searchEngine))
    }

    @Test
    fun testResolveUrl_Localhost() {
        assertEquals("http://localhost:8080", UrlUtils.resolveUrl("localhost:8080", searchEngine))
        assertEquals("http://127.0.0.1", UrlUtils.resolveUrl("127.0.0.1", searchEngine))
    }

    @Test
    fun testResolveUrl_AboutHome() {
        assertEquals("about:home", UrlUtils.resolveUrl("", searchEngine))
        assertEquals("about:home", UrlUtils.resolveUrl("   ", searchEngine))
    }

    @Test
    fun testIsBookmarklet() {
        assertEquals(true, UrlUtils.isBookmarklet("javascript:alert(1)"))
        assertEquals(false, UrlUtils.isBookmarklet("https://google.com"))
    }

    @Test
    fun testResolveUrl_Bangs() {
        // Test standard bang with query
        assertEquals("https://www.google.com/search?q=kotlin", UrlUtils.resolveUrl("!g kotlin", searchEngine))
        assertEquals("https://duckduckgo.com/?q=jetpack%20compose", UrlUtils.resolveUrl("!ddg jetpack compose", searchEngine))
        assertEquals("https://en.wikipedia.org/wiki/Special:Search?search=Android%20Studio", UrlUtils.resolveUrl("!w Android Studio", searchEngine))
        assertEquals("https://github.com/search?q=omni-web", UrlUtils.resolveUrl("!gh omni-web", searchEngine))

        // Test bang without query
        assertEquals("https://www.google.com/search?q=", UrlUtils.resolveUrl("!g", searchEngine))
    }

    @Test
    fun testResolveUrl_ChromeUrls() {
        assertEquals("about:home", UrlUtils.resolveUrl("chrome://home", searchEngine))
        assertEquals("about:home", UrlUtils.resolveUrl("chrome://home/", searchEngine))
        assertEquals("chrome://settings", UrlUtils.resolveUrl("chrome://settings", searchEngine))
    }

    @Test
    fun testResolveUrl_FilePaths() {
        assertEquals("file:///sdcard/download/test.pdf", UrlUtils.resolveUrl("/sdcard/download/test.pdf", searchEngine))
    }

    @Test
    fun testResolveUrl_SpecialUrlFormats() {
        // Param queries which look like url
        assertEquals("https://test.com?param=value", UrlUtils.resolveUrl("test.com?param=value", searchEngine))
        // Multiple subdomains
        assertEquals("https://sub.sub.domain.co.uk", UrlUtils.resolveUrl("sub.sub.domain.co.uk", searchEngine))
    }
}
