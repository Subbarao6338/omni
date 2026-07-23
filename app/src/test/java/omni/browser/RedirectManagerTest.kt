package omni.browser

import omni.browser.data.CustomRedirectEntry
import omni.browser.util.RedirectManager
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

class RedirectManagerTest {

    @Test
    fun testGetRedirect_MatchingPattern() {
        val redirects = listOf(
            CustomRedirectEntry(source = "twitter.com", target = "nitter.net"),
            CustomRedirectEntry(source = "youtube.com/watch?v=", target = "piped.video/watch?v=")
        )

        val manager = RedirectManager(redirects)

        assertEquals("https://nitter.net/test", manager.getRedirect("https://twitter.com/test"))
        assertEquals("https://piped.video/watch?v=123", manager.getRedirect("https://youtube.com/watch?v=123"))
    }

    @Test
    fun testGetRedirect_NoMatch() {
        val redirects = listOf(
            CustomRedirectEntry(source = "twitter.com", target = "nitter.net")
        )

        val manager = RedirectManager(redirects)

        assertNull(manager.getRedirect("https://google.com"))
        assertNull(manager.getRedirect("https://github.com"))
    }

    @Test
    fun testGetRedirect_MultipleRedirectsOrder() {
        val redirects = listOf(
            CustomRedirectEntry(source = "news.ycombinator.com", target = "hacker-news.org"),
            CustomRedirectEntry(source = "ycombinator.com", target = "yc.com")
        )

        val manager = RedirectManager(redirects)

        // The first match in the list should win
        assertEquals("https://yc.com/news", manager.getRedirect("https://ycombinator.com/news"))
    }
}
